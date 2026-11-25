# Retrospective architecture decisions

These are inferred design rationales, not historical decision approvals.

## Model design
Observed design: Smooth and unknown: log-transformed XGBoost regression. Erratic: spike classifier and separate quantity regressors. Intermittent and lumpy: occurrence classifier and two positive-demand regressors. The latter are named q60/q90 in code but squared-error objectives are present; calibrated quantile estimation is not established.

Review alternatives, trade-offs and acceptance evidence before publication.

## Engineering
Observed design: Chunked SQL reads, dtype downcasting, sparse-compatible transformations, feature alignment, serialized preprocessing and model artifacts, batch database writes. Chunk concatenation still requires memory proportional to the accumulated dataset.

Review alternatives, trade-offs and acceptance evidence before publication.

## Evaluation
Observed design: GroupKFold and out-of-fold predictions support evaluation across held-out product-store groups. MAE, RMSE and R² are available in the code. No executed metric results were supplied. Chronological backtesting and naïve baselines are recommended before claiming forecasting accuracy.

Review alternatives, trade-offs and acceptance evidence before publication.