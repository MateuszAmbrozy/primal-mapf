# Fine-tuned policy demonstrations

These animations show the improved PRIMAL model using map-specific
pretrained weights. Each displayed run has eight agents and seed 123. Actions are sampled
from the legal-action policy using sequential execution and the variant-specific
environment profile (`historical` in the CLI).

| Map | Agents | Timesteps | Goals reached | GIF | MP4 |
| --- | --- | --- | --- | --- | --- |
| Maze | 8 | 67 | 8/8 | [View](maze_improved/animation.gif) | [Video](maze_improved/animation.mp4) |
| Room | 8 | 168 | 8/8 | [View](room_improved/animation.gif) | [Video](room_improved/animation.mp4) |
| Warehouse | 8 | 137 | 8/8 | [View](warehouse_improved/animation.gif) | [Video](warehouse_improved/animation.mp4) |

Circles represent agents and outlined squares their goals; matching colors identify
each pair. Short trails show recent movement. Playback is accelerated to 12
timesteps per second, with pauses at the beginning and end. All transitions
come from policy inference; no solver plans or corrections are applied.

## Trials and selection

The models were run once per map with four agents and once with eight, always
using seed 123 and a limit of 512 timesteps. All six attempts completed. The
eight-agent runs are shown here. [trials.csv](trials.csv) includes every attempt.
This small set illustrates behavior on these scenarios; it is not an estimate
of success over arbitrary maps, starts, or goals. The sequential protocol also
differs from the common-profile joint protocol used by the default experiments.

## Reproduce

From the repository root:

```bash
python -m pip install -e ".[visualization]"
python scripts/animate_policy.py --map maze --variant improved --checkpoint results/fixed_maps/maze/train_improved/checkpoint.pt --agents 8 --seed 123 --output results/animations/maze
python scripts/animate_policy.py --map room --variant improved --checkpoint results/fixed_maps/room/train_improved/checkpoint.pt --agents 8 --seed 123 --output results/animations/room
python scripts/animate_policy.py --map warehouse --variant improved --checkpoint results/fixed_maps/warehouse/train_improved/checkpoint.pt --agents 8 --seed 123 --output results/animations/warehouse
```

With `--map`, provide an existing compatible `.pt` file using `--checkpoint`.
Use `--variant classic` for the classic architecture and a new output directory
for each run. New weights may produce different trajectories from the displayed examples.
The recorded trajectories below can be rendered without model files.

Add `--mp4` to also export a video; this requires `ffmpeg` on PATH. GIF export
requires Pillow only. `--max-frames` controls the number of rendered states;
the first and final states are always retained, and the complete trace is saved.
These examples render every timestep.

Each animation directory contains the full `trajectory.json`, checkpoint hash,
render settings and output hashes in `render.json`, a final-state poster, and
runtime metadata. The maps, endpoints, and action-sampling seed are recorded
so a run can be checked independently. To render the saved trace without inference:

```bash
python scripts/animate_policy.py --from-trace docs/animations/maze_improved/trajectory.json --output results/animations/maze_render
```

Rendering a saved trace does not require the model weights. If the checkpoint
is present locally, its hash is checked against the recorded value.

A failed rollout is exported with its actual terminal state and a time-limit
label. The script does not search for a successful seed or replace the policy
with a solver.
