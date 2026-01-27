#!/usr/bin/env python3

import argparse
import math
import re
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


LINE_RE = re.compile(
    r"(?P<unit>KBytes|Bytes):\s*(?P<size>\d+)\s+(?P<padding>\d+)\s+(?P<lat>\d+)\s+(?P<bw>\d+)"
)


def parse_points(text: str):
    sizes_bytes = []
    lats_ns = []
    for line in text.splitlines():
        m = LINE_RE.search(line)
        if not m:
            continue
        size = int(m.group("size"))
        if m.group("unit") == "KBytes":
            size *= 1024
        sizes_bytes.append(size)
        # bench_cache prints ns per 100 accesses; convert to ns per access
        lats_ns.append(int(m.group("lat")) / 100.0)
    return sizes_bytes, lats_ns


def _fmt_bytes(x, _pos):
    if x >= 1024 * 1024:
        return f"{int(x / (1024 * 1024))}M"
    if x >= 1024:
        return f"{int(x / 1024)}K"
    return f"{int(x)}"


def _power_ticks(lo, hi):
    lo_p = int(math.floor(math.log2(lo)))
    hi_p = int(math.ceil(math.log2(hi)))
    return [2 ** p for p in range(lo_p, hi_p + 1)]


def main():
    parser = argparse.ArgumentParser(
        description="Plot bench_cache results: working set size vs latency."
    )
    parser.add_argument("input", type=Path, help="Path to bench_cache output text file")
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Optional output image path (e.g., plot.png). If omitted, show interactively.",
    )
    args = parser.parse_args()

    text = args.input.read_text(encoding="utf-8", errors="ignore")
    sizes, lats = parse_points(text)

    if not sizes:
        raise SystemExit("No bench_cache data lines found. Check the input file.")

    pairs = sorted(zip(sizes, lats), key=lambda p: p[0])
    sizes = [p[0] for p in pairs]
    lats = [p[1] for p in pairs]

    fig, ax = plt.subplots(figsize=(9.5, 5.8))
    ax.plot(sizes, lats, marker="o", markersize=4, linewidth=1.6)
    ax.set_xlabel("Working set size (Bytes)")
    ax.set_ylabel("Latency (ns)")
    ax.set_title("DPA -> Host memory: Working set vs latency")
    ax.set_xscale("log", base=2)
    ax.set_yscale("log", base=2)
    ax.grid(True, which="both", linestyle="--", alpha=0.35)

    x_ticks = _power_ticks(min(sizes), max(sizes))
    y_ticks = _power_ticks(max(min(lats), 1e-6), max(lats))
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    ax.xaxis.set_major_formatter(FuncFormatter(_fmt_bytes))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _pos: f"{y:g}"))

    fig.tight_layout()

    out_path = args.out or Path("bench_cache.png")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=300)
    print(f"Saved plot to {out_path}")



if __name__ == "__main__":
    main()
