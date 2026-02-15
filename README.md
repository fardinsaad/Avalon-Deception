# Avalon Deception Dataset - Dialogue Verification System

## Overview

This repository contains a verification system for AI-generated Avalon Round 1 dialogues along with other dataset feature generation files with their verifications. After generating seed dialogues with GPT-4o and GPT-5.2, we use **Claude 4.5 Haiku** as an independent verifier to evaluate both outputs using **5 binary pass/fail criteria** and select the best response or apply targeted corrections.

## Game Background

**The Resistance: Avalon** is a social deception game where:
- **5 players** split into **Good** (3 players) and **Evil** (2 players) teams
- Players discuss quest outcomes to identify hidden roles
- Good players use transparent, cooperative tactics
- Evil players employ deception to avoid detection

## Project Structure

```
Avalon-deception/
├── log-gen-verifier.ipynb             # Dialogue verification notebook
├── log-gen.ipynb                      # Dialogue generation notebook
├── generated_r1_seeds_gpt4o.csv       # GPT-4o generated dialogues (225 games)
├── generated_r1_seeds_gpt5_2.csv      # GPT-5.2 generated dialogues (225 games)
├── verified_r1_seeds_combined.csv     # Output: Selected/corrected dialogues
├── verified_r1_criteria_scores.csv    # Output: Per-criterion validation scores
├── dataset-aug.ipynb                  # Player roles notebook
├── dataset-aug-public-history.ipynb   # Public History notebook
├── Deception-Dataset.csv              # Original dataset (14,481 rows, 250 games)
├── llm.py                             # OpenAI API wrapper
├── requirements-seed-generation.txt   # Python dependencies
└── .env.example                       # API keys template
```

## Features

### Binary Multi-Criteria Validation System

Claude 4.5 Haiku evaluates each dialogue using **5 binary pass/fail checks**:

1. **Player Roles Consistency** (✓/✗) - Good players use honest tactics, Evil players use deceptive tactics
2. **Public History Alignment** (✓/✗) - Dialogue contextually appropriate to game state
3. **Matrix Tactic Scale Validity** (✓/✗) - Correct row, col, tactic, scale, and level
4. **Avalon Gameplay Authenticity** (✓/✗) - Natural dialogue with strategic plausibility
5. **Dialogue Format Compliance** (✓/✗) - Exactly 4 speakers, no protagonist, correct format

### Decision Logic

Verification follows this priority system:

1. **Both 5/5 pass** → Claude performs pairwise comparison to select the better dialogue
2. **One 5/5, other <5/5** → Select the 5/5 response
3. **At least one 4/5**:
   - One 4/5, other <4/5 → Choose 4/5, apply **Targeted Correction** (fix only the failing criterion)
   - Both 4/5 → Choose GPT-5.2, apply **Targeted Correction**
4. **Both ≤3/5** → **Full Custom Generation** (generate new dialogue from scratch)

### 4×4 Behavior Matrix

The verification system validates tactics against a research-based behavior matrix:

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

## Installation

### Prerequisites

- Python 3.8+
- Anthropic API key (for Claude 4.5 Haiku)
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
   # Create .env file and add your Anthropic API key:
   echo "ANTHROPIC_API_KEY=your_actual_api_key_here" > .env
   ```

## Usage

### Quick Start

1. **Open the verification notebook**:
   ```bash
   jupyter notebook log-gen-verifier.ipynb
   ```

2. **Configure test mode** (Cell 5):
   - Locate the `TEST_LIMIT` variable
   - Set `TEST_LIMIT = 2` for testing (validates first 2 games)
   - Set `TEST_LIMIT = len(gpt4o_df)` or `225` for full verification

3. **Run all cells sequentially**:
   - Executes: Load datasets → Initialize Claude → Verify pairs → Save results

### Verification Process

The notebook performs these steps:

#### Step 1: Import Libraries and Set Paths
- Loads pandas, Anthropic client, and required modules
- Defines input files (`generated_r1_seeds_gpt4o.csv`, `generated_r1_seeds_gpt5_2.csv`)
- Defines output files (`verified_r1_seeds_combined.csv`, `verified_r1_criteria_scores.csv`)

#### Step 2: Load GPT-4o and GPT-5.2 Datasets
- Reads both generated seed files
- Displays dataset shapes and column names
- Verifies data integrity

#### Step 3: Review Validation System
- Describes 5 binary criteria
- Explains decision logic (5/5, 4/5, ≤3/5 scenarios)
- Documents correction modes

#### Step 4: Initialize Claude 4.5 Haiku
- Loads API key from `.env` file
- Creates Anthropic client with 5 max retries
- Defines system prompt for verification

#### Step 5: Run Verification Loop
- Iterates through first `TEST_LIMIT` games
- For each game pair:
  - Sends both dialogues to Claude (Response A vs Response B)
  - Receives binary pass/fail scores for 5 criteria
  - Applies decision logic based on total scores
  - Selects or corrects the best dialogue
- **Rate limiting**: 1 second delay between API calls

#### Step 6: Create Output DataFrames
- **verified_r1_seeds_combined.csv**: Selected dialogues with source labels (`LLM_used`, `Correction_Mode`)
- **verified_r1_criteria_scores.csv**: Per-criterion pass/fail tracking for analysis

#### Step 7: Save Results
- Saves both CSV files with UTF-8 encoding
- Displays summary statistics (LLM distribution, correction modes)

### TEST_LIMIT Configuration

```python
# In Cell 5 (verification loop)
TEST_LIMIT = 2  # Quick test with first 2 games (~30 seconds)

# For full verification:
TEST_LIMIT = len(gpt4o_df)  # All 225 games (~4-5 minutes)
```

**Recommended values:**
- **2**: Quick validation to test the system
- **10**: Small batch for debugging
- **225** or `len(gpt4o_df)`: Full dataset verification

### Output Files

#### 1. verified_r1_seeds_combined.csv

Selected/corrected dialogues with metadata:
- All original columns from input datasets
- `LLM_used`: Source model (GPT-4o, GPT-5.2, or Claude_Custom)
- `Correction_Mode`: None, Pairwise_Tiebreaker, Targeted, or Full_Custom

Example row:
```csv
game_id,round_id,discussion_log,matrix_tactic_scale,LLM_used,Correction_Mode
G026,1,"Discussion after Quest 1:...","{\"P2\": {\"row\":...}}",GPT-5.2,None
```

#### 2. verified_r1_criteria_scores.csv

Per-criterion validation tracking:
- `ID`: Game/Round identifier (e.g., G026_R1)
- `GPT4o_Roles`, `GPT4o_History`, `GPT4o_Matrix`, `GPT4o_Authenticity`, `GPT4o_Format`: ✓/✗
- `GPT4o_Total`: Score summary (e.g., "5/5", "4/5")
- `GPT52_Roles`, `GPT52_History`, `GPT52_Matrix`, `GPT52_Authenticity`, `GPT52_Format`: ✓/✗
- `GPT52_Total`: Score summary
- `Selected_LLM`: Chosen model
- `Correction_Mode`: Applied correction type
- `Failed_Criterion`: Which criterion failed (for Targeted corrections)

**Use for analysis**: Calculate pass rates per criterion (e.g., "GPT-4o achieved 95% format compliance")

## Key Components

### log-gen-verifier.ipynb

Main verification notebook with 7 sequential steps:
- **Steps 1-2**: Load libraries and datasets
- **Step 3**: Review binary validation system
- **Step 4**: Initialize Claude 4.5 Haiku client and verification function
- **Step 5**: Run verification loop with TEST_LIMIT configuration
- **Steps 6-7**: Create output DataFrames and save results

The verification function sends both dialogues to Claude as "Response A" and "Response B" (blind evaluation), receives binary scores for 5 criteria, and applies the decision logic.

### Anthropic API Integration

Claude 4.5 Haiku configuration:
```python
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv(override=True)
client = Anthropic(
    api_key=os.getenv('ANTHROPIC_API_KEY'),
    max_retries=5
)

# API call parameters
response = client.messages.create(
    model="claude-3-5-haiku-20241022",
    max_tokens=2048,
    temperature=0.0,
    system=SYSTEM_PROMPT,
    messages=[{"role": "user", "content": verification_prompt}]
)
```

## Scoring System

### Binary Pass/Fail Criteria

Each dialogue is evaluated on 5 independent criteria:

| Criterion | Description | Pass Example | Fail Example |
|-----------|-------------|--------------|--------------|
| **Player Roles Consistency** | Role-tactic alignment | Good player uses "Evidence sharing" | Evil player uses "Evidence sharing" |
| **Public History Alignment** | Context appropriateness | Discusses actual quest results | Mentions non-existent events |
| **Matrix Tactic Scale Validity** | Correct matrix structure | All 5 fields valid | Missing tactic or wrong scale |
| **Avalon Gameplay Authenticity** | Strategic plausibility | Natural role deduction | Unrealistic meta-gaming |
| **Dialogue Format Compliance** | Structural correctness | 4 speakers, no protagonist | Protagonist speaks or <4 players |

**Total Score**: 0/5 to 5/5 (sum of passed criteria)

### Decision Thresholds

- **5/5**: Perfect score → Pairwise comparison if both models achieve this
- **4/5**: Single criterion failure → Targeted correction applied
- **≤3/5**: Multiple failures → Full custom generation if both models score this low

## Configuration Options

### TEST_LIMIT Setting

Located in Cell 5 (verification loop):

```python
# Test with first 2 games (recommended for initial validation)
TEST_LIMIT = 2  

# Full verification of all games
TEST_LIMIT = len(gpt4o_df)  # or 225
```

**Timing estimates:**
- `TEST_LIMIT = 2`: ~30 seconds
- `TEST_LIMIT = 10`: ~2-3 minutes
- `TEST_LIMIT = 225`: ~4-5 minutes (with 1-second rate limiting)

## Cost Estimation

- **Model**: Claude 3.5 Haiku (claude-3-5-haiku-20241022)
- **Input tokens per game**: ~5,000 (context + both dialogues)
- **Output tokens per game**: ~1,500 (evaluation + corrections)
- **Cost per 1M tokens**: $1.00 input, $5.00 output

**Estimated cost for 225 games:**
- Input: 225 × 5,000 = 1.125M tokens → ~$1.13
- Output: 225 × 1,500 = 337.5K tokens → ~$1.69
- **Total**: ~$2.82

## Troubleshooting

### API Key Issues

```bash
# Verify .env file exists and contains Anthropic key
cat .env
# Should show: ANTHROPIC_API_KEY=sk-ant-...

# Test in Python
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Key loaded:', 'ANTHROPIC_API_KEY' in os.environ)"
```

### Verification Failures

Common issues:
- **JSON parse error**: Claude returned invalid JSON → Automatic retry (up to 5 attempts)
- **Missing criteria**: Check that all 5 criteria are evaluated
- **Rate limiting**: 1-second delay between calls prevents rate limits

Review verification results:
```python
# After running Cell 6
import pandas as pd
criteria_df = pd.read_csv('verified_r1_criteria_scores.csv')

# Check criterion-specific pass rates
print("GPT-4o pass rates:")
for criterion in ['Roles', 'History', 'Matrix', 'Authenticity', 'Format']:
    col = f'GPT4o_{criterion}'
    pass_rate = (criteria_df[col] == '✓').sum() / len(criteria_df) * 100
    print(f"  {criterion}: {pass_rate:.1f}%")
```

### Incremental Progress

Verification does not save incrementally (runs in-memory). If interrupted:
1. Note the last processed game from console output
2. Modify Cell 5 to start from that index:
   ```python
   for idx in range(START_INDEX, TEST_LIMIT):  # Adjust START_INDEX
   ```
3. Re-run verification loop

## Dataset Statistics

- **Input datasets**: 2 files (GPT-4o and GPT-5.2 generated dialogues)
- **Games per dataset**: 225 (G026-G250)
- **Total verifications**: 225 pairwise comparisons
- **Criteria evaluated**: 5 per dialogue × 2 dialogues = 10 checks per game
- **Total criterion checks**: 2,250 (225 games × 10 checks)
- **Output records**: 225 selected/corrected dialogues

### Expected Distribution (based on testing):
- **5/5 selections**: ~60-70% (use best response as-is)
- **4/5 targeted corrections**: ~20-30% (fix single criterion)
- **Custom generations**: ~5-10% (both models scored ≤3/5)

## Next Steps

After verification completes:

1. **Review Results**:
   ```python
   import pandas as pd
   verified_df = pd.read_csv('verified_r1_seeds_combined.csv')
   criteria_df = pd.read_csv('verified_r1_criteria_scores.csv')
   
   # Check LLM distribution
   print(verified_df['LLM_used'].value_counts())
   
   # Check correction modes
   print(verified_df['Correction_Mode'].value_counts())
   ```

2. **Analyze Per-Criterion Performance**:
   - Calculate pass rates for each of the 5 criteria
   - Compare GPT-4o vs GPT-5.2 strengths/weaknesses
   - Identify most challenging criteria

3. **Merge with Manual Seeds**:
   - Combine verified 225 games with 25 manually created seeds (G001-G025)
   - Create final 250-game dataset

4. **Quality Assurance**:
   - Manually review samples from "Targeted" and "Full_Custom" categories
   - Verify corrections address the failing criteria

## Contributing

For the main Avalon AI agent project, see [README-v1.md](README-v1.md).





