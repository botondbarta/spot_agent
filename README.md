# SPOT agent

SPOT Agent is a Python framework for an embodied AI agent designed to operate within the AI2-THOR simulation environment. It uses a Large Language Model (LLM) to process visual information from the simulator and determine actions.

### Techniques

*   **Simulator Interaction**: The agent interfaces with the [AI2-THOR](https://ai2thor.allenai.org/) physics-enabled simulator. The logic for this connection and control is managed in `spot_agent/ai2thor_sim.py`.
*   **LLM-based Decision Making**: The core logic for action selection is delegated to an LLM. The `spot_agent/llm.py` module contains the integration with the LLM service.
*   **Prompt Engineering**: Prompts are decoupled from the application logic and stored in `spot_agent/prompts.py`. This allows for easier iteration and management of the prompts sent to the LLM.
*   **Image Handling**: Visual data from the simulator is processed by `spot_agent/img_handler.py` before being passed to the model.

### Project Structure

```
config/
├── config.yaml
spot_agent/
├── __init__.py
├── ai2thor_sim.py
├── img_handler.py
├── llm.py
├── prompts.py
└── utils.py
```

*   `spot_agent`: This directory contains the core source code for the agent, including modules for simulation interaction, image processing, and LLM communication.
*   `config`: Contains configuration files, such as config.yaml, for setting up the agent and its connection to services.

## Setup
```
conda create -n spot_agent python=3.12.9
conda activate spot_agent

pip install -e .
```