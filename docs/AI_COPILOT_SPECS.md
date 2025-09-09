# AI Copilot Technical Specifications

## Features
- Frontend: Dialog panel floats over BEV, triggers on sensor incident
- Modal: "Are you okay?" speech/Text UI, listens and adapts escalation flow
- Multi-channel notification: SMS, TTS voice, email (Twilio, simulated/web)
- Adaptive: Uses LLM (Llama/Mistral/RAG) for context and dialog extension
- Modular: Python or Node.js backend, WebSocket/socket.io for real-time bidirectional data

## Data Models
- Incident/event input (type, severity, vehicle)
- User/AI/copilot dialog object (time, text, channel)
- Contact & consent registry
- Escalation and resolution log
