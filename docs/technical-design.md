# Retail Demand Forecasting ML — Technical design

Reconstructed from supplied source; not an original approved design.

## Business problem

Retail product-store demand differs in frequency and variability. The objective was to estimate daily sales quantities using differentiated models rather than a single universal predictor.

## Architecture

Calendarized sales input → data preparation and calendar features → ADI/CV² demand segmentation → specialized model training → grouped evaluation → serialized artifacts → batch inference and forward forecast outputs.

## Model design

Smooth and unknown: log-transformed XGBoost regression. Erratic: spike classifier and separate quantity regressors. Intermittent and lumpy: occurrence classifier and two positive-demand regressors. The latter are named q60/q90 in code but squared-error objectives are present; calibrated quantile estimation is not established.

## Engineering

Chunked SQL reads, dtype downcasting, sparse-compatible transformations, feature alignment, serialized preprocessing and model artifacts, batch database writes. Chunk concatenation still requires memory proportional to the accumulated dataset.

## Evaluation

GroupKFold and out-of-fold predictions support evaluation across held-out product-store groups. MAE, RMSE and R² are available in the code. No executed metric results were supplied. Chronological backtesting and naïve baselines are recommended before claiming forecasting accuracy.

## Forward inference

The separate inference script loads model artifacts and historical demand, aligns features and processes future inputs including a 14-day source. It contains classical intermittent forecasting helpers and experimental variability/safety-stock adjustments; these require validation and should not be represented as calibrated uncertainty.

## Explainability

The supplied training script labels its residual-correlation analysis SHAP-like. This is not verified Shapley attribution. Describe it as residual diagnostics; true SHAP validation is a future improvement.

## Value and limitations

Potential planning benefits include better demand visibility and differentiated inventory decisions. No verified savings, production adoption, accuracy improvement or go-live approval was supplied. Sales are a proxy for demand and may be censored by stockouts.

## Validation plan

Test segmentation boundaries, zero-only series, schema drift, unseen categories, artifact compatibility, deterministic predictions, temporal leakage, feature availability at forecast time, forecast bias and duplicate output keys. Recompute demand type using training history only; review preprocessing fitted before splitting.