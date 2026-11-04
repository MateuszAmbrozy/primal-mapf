# Training and evaluation on fixed maps

The `fixed_map.py` command selects the map and model architecture; you provide a `.pt` model path.
Run it from the repository root with your Python environment active.

| Map name | File |
| --- | --- |
| `maze` | `maps/maze-32-32-4.map` |
| `room` | `maps/room-64-64-16.map` |
| `warehouse` | `maps/warehouse-10-20-10-2-1.map` |

The map stays fixed; starts and goals are resampled each episode from its largest
connected free component. Training defaults to four agents and 10,000 episodes
for either architecture. Settings are in `configs/maps/<map>/`.

## Train from scratch

```bash
python scripts/fixed_map.py train --map maze --variant classic
python scripts/fixed_map.py train --map maze --variant improved
```

Replace `maze` with `room` or `warehouse` for the other maps.
Outputs go to `results/fixed_maps/maze/train_classic/` and `train_improved/`.

## Fine-tune a saved model

```bash
python scripts/fixed_map.py train --map maze --variant classic --init results/train_classic/checkpoint.pt
python scripts/fixed_map.py train --map maze --variant improved --init results/train_improved/checkpoint.pt
```

Use any compatible `.pt` file. Initialization loads weights only, with a fresh
optimizer and episode count. Outputs go to
`results/fixed_maps/maze/finetune_<variant>/`.

## Choose a training budget

```bash
python scripts/fixed_map.py train --map maze --variant improved --init results/train_improved/checkpoint.pt --episodes 1000 --agents 8 --output results/my_maze_run
```

Other options include `--max-steps`, `--seed`, and `--expert pibt|ca|cbs`.
CA* and CBS require compilation. Use `--dry-run` to print the selected
configuration without training.

Each new run requires an empty output directory. Source checkpoints are read
only. The run's own `checkpoint.pt` is periodically replaced with its latest
state; copy any model you want to retain before continuing.

## Resume a map-specific run

```bash
python scripts/fixed_map.py train --map maze --variant classic --resume results/fixed_maps/maze/finetune_classic/checkpoint.pt --episodes 20000
```

Resume reads the configuration saved in the checkpoint, including its original
output directory and training settings. `episodes` is the total target count,
not the number of additional episodes. The requested map and variant must match
the checkpoint. Changing training parameters other than those permitted by
resume is rejected.

## Evaluate

Pass the model file and its architecture explicitly:

```bash
python scripts/fixed_map.py evaluate --map maze --variant improved --checkpoint results/my_maze_run/checkpoint.pt --output results/my_maze_evaluation
```

The command evaluates the selected model and PIBT with 4, 8, 16, and 32 agents,
using 20 scenarios per setting. Use `--agents 4 --episodes 2 --max-steps 64`
for a short check. There are no predefined weight groups or required model folders.

Use `--solvers pibt ca cbs` to include all solvers, or `--solvers` with no names
to evaluate models only. Repeated evaluations need a new `--output` directory.

Training and evaluation default to the common environment profile with joint
movement. For variant-specific observations and sequential movement, add
`--environment-profile historical --execution sequential`. Use the same
evaluation settings when comparing models.

The same configuration files can be used with `scripts/train.py` and
`scripts/evaluate.py` directly. For example:

```bash
python scripts/train.py --config configs/maps/maze/finetune_classic.json --init results/train_classic/checkpoint.pt
python scripts/evaluate.py --config configs/maps/maze/evaluate_trained.json
```

The last evaluation expects both fine-tuned variants to have been trained.
