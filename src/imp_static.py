#!/usr/bin/env python3

import argparse
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


def load_inputs(npz_path, ps4g_path, sep):
    data = np.load(npz_path, allow_pickle=True)
    final_predictions = data['path']
    background = data['background']
    model_predictions = data['predictions']

    df = pd.read_csv(ps4g_path, sep=sep, header=0)
    gamete = df['gamete'].values
    index = df['gamete_index'].values
    y_labels = list(gamete[index])

    return final_predictions, background, model_predictions, y_labels


def compute_accuracies(preds, background, model_preds, start, end):
    preds_slice = preds[start:end]
    bg_slice = background[start:end]
    model_slice = model_preds[start:end]

    HMM_acc = bg_slice[np.arange(preds_slice.shape[0]), preds_slice].mean()
    model_acc = bg_slice[np.arange(model_slice.shape[0]), model_slice].mean()
    return bg_slice, preds_slice, model_slice, HMM_acc, model_acc


def make_plot(bg_slice, preds_slice, model_slice, y_labels, start, end,
              HMM_acc, model_acc, title, out_path):
    bg_T = bg_slice.T

    plt.figure(figsize=(12, 8))
    sns.heatmap(
        bg_T,
        cmap=LinearSegmentedColormap.from_list("GrayWhite", ["white", "gray"]),
        cbar=False,
        xticklabels=False,
        yticklabels=y_labels
    )

    plt.plot(
        range(len(preds_slice)),
        preds_slice + 0.5,
        color="red",
        label=f"HMM predictions: {HMM_acc*100:.2f}%",
        linewidth=2
    )
    plt.plot(
        range(len(model_slice)),
        model_slice + 0.5,
        color="blue",
        label=f"Model predictions: {model_acc*100:.2f}%",
        linewidth=2
    )

    plt.legend(loc="upper right", fontsize=12)
    plt.title(title, fontsize=16)
    plt.xlabel("Label")
    plt.ylabel("Feature Index")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    print(f"Saved plot to {out_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Plot HMM vs model predictions over a background heatmap."
    )
    parser.add_argument("-n", "--npz",    required=True,
                        help="Input .npz file")
    parser.add_argument("-p", "--ps4g",   required=True,
                        help="Input PS4G/CSV file")
    parser.add_argument("-s", "--sep",    default="\t",
                        help="Field delimiter for PS4G file (default: tab)")
    parser.add_argument("-o", "--out",    default="output.png",
                        help="Output image path")
    parser.add_argument("--start", type=int, default=0,
                        help="Start index for slicing (inclusive, default: 0)")
    parser.add_argument("--end",   type=int, default=None,
                        help="End index for slicing (exclusive, default: array length)")
    parser.add_argument("--title", default=None,
                        help="Plot title (defaults to '<filename> [start:end]')")
    args = parser.parse_args()

    preds, bg, model_preds, y_labels = load_inputs(
        args.npz, args.ps4g, args.sep)
    end_idx = args.end if args.end is not None else preds.shape[0]
    end_idx = min(end_idx, preds.shape[0])

    bg_slice, p_slice, m_slice, HMM_acc, model_acc = compute_accuracies(
        preds, bg, model_preds, args.start, end_idx
    )

    if args.title:
        title = args.title
    else:
        base = os.path.splitext(os.path.basename(args.npz))[0]
        title = f"{base} [{args.start}:{end_idx}]"

    make_plot(
        bg_slice, p_slice, m_slice, y_labels,
        args.start, end_idx, HMM_acc, model_acc,
        title, args.out
    )


if __name__ == "__main__":
    main()
