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
├── log-gen.ipynb                      # Round 1: Dialogue generation notebook
├── log-gen-r2.ipynb                   # Round 2: Two-pass dialogue generation notebook
├── log-gen-verifier.ipynb             # Dialogue verification notebook (all rounds)
├── Deception-Dataset.csv              # Master dataset (250 games, all rounds)
├── tactics_knowledge_base.json        # 4×4 behavior matrix (37 tactics)
├── llm.py                             # OpenAI API wrapper
├── gemini.py                          # Google Gemini API wrapper
├── requirements-seed-generation.txt   # Python dependencies
└── .env                               # API keys (create this file)
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

> **Prerequisite**: `Deception-Dataset.csv` must have Round 1 `discussion_log` and `matrix_tactic_scale` populated (completed via `log-gen.ipynb` + `log-gen-verifier.ipynb`).

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

Run `log-gen-verifier.ipynb` on both PASS 2 outputs (same 5-criteria pipeline as Round 1):
- Input: `generated_r2_seeds_gemini3.csv` + `generated_r2_seeds_gpt5_2.csv`
- Output: `verified_r2_seeds_combined.csv` + `verified_r2_criteria_scores.csv`

---

## Quick Reference

| Run type | PASS1_NUM_GAMES | PASS2_NUM_GAMES | Estimated time |
|---|---|---|---|
| Test (2 games) | `2` | `2` | ~1 minute |
| Full (250 games) | `len(games_to_generate)` | `len(p2_candidates)` | ~3–4 hours |

---

## Troubleshooting

**API Key Errors**: Verify `.env` file exists with correct keys. Run `python llm.py` to test.

**PASS 1 already exists warning**: Expected behavior — the cell skips PASS 1 and uses the cached file. Delete `pass1_r2_tactic_precompute.csv` to force a re-run.

**Validation failures**: Check that `Deception-Dataset.csv` has R1 `discussion_log` populated for all games. Games with empty R1 context will be skipped.

**Memory issues**: Restart kernel and clear outputs via Kernel → Restart & Clear Output.

---

## Citation

```bibtex
[Citation information to be added]
```

## License

[License information to be added]
