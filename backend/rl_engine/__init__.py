"""
Reinforcement Learning Engine Module

This module provides the core reinforcement learning functionality
for the V2V Safety Ecosystem, including:
- Q-learning and Deep Q-Network (DQN) algorithms
- Environment interaction and state management
- Policy optimization and decision making
- Training and evaluation utilities

Author: V2V Safety Ecosystem Team
Created: September 2025
"""

from .agent import RLAgent
from .environment import V2VEnvironment
from .trainer import RLTrainer
from .utils import PolicyUtils, RewardUtils

__version__ = "1.0.0"
__all__ = [
    "RLAgent",
    "V2VEnvironment", 
    "RLTrainer",
    "PolicyUtils",
    "RewardUtils"
]

# Module-level configuration
DEFAULT_CONFIG = {
    "learning_rate": 0.001,
    "discount_factor": 0.95,
    "epsilon_decay": 0.995,
    "batch_size": 32,
    "memory_size": 10000
}

def get_version():
    """Return the current version of the RL engine."""
    return __version__

def get_default_config():
    """Return the default configuration for the RL engine."""
    return DEFAULT_CONFIG.copy()
