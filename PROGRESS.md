# Avalon Deception Dataset Augmentation - Progress Tracker

**Project Start Date**: January 23, 2026  
**Last Updated**: April 10, 2026
**Status**: Phase 1 ✅ COMPLETE. Phase 2 ✅ COMPLETE. Phase 4 (R2-R5 generation) IN PROGRESS. R2 generation complete (`log-gen-r2.ipynb`). R3 dialogues generated (`log-gen-r3.ipynb`). **Next: verify R3 dialogues** using `log-gen-verifier.ipynb`.

---

## ⚠️ Important Notes (April 10, 2026)

### File Reorganization
All generated CSV files moved into `Datasets/` with sub-structure:
- `Datasets/seeds/` — raw generated seeds (unverified dialogue CSVs)
- `Datasets/verified/` — verified outputs (combined + criteria scores)
- `Datasets/role_history/` — player role assignments and public history files

**Path registry** — notebooks that reference these paths (update here if paths change):
| File | Variable | Current Path |
|---|---|---|
| `log-gen-verifier.ipynb` | `GEMINI3_FILE` | `Datasets/seeds/generated_r1_seeds_gemini3.csv` |
| `log-gen-verifier.ipynb` | `GPT52_FILE` | `Datasets/seeds/generated_r1_seeds_gpt5_2.csv` |
| `log-gen-verifier.ipynb` | `OUTPUT_FILE_COMBINED` | `Datasets/verified/verified_r1_seeds_combined.csv` |
| `log-gen-verifier.ipynb` | `OUTPUT_FILE_CRITERIA` | `Datasets/verified/verified_r1_criteria_scores.csv` |
| `log-gen-verifier-4c.ipynb` | `GEMINI3_FILE` | `Datasets/seeds/generated_r1_seeds_gemini3.csv` |
| `log-gen-verifier-4c.ipynb` | `OUTPUT_FILE_COMBINED` | `Datasets/verified/verified_r1_seeds_combined.csv` |
| `log-gen-verifier-4c.ipynb` | `OUTPUT_FILE_CRITERIA` | `Datasets/verified/verified_r1_criteria_scores.csv` |
| `log-gen-r2.ipynb` | `PASS1_OUTPUT_FILE` | `pass1_r2_tactic_precompute.csv` (root — not moved) |
| `log-gen-r2.ipynb` | `PASS2_OUTPUT_FILE` | `Datasets/seeds/generated_r2_seeds_*.csv` |

> **Warning**: git merges can silently revert uncommitted notebook edits. Always commit path changes immediately.

### Role-Balance Figures
Figures `fig/a–e` regenerated directly from `Deception-Dataset.csv` on April 10, 2026 (ground truth). The `dataset-aug.ipynb` notebook is not used for figure generation — it contains deletions that prevent exact reproduction of the original player role assignment. Role generation process will be described in the paper; figures are verified correct.

### Player Role Reproducibility
`dataset-aug.ipynb` cannot exactly reproduce the 250 game-by-game role assignments because the macro-distribution solver used an unseeded `random.shuffle`. The statistical balance (10 combinations × 25 games each, 100 Evil / 150 Good per player) is correct and verifiable from `Deception-Dataset.csv`. Exact reproduction is not possible from the notebook alone.

---

## 📋 Project Overview

**Goal**: Create a comprehensive Avalon social deduction game dataset with **10,000-20,000 samples** augmented with rich tactical annotations and Theory of Mind (ToM) gold labels, grounded in three deception theories (IDT, TDT, IMT2).

**Development Strategy**: 
- **Phase 1 (Current)**: Complete 250 games × 5 rounds ≈ 1,000 validated samples with full pipeline
- **Phase 2 (Immediate Next)**: Generate ToM gold labels for all 1,000 samples  
- **Phase 3 (Scale-Up)**: Expand to 10,000-20,000 samples using validated pipeline

**Current Target**: 250 games with 5 rounds each (≈1,000 samples)  
**Current Completion**: Round 1 complete and verified (225 games × 2 LLM models = 450 dialogues)

---

## 🏗️ Project Architecture: Three Augmentation Stages

### **STAGE 1: Player Role Augmentation** ✅ COMPLETE
**File**: `dataset-aug.ipynb` (2362 lines, 20+ cells)  
**Purpose**: Assign balanced Good/Evil player roles to each game

**Methodology**:
- Fixed composition: 3 Good players + 2 Evil players per game
- Balanced distribution: Each position (P1-P5) assigned equally across Good/Evil
- Deterministic assignment: Fixed for reproducible evaluation
- Output column: `player_roles` (JSON mapping P1-P5 to roles)

**Status**: ✅ Complete - 250 games augmented with role assignments

**Key Outputs**:
- `player_roles` JSON column with format: `{"P1":"Good","P2":"Evil","P3":"Good","P4":"Good","P5":"Evil"}`
- Balanced distribution validated: each position appears ~125 times as Good/Evil

---

### **STAGE 2: Public History Augmentation** ✅ COMPLETE
**File**: `dataset-aug-public-history.ipynb` (1720 lines, 25+ cells)  
**Verifier**: `ph-verifier.ipynb` (validation notebook)  
**Purpose**: Generate realistic game histories (quest outcomes, team compositions, voting patterns)

**Methodology**:
1. **Quest outcome sequence**: Predefined per game (e.g., [PASS, PASS, FAIL, PASS, PASS])
2. **Team composition generation**: 
   - PASS teams: All-Good or Good-majority
   - FAIL teams: At least one Evil player
   - Outcome-dependent selection
3. **Voting patterns**: 
   - Good players vote YES on trusted/safe teams
   - Evil players vote strategically (approval for favorable teams, rejection for threats)
4. **Constraint satisfaction**: All votes, team sizes, game termination validated

**Verification Results** (ph-verifier.ipynb):
- **Hard constraints**: 0 violations across 250 games ✅
  - Quest outcomes match predefined sequence
  - Team sizes valid (3 for R1-R4, 2 for R5)
  - Vote counts consistent (5 per round)
  - Game termination correct
- **Soft constraints**: Acceptable variation
  - Voting patterns realistic
  - Team diversity adequate

**Status**: ✅ Complete - 250 games with public history validated

**Key Outputs**:
- `public_history` text field with complete game progression
- Example format:
  ```
  Round: 1
  Leader: P3
  Team: P1, P3
  Votes: P1:Y P2:Y P3:Y P4:Y P5:Y
  Quest 1 Outcome: PASS
  ```

---

### **STAGE 3: Discussion Log & Tactic Annotation Generation** ✅ COMPLETE (Verification In Progress)

#### **Part A: Behavioral Framework Definition** ✅
**Purpose**: Define 37 deception tactics organized in 4×4 matrix

**Matrix Structure**:
- **Rows (Information Strategy)**: 
  - Transparent, Selective/Framing, Careless-to-truth, Counterfactual
- **Columns (Goal Orientation)**: 
  - Cooperative, Defensive, Opportunistic, Adversarial
- **16 cells × 1-3 tactics each = 37 total tactics**

**Theoretical Grounding**:
- **Columns (Goal)**: Interpersonal Deception Theory (IDT) + Truth-Default Theory (TDT)
- **Rows (Information)**: Information Manipulation Theory 2 (IMT2) + Philosophy of Lying/Bullshitting

**Tactic Color-Coding**:
- 🟢 **Green (Good-only)**: 10 tactics (transparent, honest strategies)
- 🔴 **Red (Evil-only)**: 18 tactics (deceptive, manipulative strategies)
- 🔵 **Blue (Both)**: 9 tactics (used by Evil players in our assignment strategy)

**Skill Assessment Scales**:
- **GRS (Goodness Rationality Spectrum)** for Good players: High/Moderate/Low
- **Mach-IV (Machiavellianism)** for Evil players: High/Moderate/Low

---

#### **Part B: LLM-Based Dialogue Generation** ✅
**File**: `log-gen.ipynb` (992 lines, 22 cells)  
**Models**: Gemini-3.1 and GPT-5.2  
**Purpose**: Generate discussion logs for each game/round with tactical annotations

**Cell Breakdown**:
- **Cells 1-7**: Dataset loading, Round-1 filtering, initial EDA
- **Cells 8-14**: Behavior matrix, 37 tactic definitions, skill scales, helper functions
- **Cell 16**: Tactic assignment algorithm (level-based distribution for balanced coverage and reduced blue tactic dominance)
- **Cell 17**: Coverage analysis (17-32 uses per tactic across 900 turns, stratified by color: green 29-32, red 17-20, blue 22-28)
- **Cell 18**: **Prompt template** with:
  - Game context (roles, public history, quest outcome)
  - Avalon rules explanation
  - Complete behavior matrix with 37 tactics
  - Skill level descriptions (GRS/Mach-IV)
  - Pre-assigned tactics for each speaker (level-appropriate)
  - **5 few-shot examples** (G001, G002, G006, G009, G023) showing diverse tactics, outcomes, skill levels
  - Strict JSON output schema
- **Cell 20**: Import LLM modules (`get_completion_with_backoff()`, `get_gemini_completion()`)
- **Cell 21**: Validation function (8-point checklist)
- **Cell 22**: Configuration (`MODEL_SELECTION`, `NUM_GAMES_TO_GENERATE`)
- **Cell 23**: Generation loop with JSON parsing, validation, incremental saving
- **Cell 24**: Results review and statistics

**Few-Shot Examples Used** (5 games from existing dataset):
- G001: Round 1 PASS - Diverse tactics, balanced Good/Evil speech
- G002: Round 1 or 2 - Different quest outcome to show contextual variation
- G006: Round 1 FAIL - Evil accusation tactics, defensive Good play
- G009: Round 1 PASS - Trust-building Evil, rational Good responses
- G023: Late round strategic play - Complex deception and reads

**Tactic Pre-Assignment Strategy (Level-Based Distribution)**:
To achieve realistic tactical diversity and reduce over-representation of defensive tactics, we implement a **level-based assignment strategy** that assigns tactics based on player skill level:

**Skill Level Pools**:
- **High Level (Skilled Players)**: Use ONLY alignment-specific tactics
  - Good High: 10 green tactics (Evidence sharing, Rational justification, etc.)
  - Evil High: 18 red tactics (Hard lying, Gaslighting, Strategic fabrication, etc.)
  - Rationale: Skilled players use sophisticated, alignment-appropriate tactics

- **Moderate Level (Competent Players)**: Use ALL available tactics (mix)
  - Good Moderate: 19 tactics (10 green + 9 blue)
  - Evil Moderate: 27 tactics (18 red + 9 blue)
  - Rationale: Competent players employ diverse strategies including defensive moves

- **Low Level (Unskilled Players)**: PREFER blue defensive tactics first
  - Good Low: 19 tactics (9 blue + 10 green, blue prioritized)
  - Evil Low: 27 tactics (9 blue + 18 red, blue prioritized)
  - Rationale: Unskilled players are more defensive, uncertain, and reactive

**Distribution Strategy**:
- Level assignment: Cycled uniformly across speakers (High → Moderate → Low → High...)
- Within each level: Tactics selected cyclically from the appropriate pool
- Duplicate prevention: No tactic appears twice within the same game's 4 speakers
- Six separate cyclic counters maintain balanced usage across all pools

**Achieved Distribution (225 games, 900 speaking turns)**:
- **Scale-Level Balance**: Each of 6 combinations (GRS_High, GRS_Moderate, GRS_Low, Mach-IV_High, Mach-IV_Moderate, Mach-IV_Low) appears ~150 times (exactly 1/6 of total)
- **Tactic Usage**:
  - Green tactics (Good-only): 29-32 uses each (dominate top 10 due to smaller pool)
  - Red tactics (Evil-only): 17-20 uses each (larger pool spreads usage)
  - Blue tactics (Both): 22-28 uses each (~25% overall usage, down from ~40%)
- **Top 10 Most Used**: Predominantly green tactics (Perspective-taking, Evidence sharing, Pragmatic silence, etc.) plus one blue tactic (Self-deception)
- **Bottom 10 Least Used**: All red tactics (Cherry-picking, Obfuscatory nonsense, Hard lying, etc.)

**Theoretical Justification**:
This level-based approach aligns with deception theory literature:
- High-skill deceivers use **sophisticated, alignment-appropriate tactics** (Hard lying, Strategic fabrication for Evil; Evidence sharing, Rational justification for Good)
- Low-skill agents exhibit **defensive, reactive behaviors** regardless of alignment (Self-justification, Deflection, Face-saving blather)
- Blue (Both) tactics represent universal defensive responses to social pressure, naturally suited to less skilled players

**Impact**: By restricting blue tactics to Moderate/Low levels, we achieve ~25% blue usage (target met!) while maintaining tactical realism and proper skill-level characterization.

**Validation Checklist** (all generated dialogues must pass):
1. Format: Starts with "Discussion after Quest R:"
2. Protagonist exclusion: Observing player doesn't appear
3. Speaker count: Exactly 4 speakers (all non-protagonist)
4. Matrix structure: 4 entries in matrix_tactic_scale
5. Scale-role alignment: GRS for Good, Mach-IV for Evil
6. Level validity: {High, Moderate, Low}
7. Tactic validity: Name in 37-tactic taxonomy
8. Field completeness: All required fields present

**Generation Results**:
- **Gemini-3.1**: 225 games → `generated_r1_seeds_gemini3.csv`
- **GPT-5.2**: 225 games → `generated_r1_seeds_gpt5_2.csv`
- **Format compliance**: 100% pass rate on validation checklist
- **Coverage**: 225 × 4 speakers = 900 utterances, balanced tactic distribution

**Output Format**:
```csv
game_id, round_id, role_id, llm_alignment, player_roles, public_history, prior_summary_gold, discussion_log, matrix_tactic_scale
G026,1,P1,Good,"{...}","{...}","","Discussion after Quest 1:\nP2: \"...\"\nP3: \"...\"\nP4: \"...\"\nP5: \"...\"","{\"P2\":{...},\"P3\":{...},...}"
```

**Status**: ✅ Complete - 450 dialogues generated (225 × 2 models)

---

#### **Part C: Dialogue Verification & Selection** ✅ COMPLETE
**File**: `log-gen-verifier.ipynb` (19 cells, fully configured)  
**Verifier Model**: Claude Sonnet 4.5 (claude-sonnet-4-5-20250929) - Independent arbiter  
**Purpose**: Compare Gemini-3.1 and GPT-5.2 responses, select best or generate custom corrections

**Blind Evaluation Methodology**:
To eliminate model name bias, Claude receives **anonymous labels** in prompts:
- **Response A** and **Response B** replace actual model names (Gemini-3.1/GPT-5.2)
- Claude evaluates dialogues without knowing which model generated them
- Python code maps recommendations back to real model names for CSV output
- Preserves traceability in outputs while preventing training data bias

**Scoring System**:
Claude Sonnet 4.5 evaluates on **5 binary criteria** (1=PASS, 0=FAIL):
1. **Discussion Coherence & Tactic Situational Fit** *(revised Mar 26)*: Tactic makes social sense given the conversational dynamics — not just a literal label match, but plausible for that specific moment in the group discussion
2. **Public History Alignment**: Dialogue references appropriate context (teams, outcomes, votes)
3. **Tactic-Dialogue Alignment** *(redesigned Mar 26, Framing B)*: The annotation accurately describes what was actually written — dialogue is ground truth, matrix must match the utterance (not the pre-assigned plan)
4. **Authenticity & Skill Consistency**: Each utterance reads as believable Avalon dialogue; linguistic sophistication matches the speaker's assigned skill level (no elaborate reasoning from Low-skill players)
5. **Dialogue Format Compliance**: Exactly 4 speakers, protagonist excluded, proper formatting

**Key Change (Mar 26)**: Criteria 1 and 3 were redesigned. Old crit 1 evaluated role stereotypes (Good=honest, Evil=deceptive) — replaced with group-level social dynamics. Old crit 3 used pre-assigned plan as ground truth — replaced with Framing B (annotation must describe what was written). A full re-run of all 225 games is required before Phase 2 integration.

**Response Format**: Claude returns **structured JSON** with:
- Per-criterion scores (1/0) and explanations for BOTH pass and fail
- Total count (0-5) for each response
- Recommendation and reasoning

**Decision Logic**:
| Response A Total | Response B Total | Action | LLM_used |
|---|---|---|---|
| 5/5 | 5/5 | Pairwise comparison, select better | Gemini-3.1 or GPT-5.2 |
| 5/5 | <5/5 | Use 5/5 response | Gemini-3.1 or GPT-5.2 |
| <5/5 | 5/5 | Use 5/5 response | Gemini-3.1 or GPT-5.2 |
| 4/5 | <4/5 | Targeted correction of 4/5 (fix failing criterion) | Gemini-3.1-Claude-4.5 |
| <4/5 | 4/5 | Targeted correction of 4/5 (fix failing criterion) | GPT-5.2-Claude-4.5 |
| 4/5 | 4/5 | Targeted correction (default GPT-5.2) | GPT-5.2-Claude-4.5 |
| ≤3/5 | ≤3/5 | Claude full custom generation | Claude-4.5 |

**Pairwise Tiebreaker (Both 5/5)**:
- Both responses meet all criteria → Claude performs qualitative comparison
- Evaluates: strategic depth, natural dialogue flow, tactical sophistication
- Selects the response with superior Avalon authenticity and nuance
- No modifications made to the selected dialogue

**Custom Generation (Neither 5/5)**:
- Neither response meets all 5 criteria → Claude generates **entirely new dialogue**
- Respects all constraints: player roles, public history, tactical assignments, format requirements
- Ensures all 5 criteria are satisfied in the custom generation
- Stored with "Claude-4.5" label and "Full_Custom" correction mode
- **Why full regeneration?** Partial fixes risk introducing inconsistencies; clean slate ensures quality

**Output CSVs**:
1. **`verified_r1_seeds_combined.csv`**: Full dataset with selected dialogues
   - All original columns plus `LLM_used` and `Claude_Reasoning`
   - Values: "Gemini-3.1", "Gemini-3.1-Claude-4.5", "GPT-5.2", "GPT-5.2-Claude-4.5", or "Claude-4.5"

2. **`verified_r1_criteria_scores.csv`**: Detailed per-criterion tracking
   - Binary scores: `Gemini31_Coherence`, `Gemini31_History`, `Gemini31_Matrix`, `Gemini31_Authenticity`, `Gemini31_Format` (1=pass, 0=fail)
   - Total scores: `Gemini31_Total`, `GPT52_Total` (e.g., "4 of 5", "5 of 5" - formatted to prevent Excel date interpretation)
   - Selection metadata: `Selected_LLM`, `Correction_Mode` (None, Pairwise_Tiebreaker, Targeted, Full_Custom)
   - Explanations: `Gemini31_Criteria_Explanations`, `GPT52_Criteria_Explanations` (JSON format, includes reasoning for all criteria)
   - Decision reasoning: `Claude_Reasoning` (2-3 sentence explanation)

**API Configuration**:
- **Client**: Anthropic Python SDK with explicit API key loading
- **Environment**: Uses `python-dotenv` to load `ANTHROPIC_API_KEY` from `.env` file
- **Retry logic**: Built-in exponential backoff with **5 retries** (SDK default: 2)
- **Token budget**: `max_tokens=4096` for verification responses (~500-1000 tokens typical, ~2000+ for custom generation)
- **Rate limiting**: SDK automatically handles 429 errors with exponential backoff
- **Error handling**: Automatic retry for connection errors, timeouts, and 5xx server errors

**Output Files**:
1. **verified_r1_seeds_combined.csv**: 
   - Columns: game_id, round_id, role_id, llm_alignment, player_roles, public_history, prior_summary_gold, discussion_log, matrix_tactic_scale, Claude_Reasoning, LLM_used
   - All original data preserved + LLM_used column for traceability
   - Matrix tactic scale reformatted to compact JSON (no linebreaks for readability)
   - **LLM_used values**: "Gemini-3.1", "GPT-5.2", "Claude-4.5"

2. **verified_r1_criteria_scores.csv**:
   - Per-criterion binary scores (1=pass, 0=fail) for both models
   - Total counts formatted as "4 of 5", "5 of 5" (prevents Excel date interpretation)
   - Selection metadata: Selected_LLM, Correction_Mode, Claude_Reasoning
   - JSON explanations for all criteria (Gemini31_Criteria_Explanations, GPT52_Criteria_Explanations)
   - Enables fine-grained analysis of model strengths/weaknesses per criterion

**Notebook Architecture** (19 cells):
- **Cells 1-2**: Markdown header and execution flow documentation
- **Cell 3**: Imports (pandas, json, anthropic, dotenv, os, time)
- **Cell 4**: Load both CSV files (`generated_r1_seeds_gemini3.csv`, `generated_r1_seeds_gpt5_2.csv`)
- **Cell 5**: Markdown: Binary validation system and decision logic overview
- **Cell 6**: Initialize Claude Sonnet 4.5 client with `load_dotenv()`, `max_retries=5`, and system prompt
- **Cell 7**: Markdown: Define Verification Function header
- **Cell 8**: `verify_dialogue_pair()` function - handles:
  - Anonymous label injection (Response A/B)
  - 5-criterion binary evaluation (1/0) with explanations for all
  - JSON parsing with fallback for string format ("5/5" → 5)
  - 4-tier decision logic: 5/5 pairwise, one 5/5 selection, 4/5 targeted correction, ≤3/5 custom generation
  - Score totaling and recommendation mapping
- **Cell 9**: Markdown: Run Verification Loop header
- **Cell 10**: Main verification loop (TEST_LIMIT for testing, `len(gemini3_df)` for full run)
- **Cell 11**: Markdown: Create Output DataFrames header
- **Cell 12**: DataFrame creation and aggregate statistics
- **Cell 13**: Markdown: Output Files documentation
- **Cell 14**: Save both CSVs with proper column formatting
- **Cells 15-16**: Next Steps and Scale-Up documentation
- **Cells 17-18**: Comprehensive Analysis markdown headers
- **Cell 19**: Full analysis cell (loads `verified_r1_criteria_scores.csv`, per-criterion stats, LLM selection breakdown, correction mode distribution)

**Verification Prompt Structure** (sent to Claude):
```
You are evaluating two AI-generated Avalon Round 1 discussion logs 
to determine which is superior. Both responses were generated for 
the same game context...

RESPONSE A:
[anonymized dialogue]

RESPONSE B:
[anonymized dialogue]

Evaluate on 5 binary criteria (1=PASS, 0=FAIL):
1. Player Roles Consistency...
2. Public History Alignment...
...

OUTPUT FORMAT (JSON):
{
  "response_a": {
    "criteria": {
      "coherence": {"score": 1/0, "explanation": "..."},
      ...
    },
    "total": x
  },
  "response_b": {...},
  "recommendation": "RESPONSE_A|RESPONSE_B|PAIRWISE_TIEBREAKER|CUSTOM_GENERATION",
  "reasoning": "..."
}
```

**Bias Mitigation**:
- **Academic pressure**: Removed "research dataset" mention from prompt (no publication pressure)
- **Model name bias**: Anonymous labels prevent Claude's preconceptions about Gemini-3.1 vs GPT-5.2
- **Recommendation mapping**: Python code converts anonymous labels to real names AFTER Claude's decision
- Result: Pure quality-based evaluation without external influence

**Production Readiness**:
- ✅ Blind evaluation implemented (Response A/B labels)
- ✅ API configuration complete (dotenv, 5 retries, max_tokens=4096)
- ✅ All 17 cells functional and tested
- ✅ Binary scoring logic validated (1/0 per criterion)
- ✅ JSON parsing with fallback for string totals
- ✅ Custom generation fallback tested
- ✅ Output format validated (CSV schema correct with Excel-safe totals)
- 📝 Ready for full 225-game verification run

**Estimated Runtime**:
- 225 games × ~4-6 seconds per verification = **15-23 minutes**
- With API rate limiting and retries: **20-30 minutes total**
- Cost estimate: ~$5-8 for 225 verifications (Claude Sonnet 4.5 pricing)

**Next Action**:
- Run Cell 6 with `TEST_LIMIT = len(gemini3_df)` (225 games)
- Monitor verification progress (incremental saves every 25 games)
- Analyze score distributions in `verified_r1_scores.csv`
- Review LLM_used distribution (how many Gemini-3.1 vs GPT-5.2 vs corrections vs custom)

---

### **STAGE 4: Theory of Mind (ToM) Gold Label Generation** 🎯 PLANNED (IMMEDIATE NEXT)

**Purpose**: Generate gold-standard Theory of Mind annotations for each dialogue, enabling evaluation of LLM reasoning capabilities in deceptive social contexts.

**Annotation Schema** (per game observation from each non-protagonist player):

```json
{
  "abduction": [
    {
      "player": "P2",
      "good_expl": "Protecting future missions by analyzing outcomes.",
      "evil_expl": "Feigning logic to confuse the group.",
      "choice": "Good"
    },
    // ... for P3, P4, P5
  ],
  "suspicion": [
    {"player": "P2", "level": "Minimal"},
    {"player": "P3", "level": "Extreme"},
    {"player": "P4", "level": "Strong"},
    {"player": "P5", "level": "Strong"}
  ],
  "depth": 2,
  "beliefs": [
    {
      "level": 1,
      "player": "P2",
      "content": "Sees P4 and P5 as suspicious since they were on the failed mission; suspects P3 for defending them."
    },
    {
      "level": 2,
      "player": "P3",
      "content": "Wants others to believe P4 and P5 are safe choices."
    },
    // ... nested belief hierarchy
  ],
  "statement": "Since the failed mission had both P4 and P5, and they now accuse each other, we should be wary of including them until more evidence appears. P3's push to re-include them both is especially suspicious, so we need to be careful with teams involving P3, P4, or P5.",
  "deduction": ["P3", "P4/P5"]
}
```

**Annotation Components**:

1. **Abduction** (Inference to Best Explanation):
   - For each observed player (excluding protagonist)
   - Two competing explanations: good_expl (innocent behavior) vs evil_expl (deceptive behavior)
   - Observer's choice: Which explanation is more plausible given the evidence

2. **Suspicion Tracking**:
   - Per-player suspicion levels: {Minimal, Low, Moderate, Strong, Extreme}
   - Reflects observer's current belief about each player's alignment

3. **Belief Depth** (ToM Recursion):
   - Level 1: "What does Player X believe?" (first-order ToM)
   - Level 2: "What does Player X want me to believe?" (second-order ToM)
   - Depth integer indicates maximum recursion level achieved in reasoning

4. **Nested Beliefs**:
   - Hierarchical belief structure tracking multi-level reasoning
   - Captures both what players believe AND what they want others to believe
   - Essential for modeling deceptive intent and strategic communication

5. **Deductive Conclusion**:
   - List of players identified as likely Evil based on accumulated evidence
   - May include uncertainty (e.g., "P4/P5" means one of them, not both)

6. **Reasoning Statement**:
   - Natural language summary of the observer's reasoning process
   - Explains how evidence leads to suspicion and deduction

**Methodology**:

- **Annotator**: Claude Sonnet 4.5 (same verifier model for consistency)
- **Input Context**: 
  - Game state (player_roles for ground truth comparison only)
  - Public history (all observable information)
  - Discussion log (utterances to analyze)
  - Round number and protagonist identity
- **Output**: JSON structure per above schema
- **Validation**: 
  - Schema compliance (all required fields present)
  - Logical consistency (suspicion levels match deductions)
  - Evidence grounding (explanations reference specific dialogue/events)

**Coverage**:
- **R1 (250 games)**: 250 games × 1 protagonist × 1 observation = **250 ToM annotations**
- **R2-R5 (cumulative)**: ~850-900 additional observations
- **Total**: ~**1,000-1,150 ToM gold labels** for initial dataset

**Pipeline Integration**:
- New column: `tom_gold_label` (JSON structure as above)
- Generation notebook: `tom-label-generation.ipynb` (to be created)
- Verification notebook: `tom-label-verifier.ipynb` (quality checks)

**Timeline**:
- **After R1-R5 dialogue generation complete** (all 1,000 samples verified)
- **Before scaling to 10k-20k samples** (validate annotation quality on 1k first)
- Estimated runtime: ~6-8 hours for 1,000 annotations (Claude Sonnet 4.5 calls)

**Scaling Strategy**:
Once ToM pipeline validated on 1,000 samples:
1. **Phase 1 (Complete)**: 250 games × 5 rounds ≈ 1,000 samples with dialogues + tactics + ToM labels
2. **Phase 2 (Scale-Up)**: Generate 2,000-5,000 additional games (10k-20k samples total)
   - **⚠️ Tactical Assignment Update**: When augmenting remaining ~750 discussion logs, use Blue (Both) tactics for Good players in addition to Green tactics. Current pool: Good=10 tactics; expand to Good=19 tactics (10 Green + 9 Blue) for more realistic defensive/ambiguous communication patterns.
3. **Phase 3 (Quality Assurance)**: Sample-based validation, inter-annotator agreement checks (if using multiple LLMs)

**Research Applications**:
- **Deception Detection**: Train models to predict player alignment from dialogues
- **ToM Evaluation**: Benchmark LLM reasoning capabilities on nested belief inference
- **Strategic Communication**: Analyze how deceptive tactics correlate with suspicion shifts
- **Abductive Reasoning**: Study how observers weigh competing explanations under uncertainty

---

## 📊 Dataset Statistics & Coverage

### **Round 1 Coverage**:
- **Total games**: 225 (subset of 250 seed games)
- **Speaking turns**: 225 × 4 speakers = 900 utterances
- **Tactic distribution**: 37 tactics with level-based assignment
  - Green (Good-only): 10 tactics, 29-32 uses each
  - Red (Evil-only): 18 tactics, 17-20 uses each
  - Blue (Both): 9 tactics, 22-28 uses each (~25% of total usage)
- **Skill level distribution**: High/Moderate/Low, ~300 each (balanced across 6 scale-level combinations)
  - Each combination (GRS_High, GRS_Moderate, GRS_Low, Mach-IV_High, Mach-IV_Moderate, Mach-IV_Low) appears ~150 times
- **Role distribution**: 450 Good turns (50%), 450 Evil turns (50%) - reflects 3:2 Good:Evil player ratio with balanced speaking

### **Expected Final Dataset** (phased scaling):
- **Phase 1 Target (Current)**: 250 games × 5 rounds ≈ 1,000 samples
  - Complete metadata + discussion logs + tactic annotations + ToM gold labels
  - Validation-ready pipeline for scaling
  
- **Phase 2 Target (Immediate Scale-Up)**: 2,000-5,000 games
  - **10,000-20,000 samples** with full augmentation pipeline
  - Same quality standards as Phase 1
  - Largest theory-grounded deception dataset in Avalon domain
  
- **Each sample includes**:
  - Player roles (Good/Evil assignments)
  - Public history (teams, votes, quest outcomes)
  - Prior round summaries (cumulative context)
  - Discussion log (4-speaker tactical dialogue)
  - Matrix tactic scale (37-tactic taxonomy annotations)
  - ToM gold labels (abduction, suspicion, beliefs, deductions)
  - Skill assessments (GRS/Mach-IV ratings)
  - LLM metadata (generation model, verification status)

---

## 📄 Documentation: dataset.tex

**File**: `dataset.tex` (470+ lines)  
**Status**: ✅ Complete and publication-ready  
**Purpose**: Academic paper documenting entire dataset augmentation pipeline

**Structure**:
1. **Title & Metadata**: "Hidden Roles, Visible Minds" - Theory of Mind in Deception
2. **Introduction**: Avalon context, related work citations (IDT, TDT, IMT2), motivation
3. **Dataset Construction Pipeline**: Overview of 3-stage approach
4. **Stage 1 Documentation**: Balanced role assignment methodology + Figure 1 (role balance)
5. **Stage 2 Documentation**: Constraint-satisfaction approach + Figures 2-3 (mission outcomes, voting patterns)
6. **Stage 3 Documentation**:
   - Behavioral framework (4×4 matrix table with all 37 tactics)
   - Skill assessment scales (GRS, Mach-IV descriptions)
   - LLM-based generation (prompt engineering, tactic pre-assignment, API integration, validation)
   - Generation statistics (225 games, 100% validation pass rate)
7. **Dataset Statistics & Analysis**:
   - Coverage analysis (tactic distribution, skill levels, role distribution)
   - Quality analysis (structural quality, speaker consistency, scale alignment)
   - Tactic distribution (balanced across all 37)
   - Dialogue diversity & realism examples
   - Model comparison (Gemini-3.1 vs GPT-5.2)
8. **Integration & Next Steps**: Merging, R2-R5 preparation (marked "working on...")
9. **Conclusion**: Three contributions summarized
10. **Scope & Limitations**: Synthetic dialogues, LLM annotations, uniform skill assignment
11. **Appendix**: Four additional few-shot dialogue examples (G001, G002, G009, G023)

**Included Figures**:
- Figure 1: Player role balance distribution
- Figure 2: Mission outcome bar chart
- Figure 3: Voting pattern distribution

**Key Citations Integrated**:
- Deception theories: Buller+96 (IDT), Levine-14 (TDT), McCornack+14 (IMT2)
- LLM capabilities: Li+23 (multiagent reasoning), Zhang+24 (workspace collaboration)
- Strategic communication: Vogel+13 (Gricean maxims), Panfili+21 (HAI lens)
- Few-shot learning: Brown+20 (few-shot learners), Min+22 (in-context learning)
- LLM generation: Shao+23 (synthetic prompting)

---

## 🎯 Next Steps (Detailed Roadmap)

### **PHASE 1: Round 1 Completion** ⚠️ RE-RUN REQUIRED (2026-03-26)

#### **Step 1.0: Redesign Verification Prompt** ✅ COMPLETE (2026-03-26)
- **Reason**: Original criteria 1 and 3 had conceptual flaws identified in review
  - Crit 1 penalized Good players for using Blue (Both-alignment) defensive tactics → replaced with group-level social dynamics check
  - Crit 3 used pre-assigned plan as ground truth → replaced with Framing B (dialogue is the ground truth, annotation must describe what was written)
- **Changes made to `log-gen-verifier.ipynb`** (Mar 26):
  - Cell 8: Corrupted code fully replaced; now builds `TACTIC_TAXONOMY_REF` dynamically from `tactics_knowledge_base.json` (37 tactics confirmed at runtime)
  - `TACTIC ANNOTATION FRAMEWORK` block: injected into prompt with `{TACTIC_TAXONOMY_REF}` — gives Claude the full taxonomy at inference time
  - Criterion 1: Renamed "Discussion Coherence & Tactic Situational Fit" — evaluates social plausibility of tactic choice given discussion flow
  - Criterion 3: "Tactic-Dialogue Alignment" — Framing B adopted; dialogue is ground truth
  - Criterion 4: "Authenticity & Skill Consistency" — restored (was accidentally deleted in earlier edit)
  - All `PRE-ASSIGNED TACTIC REFERENCE` mentions removed from prompt
  - Output schema: `targeted_correction` and `custom_dialogue` are now objects with `dialogue` + `matrix_tactic_scale` fields
  - Cell 10 selection logic: all 5 paths use `reorder_matrix_by_speaking_order()`
  - Cell 12: centralized `selected_tactic_scale` extraction
  - Cell 27: `normalize_matrix` reorders by speaking order from dialogue
- **Changes made to `log-gen-verifier.ipynb`** (Mar 27):
  - JSON criterion key renamed: `roles` → `coherence` everywhere (prompt schema, result dicts, CSV columns, analysis lists)
  - Criterion 4 text rewritten: removed "implausible strategy" overlap with C1; now focuses on naturalness + skill-level sophistication mismatch
  - Criterion 5 text fixed: removed duplicate `1 =` label; header line now reads as a single pass-condition with example block below
  - Step 3 overview markdown updated: criterion names for C1, C3, C4, C5 now match official prompt text
- **Test run**: Cells 8 and 12 executed successfully with `TEST_LIMIT = 1`; 37 tactics confirmed at runtime

#### **Step 1.1: Re-run Full Verification Pipeline** ✅ COMPLETE (2026-03-27)
- **File**: `log-gen-verifier.ipynb`
- **Results** (225 games, Claude Sonnet 4.5 verifier):
  - Total verified: 224 (1 api_error queued for Step 4b retry)
  - Gemini-3.1 selected (original): 24
  - GPT-5.2 selected (original): 157
  - Pairwise tiebreaker used: 8
  - Gemini-3.1 + Targeted correction: 10
  - GPT-5.2 + Targeted correction: 30
  - Claude 4.5 full custom generation: 3
  - Errors: 1 → queued for retry
  - 2 rows queued for Step 4b retry (1 api_error: G073/1, 1 Full_Custom: G188/1)
- **Step 4b (Retry)** ✅ COMPLETE: Both rows resolved successfully (0 still failed)
  - G073/1 (api_error) → GPT-5.2 selected on retry
  - G188/1 (Full_Custom) → GPT-5.2-Claude-4.5 / Targeted on retry
  - Final: verified_results = 225 rows | criteria_results = 225 rows
- **Output files saved**:
  - `verified_r1_seeds_combined.csv` (225 rows)
  - `verified_r1_criteria_scores.csv` (225 rows, per-criterion scores)

#### **Step 1.2: Run Verification Analysis** ✅ COMPLETE (2026-03-27)
- **File**: `log-gen-verifier.ipynb` (analysis cells run)
- **Key findings**:
  - GPT-5.2 total usage: 84.00% (direct: 70.22%, corrected: 13.78%)
  - Gemini-3.1 total usage: 15.11% (direct: 10.67%, corrected: 4.44%)
  - Claude full custom: 0.89% (2 games)
  - Pairwise tiebreaker: 3.11% (7 games)
  - Correction mode: None=174, Targeted=41, Pairwise=8, Full_Custom=2
  - Gemini-3.1 weakest criterion: Matrix alignment (50.2% pass rate)
  - GPT-5.2 weakest criterion: Matrix alignment (78.22% pass rate)

#### ~~**Step 1.1 (old): Run Full Verification Pipeline**~~ ✅ SUPERSEDED
- Completed 2026-03-23 under old criteria; G122 manually scored & inserted 2026-03-25
- Results are stale — will be overwritten by Step 1.1 re-run above

#### **Step 1.3 (Step 4c): Second-Pass Recheck of Corrected Rows** ✅ COMPLETE (2026-04-04)
- **File**: `log-gen-verifier-4c.ipynb` (standalone one-time notebook)
- **Purpose**: Independent second-pass recheck of the 43 R1 rows corrected in Steps 4a/4b — verify that fixing one criterion didn't silently break another
- **Scope**: 41 `Correction_Mode == 'Targeted'` rows + 2 `Correction_Mode == 'Full_Custom'` rows
- **Verifier**: Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`) with prompt caching
- **Prompt engineering**: `STATIC_EVAL_PROMPT` (taxonomy + 5 criteria + output format) as a cached first content block — written once, read at 10% cost on subsequent calls. `SYSTEM_PROMPT` passed separately. ACCEPT-first bias and Benefit of the Doubt wording applied across all 5 criteria.
- **Decision logic**: 5/5 → ACCEPTED (no change), 4/5 → RECORRECTED (targeted fix), ≤3/5 → REGENERATED
- **LLM suffix**: `-Recorrected` / `-Regenerated` appended to existing `LLM_used` value for changed rows
- **Output columns added to `verified_r1_criteria_scores.csv`**: `Recheck_4c`, `Recheck_4c_Score`, `Recheck_4c_Reasoning`, `Recheck_4c_Explanations`
- **Result**: Corrections verified as methodologically sound — all original failures were objectively verifiable (wrong scale, wrong row/col, factual history contradictions). Majority accepted as-is on second pass.

---

### **PHASE 2: Dataset Integration** ✅ COMPLETE

#### **Step 2.1: Merge Verified R1 Seeds into Deception-Dataset.csv** ✅ COMPLETE (2026-04-04)
- **Input Files**:
  - `Deception-Dataset.csv` (master dataset, 250 games with role + public history augmentation)
  - `verified_r1_seeds_combined.csv` (225 verified R1 dialogues — `discussion_log`, `matrix_tactic_scale`, `LLM_used`, `Claude_Reasoning`)
  
- **Merge Strategy**:
  1. Load both CSVs into pandas
  2. Filter master dataset to Round 1 only: `master_r1 = master_df[master_df['round_id'] == 1]`
  3. Merge on `game_id`: `merged = master_r1.merge(verified_r1, on='game_id', suffixes=('_old', '_verified'))`
  4. For matched rows (225 games):
     - Keep verified `discussion_log`, `matrix_tactic_scale`, `LLM_used`, `Claude_Reasoning`
     - Keep master `player_roles`, `public_history`, other metadata
  5. For unmatched rows (25 manual games):
     - Keep original data from master
     - Set `LLM_used = 'Manual'`
  6. Combine with other rounds (R2-R5 if present, currently empty)
  
- **Output**: R1 rows merged into `Deception-Dataset.csv` (250 games × 1 round = 250 R1 rows)

- **Validation Checks**:
  - ✅ 250 R1 rows total (225 verified + 25 manual)
  - ✅ All columns present: game_id, round_id, role_id, llm_alignment, player_roles, public_history, prior_summary_gold, discussion_log, matrix_tactic_scale, LLM_used
  - ✅ No duplicate game_ids for R1
  - ✅ `prior_summary_gold` is empty string for R1 (no prior rounds)

---

### **PHASE 2b: R2-R5 Generation (remaining 750 rows)** ⏳ NEXT (after Phase 3)

**Scope**: 250 games × 5 rounds = 1,000 total rows. Round 1 is complete (225 verified + 25 manual). The remaining ~750 rows (R2-R5, accounting for game termination) need:
1. **Prior history** (`prior_summary_gold`) — cumulative summaries of all previous rounds for each game
2. **Discussion log** (`discussion_log`) — 4-speaker tactical dialogue for each round
3. **Matrix tactic scale** (`matrix_tactic_scale`) — per-speaker tactic annotations following the 37-tactic taxonomy

**Strategy**:
- Use the same `log-gen.ipynb` pipeline (Gemini-3.1 + GPT-5.2) for dialogue generation
- Use the same `log-gen-verifier.ipynb` pipeline (Claude Sonnet 4.5) for verification and selection
- Generate `prior_summary_gold` iteratively: R1 summary feeds R2 generation, R1+R2 summaries feed R3, etc.
- Filter active games per round (game ends after 3 PASS or 3 FAIL outcomes)
- Tactic assignment: expand Good player tactic pool to include Blue (Both) tactics (Good=19 tactics: 10 green + 9 blue) for R2+ to reflect evolving defensive communication

**See Phase 3 (Prior Summary Generation) and Phase 4 (Rounds 2-5 Augmentation) below for detailed implementation.**

---

### **PHASE 3: Prior Summary Generation** 📝 NEXT IMMEDIATE

#### **Step 3.1: Generate prior_summary_gold for R1** (30 min)
**Purpose**: Create summaries of R1 discussions to use as context for R2 generation

**Content Structure** (for each game's R1):
```
Round 1 Discussion Summary:
- Team: P1, P3 proposed by leader P3
- Voting: Unanimous approval (5 YES votes)
- Quest Outcome: PASS
- Key Discussion Points:
  * P2 questioned the pass meaning (doesn't clear players)
  * P3 raised suspicion about unanimous vote
  * P4 supported P3's logic
  * P5 expressed uncertainty about information gained
- No player identities revealed yet
```

**Implementation**:
- **Option 1 (Recommended)**: Use Claude Sonnet 4.5 to summarize each R1 dialogue
  - Prompt: "Summarize this Round 1 Avalon discussion. Include: team composition, vote result, quest outcome, key discussion points. Do NOT reveal player identities (Good/Evil). Keep it factual and concise (3-4 sentences)."
  - Input: R1 `discussion_log` + `public_history`
  - Output: 3-4 sentence summary
  
- **Option 2**: Manual template-based extraction
  - Extract team/votes/outcome from `public_history`
  - Extract key phrases from `discussion_log`
  - Combine into standardized format

**Output**: Update `prior_summary_gold` column in R1 rows (currently empty → filled)

**File**: Create `generate-prior-summaries.ipynb` (new notebook)

---

#### **Step 3.2: Augment prior_summary_gold for R2-R5** (Iterative)
**Strategy**: Generate summaries incrementally as we create R2, R3, R4, R5 dialogues

- R2 generation uses R1 summary → R2 dialogue created → summarize R2 → R3 generation uses R1+R2 summaries
- R3 generation uses R1+R2 summaries → R3 dialogue created → summarize R3 → R4 generation uses R1+R2+R3 summaries
- And so on...

**Format**: Concatenate previous round summaries with separators
```
=== Prior Rounds ===
Round 1: [summary]
Round 2: [summary]
=== Current Round: 3 ===
```

---

### **PHASE 4: Rounds 2-5 Augmentation** 🚀 AFTER R1 COMPLETE

#### **Step 4.1: Identify Active Games per Round**
**Objective**: Filter games that haven't ended yet (Avalon ends after 3 PASS or 3 FAIL)

**Implementation**:
```python
def get_active_games_for_round(df, round_num):
    """Returns game_ids still active for the given round."""
    active_games = []
    for game_id in df['game_id'].unique():
        game_history = df[df['game_id'] == game_id].sort_values('round_id')
        
        # Count outcomes up to (but not including) this round
        prior_rounds = game_history[game_history['round_id'] < round_num]
        pass_count = (prior_rounds['public_history'].str.contains('PASS')).sum()
        fail_count = (prior_rounds['public_history'].str.contains('FAIL')).sum()
        
        # Game continues if neither side has won yet
        if pass_count < 3 and fail_count < 3:
            active_games.append(game_id)
    
    return active_games
```

**Expected Counts**:
- R1: 250 games (all start)
- R2: ~250 games (no game ends after 1 round)
- R3: ~250 games (few end after 2 rounds with 2-0 score)
- R4: ~200 games (games end at 3-0, 0-3, 3-1, 1-3)
- R5: ~100 games (only games with 2-2 score continue to R5)

**File**: Add function to `log-gen.ipynb` or create `filter-active-games.ipynb`

---

#### **Step 4.2: Adapt Tactic Assignment for R2-R5** (Evolving Tactics Strategy)
**Objective**: Tactics evolve based on game progression and events

**Strategy**: 
1. **R1 Tactics**: Baseline exploratory/cautious (already generated)
2. **R2+ Tactics**: Players shift tactics based on:
   - Quest outcomes (success/failure patterns)
   - Voting patterns (who voted for what)
   - Suspicion accumulation (who has been questioned)
   - Player skill level (more sophisticated players adapt faster)

**Implementation Options**:

- **Option A: Skill-Based Evolution Rules** (Recommended)
  ```
  High Skill Players:
    - After seeing 2+ FAILs → Shift to more adversarial tactics (accusatory)
    - After successful team → Shift to cooperative/consolidating tactics
    
  Moderate Skill Players:
    - Make gradual shifts based on quest outcomes
    - Less aggressive, more defensive adaptations
    
  Low Skill Players:
    - Minimal tactic changes (stick to initial patterns)
    - May show inconsistent strategy
  ```

- **Option B: Simple Cyclic Evolution**
  - Each player rotates through 2-3 compatible tactics across rounds
  - Maintains role consistency (Good → Green tactics, Evil → Red tactics)
  - Simpler but less realistic

- **Option C: Context-Free (Static)**
  - Players maintain same tactic throughout all 5 rounds
  - Easiest but least authentic

**Recommendation**: Use Option A (Skill-Based Evolution) for realism  
**File**: Update `log-gen.ipynb` with evolution logic or create `evolve-tactics.ipynb`

---

#### **Step 4.3: Generate R2 Dialogues** (3-4 hours per round × 2 models)
**File**: Adapt `log-gen.ipynb` for R2 context

**Key Modifications**:
1. **Add prior_summary_gold to prompt**:
   ```
   === Prior Round Summary ===
   {prior_summary_gold}
   
   === Current Game State ===
   Round: 2
   Public History: {public_history}
   Player Roles: {player_roles}
   ...
   ```

2. **Filter to active games**: Only process games with <3 PASS and <3 FAIL

3. **Evolve tactics**: Apply evolution rules based on R1 outcomes

4. **Update output format**: Round 2 header, protagonist updated for R2 leader

**Generation Process**:
- Run Gemini-3.1 generation: `generated_r2_seeds_gemini3.csv` (~250 rows)
- Run GPT-5.2 generation: `generated_r2_seeds_gpt5_2.csv` (~250 rows)
- Total: ~500 R2 dialogues generated

**Validation**: Same checklist as R1 (format, speakers, matrix validity, etc.)

---

#### **Step 4.4: Verify R2 Dialogues** (4-5 hours)
**File**: Use `log-gen-verifier.ipynb` (same pipeline as R1)

**Input**:
- `generated_r2_seeds_gemini3.csv`
- `generated_r2_seeds_gpt5_2.csv`

**Context Additions**:
- Include `prior_summary_gold` (R1 summary) in verification prompt
- Claude checks consistency with prior round behaviors

**Output**:
- `verified_r2_seeds_combined.csv` (~250 verified R2 dialogues)
- `verified_r2_criteria_scores.csv` (per-criterion tracking)

---

#### **Step 4.5: Generate R2 Summaries** (30 min)
- Use Claude Sonnet 4.5 to summarize each R2 dialogue
- Store in `prior_summary_gold` for R3 context
- Format: Concatenate R1 + R2 summaries

---

#### **Step 4.6: Repeat for R3, R4, R5** (Iterative)
**R3 Process**:
1. Filter active games (~245 games)
2. Generate R3 dialogues (Gemini-3.1 + GPT-5.2) with R1+R2 summaries
3. Verify with Claude Sonnet 4.5
4. Generate R3 summaries for R4 context

**R4 Process**:
1. Filter active games (~200 games)
2. Generate R4 dialogues with R1+R2+R3 summaries
3. Verify with Claude Sonnet 4.5
4. Generate R4 summaries for R5 context

**R5 Process**:
1. Filter active games (~100 games, 2-2 score)
2. Generate R5 dialogues with R1+R2+R3+R4 summaries
3. Verify with Claude Sonnet 4.5
4. Final summaries generated (for completeness)

**Total Estimated Time**: 
- R2-R5 generation: ~12-15 hours (3-4 hrs per round)
- R2-R5 verification: ~16-20 hours (4-5 hrs per round)
- **Grand Total: ~28-35 hours of compute time** (can run overnight)

---

### **PHASE 5: Final Dataset Assembly** 🎁 FINAL

#### **Step 5.1: Combine All Verified Rounds** (15 min)
**Input Files**:
- `verified_r1_seeds_combined.csv` (250 games)
- `verified_r2_seeds_combined.csv` (~250 games)
- `verified_r3_seeds_combined.csv` (~245 games)
- `verified_r4_seeds_combined.csv` (~200 games)
- `verified_r5_seeds_combined.csv` (~100 games)

**Merge Process**:
```python
import pandas as pd

# Load all verified rounds
r1 = pd.read_csv('verified_r1_seeds_combined.csv')
r2 = pd.read_csv('verified_r2_seeds_combined.csv')
r3 = pd.read_csv('verified_r3_seeds_combined.csv')
r4 = pd.read_csv('verified_r4_seeds_combined.csv')
r5 = pd.read_csv('verified_r5_seeds_combined.csv')

# Concatenate
final_dataset = pd.concat([r1, r2, r3, r4, r5], ignore_index=True)

# Sort by game_id and round_id
final_dataset = final_dataset.sort_values(['game_id', 'round_id'])

# Save
final_dataset.to_csv('Avalon-Deception-Dataset-FINAL.csv', index=False)
```

**Output**: `Avalon-Deception-Dataset-FINAL.csv` 
- **Total Rows**: ~1,045 dialogue entries (250+250+245+200+100)
- **Columns**: All original + LLM_used, Claude_Reasoning, prior_summary_gold

---

#### **Step 5.2: Generate Final Statistics** (30 min)
**Analysis Notebooks**: Create summary reports

1. **Dataset Statistics**:
   - Total games: 250
   - Total dialogue entries: ~1,045
   - Dialogues per round: [250, 250, 245, 200, 100]
   - Tactic distribution across all rounds
   - Skill level distribution
   - LLM_used distribution (Gemini-3.1 vs GPT-5.2 vs Claude-4.5)

2. **Quality Metrics**:
   - Per-criterion pass rates (aggregated across all rounds)
   - Correction mode distribution
   - Model performance comparison (Gemini-3.1 vs GPT-5.2)

3. **Tactical Analysis**:
   - Tactic frequency per alignment (Good vs Evil)
   - Tactic evolution patterns (how tactics shift R1→R5)
   - Scale usage (GRS vs Mach-IV distribution)

**Output**: 
- `Dataset-Statistics.md` (summary report)
- `dataset-analysis.ipynb` (interactive analysis)

---

#### **Step 5.3: Update Documentation** (1 hour)
**Files to Update**:
1. **README.md**: 
   - Update dataset size (1,045 entries)
   - Add Round 2-5 generation methodology
   - Document prior_summary_gold field

2. **dataset.tex**: 
   - Update Section 3 (Discussion Log Generation) with R2-R5 details
   - Add subsection on tactic evolution strategy
   - Document active game filtering logic

3. **PROGRESS.md**: 
   - Mark all phases COMPLETE ✅
   - Add final dataset release date
   - Archive development notes

---

#### **Step 5.4: Final Dataset Release** 🚀
**Package Contents**:
- `Avalon-Deception-Dataset-FINAL.csv` (main dataset)
- `verified_r*_criteria_scores.csv` files (quality tracking)
- `README.md` (dataset description)
- `dataset.tex` (paper draft)
- All generation notebooks (`log-gen.ipynb`, `log-gen-verifier.ipynb`, etc.)
- `tactics_knowledge_base.json` (37-tactic taxonomy)

**Release Checklist**:
- ✅ All rounds generated and verified
- ✅ Quality metrics calculated and documented
- ✅ Code notebooks cleaned and commented
- ✅ README comprehensive and clear
- ✅ License file added
- ✅ Example usage code provided

**Target**: Ready for research community and paper submission

---

### **PHASE 6: Theory of Mind (ToM) Gold Label Generation** 🧠 NEXT

#### **Step 6.1: Create ToM Annotation Pipeline** (1-2 hours)
**File**: Create `tom-label-generation.ipynb` (new notebook)

**Methodology**:
1. Load `Avalon-Deception-Dataset-FINAL.csv` (1,000 samples from PHASE 5)
2. For each sample, generate ToM annotation via Claude Sonnet 4.5:
   - **Input context**: player_roles (ground truth), public_history, discussion_log, round_id, protagonist
   - **Output**: JSON with abduction, suspicion, beliefs, deduction, statement (see Stage 4 schema)
3. Validate JSON schema compliance
4. Incremental saving every 50 samples

**Prompt Structure**:
```
You are analyzing an Avalon game discussion from the perspective of 
an observer (Player {protagonist}). Based on the game history and 
dialogue, provide a Theory of Mind analysis...

[Include full schema with examples]
```

**Expected Runtime**: ~6-8 hours for 1,000 annotations

---

#### **Step 6.2: Validate ToM Annotations** (1 hour)
**File**: Create `tom-label-verifier.ipynb` (quality checks)

**Validation Checks**:
1. **Schema compliance**: All required fields present, correct data types
2. **Logical consistency**: Suspicion levels align with deduction
3. **Evidence grounding**: Explanations reference specific events/utterances
4. **Belief depth validity**: Level values are sequential (1, 2, ..., depth)
5. **Player coverage**: All non-protagonist players annotated

**Quality Metrics**:
- % samples with valid schema
- % samples with consistent suspicion/deduction
- Average belief depth (measures ToM sophistication)
- Deduction accuracy (vs ground truth player_roles)

---

#### **Step 6.3: Integrate ToM Labels** (30 min)
- Add `tom_gold_label` column to `Avalon-Deception-Dataset-FINAL.csv`
- Save as `Avalon-Deception-Dataset-v1.0-Complete.csv`
- Generate ToM statistics (distribution of suspicion levels, belief depths, deduction accuracy)

**Output**: 1,000 samples with full augmentation (roles + history + dialogues + tactics + ToM labels)

---

### **PHASE 7: Dataset Scaling to 10k-20k Samples** 🚀 FINAL SCALE-UP

#### **Step 7.1: Expand Seed Game Generation** (Variable time)
**Objective**: Generate 2,000-5,000 additional games (10x-20x current size)

**Strategy**:
- **Option A (Recommended)**: Use existing 250 games as templates, permute:
  - Quest outcome sequences (120+ valid combinations)
  - Team composition variations
  - Vote pattern variations
  - Tactic assignments (different cyclic offsets)
  
- **Option B**: Fully synthetic game generation via LLM-based simulation
  - Generate game state progressions from scratch
  - Higher diversity but longer runtime

**Resource Planning**:
- API costs: ~$200-500 for 10k samples (Claude + GPT calls)
- Compute time: ~200-400 hours (parallelizable across multiple machines)
- Storage: ~500MB-1GB (CSV + JSON annotations)

---

#### **Step 7.2: Parallel Pipeline Execution** (Weeks, parallelizable)
**Approach**: Batch processing with distributed computation

1. **Batch 1 (2,000 games → 10k samples)**:
   - Split into 10 batches of 200 games each
   - Run dialogue generation (Gemini-3.1 + GPT-5.2) in parallel
   - Run verification (Claude Sonnet 4.5) in parallel
   - Generate ToM labels in parallel
   - Merge verified samples

2. **Batch 2 (Additional 2,000-3,000 games → 10k-15k more samples)**:
   - Same parallel pipeline
   - Quality monitoring: random sampling for manual review

**Success Criteria**:
- All samples pass verification (5/5 criteria or custom generation)
- ToM annotations achieve >95% schema compliance
- Tactic distribution remains balanced (no single tactic >5% dominance)
- Skill level distribution remains balanced

---

#### **Step 7.3: Final Quality Assurance** (2-3 hours)
**Analysis**:
1. **Coverage analysis**:
   - Tactic usage distribution (all 37 tactics well-represented)
   - Skill level balance (High/Moderate/Low roughly equal)
   - LLM model distribution (Gemini-3.1 vs GPT-5.2 vs Claude custom)

2. **Quality metrics**:
   - Dialogue authenticity (spot-check 100+ samples)
   - ToM label consistency (deduction accuracy vs ground truth)
   - Inter-rater reliability (if using multiple annotators)

3. **Bias detection**:
   - Positional bias (P1-P5 role frequencies)
   - Outcome bias (PASS vs FAIL quest distributions)
   - Tactic-alignment correlation (Good uses only Green tactics, etc.)

**Documentation**: Update `dataset.tex` with final statistics

---

#### **Step 7.4: Public Dataset Release** 🌐
**Release Package**:
- `Avalon-Deception-Dataset-v2.0-10k.csv` (or 20k version)
- `README.md` (comprehensive documentation)
- `dataset.tex` (full paper manuscript)
- All generation/verification notebooks (reproducibility)
- `tactics_knowledge_base.json` (37-tactic taxonomy)
- License file (MIT or CC-BY)

**Release Platforms**:
- GitHub repository (code + documentation)
- Hugging Face Datasets (standardized format)
- Zenodo (DOI for academic citation)

**Target Venues**:
- AAMAS 2026 Datasets & Benchmarks track
- NeurIPS 2026 Datasets & Benchmarks track
- EMNLP 2026 (if NLP-focused analysis included)

---

## 📊 Progress Summary

### **Completed Phases**:
- ✅ **Stage 1**: Player role augmentation (250 games)
- ✅ **Stage 2**: Public history generation & verification (250 games)
- ✅ **Stage 3A**: Behavioral framework (37-tactic taxonomy defined)
- ✅ **Stage 3B**: R1 dialogue generation (450 dialogues — Gemini-3.1 + GPT-5.2)
- ✅ **Stage 3C prompt redesign**: Verification criteria overhauled (crit 1 + 3 redesigned, taxonomy injected dynamically, Framing B adopted)
- ✅ **Stage 3C run**: Full 225-game verification complete (2026-03-27) — 225 rows verified, 2 retries resolved, 0 still failed
- ✅ **Stage 3C analysis**: Verification analysis run — GPT-5.2 dominant (84%), Gemini-3.1 (15%), Claude custom (1%)
- ✅ **Step 4c (2nd-layer recheck)**: All 43 corrected/custom rows rechecked independently via `log-gen-verifier-4c.ipynb` — corrections verified as accurate, `Recheck_4c` columns added to criteria CSV (2026-04-04)
- ✅ **Phase 2 Step 2.1**: Verified R1 seeds merged into `Deception-Dataset.csv` — 225 verified + 25 manual = 250 R1 rows complete (2026-04-04)

### **log-gen-r2.ipynb Refinements** ✅ COMPLETE (2026-04-05, Session 2)
**Purpose**: Quality improvements to Pass 1 and Pass 2 prompts

**Changes to Pass 1 Prompt (Cell 13 — `build_pass1_prompt`)**:
1. ✅ Fixed triple-quote corruption: Added missing closing `"""` before `return prompt`
2. ✅ Improved tactic evolution guidelines:
   - Good players: Expanded from vague rules to 4 situation-based sections (Quest FAILED, Quest PASSED, Being falsely accused, Identifying a suspect)
   - Evil players: Expanded from limited coverage to 6 situation sections (Quest FAILED, Quest PASSED, teammate under suspicion, self under suspicion, framing opportunities, game stage guidance)
   - Added level-specific bullets for context (High GRS / Moderate GRS / Low GRS under Quest FAILED; similar for Evil)
   - Added dynamic `stage_guidance` variable computed from `round_id` (Early/Mid/Late game stage advice)
3. ✅ Added format specification with per-player linebreaks:
   - OUTPUT FORMAT section now explicitly shows 4 individual player lines in `matrix_tactic_scale`
   - STRICT RULES clarified: "level: copy exactly from the R1 seeds shown above — do not change it"
4. ✅ Audit & bug fixes (full codebase review):
   - Cell 1 design note: Updated to reflect new Good player situation-based transitions
   - Added blank line separation in STRICT RULES section to prevent visual merging

**Changes to Pass 2 Prompt (Cell 15 — `build_pass2_prompt`)**:
1. ✅ Fixed triple-quote corruption: Added missing closing `"""` before `return prompt`
2. ✅ Removed few-shot examples (2 FORMAT EXAMPLES + variable):
   - Deleted `PASS2_FORMAT_EXAMPLES` variable entirely (saved ~300 tokens of potentially misleading constraint)
   - Removed `# FORMAT EXAMPLES` section from f-string
   - Rationale: Examples anchor model to specific player IDs and outcomes that may not match actual generation; prior-round dialogue provides format template; verifier handles format errors
3. ✅ Enhanced tactic pool clarity:
   - Added explanatory note after TACTIC DEFINITIONS: "some tactics are available to both Good and Evil players (shared pool). Good-only tactics may not be used by Evil players and vice versa. The pre-assigned tactic already respects each player's alignment pool."
4. ✅ Improved pre-assigned tactics instruction (more concrete):
   - Old: "Use these suggested tactics for each speaker (you may adjust ...)"
   - New: "Each speaker's tactic has been pre-assigned based on their role, scale level, and the current game state. Write dialogue that authentically expresses it. If a substitution improves natural flow, you may use a neighboring tactic — but the annotation must match what was actually written, and the tactic must remain within the player's alignment pool."
5. ✅ Explicitly required scale/level to be immutable:
   - Old: "Scale: 'GRS' for Good players, 'Mach-IV' for Evil players (unchanged from Round 1)"
   - New: "Scale: 'GRS' for Good players, 'Mach-IV' for Evil players — copy exactly from the pre-assigned entry above; do not change it"
   - Similar update for Level: "copy exactly from the pre-assigned entry above; do not change it under any circumstance"

**File State**:
- `log-gen-r2.ipynb`: All 27 cells functional, both Pass 1 and Pass 2 prompts ready for execution
- Helper scripts cleaned up: `_audit.py` and `_fix_quotes.py` removed
- Next action: Run PASS 1 test (3 games) to validate prompt behavior

### **Current Status**: 
- ✅ **Phase 1 & 2 COMPLETE**: R1 verified (225 games), merged into Deception-Dataset.csv (250 R1 rows total)
- ✅ **log-gen-r2.ipynb pipeline TESTED end-to-end**: G001 R2 dialogue generated and reviewed; PASS 1 (GPT-5.2 tactic precompute) + PASS 2 (GPT-5.2 dialogue) both functional
- ✅ **Vote-confusion flaw FIXED**: PASS 2 prompt now has comprehensive `# AVALON RULES AND PUBLIC HISTORY FORMAT` section explaining team approval votes (P#:Y/N, public) vs quest execution (PASS/FAIL, anonymous). PASS 1 prompt also updated with format guide. Cell 15 f-string corruption fixed (preview code was merged into f-string).
- ✅ **README updated**: `README-v3.md` created with log-gen-r2.ipynb pipeline instructions; old `README.md` deleted.
- ⏳ **NEXT IMMEDIATE**: Phase 4 — full R2 generation run
  - Notebook: `log-gen-r2.ipynb` (27 cells, all tested)
  - Step A: Run full PASS 1 (change `PASS1_NUM_GAMES = len(games_to_generate)` — 250 games)
  - Step B: Run full PASS 2 with GPT-5.2 (`PASS2_MODEL_SELECTION = 'gpt-5.2'`, `PASS2_NUM_GAMES = len(pass1_df)`)
  - Step C: Run PASS 2 again with Gemini-3.1 (`PASS2_MODEL_SELECTION = 'gemini-3'`)
  - Step D: Merge outputs; adapt verifier (`log-gen-verifier.ipynb`) for R2
  - Step E: Repeat for R3, R4, R5 (ROUND_ID variable makes notebook reusable)
- 📝 **Phase 3 redesigned**: `prior_summary_gold` is now ***post-hoc only*** — generated after ALL 5 rounds complete. NOT used as generation context. `generate-prior-summaries.ipynb` to be created LAST (after R5).
- ⏳ **Phase 6 (ToM)**: Blocked until all 5 rounds of dialogue are finalized

### **Remaining Work (Short-term - 1k samples)**:
- ✅ ~~Phase 2~~: R1 seeds merged into `Deception-Dataset.csv`
- 🚀 **Phase 4** (CURRENT): R2-R5 two-pass dialogue generation
  - Two-pass design: Pass 1 (GPT-5.2 tactic precomputation) → Pass 2 (Gemini-3.1 + GPT-5.2 dialogue)
  - Context: Full verbatim prior dialogue (NOT summaries) + cumulative public history
  - Notebooks: `log-gen-r2.ipynb` (ready), R3-R5 will reuse same structure with ROUND_ID variable
- 🎁 Phase 5: Final assembly (1k sample dataset v1.0)
- 📝 **Phase 3 (POST-HOC LAST)**: `prior_summary_gold` generation → run AFTER R5 complete
  - Notebook: `generate-prior-summaries.ipynb` (create last)
  - Uses full finalized dialogues as input; outputs 4-6 sentence behavioral summaries
  - R1 rows keep `prior_summary_gold = ""` (no prior round)
- 🧠 Phase 6: ToM gold label generation (1k samples)

### **Remaining Work (Long-term - 10k-20k samples)**:
- 🚀 Phase 7: Dataset scaling (2,000-5,000 games → 10k-20k samples)

### **Estimated Timeline**:
**Immediate (analysis + R1 merge)**:
- Step 1.2 analysis: ~15 min
- Phase 2 merge: ~30 min
**Phase 3-5 (R2-R5 + final assembly)**:
- Phases 3: ~1-2 hours
- Phase 4 (R2-R5): ~30-35 hours (parallelizable)
- Phase 5: ~2-3 hours
- **Subtotal: ~34-40 hours** of compute + manual work

**Phase 6 (ToM generation)**:
- ~8-10 hours for 1,000 annotations + validation

**Phase 7 (10k-20k scaling)**:
- ~200-400 hours (highly parallelizable across multiple machines/API keys)
- Expected to run over 2-4 weeks with distributed processing

**Total Project Timeline**: ~250-450 hours compute time (or 3-6 weeks with parallelization)

---


  - R4: ~100 games (many ended after R3)
  - R5: ~50 games (final missions only)

**6. Final Dataset Release**
- Combine all verified seeds (R1-R5)
- Generate final statistics
- Document in dataset.tex
- Release to research community with code notebooks

---

## 🔑 Key Technical Decisions & Thresholds

### **R2-R5 Pipeline Design (finalized 2026-04-05)**:
- **Two-pass architecture**: Pass 1 (GPT-5.2 tactic precomputation) → Pass 2 (dialogue generation)
  - Pass 1 chosen for GPT-5.2 to avoid circularity (Claude is verifier, not planner)
  - Pass 1 output: `pass1_r{N}_tactic_precompute.csv` (intermediate, inspectable)
  - Pass 2 models: Both Gemini-3.1 and GPT-5.2 run independently (same as R1)
- **Generation context**: Full verbatim prior dialogue (NOT summaries) + cumulative public history
  - Summaries are lossy; full dialogue used since compute is unconstrained
  - Cumulative public history = R1 + R2 + ... + R(N-1) public_history strings concatenated
- **prior_summary_gold**: Post-hoc only — generated AFTER all 5 rounds finalized, NOT used during generation
  - R1 rows keep `prior_summary_gold = ""` (no prior round)
  - Created via `generate-prior-summaries.ipynb` (last step of pipeline)
- **Tactic evolution**: Asymmetric design
  - Good players (GRS): Stable — maintain R1 tactic unless game state demands shift
  - Evil players (Mach-IV): Adaptive — shift based on quest outcomes/suspicion state
  - Expanded Good pool for R2+: 19 tactics (10 green + 9 blue); Evil pool: 27 tactics unchanged
  - Scale & level: Fixed per player from R1 — only tactic may change
  - Soft uniqueness: prefer different tactics across speakers, but same tactic is acceptable if contextually motivated
- **Protagonist rotation**: Protagonist (silent observer) changes each round — verified in data
  - Player who was R1 protagonist has no R1 tactic seed → assigned fresh cyclic level in Pass 1
- **Notebooks**: `log-gen-r2.ipynb` (created 2026-04-05, 27 cells, verified)
  - Reusable for R3-R5 via `ROUND_ID` global variable

### **Verification Scoring**:
- **Binary scoring**: 1=PASS, 0=FAIL per criterion (5 criteria total)
- **Total format**: \"X of 5\" (e.g., \"4 of 5\", \"5 of 5\") to prevent Excel date misinterpretation
- **Decision thresholds**:
  - Both 5/5: Pairwise comparison, select superior response (Correction_Mode: Pairwise_Tiebreaker)
  - One 5/5, other <5/5: Select the 5/5 response (Correction_Mode: None)
  - At least one 4/5: Targeted correction of 4/5 response (Correction_Mode: Targeted)
    - Both 4/5: Default to GPT-5.2 response with targeted correction
  - Both ≤3/5: Claude generates full custom dialogue (Correction_Mode: Full_Custom)
- **Correction system**: Four-tier selection with targeted fix capability
- **JSON output**: Structured response with per-criterion explanations for all (pass and fail)

### **Tactic Assignment**:
- **Strategy**: Level-based distribution (High/Moderate/Low skill pools)
- **Good tactics pool**: High=10 Green; Moderate=19 (10 Green + 9 Blue); Low=19 (Blue prioritized, then Green)
- **Evil tactics pool**: High=18 Red; Moderate=27 (18 Red + 9 Blue); Low=27 (Blue prioritized, then Red)
- **Skill levels**: {High, Moderate, Low} cycled uniformly across speakers (6 scale-level combinations, ~150 each)
- **Result**: Green: 29-32 uses each; Red: 17-20 uses each; Blue: 22-28 uses each (~25% blue overall)

### **JSON Formatting**:
- **Matrix tactic scale**: Compact JSON (no linebreaks within structure)
- **Format**: `{"P2":{"row":"...","col":"...","tactic":"...","scale":"...","level":"..."},...}`
- **Example player entry**: 
  ```json
  "P2": {"row": "Selective / Framing", "col": "Cooperative", "tactic": "Strategic uncertainty", "scale": "GRS", "level": "High"}
  ```

### **ID Naming Convention**:
- **Game ID format**: G001, G002, ..., G250
- **Round ID format**: R1, R2, R3, R4, R5
- **Combined ID** (for scores CSV): "G001/1", "G002/1", etc.
- **Total format**: "X of 5" (e.g., "4 of 5", "5 of 5") to prevent Excel date conversion
- **LLM_used values**: 
  - "Gemini-3.1" (selected directly from Gemini-3.1)
  - "Gemini-3.1-Claude-4.5" (Gemini-3.1 with targeted correction by Claude)
  - "GPT-5.2" (selected directly from GPT-5.2)
  - "GPT-5.2-Claude-4.5" (GPT-5.2 with targeted correction by Claude)
  - "Claude-4.5" (full custom generation by Claude)
  - "[base]-Recorrected" (row was rechecked in Step 4c and received a targeted fix, e.g. "GPT-5.2-Claude-4.5-Recorrected")
  - "[base]-Regenerated" (row was rechecked in Step 4c and fully regenerated, e.g. "Claude-4.5-Regenerated")

---

## 📁 File Structure & Locations

```
d:\Projects\Avalon-deception\
│
├── 📄 PROGRESS.md (this file)
├── 📄 README.md (project overview)
├── 📄 dataset.tex (publication documentation, 470+ lines)
│
├── 📓 STAGE 1 - Player Roles
│   └── dataset-aug.ipynb (2362 lines, 20+ cells)
│       Status: ✅ Complete
│       Output: player_roles column in all seed CSVs
│
├── 📓 STAGE 2 - Public History
│   ├── dataset-aug-public-history.ipynb (1720 lines, 25+ cells)
│   │   Status: ✅ Complete
│   │   Output: public_history column in all seed CSVs
│   └── ph-verifier.ipynb (validation notebook)
│       Status: ✅ Complete
│       Result: 0 hard constraint violations across 250 games
│
├── 📓 STAGE 3A - Dialogue Generation
│   ├── log-gen.ipynb (992 lines, 22 cells)
│   │   Status: ✅ Complete
│   │   Output: generated_r1_seeds_gemini3.csv, generated_r1_seeds_gpt5_2.csv
│   │   Models: Gemini-3.1, GPT-5.2
│   │   Coverage: 225 games each, 100% validation pass
│   └── llm.py (supporting module for LLM calls)
│       Status: ✅ Exists (not modified)
│
├── 📓 STAGE 3B - Dialogue Verification
│   ├── log-gen-verifier.ipynb (19 cells)
│   │   Status: ✅ COMPLETE (225 games verified)
│   │   Inputs: generated_r1_seeds_gemini3.csv, generated_r1_seeds_gpt5_2.csv
│   │   Outputs: verified_r1_seeds_combined.csv, verified_r1_criteria_scores.csv
│   │   Verifier: Claude Sonnet 4.5
│   │   Legacy: log-gen-verifier-gpt4o.ipynb (old GPT-4o version, kept for reference)
│   └── log-gen-verifier-4c.ipynb (Step 4c — 2nd-layer recheck)
│       Status: ✅ COMPLETE (43 corrected rows rechecked)
│       Inputs: verified_r1_seeds_combined.csv, verified_r1_criteria_scores.csv, generated_r1_seeds_gemini3.csv
│       Outputs: verified_r1_seeds_combined.csv (patched), verified_r1_criteria_scores.csv (4 new columns)
│       Verifier: Claude Sonnet 4.5 with prompt caching
│
├── 📊 Data Files
│   ├── Deception-Dataset.csv (original 250 games, baseline)
│   ├── generated_r1_seeds_gemini3.csv (225 Round-1 games, Gemini-3.1 generated)
│   ├── generated_r1_seeds_gpt5_2.csv (225 Round-1 games, GPT-5.2 generated)
│   ├── verified_r1_seeds_combined.csv (225 verified dialogues with LLM_used)
│   ├── verified_r1_criteria_scores.csv (225 per-criterion score records)
│   ├── verified_r1_seeds_combinedgpt4o.csv (legacy GPT-4o verification, kept for reference)
│   └── verified_r1_criteria_scores-gpt4o.csv (legacy GPT-4o scores, kept for reference)
│
├── 📁 fig/
│   ├── player_role_balance.png (Figure 1)
│   ├── mission_outcome_bar_chart.png (Figure 2)
│   ├── voting_pattern_distribution.png (Figure 3)
│   └── [12 other analysis figures]
│
├── 📁 remote/
│   ├── GRPO_prac.ipynb (separate GRPO training work)
│   ├── instructions.txt
│   └── requirements.txt
│
├── Fardin.bib (bibliography for papers by Fardin)
└── Munindar.bib (bibliography for papers by Munindar)
```

---

## 🔗 File Dependencies & Data Flow

```
Deception-Dataset.csv (250 seed games)
    ↓
dataset-aug.ipynb
    ↓ [Adds: player_roles column]
    ↓
dataset-aug-public-history.ipynb
    ↓ [Adds: public_history column]
    ↓
ph-verifier.ipynb [Validates: 0 hard violations]
    ↓
log-gen.ipynb
    ├─→ [Generates with Gemini-3.1]
    │   ↓
    │   generated_r1_seeds_gemini3.csv (225 games)
    │
    └─→ [Generates with GPT-5.2]
        ↓
        generated_r1_seeds_gpt5_2.csv (225 games)
            ↓
            [Both inputs to]
            ↓
            log-gen-verifier.ipynb [Claude Sonnet 4.5 arbiter]
                ↓
                verified_r1_seeds_combined.csv (225 selected/corrected/custom)
                verified_r1_scores.csv (225 score records)
```

---

## 💾 CSV Column Descriptions

### **Source CSVs** (gemini3 and gpt5_2):
| Column | Type | Example | Notes |
|---|---|---|---|
| game_id | str | G026 | Unique game identifier |
| round_id | int | 1 | Round number (1-5) |
| role_id | str | P1 | Focal player for generation |
| llm_alignment | str | Good | Focal player's role |
| player_roles | JSON | {"P1":"Good",...} | All 5 player roles |
| public_history | str | "Round: 1\nLeader: P3\n..." | Quest outcomes, teams, votes |
| prior_summary_gold | str | "" | Empty for R1, filled in R2-R5 |
| discussion_log | str | "Discussion after Quest 1:\n..." | 4-speaker dialogue |
| matrix_tactic_scale | JSON | {"P2":{...},"P3":{...},...} | Tactic annotations (compact format) |

### **Verified Output CSVs**:
**verified_r1_seeds_combined.csv** - All original columns + verification metadata:
| Column | Type | Example | Notes |
|---|---|---|---|
| [original 9 cols] | | | Same as source CSVs |
| Claude_Reasoning | str | "Response B achieves 5/5..." | Claude's decision explanation (2-3 sentences) |
| LLM_used | str | "GPT-5.2" | Which model's dialogue was selected |

**verified_r1_criteria_scores.csv** - Detailed per-criterion tracking:
| Column | Type | Example | Notes |
|---|---|---|---|
| ID | str | G026/1 | game_id/round_id format |
| Gemini31_Coherence | int | 1 | Binary: 1=pass, 0=fail |
| Gemini31_History | int | 1 | Binary: 1=pass, 0=fail |
| Gemini31_Matrix | int | 1 | Binary: 1=pass, 0=fail |
| Gemini31_Authenticity | int | 0 | Binary: 1=pass, 0=fail |
| Gemini31_Format | int | 1 | Binary: 1=pass, 0=fail |
| Gemini31_Total | str | "4 of 5" | Total passed criteria |
| GPT52_[criteria] | int | 1 | Same structure for GPT-5.2 |
| GPT52_Total | str | "5 of 5" | Total passed criteria |
| Selected_LLM | str | "GPT-5.2" | Which model was selected |
| Correction_Mode | str | "None" | None / Pairwise_Tiebreaker / Targeted / Full_Custom |
| Claude_Reasoning | str | ... | Decision explanation |
| Gemini31_Criteria_Explanations | JSON str | {"coherence":"...", ...} | Explanations for all 5 criteria |
| GPT52_Criteria_Explanations | JSON str | {"coherence":"...", ...} | Explanations for all 5 criteria |

---

## 🧠 Key Theoretical Foundations

### **Deception Theories Integrated**:

1. **Interpersonal Deception Theory (IDT)** - Buller & Burgoon
   - Deception is goal-directed and adaptive
   - Maps to "Goal Orientation" columns (Cooperative, Defensive, Opportunistic, Adversarial)

2. **Truth-Default Theory (TDT)** - Levine
   - Complements IDT on how deception goals manifest
   - Used for column definitions

3. **Information Manipulation Theory 2 (IMT2)** - McCornack et al.
   - Focuses on how deceptive messages relate to truth
   - Maps to "Information Strategy" rows (Transparent, Selective, Careless, Counterfactual)

4. **Philosophy of Lying/Bullshitting** - Carson, Frankfurt
   - Distinguishes different deceptive communication styles
   - Informs row definitions

### **Avalon Game Rules** (encoded in validation):
- 5 players, 3 Good vs 2 Evil
- 5 quests with varying team sizes
- Team proposals, voting (need majority), then quest success/fail votes
- Good wins if 3 quests pass; Evil wins if 3 quests fail
- Players can see roles only of themselves (except finally at end)

---

## 🎓 Related Work & Literature

**Key papers referenced in dataset.tex**:
- LLM multiagent reasoning (Li+23, Zhang+24)
- Gricean pragmatics in human-AI interaction (Vogel+13, Panfili+21)
- In-context learning (Brown+20, Min+22)
- LLM-based generation of synthetic data (Shao+23)
- Theory of Mind in LLMs (Street+24, Kosinski+24)
- Deception detection (Sarkadi+18, Jones-15)
- Avalon-specific research (Light+23, Wang+23, Wang+24)

See `dataset.tex` for complete bibliography entries.

---

## 📝 Version History

| Date | Work | Status |
|---|---|---|
| Jan 23, 2026 | Stage 1 & 2 pipelines created | ✅ Complete |
| Jan 23-24 | Behavior matrix designed, 37 tactics defined | ✅ Complete |
| Jan 25-29 | log-gen.ipynb created, GPT-4o generation complete | ✅ Complete (legacy) |
| Jan 29-30 | Initial dataset.tex documentation | ✅ Complete |
| Jan 31-Feb 5 | Prompt refinement, dataset.tex expanded | ✅ Complete |
| Feb 5 | log-gen-verifier.ipynb created & tested (5 games, GPT-4o) | ✅ Complete (legacy) |
| Feb 6 | Full dataset.tex finalized with examples & figures | ✅ Complete |
| Feb 6 | PROGRESS.md created | ✅ Complete |
| Feb 6-17 | R1 verification (GPT-4o version) | ✅ Complete (legacy) |
| **Feb 17** | **ToM gold label generation planned (Stage 4)** | 📋 PLANNED |
| **Feb 17** | **10k-20k scaling roadmap finalized (Phase 7)** | 📋 PLANNED |
| **Feb 17** | **Abstract written for dataset.tex** | ✅ Complete |
| **Mar 2026** | **Switched generation from GPT-4o → Gemini-3.1** | ✅ Complete |
| **Mar 2026** | **Updated log-gen.ipynb for Gemini-3.1** | ✅ Complete |
| **Mar 2026** | **Updated log-gen-verifier.ipynb for Gemini-3.1 vs GPT-5.2** | ✅ Complete |
| **Mar 2026** | **Full 225-game verification run (Gemini-3.1 vs GPT-5.2)** | ✅ Complete |
| **Mar 23, 2026** | **Verification analysis + R1 merge pending** | ⏳ NEXT |
| **Mar 25, 2026** | **Verification analysis done; G122 manually scored & inserted in both CSVs (225 rows each); Phase 1 complete** | ✅ Complete |
| **Mar 26, 2026** | **Verification prompt redesigned: crit 1 → Discussion Coherence & Tactic Situational Fit; crit 3 → Framing B (dialogue = ground truth); crit 4 restored; TACTIC_TAXONOMY_REF built dynamically from JSON; cell 8 corruption fixed; all PRE-ASSIGNED refs removed. Full re-run pending.** | ⏳ Re-run pending |
| **Mar 27, 2026** | **Prompt finalized: `roles` JSON key → `coherence`; C4 rewritten (no strategy overlap); C5 duplicate 1= fixed; Step 3 markdown updated. All 225-game re-run prerequisites complete.** | ⏳ Re-run pending |
| **Mar 27, 2026** | **Full 225-game re-run completed with finalized prompt (Discussion Coherence & Tactic Situational Fit; dialogue = ground truth framing; TACTIC_TAXONOMY_REF).** | ✅ Complete |
| **Mar 27, 2026** | **verify_dialogue_pair() finalized post-run: 4/4 pairwise logic (Claude chooses winner, not hardcode B); field explanations corrected (CHOSEN response, matrix_tactic_scale restored); tc_dialogue=None warning; Cell 14 rewritten to re-run Targeted rows + empty-dialogue rows; cell 10 syntax corruption fixed.** | ✅ Complete |
| **Apr 4, 2026** | **R1 seeds merged into Deception-Dataset.csv (Phase 2 Step 2.1 complete): 225 verified + 25 manual = 250 R1 rows.** | ✅ Complete |
| **Apr 4, 2026** | **Step 4c: 2nd-layer recheck of 43 corrected rows via log-gen-verifier-4c.ipynb. Prompt caching (STATIC_EVAL_PROMPT). ACCEPT-first + Benefit of Doubt. Recheck_4c_* columns added to criteria CSV. Corrections verified accurate. LLM suffix renamed -Recorrected / -Regenerated.** | ✅ Complete |
| **Apr 5, 2026 (Evening)** | **log-gen-r2.ipynb prompt refinements: Fixed triple-quote corruption in cells 13 & 15. Pass 1 tactic eval guidelines expanded (4 Good situations + 6 Evil situations + level-specific behavior + dynamic stage_guidance). Pass 2: Removed FORMAT_EXAMPLES, added tactic pool note, improved pre-assigned tactics instruction, explicitly required scale/level immutability. Ready for test run.** | ✅ Complete |
| **Apr 6, 2026** | **log-gen-r2.ipynb full pipeline test: All cells run for G001. Discovered vote-confusion flaw (P4 confused team approval votes with quest execution votes). Fixed: PASS 1 + PASS 2 prompts now include comprehensive Avalon rules section distinguishing team approval votes (P#:Y/N, public) from quest outcome (PASS/FAIL, anonymous). Cell 15 f-string corruption fixed (preview code was merged into f-string by prior edit). README-v3.md created; README.md deleted. G001 re-generated without vote confusion.** | ✅ Complete |
| **Apr 9, 2026** | **G016-G023 malformed JSON fixed in Deception-Dataset.csv (missing comma in matrix_tactic_scale — human annotation error). All 250 R1 matrices audited clean. log-gen-r2.ipynb: Cell 5 repair_matrix_json fallback + diagnostics added; Cell 23 p2_candidates defined before use (bug fix). Pushed commits 704cbb0, d3c036f. log-gen-r3.ipynb: same two fixes applied locally, NOT pushed (needs full review first).** | ✅ r2 pushed; r3 local only |
| **May 2026** | **Full R2/R3 notebook review vs each other. repair_matrix_json regex fixed in R2. R3 removed from remote (git rm --cached; untracked locally). R3 Cell 13 fix: hardcoded \"# ROUND 1 DISCUSSION\" and \"# ROUND 1 TACTIC SEEDS\" → `{PRIOR_ROUND_ID}`. Deception-Dataset.csv R1 discussion_log formatting fixed: G013 bad header+trailing-quote+P\\d\\ :spacing, G014-G015/G017-G020 P\\d\\ :spacing+single-\\n normalization, G016/G025 bad headers, G025 single-quote dialogue markers→double. 0 issues remaining.** | ✅ Local fixes done; pending push |

---

## 💡 For Next Session: Quick Start Guide

**CURRENT NEXT STEP: Push `Deception-Dataset.csv` fixes to GitHub. Then set up R2 verifier (adapt `log-gen-verifier.ipynb` for R2 input CSVs from Zhe). After verification, merge R2 into master CSV, then start R3 generation.**

All R1 work is ✅ COMPLETE:
- 225 games verified by Claude Sonnet 4.5 (`log-gen-verifier.ipynb`)
- 43 corrected rows independently rechecked (Step 4c, `log-gen-verifier-4c.ipynb`) — corrections verified accurate
- R1 seeds merged into `Deception-Dataset.csv` (250 R1 rows: 225 verified + 25 manual)

**Phase 3 — Prior Summary Generation:**
1. Create `generate-prior-summaries.ipynb`
2. Load `verified_r1_seeds_combined.csv` + `Deception-Dataset.csv`
3. For each R1 game, use Claude Sonnet 4.5 to summarize the R1 discussion:
   - Input: `discussion_log` + `public_history` for that round
   - Output: 3-4 sentence factual summary (team, vote result, quest outcome, key points)
   - Do NOT reveal player alignments in the summary
4. Write summaries into the `prior_summary_gold` column for R1 rows in `Deception-Dataset.csv`
5. This feeds directly into R2 generation context

**After Phase 3 — Phase 4 (R2-R5):**
- Follow PHASE 4 steps (4.1–4.6) in this document
- Adapt `log-gen.ipynb` for R2+ context (include `prior_summary_gold` in prompt)
- Filter active games per round (game ends after 3 PASS or 3 FAIL)
- Expand Good tactic pool to 19 (10 Green + 9 Blue) for R2+

**IF STARTING ToM GENERATION (Phase 6)**:
1. Complete Phases 1-5 first (R1-R5 dialogues verified)
2. Review Stage 4 schema in PROGRESS.md (abduction, suspicion, beliefs structure)
3. Create `tom-label-generation.ipynb` following Step 6.1 methodology
4. Test on 5-10 samples before full 1,000-sample run
5. Validate JSON schema compliance and logical consistency

**IF PLANNING SCALE-UP (Phase 7)**:
1. Ensure 1,000-sample v1.0 dataset is complete and validated
2. Review Step 7.1 strategies (template permutation vs fully synthetic)
3. Plan resource allocation (API budget, compute time, storage)
4. Set up parallel processing infrastructure (multiple API keys, distributed batches)
5. Implement quality monitoring (random sampling, bias detection)

**IF STARTING FRESH COMPONENT**:
- **For understanding dataset**: Read dataset.tex (publication-ready doc)
- **For understanding Stage 1**: Check dataset-aug.ipynb
- **For understanding Stage 2**: Check dataset-aug-public-history.ipynb + ph-verifier.ipynb results
- **For understanding Stage 3**: Check log-gen.ipynb + log-gen-verifier.ipynb logic

**IF DEBUGGING/MODIFYING**:
- Scoring logic: See client initialization cell & `verify_dialogue_pair()` function
- Decision logic: 4-tier system (5/5 → pairwise; 4/5 → targeted; ≤3/5 → custom)
- Output format: See DataFrame creation cell & CSV saving cell
- Verification rules: See "Validation Checklist" section above

---

## ✅ Checklist for Next Steps

**Step 1.2: Run Verification Analysis**: ✅ DONE (2026-03-27)
- [x] Open `log-gen-verifier.ipynb`
- [x] Run the last cell (Comprehensive Analysis)
- [x] Per-criterion pass rates: Gemini-3.1 weakest = Matrix (50.2%), GPT-5.2 weakest = Matrix (78.2%)
- [x] LLM_used: GPT-5.2 84%, Gemini-3.1 15%, Claude custom 1%

**Step 2.1: Merge R1 with Master Dataset**: ✅ COMPLETE (2026-04-04)
- [x] Load `Deception-Dataset.csv` (250 games)
- [x] Load `verified_r1_seeds_combined.csv` (225 verified rows)
- [x] Merge on `game_id`, keep verified `discussion_log` + `matrix_tactic_scale` for 225 games
- [x] Preserve original for 25 manual games (`LLM_used = 'Manual'`)
- [x] Saved into `Deception-Dataset.csv`
- [x] Validated: 250 R1 rows, no duplicate game_ids

**Step 4c: 2nd-layer recheck of corrected rows**: ✅ COMPLETE (2026-04-04)
- [x] Rechecked 43 corrected rows via `log-gen-verifier-4c.ipynb`
- [x] Prompt caching implemented, ACCEPT-first bias applied
- [x] `Recheck_4c_*` columns added to `verified_r1_criteria_scores.csv`
- [x] Corrections verified accurate; LLM suffix updated for changed rows

**Phase 3–4: R2-R5 Generation (remaining ~750 rows)**:
- [ ] Generate `prior_summary_gold` for R1 (Claude summaries of each R1 dialogue)
- [ ] Generate R2 dialogue + matrix_tactic_scale (Gemini-3.1 + GPT-5.2)
- [ ] Verify R2 with Claude Sonnet 4.5 → `verified_r2_seeds_combined.csv`
- [ ] Repeat for R3, R4, R5 (iterative: summarize → generate → verify)
- [ ] Assemble final 1k-sample dataset

## 📞 Contact & Attribution

**Project Lead**: Fardin (Feb–Mar 2026)  
**Collaborators**: Deepika Patibandla, Zhe Zhang, Amanul Haque, Munindar P. Singh  
**Verifier Implementation**: Claude Sonnet 4.5 (Anthropic)  
**Dialogue Generation**: Gemini-3.1 (Google), GPT-5.2 (OpenAI)

---

**Last Updated**: April 4, 2026  
**Next Review**: After Phase 3 (prior summaries) and R2 generation complete
