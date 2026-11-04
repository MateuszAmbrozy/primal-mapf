"""Regenerate benchmark figures from the published CSV measurements."""
import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def plot(csv_path, destination, metric):
    with csv_path.open(newline="") as stream:
        reader = csv.DictReader(stream)
        parameter = reader.fieldnames[0]
        rows = list(reader)
    key = lambda value: float(value.strip("()").split(",")[0])
    values = sorted({row[parameter] for row in rows}, key=key)
    algorithms = sorted({row["Algorithm"] for row in rows})
    grouped = defaultdict(list)
    for row in rows:
        success = row["Success"].lower() in {"true", "1"}
        if metric == "success_rate":
            value = float(success) * 100
        elif metric == "time":
            value = float(row["Time"])
        elif success:
            value = float(row["Makespan"])
        else:
            continue
        grouped[row["Algorithm"], row[parameter]].append(value)
    fig, ax = plt.subplots(figsize=(10, 6))
    for algorithm in algorithms:
        means = [np.mean(grouped[algorithm, value]) if grouped[algorithm, value] else np.nan for value in values]
        ax.plot(range(len(values)), means, marker="o", label=algorithm.replace("_", " "))
    xlabel = {"agents": "Number of agents", "size": "Map size", "density": "Obstacle density"}[parameter]
    ylabel = {"success_rate": "Success rate (%)", "time": "Mean computation time (s)",
              "makespan": "Mean makespan (successful attempts only)"}[metric]
    ax.set(title=f"{ylabel} by {xlabel.lower()}", xlabel=xlabel, ylabel=ylabel)
    ax.set_xticks(range(len(values)), values)
    if metric == "success_rate":
        ax.set_ylim(-5, 105)
    if metric == "time" and "fixed_maps_base_vs_fine_tuned" not in str(csv_path):
        ax.set_yscale("log")
    ax.grid(True, alpha=0.3)
    ax.legend(title="Algorithm", loc="best")
    fig.tight_layout()
    destination.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(destination, dpi=180)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    research = ROOT / "research"
    checksums_path = research / "checksums.json"
    checksums = json.loads(checksums_path.read_text())
    count = 0
    for csv_path in sorted((research / "results").rglob("raw_*.csv")):
        stem = csv_path.stem.removeprefix("raw_")
        for metric in ("success_rate", "makespan", "time"):
            filename = f"{stem}_{metric}.png"
            candidates = (csv_path.parent / "plots" / filename, csv_path.parent / filename)
            path = next((candidate for candidate in candidates if candidate.exists()), candidates[0])
            plot(csv_path, path, metric)
            checksums[path.relative_to(research).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
            count += 1
    checksums_path.write_text(json.dumps(checksums, indent=2)+"\n")
    print(f"Regenerated {count} benchmark figures.")


if __name__ == "__main__":
    main()
