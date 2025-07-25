#!/usr/bin/env python
import argparse
import os
import numpy as np
import pandas as pd
from d3blocks import D3Blocks


def load_data(npz_path, meta_path, start, end):
    # ─── load arrays ───────────────────────────────────────────────────────────
    data = np.load(npz_path, allow_pickle=True)
    path_preds = data["path"]
    background = data["background"]
    model_preds = data["predictions"]

    # slice
    path_preds = path_preds[start:end]
    background = background[start:end]
    model_preds = model_preds[start:end]

    # ─── build labels ──────────────────────────────────────────────────────────
    meta = pd.read_csv(meta_path, sep="\t", header=0)
    # assume meta has columns 'gamete_index' (integer) and 'gamete' (name)
    n_rows = background.shape[1]     # after transpose, rows = this
    idx_to_name = dict(zip(meta["gamete_index"], meta["gamete"]))
    labels = [idx_to_name.get(i, f"row_{i}") for i in range(n_rows)]

    return background, path_preds, model_preds, labels


def make_heatmap(bg, labels, out_html, title):
    # transpose so each row = one of 'labels'
    df = pd.DataFrame(bg.T, index=labels, columns=[
                      str(i) for i in range(bg.shape[0])])
    df.columns = [""] * df.shape[1]   # hide x‑ticks

    os.makedirs(os.path.dirname(out_html), exist_ok=True)
    d3 = D3Blocks()
    d3.heatmap(
        df,
        scaler=None,
        color="label",
        cmap=["white", "gray"],
        title=title,
        filepath=out_html,
        notebook=False,
        showfig=True
    )


def make_timeseries(path_preds, model_preds, out_html, title):
    import os
    import numpy as np
    from d3blocks import D3Blocks

    # build two series: x/y for HMM, x1/y1 for Model
    x = np.arange(len(path_preds))
    y = path_preds
    x1 = np.arange(len(model_preds))
    y1 = model_preds

    # ensure output directory exists
    os.makedirs(os.path.dirname(out_html), exist_ok=True)

    d3 = D3Blocks()
    # size must be > 0
    d3.scatter(
        x=x,
        y=y,
        x1=x1,
        y1=y1,
        size=3,
        title=title,
        filepath=out_html,
        showfig=True
    )


def main():
    p = argparse.ArgumentParser(
        description="Generate interactive heatmap + prediction plots"
    )
    p.add_argument("--npz",      "-z", required=True,
                   help="Path to .npz file (with ‘path’, ‘background’, ‘predictions’ arrays)")
    p.add_argument("--metadata", "-m", required=True,
                   help="Path to metadata .csv with ‘gamete_index’ & ‘gamete’ columns")
    p.add_argument("--start",    "-s", type=int, default=0,
                   help="Slice start index")
    p.add_argument("--end",      "-e", type=int, default=None,
                   help="Slice end index (default = full length)")
    p.add_argument("--outdir",   "-o", default="results",
                   help="Directory to write HTML files")
    args = p.parse_args()

    bg, hmm, mod, labels = load_data(
        args.npz, args.metadata, args.start, args.end
    )
    end_idx = args.end if args.end is not None else args.start + bg.shape[0]
    title_base = f"IMP Window {args.start}–{end_idx}"

    # heatmap
    make_heatmap(
        bg,
        labels,
        out_html=f"{args.outdir}/heatmap.html",
        title=title_base
    )
    # timeseries
    make_timeseries(
        hmm,
        mod,
        out_html=f"{args.outdir}/predictions.html",
        title=f"{title_base}: HMM vs Model"
    )


if __name__ == "__main__":
    main()
