# Avalon Deception Dataset - Seed Dialog Generation

## Overview

This repository contains tools for generating synthetic Round 1 game discussions for the **Avalon Deception Dataset**. Using GPT-4o and a structured behavior matrix framework, we augment the dataset with realistic tactical communication patterns across 24 deception tactics and multiple skill levels.

## Game Background

**The Resistance: Avalon** is a social deduction game where:
- **5 players** split into **Good** (3 players) and **Evil** (2 players) teams
- Players discuss quest outcomes to identify hidden roles
- Good players use transparent, cooperative tactics
- Evil players employ deception to avoid detection

## Project Structure

```
Avalon-deception/
├── log-gen.ipynb                      # Main seed generation notebook
├── llm.py                             # OpenAI API wrapper with retry logic
├── Deception-Dataset.csv              # Input dataset (14,481 rows, 250 games)
├── requirements-seed-generation.txt   # Python dependencies
├── .env.example                       # API key template
├── .gitignore                         # Git ignore rules
└── generated_r1_seeds.csv             # Output (generated)
```

## Features

### 4×4 Behavior Matrix

The generation framework uses a research-based behavior matrix:

**Rows (Information Strategy):**
- Transparent
- Selective/Framing  
- Careless-to-truth
- Counterfactual

**Columns (Goal Orientation):**
- Cooperative
- Defensive
- Opportunistic
- Adversarial

**37 Tactical Patterns** including:
- Evidence sharing, Rational justification (Good players)
- Hard lying, Gaslighting, Strategic fabrication (Evil players)
- Deflection, Half-truths (Both alignments)

### Skill Assessment Scales

- **GRS (Goodness Rationality Spectrum)** for Good players: High/Moderate/Low rationality
- **Mach-IV (Machiavellianism Scale)** for Evil players: High/Moderate/Low deception skill

### Generation Pipeline

1. **Dataset Loading**: Filter Round 1 games needing discussion logs
2. **Tactic Assignment**: Pre-compute balanced coverage across all 24 tactics
3. **Prompt Engineering**: 5 few-shot examples with tactical diversity
4. **LLM Generation**: GPT-4o with JSON mode and validation
5. **Quality Control**: Format validation, protagonist exclusion, scale matching

## Installation

### Prerequisites

- Python 3.8+
- OpenAI API key
- Jupyter Notebook

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Avalon-deception
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements-seed-generation.txt
   ```

3. **Configure API key**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key:
   # OPENAI_API_KEY=your_actual_api_key_here
   ```

## Usage

### Quick Start

1. **Open the notebook**:
   ```bash
   jupyter notebook log-gen.ipynb
   ```

2. **Configure generation**:
   - Navigate to Cell 20
   - Set `NUM_GAMES_TO_GENERATE = 2` for testing (or 225 for full batch)

3. **Run all cells**:
   - Executes: Data loading → Tactic assignment → Generation loop
   - Output: `generated_r1_seeds.csv`

### Generation Process

The notebook performs these steps:

#### Step 1: Load Dataset
- Filters Round 1 games (G026-G250) without discussion logs
- Identifies 225 games needing generation

#### Step 2: Build Tactics Knowledge Base
- Constructs 4×4 behavior matrix with 24 tactics
- Defines tactic descriptions and scale levels
- Saves to `tactics_knowledge_base.json`

#### Step 3: Pre-compute Assignments
- Assigns tactics to each speaking player (4 per game)
- Ensures balanced coverage: ~37-38 uses per tactic
- Cycles through skill levels (High/Moderate/Low)

#### Step 4: Design Prompts
- Includes game context (roles, public history)
- 5 few-shot examples with diverse tactics
- Suggested tactics with scales and levels

#### Step 5: Generate with Validation
- Calls `get_completion_with_backoff` from llm.py
- Validates output format and protagonist exclusion
- Incremental saves every 10 games
- Rate limiting: 1 second between API calls

### Output Format

Generated CSV contains:
- `discussion_log`: Formatted dialogue text
- `matrix_tactic_scale`: JSON with player tactics, scales, levels

Example:
```json
{
  "discussion_log": "Discussion after Quest 1:\n\nP3: \"I think that P1, P4, and me would make a great team\"\n\nP2: \"P1 and P4 went on the last mission and it failed. P3 must be evil\"\n\nP4: \"I know the first mission with me and P1 failed, but it was obviously P1 who failed it\"\n\nP5: \" It is not a good idea to form a team with both P1 and P4.\"",
  "matrix_tactic_scale": {
    "P3": {"row":"Selective / Framing","col":"Opportunistic","tactic":"False consensus","scale":"Mach-IV","level":"Moderate"},
    "P2": {"row":"Transparent","col":"Cooperative","tactic":"Rational justification","scale":"GRS","level":"High"},
    "P4": {"row":"Counterfactual","col":"Defensive","tactic":"Deflection","scale":"Mach-IV","level":"High"},
    "P5": {"row":"Selective / Framing","col":"Cooperative","tactic":"Strategic uncertainty","scale":"GRS","level":"High"}
  }
}
```

## Key Components

### llm.py

OpenAI API wrapper providing:
- **get_completion_with_backoff()**: Automatic retry with exponential backoff
- **Rate limit handling**: Up to 100 seconds max wait time
- **Flexible parameters**: Supports all OpenAI API options via `**kwargs`

Used in [log-gen.ipynb](log-gen.ipynb):
```python
from llm import get_completion_with_backoff

response = get_completion_with_backoff(
    model="gpt-4o",
    messages=[...],
    response_format={"type": "json_object"},
    temperature=0.5,
    max_tokens=1024
)
```

### log-gen.ipynb

Main notebook with 22+ cells:
- **Cells 1-7**: Dataset loading and filtering
- **Cells 8-14**: Behavior matrix, tactics, scales
- **Cells 15-16**: Tactic assignment algorithm
- **Cell 17**: Prompt template with 5 examples
- **Cell 18**: Import llm.py functions
- **Cell 19**: Validation logic
- **Cells 20-21**: Configuration and generation loop
- **Cell 22**: Results review

## Validation

The `validate_generation()` function ensures:
- ✓ Discussion starts with "Discussion after Quest 1:"
- ✓ Protagonist (role_id) does NOT speak
- ✓ Exactly 4 speakers (excluding protagonist)
- ✓ Matrix has required fields: row, col, tactic, scale, level
- ✓ Scale matches role (GRS for Good, Mach-IV for Evil)
- ✓ Tactic exists in definitions
- ✓ Protagonist not in matrix_tactic_scale

## Configuration Options

### Cell 20 Settings

```python
NUM_GAMES_TO_GENERATE = 225  # Number of games to generate

# Recommended values:
# - 2: Quick test (2-3 minutes)
# - 25: Small batch validation (~30 minutes)
# - 225: Full dataset (~4 hours with rate limiting)
```

### API Call Parameters (Cell 21)

```python
response = get_completion_with_backoff(
    model="gpt-4o",              # Model choice
    temperature=0.5,             # Creativity (0.0-1.0)
    max_tokens=1024,             # Max response length
    response_format={"type": "json_object"}  # Force JSON output
)
```

## Cost Estimation

- **Model**: GPT-4o (gpt-4o)
- **Input tokens per game**: ~4,000 (prompt with examples)
- **Output tokens per game**: ~600 (discussion + matrix)
- **Cost per 1M tokens**: $2.50 input, $10.00 output

**Estimated cost for 225 games:**
- Input: 225 × 4,000 = 900K tokens → ~$2.25
- Output: 225 × 600 = 135K tokens → ~$1.35
- **Total**: ~$3.60

## Troubleshooting

### API Key Issues

```bash
# Verify .env file exists
cat .env

# Check API key is loaded (in llm.py)
python llm.py
# Should print: "API key loaded successfully."
```

### Generation Failures

Common issues:
- **JSON parse error**: LLM returned invalid JSON → Automatic retry
- **Validation failed**: Check error messages in output
- **Rate limit**: Backoff logic handles automatically

Review failed games:
```python
# In Cell 21 output
if failed_games:
    for game_id, errors in failed_games:
        print(f"{game_id}: {errors}")
```

### Incremental Progress

Generation saves every 10 games to `generated_r1_seeds.csv`. If interrupted:
1. Check current progress: `len(pd.read_csv('generated_r1_seeds.csv'))`
2. Adjust starting index in Cell 21
3. Resume generation

## Dataset Statistics

- **Total rows**: 14,481
- **Unique games**: 250
- **Rounds per game**: 5 (R1-R5)
- **Games with R1 discussion**: 25 (G001-G025)
- **Games needing generation**: 225 (G026-G250)
- **Speakers per game**: 4 (1 protagonist observes)
- **Total assignments**: 900 (225 games × 4 speakers)
- **Tactics coverage**: ~37-38 uses per tactic

## Contributing

For the main Avalon AI agent project, see [README-v1.md](README-v1.md).





