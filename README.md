# Retail Demand Forecasting ML
[![Demo checks](https://github.com/DesmondJiaLiangLoh/retail-demand-forecasting-ml/actions/workflows/demo.yml/badge.svg)](https://github.com/DesmondJiaLiangLoh/retail-demand-forecasting-ml/actions/workflows/demo.yml)

**Historical engineering case study** · Professional engineering portfolio

## Architecture

![Conceptual architecture](docs/architecture.svg)

This is a generalized reconstruction, not an internal deployment diagram.

## Technical capabilities and personal contributions

- **Demand classification:** Designed demand-aware routing instead of one universal model.
- **Model engineering:** Developed regression and two-stage modelling paths.
- **Scalable processing:** Implemented dtype control, batch processing and feature alignment.
- **Evaluation:** Implemented grouped evaluation and out-of-fold metrics.
- **Operational integration:** Developed forward forecasting and SQL output integration.

## Implementation boundaries

Some q60/q90-labelled regressors use squared-error objectives. Residual-based diagnostics are not verified SHAP. A strict temporal splitter exists but its use and leakage controls require validation. No independently verified forecast accuracy or business impact is claimed.

## Explore

- [Architecture walkthrough](docs/architecture.md)
- [Executive case study](docs/case-study.pdf)
- [Technical design](docs/technical-design.md)
- [Showcase slides](docs/showcase.pptx)
- [Interactive illustrative walkthrough](https://desmondjialiangloh.github.io/retail-demand-forecasting-ml.html)

Original enterprise implementation excluded from this reference edition.

## Executable reference demonstration

Run `python demo/forecast.py` and `python -m unittest discover -s demo -v` from the repository root. [Source](demo/forecast.py) · [Generated results](demo/results.json). This newly authored synthetic reference is distinct from the original enterprise implementation; it does not establish historical production performance.
