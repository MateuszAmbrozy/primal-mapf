# Benchmark results

CSV measurements and figures comparing the classic and improved PRIMAL models
with planning baselines.

| Directory | Experiments |
| --- | --- |
| `results/random/` | Agent count, map size, and obstacle density |
| `results/fixed_maps/` | Models on maze, room, and warehouse maps |
| `results/fixed_maps_fine_tuned/` | Map-specific fine-tuned models |
| `results/fixed_maps_base_vs_fine_tuned/` | Models before and after fine-tuning |
| `fine_tuning/improved/maze/` | Training reward figures |

The collection includes 22 CSV datasets, 66 comparison figures, and two training
figures. CSV files contain per-attempt measurements; plots show success rate,
makespan, and computation time.

## Interpretation

Full training configurations, seeds, and model revisions are not available for
these measurements. They do not establish performance for models trained with
the default configurations in this repository. Collections named `run_01`,
`run_02`, and measurements at experiment roots may overlap; do not pool them as
independent repetitions. Per-episode data for the two training figures is not
included.

For an experiment with recorded settings, training seeds, and shared evaluation
scenarios, see the [multi-seed example](../docs/portfolio/README.md).
New runs write their outputs to [`results/`](../results/README.md).

## Verify file integrity

```bash
python scripts/verify_research.py
```

[checksums.json](checksums.json) records SHA-256 hashes of the published data and
figures. Verification requires only the Python standard library.

## Regenerate figures

```bash
python -m pip install -e ".[research]"
python scripts/plot_results.py
```

This redraws the comparison figures from their CSV files and updates their
checksums. It leaves measurements and training reward figures unchanged.

## Run new comparisons

Use `scripts/evaluate.py` with the configurations in `configs/experiments/`.
Set the model paths to your `.pt` files and choose a new output directory.
See the [evaluation guide](../README.md#evaluation) for commands and metrics.
