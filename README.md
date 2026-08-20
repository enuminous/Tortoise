# TORTOISE

**Temporal Out-of-sample Recursive Testing of Operational Information Structure through Exclusion**

TORTOISE is a minimal, falsifiable EFMW-derived evaluation framework for prospective prediction experiments.

Its job is not to make EFMW win.

Its job is to make it difficult to misunderstand whether an EFMW-derived signal adds measurable predictive information beyond matched controls and conventional baselines.

## Core cycle

**Freeze → Predict → Score → Ablate → Replicate**

TORTOISE is intended for:

- machine degradation
- AI reliability
- network failure
- logistics
- control systems
- organizational dynamics
- sports forecasting
- other sequential systems with measurable future outcomes

## Scientific claim

The default hypothesis is narrow:

> Recursive relational state may contribute incremental predictive information in systems with temporal depth, partial observability, feedback, contradiction, and distributed state.

TORTOISE does **not** assume that this claim is true.

## Flat-stack repository

Every file lives in the repository root.

```text
README.md
LICENSE
CITATION.cff
pyproject.toml
requirements.txt
tortoise.py
model_full.py
model_control.py
ablations.py
baselines.py
metrics.py
freeze.py
forecast_schema.json
example_config.yaml
example_data.csv
example_run.py
test_tortoise.py
MANIFEST.sha256
```

## Model family

### M1 — Full TORTOISE candidate

Uses:

- robust normalization
- local state
- first and second differences
- relational features
- temporal memory
- contradiction
- coherence
- coherence velocity
- coherence acceleration
- recursive state update
- probabilistic prediction

### C0 — Matched non-EFMW control

Uses the same observations and temporal history but removes explicit:

- contradiction mapping
- coherence mapping
- coherence dynamics
- recursive coherence update

### Ablations

TORTOISE includes:

- no recursion
- no coherence
- no contradiction
- no relational features
- short memory
- shuffled relations
- shuffled temporal order

## Installation

```bash
python -m pip install -r requirements.txt
```

## Run the example

```bash
python example_run.py
```

## Run tests

```bash
pytest -q
```

## Minimal use

```python
import pandas as pd
from tortoise import TortoiseExperiment

df = pd.read_csv("example_data.csv")

exp = TortoiseExperiment(
    target_column="failure",
    time_column="time",
    feature_columns=["sensor_a", "sensor_b", "sensor_c"],
    horizons=(1, 3, 7, 23),
    random_state=23,
)

result = exp.run(df)
print(result)
```

## Freeze rule

Before prospective evaluation, freeze:

- source code
- configuration
- feature definitions
- horizons
- seeds
- baselines
- prediction target
- cutoff
- resolution rule
- metrics
- exclusions

Use:

```bash
python freeze.py
```

The script writes SHA-256 hashes for the repository files.

Once outcomes begin arriving, do not alter the frozen machine. Create a new version instead.

## Primary metric

For binary probabilistic prediction, TORTOISE uses Brier score as the default primary metric.

Lower is better.

Incremental advantage:

```text
Delta Brier = Brier(control) - Brier(TORTOISE)
```

Positive values favor TORTOISE.

Secondary metrics include:

- log loss
- ROC-AUC
- average precision
- calibration error
- accuracy at 0.5 threshold

## Interpretation

A useful result hierarchy:

0. no detectable effect  
1. better than null/base rate  
2. better than conventional baseline  
3. better than matched non-EFMW control  
4. advantage increases in preregistered structural habitat  
5. ablations identify the responsible operation  
6. independent prospective replication

## Negative results

A null or negative result is a successful experiment.

If the matched control performs equally well, no EFMW-specific contribution has been demonstrated.

If the matched control performs better, the tested EFMW formulation has degraded prediction.

Do not rescue the frozen version after observing outcomes.

## License

MIT.

## Status

Research software. Experimental. Not validated for medical, safety-critical, financial, or autonomous decision-making.
