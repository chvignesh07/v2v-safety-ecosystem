"""DQN Agent for V2V Collision Avoidance

This module implements a Deep Q-Network (DQN) reinforcement learning agent
for vehicle collision avoidance in the V2V Safety Ecosystem.

Author: V2V Safety Team
Date: December 7, 2025
Version: 1.0.0
"""

import numpy as np
import random
from collections import deque
from typing import Dict, List, Tuple, Any
import logging

logger = logging.getLogger(__name__)

class DQNAgent:
    """Deep Q-Network Agent for collision avoidance decisions.
    
    The agent learns optimal collision avoidance strategies through
    reinforcement learning, trained on NHTSA FARS 2023 crash data.
    
    Attributes:
        state_size (int): Dimension of state space
        action_size (int): Number of possible actions
        memory (deque): Experience replay buffer
        gamma (float): Discount factor for future rewards
        epsilon (float): Exploration rate
        learning_rate (float): Learning rate for Q-network
    """
    
    def __init__(self, state_size: int = 8, action_size: int = 5):
        """Initialize DQN Agent.
        
        Args:
            state_size: Size of state vector (default: 8)
                - distance_to_vehicle (m)
                - relative_speed (m/s)
                - vehicle_angle (degrees)
                - road_type (0-3)
                - weather_condition (0-4)
                - time_of_day (0-23)
                - driver_attention (0-1)
                - collision_probability (0-1)
            action_size: Number of actions (default: 5)
                - 0: Maintain speed
                - 1: Decelerate gradually
                - 2: Hard brake
                - 3: Change lane left
                - 4: Change lane right
        """
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        
        # Hyperparameters
        self.gamma = 0.95    # Discount factor
        self.epsilon = 1.0   # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        
        # Simple Q-table for demonstration (in production, use neural network)
        self.q_table = {}
        
        # Performance metrics
        self.collisions_avoided = 0
        self.total_actions = 0
        self.success_rate = 0.0
        
        logger.info(f"DQN Agent initialized: state_size={state_size}, action_size={action_size}")
    
    def _discretize_state(self, state: List[float]) -> str:
        """Convert continuous state to discrete for Q-table lookup.
        
        Args:
            state: Continuous state vector
            
        Returns:
            String representation of discretized state
        """
        discretized = []
        for i, val in enumerate(state):
            if i == 0:  # Distance
                bin_val = int(min(val // 10, 20))  # 10m bins, max 200m
            elif i == 1:  # Speed
                bin_val = int(min(abs(val) // 5, 10))  # 5 m/s bins
            else:
                bin_val = int(val)
            discretized.append(str(bin_val))
        return '-'.join(discretized)
    
    def remember(self, state: List[float], action: int, reward: float, 
                 next_state: List[float], done: bool):
        """Store experience in replay memory.
        
        Args:
            state: Current state
            action: Action taken
            reward: Reward received
            next_state: Resulting state
            done: Whether episode ended
        """
        self.memory.append((state, action, reward, next_state, done))
    
    def act(self, state: List[float]) -> int:
        """Choose action using epsilon-greedy policy.
        
        Args:
            state: Current state vector
            
        Returns:
            Selected action index
        """
        # Epsilon-greedy action selection
        if np.random.rand() <= self.epsilon:
            action = random.randrange(self.action_size)
            logger.debug(f"Exploration: random action {action}")
            return action
        
        # Exploit: choose best known action
        state_key = self._discretize_state(state)
        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(self.action_size)
        
        q_values = self.q_table[state_key]
        action = np.argmax(q_values)
        
        self.total_actions += 1
        logger.debug(f"Exploitation: action {action} from Q-values {q_values}")
        return action
    
    def replay(self, batch_size: int = 32):
        """Train agent on batch of experiences.
        
        Args:
            batch_size: Number of experiences to sample
        """
        if len(self.memory) < batch_size:
            return
        
        minibatch = random.sample(self.memory, batch_size)
        
        for state, action, reward, next_state, done in minibatch:
            state_key = self._discretize_state(state)
            next_state_key = self._discretize_state(next_state)
            
            # Initialize Q-values if needed
            if state_key not in self.q_table:
                self.q_table[state_key] = np.zeros(self.action_size)
            if next_state_key not in self.q_table:
                self.q_table[next_state_key] = np.zeros(self.action_size)
            
            # Q-learning update
            target = reward
            if not done:
                target += self.gamma * np.amax(self.q_table[next_state_key])
            
            current_q = self.q_table[state_key][action]
            self.q_table[state_key][action] = current_q + self.learning_rate * (target - current_q)
        
        # Decay exploration rate
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def evaluate_collision_risk(self, state: List[float]) -> float:
        """Evaluate collision risk for current state.
        
        Args:
            state: Current state vector
            
        Returns:
            Collision risk probability (0-1)
        """
        distance = state[0]
        relative_speed = state[1]
        
        # Simple risk calculation based on stopping distance
        if distance <= 0:
            return 1.0
        
        # Time to collision
        if relative_speed > 0:
            ttc = distance / relative_speed
            if ttc < 2.0:  # Less than 2 seconds
                risk = 1.0 - (ttc / 2.0)
                return min(max(risk, 0.0), 1.0)
        
        # Distance-based risk
        safe_distance = 30.0  # meters
        if distance < safe_distance:
            risk = 1.0 - (distance / safe_distance)
            return min(max(risk, 0.0), 1.0)
        
        return 0.0
    
    def get_action_name(self, action: int) -> str:
        """Get human-readable action name.
        
        Args:
            action: Action index
            
        Returns:
            Action name string
        """
        action_names = {
            0: "Maintain Speed",
            1: "Decelerate Gradually",
            2: "Hard Brake",
            3: "Change Lane Left",
            4: "Change Lane Right"
        }
        return action_names.get(action, "Unknown")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent performance statistics.
        
        Returns:
            Dictionary of performance metrics
        """
        if self.total_actions > 0:
            self.success_rate = self.collisions_avoided / self.total_actions
        
        return {
            'total_actions': self.total_actions,
            'collisions_avoided': self.collisions_avoided,
            'success_rate': self.success_rate,
            'epsilon': self.epsilon,
            'memory_size': len(self.memory),
            'q_table_size': len(self.q_table)
        }
    
    def save_model(self, filepath: str):
        """Save Q-table to file.
        
        Args:
            filepath: Path to save file
        """
        import json
        
        model_data = {
            'q_table': {k: v.tolist() for k, v in self.q_table.items()},
            'epsilon': self.epsilon,
            'stats': self.get_stats()
        }
        
        with open(filepath, 'w') as f:
            json.dump(model_data, f)
        
        logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load Q-table from file.
        
        Args:
            filepath: Path to load file
        """
        import json
        
        with open(filepath, 'r') as f:
            model_data = json.load(f)
        
        self.q_table = {k: np.array(v) for k, v in model_data['q_table'].items()}
        self.epsilon = model_data['epsilon']
        
        logger.info(f"Model loaded from {filepath}")


class RuleBasedAgent:
    """Rule-based agent for baseline comparison.
    
    Uses hand-crafted rules for collision avoidance decisions.
    Serves as a baseline for DQN agent performance.
    """
    
    def __init__(self):
        """Initialize rule-based agent."""
        self.total_actions = 0
        self.collisions_avoided = 0
        logger.info("Rule-based agent initialized")
    
    def act(self, state: List[float]) -> int:
        """Choose action based on rules.
        
        Args:
            state: Current state vector
            
        Returns:
            Selected action index
        """
        distance = state[0]
        relative_speed = state[1]
        
        self.total_actions += 1
        
        # Emergency braking
        if distance < 10 and relative_speed > 0:
            return 2  # Hard brake
        
        # Decelerate if too close
        if distance < 30 and relative_speed > 0:
            return 1  # Decelerate gradually
        
        # Lane change if approaching fast
        if distance < 50 and relative_speed > 10:
            return 3 if random.random() > 0.5 else 4  # Change lane
        
        # Maintain speed
        return 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics.
        
        Returns:
            Dictionary of performance metrics
        """
        success_rate = self.collisions_avoided / self.total_actions if self.total_actions > 0 else 0.0
        
        return {
            'total_actions': self.total_actions,
            'collisions_avoided': self.collisions_avoided,
            'success_rate': success_rate
        }
