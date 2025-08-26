# Avalon Deception Analysis Project

## Overview

This project implements an AI-powered analysis system for **The Resistance: Avalon**, a social deduction game involving hidden roles and strategic deception. The system uses various Large Language Models (LLMs) to analyze game discussions and generate strategic responses from the perspective of Good players trying to identify Evil players.

## Game Background

**Avalon** is a social deduction game where:
- **5 players** are divided into **2 teams**:
  - **Good team** (3 players): Servants of Arthur and Merlin
  - **Evil team** (2 players): Minions of Mordred and the Assassin
- **Goal**: Good team tries to pass 3 out of 5 missions; Evil team tries to sabotage 3 missions
- **Special roles**: 
  - **Merlin** knows who the Evil players are but must remain hidden
  - **Assassin** can win by correctly identifying and assassinating Merlin
- **Gameplay**: Players discuss, propose teams, vote, and try to deduce each other's roles

## Project Structure

```
Avalon-deception/
├── agent.py                 # Main agent class with reasoning logic
├── test_agent.ipynb         # Jupyter notebook for experiments
├── Deception.csv           # Dataset with game discussions and responses
├── Legacy-Deception.csv    # Backup/legacy dataset
├── llm.py                  # OpenAI GPT-4 integration
├── o1.py                   # OpenAI o1 model integration
├── gemma.py                # Google Gemma model integration
├── deepseek.py             # DeepSeek model integration
├── qwen_llm.py             # Qwen model integration
├── .env                    # Environment variables (API keys)
└── remote/                 # Additional files and requirements
```

## Features

### Multi-Level Reasoning System

The agent implements a sophisticated reasoning framework:

1. **First-Order Belief Modeling**: Analyzes what each player believes about the game state
2. **Second-Order Belief Modeling**: Infers what each player wants others to believe
3. **Abductive Reassessment**: Compares Good vs. Evil explanations for each player's behavior
4. **Suspicion Level Assessment**: Assigns Low/Medium/High suspicion scores
5. **Strategic Discussion Statement**: Generates persuasive statements to influence decisions
6. **Final Deduction**: Identifies the most likely Evil players

### Multi-Model Support

The system supports multiple state-of-the-art language models:
- **GPT-4o** (OpenAI)
- **GPT-4.1** (OpenAI)
- **o1** (OpenAI reasoning model)
- **Gemma 3** (Google)
- **DeepSeek R1** (DeepSeek)
- **Qwen** (Alibaba)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Avalon-deception
   ```

2. **Install dependencies**:
   ```bash
   pip install -r remote/requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   GEMINI_API_KEY=your_gemini_api_key
   DEEPSEEK_API_KEY=your_deepseek_api_key
   QWEN_API_KEY=your_qwen_api_key
   ```

## Usage

### Basic Agent Usage

```python
from agent import Agent

# Initialize the agent
my_agent = Agent()

# Example game discussion
story = """Failed Mission: Quest 2 (Team: Players 1, 3, 4)
Discussion after Quest 2:
Player 3: "I think our last team was solid. One fail might've been an accident."
Player 4: "I don't trust that logic. Someone sabotaged the mission."
"""

# Generate response
role = "Good"
model = "gpt-4o"  # or "o1", "gemma", "deepseek", "qwen"
response = my_agent.chain_of_thought_prompt(story, role, model)
print(response)
```

### Running Experiments

Use the Jupyter notebook `test_agent.ipynb` to run systematic experiments:

1. **Experiment 1**: GPT-4o responses
2. **Experiment 1.2**: GPT-4.1 responses  
3. **Experiment 1.3**: o1 model responses

Each experiment processes the dataset and generates responses using different models for comparison.

## Dataset

The `Deception.csv` file contains:
- **Discussion Phase**: Game scenarios with player discussions
- **Generated_response_gpt_4o**: AI-generated strategic responses
- Additional columns for different model responses

## Key Components

### Agent Class (`agent.py`)

The main `Agent` class provides:
- `chain_of_thought_prompt()`: Main method for generating responses
- `create_prompt()`: Builds structured prompts with game context and reasoning framework
- `get_ToM_examples()`: Provides examples for Theory of Mind reasoning

### Model Integration Files

Each model has its own integration file:
- **llm.py**: OpenAI GPT models with rate limiting and error handling
- **gemma.py**: Google Gemma with generation configuration
- **deepseek.py**: DeepSeek R1 integration
- **o1.py**: OpenAI o1 reasoning model
- **qwen_llm.py**: Qwen model integration

## Theory of Mind Reasoning

The system implements sophisticated Theory of Mind reasoning:

```
Player X believes [Y] because [Z].
Player X wants Player Y to believe [P], likely to achieve [Q].
```

This allows the AI to:
- Understand what each player thinks
- Predict what each player wants others to think
- Make strategic deductions about hidden roles



