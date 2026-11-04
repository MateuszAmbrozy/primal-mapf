"""Configuration selection for fixed-map training and evaluation."""
from .runtime import ROOT, read_config

MAPS = {
    "maze": "maps/maze-32-32-4.map",
    "room": "maps/room-64-64-16.map",
    "warehouse": "maps/warehouse-10-20-10-2-1.map",
}


def training_config(map_name: str, variant: str, init=None) -> dict:
    mode = "finetune" if init else "train"
    return read_config(ROOT/f"configs/maps/{map_name}/{mode}_{variant}.json")


def evaluation_config(map_name: str, variant: str, checkpoint: str) -> dict:
    if variant not in ("classic", "improved"):
        raise ValueError("Select --variant classic or improved")
    if not checkpoint:
        raise ValueError("Provide a model file with --checkpoint PATH.pt")
    config = read_config(ROOT/f"configs/maps/{map_name}/evaluate_scratch.json")
    config["models"] = {variant: checkpoint}
    config["output"] = f"results/fixed_maps/{map_name}/evaluate_{variant}"
    return config


def apply_overrides(config: dict, args) -> dict:
    config = dict(config)
    for key in ("episodes", "max_steps", "output", "seed", "execution", "environment_profile"):
        value = getattr(args, key, None)
        if value is not None:
            config[key] = value
    if args.agents is not None:
        config["agents"] = args.agents
        config.pop("scenarios", None)
    return config
