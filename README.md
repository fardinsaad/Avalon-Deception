# Avalon Deception Dataset - Dialogue Generation & Verification System

## Overview

This repository contains a complete pipeline for generating and verifying AI-generated Avalon Round 1 dialogues. The system uses Large Language Models (LLMs) to generate realistic game discussions, then employs **Claude Sonnet 4.5** as an independent verifier to evaluate and select the best outputs using **5 binary pass/fail criteria**.

## Game Background

**The Resistance: Avalon** is a social deduction game where:
- **5 players** split into **Good** (3 players) and **Evil** (2 players) teams
- Players discuss quest outcomes to identify hidden roles
- Good players use transparent, cooperative tactics
- Evil players employ deception to avoid detection

## Project Structure

```
Avalon-deception/
├── log-gen-r1.ipynb                   # Round 1: Dialogue generation notebook
├── log-gen-r2.ipynb                   # Round 2: Two-pass dialogue generation notebook
├── log-gen-verifier-r1.ipynb          # Round 1: Dialogue verification (Layer 1 pair comparison + Layer 2 recheck)
├── log-gen-verifier-r1-4c.ipynb       # Round 1: Standalone second-pass recheck (historical; Layer 2 now integrated into per-round verifiers)
├── log-gen-verifier-r2.ipynb          # Round 2: Combined verification notebook (Layer 1 + Layer 2, prior_summary_gold context)
├── Deception-Dataset.csv              # Master dataset (250 games, all rounds)
├── tactics_knowledge_base.json        # 4×4 behavior matrix (37 tactics)
├── llm.py                             # OpenAI API wrapper
├── gemini.py                          # Google Gemini API wrapper
├── requirements-seed-generation.txt   # Python dependencies
├── .env                               # API keys (create this file)
├── Datasets/
│   ├── seeds/                         # Generated (unverified) dialogue CSVs
│   │   ├── generated_r1_seeds_gemini3.csv
│   │   ├── generated_r1_seeds_gpt5_2.csv
│   │   ├── generated_r2_seeds_gemini3.csv
│   │   └── generated_r2_seeds_gpt5_2.csv
│   ├── verified/                      # Verified dialogue CSVs (Claude verifier output)
│   │   ├── verified_r1_seeds_combined.csv
│   │   ├── verified_r1_criteria_scores.csv
│   │   ├── verified_r2_seeds_combined.csv      # (generated after R2 verification)
│   │   └── verified_r2_criteria_scores.csv     # (generated after R2 verification)
│   └── role_history/                  # Player role assignment and public history files
│       ├── Avalon_Balanced_250_Dataset_Round1.csv
│       ├── Avalon_R1_Public_History.csv
│       ├── Avalon_R1_Public_History_F.csv
│       ├── Avalon_FINAL_Public_history.csv
│       └── Deception_Dataset_Augmented_Public_History-Full.csv
└── fig/                               # Role balance and distribution figures
```

## Installation

### Prerequisites

- Python 3.8+
- Jupyter Notebook
- API keys for:
  - **OpenAI** (for GPT-5.2) - https://platform.openai.com/api-keys
  - **Google Gemini** (for Gemini-3.1) - https://aistudio.google.com/app/apikey
  - **Anthropic** (for Claude Sonnet 4.5) - https://console.anthropic.com/

### Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements-seed-generation.txt
   ```

2. **Configure API keys** — create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your_openai_key_here
   GEMINI_API_KEY=your_gemini_key_here
   ANTHROPIC_API_KEY=your_anthropic_key_here
   ```

3. **Verify installation**:
   ```bash
   python llm.py      # Test OpenAI connection
   python gemini.py   # Test Gemini connection
   ```

---

## Pipeline Overview — Round 2 (`log-gen-r2.ipynb`)

Round 2 generation uses a **two-pass pipeline**:

- **PASS 1 (GPT-5.2)** — Tactic pre-computation: reads each player's Round 1 tactic as a seed anchor, considers the current game state, and outputs a strategically evolved `matrix_tactic_scale` for Round 2.
- **PASS 2 (GPT-5.2 or Gemini-3.1)** — Dialogue generation: uses the PASS 1 pre-computed matrix as assigned tactics, generates a 4-speaker discussion log grounded in the cumulative public history and prior Round 1 dialogue.

> **Prerequisite**: `Deception-Dataset.csv` must have Round 1 `discussion_log` and `matrix_tactic_scale` populated (completed via `log-gen-r1.ipynb` + `log-gen-verifier-r1.ipynb`).

---

## Running `log-gen-r2.ipynb`

### Step 1 — Load data and build tactics (Cells 1–11)

Run all setup cells in order. These load the dataset, build the R1 context lookup, extract per-player skill levels, and define helper functions. No configuration needed.

Expected output from Cell 4:
```
Total Round 2 rows: 250
Games needing generation: 250
```

---

### Step 2 — PASS 1: Tactic pre-computation (Cells 12–14)

**Cell 12 — Configure PASS 1:**
```python
PASS1_NUM_GAMES = 2                   # Test: 2 games
# PASS1_NUM_GAMES = len(games_to_generate)  # Full: 250 games
```

**Cell 13 — Run PASS 1 execution.** GPT-5.2 pre-assigns tactics for each speaker based on R1 seeds and current game state. Saves to `pass1_r2_tactic_precompute.csv`.

> If the file already exists, Cell 13 skips automatically — proceed directly to PASS 2.

**Cell 14 — Load and inspect.** Prints the pre-assigned matrix for the first game to verify output.

---

### Step 3 — PASS 2: Dialogue generation (Cells 15–17)

**Cell 15 — Configure PASS 2:**
```python
PASS2_MODEL_SELECTION = 'gpt-5.2'   # Options: 'gpt-5.2' or 'gemini-3'
PASS2_NUM_GAMES = 2                  # Test: 2 games
# PASS2_NUM_GAMES = len(p2_candidates)   # Full: all PASS 1 games
```

| Model | Output file |
|---|---|
| `'gpt-5.2'` | `generated_r2_seeds_gpt5_2.csv` |
| `'gemini-3'` | `generated_r2_seeds_gemini3.csv` |

**Cell 16 — Run PASS 2 execution.** Generates a 4-speaker dialogue per game using the PASS 1 matrix.

**To generate both model outputs**, run Cells 15–16 twice:
1. `PASS2_MODEL_SELECTION = 'gpt-5.2'` → run Cell 16
2. `PASS2_MODEL_SELECTION = 'gemini-3'` → run Cell 16

**Cell 17 — Review.** Prints the first generated dialogue and its `matrix_tactic_scale`.

---

### Step 4 — Verify outputs

Run `log-gen-verifier-r2.ipynb` (see next section) with both PASS 2 seed files as input.

---

## Running `log-gen-verifier-r2.ipynb`

The verifier uses a **two-layer pipeline**:

- **Layer 1** (`verify_dialogue_pair()`) — Blind pair comparison: Claude Sonnet 4.5 evaluates both model outputs against 5 binary criteria (coherence, history alignment, tactic-dialogue alignment, authenticity, format). Produces a decision: direct selection, targeted correction, or full custom generation.
- **Layer 2** (`verify_single_dialogue()`) — Inline recheck: immediately after every targeted or custom correction, the corrected dialogue is verified on the same 5 criteria (up to 3 attempts). Rows that fail all 3 attempts are flagged `NEEDS_HUMAN`.

**Inputs:**
- `Datasets/seeds/generated_r2_seeds_gemini3.csv` — Gemini-3.1 PASS 2 output
- `Datasets/seeds/generated_r2_seeds_gpt5_2.csv` — GPT-5.2 PASS 2 output

**Outputs:**
- `Datasets/verified/verified_r2_seeds_combined.csv` — Selected and corrected dialogues
- `Datasets/verified/verified_r2_criteria_scores.csv` — Per-criterion scores + inline recheck metadata

> **Prerequisite**: Both PASS 2 seed files must be generated (see above). R1 summaries (`prior_summary_gold`) are read directly from the seed CSVs and passed to the verifier prompt.

---

### Step 1 — Setup (Cells 1–5)

Run all setup cells in order. No configuration needed.

- **Cell 1**: Imports (`pandas`, `json`, `anthropic`, `dotenv`, `os`, `time`)
- **Cell 2**: Load both seed CSVs. Expected output:
  ```
  Gemini-3.1 dataset loaded: 250 rows, 9 columns
  GPT-5.2 dataset loaded: 250 rows, 9 columns
  ```
- **Cell 3**: Initialize Claude Sonnet 4.5 client and system prompt (with `max_retries=5`)
- **Cell 4**: Define `verify_dialogue_pair()` — Layer 1 pair evaluator
- **Cell 5**: Define `verify_single_dialogue()` — Layer 2 inline recheck

---

### Step 2 — Configure the decision logic (Cells 6–7, Markdown)

These markdown cells document the 5-tier decision logic applied by Layer 1:

| Gemini-3.1 Score | GPT-5.2 Score | Action | `LLM_used` |
|---|---|---|---|
| 5/5 | 5/5 | Claude pairwise tiebreaker → select better | `Gemini-3.1` or `GPT-5.2` |
| 5/5 | <5/5 | Select the 5/5 response | `Gemini-3.1` |
| <5/5 | 5/5 | Select the 5/5 response | `GPT-5.2` |
| 4/5 | 4/5 | Claude pairwise judgment → targeted correction | `*-Claude-4.5` |
| 4/5 | <4/5 | Targeted correction of 4/5 response | `Gemini-3.1-Claude-4.5` |
| <4/5 | 4/5 | Targeted correction of 4/5 response | `GPT-5.2-Claude-4.5` |
| ≤3/5 | ≤3/5 | Claude full custom generation | `Claude-4.5` |

Any targeted or custom-generated dialogue is immediately passed through Layer 2 inline recheck.

---

### Step 3 — Step 4a: Main verification loop (Cell 8)

**Configure the test limit before running:**
```python
TEST_LIMIT = 2                    # Test: 2 games
# TEST_LIMIT = len(gemini3_df)   # Full: 250 games
```

Run Cell 8. For each game, Layer 1 fires, and Layer 2 fires inline if a correction was made. Progress is printed per-game. Expected summary output (2-game test):
```
================================================================================
Verification Summary (2 games):
  Total verified:                          2
  Gemini-3.1 selected (original):          0
  GPT-5.2 selected (original):             2
  Pairwise tiebreaker used:                0
  Gemini-3.1 + Targeted correction:        0
  GPT-5.2 + Targeted correction:           0
  Claude 4.5 full custom generation:       0
  Flagged NEEDS_HUMAN (inline L2 failed):  0
  Errors (API/parse failure):              0
  Queued for Step 4b retry:                0
```

---

### Step 4 — Step 4b: Retry failed rows (Cell 9)

Automatically retries any rows from Step 4a that failed due to API errors or silent fallbacks (`Targeted`/`Full_Custom` producing empty output). If the cell prints `✅ No rows to retry`, proceed immediately.

For each successfully retried row that produced a targeted or custom correction, **the same inline Layer 2 recheck (up to 3 attempts) runs automatically**, identical to Step 4a.

Rows that still fail after retry receive a hard fallback (best-scoring raw model dialogue), logged with `-Fallback` suffix in `LLM_used`.

---

### Step 5 — Step 4c: NEEDS_HUMAN summary (Cell 10)

Prints a summary of all inline Layer 2 recheck outcomes:

```
============================================================
Step 4c — Inline Layer 2 Recheck Summary
============================================================
  N/A (direct selections, no recheck):     X
  INLINE_ACCEPTED (passed 5/5 on recheck): X
  INLINE_FIXED (passed after >=1 fix):     X
  NEEDS_HUMAN (all 3 attempts failed):     X
```

If any rows are flagged `NEEDS_HUMAN`, they are printed with their game IDs. These rows require manual inspection before merging into the master dataset.

---

### Step 6 — Save outputs (Cell 11)

Cell 11 saves both output CSVs. Expected output:
```
✓ Saved verified_r2_seeds_combined.csv (250 rows)
✓ Saved verified_r2_criteria_scores.csv (250 rows)
```

Both files are written to `Datasets/verified/`.

---

### Step 7 — Analysis (Cells 12–17, optional)

Run any or all analysis cells to inspect score distributions, per-criterion pass rates, correction mode breakdown, and LLM selection statistics. These cells read directly from the saved `verified_r2_criteria_scores.csv` file and do not modify data.

---

## Quick Reference

### `log-gen-r2.ipynb` (Generation)

| Run type | PASS1_NUM_GAMES | PASS2_NUM_GAMES | Estimated time |
|---|---|---|---|
| Test (2 games) | `2` | `2` | ~1 minute |
| Full (250 games) | `len(games_to_generate)` | `len(p2_candidates)` | ~3–4 hours |

### `log-gen-verifier-r2.ipynb` (Verification)

| Run type | `TEST_LIMIT` | Estimated time | Estimated cost |
|---|---|---|---|
| Test (2 games) | `2` | ~1–2 minutes | <$0.05 |
| Full (250 games) | `len(gemini3_df)` | ~25–40 minutes | ~$6–10 |

---

## Troubleshooting

**API Key Errors**: Verify `.env` file exists with correct keys. Run `python llm.py` to test.

**PASS 1 already exists warning**: Expected behavior — the cell skips PASS 1 and uses the cached file. Delete `pass1_r2_tactic_precompute.csv` to force a re-run.

**Validation failures**: Check that `Deception-Dataset.csv` has R1 `discussion_log` populated for all games. Games with empty R1 context will be skipped.

**Verifier rows flagged NEEDS_HUMAN**: All 3 inline Layer 2 attempts failed for those rows. Inspect manually, fix the dialogue, and patch `verified_r2_seeds_combined.csv` before merging.

**Memory issues**: Restart kernel and clear outputs via Kernel → Restart & Clear Output.

---

## Citation

```bibtex
[Citation information to be added]
```

## License

[License information to be added]
