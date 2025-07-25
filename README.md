<p align="center"><img src="assets/images/doom_imp.gif" alt="imp" height="100"/></p>
<p align="center"><strong>Command-line tool to visualize imputation results from PS4G files</strong></p>


## Prerequisites

* [Pixi](https://pixi.sh/latest/)

## Setup

```bash
git clone https://github.com/btmonier/imp.git && cd imp

pixi install
```



## Usage

```bash
pixi run impstat \
  --npz <path/to/data.npz> \
  --ps4g <path/to/annotations.csv> \
  [--sep <delimiter>] \
  [--start <int>] \
  [--end <int>] \
  [--out <output_image.png>] \
  [--title "Custom Title"]
```

### Required arguments

| Argument     | Description                                                                                    |
| ------------ | ---------------------------------------------------------------------------------------------- |
| `-n, --npz`  | Path to the input `.npz` file containing arrays named `path`, `background`, and `predictions`. |
| `-p, --ps4g` | Path to the PS4G (or CSV) file with at least two columns: `gamete` and `gamete_index`.         |

### Optional arguments

| Argument    | Description                                                                                                   | Default                             |
| ----------- | ------------------------------------------------------------------------------------------------------------- | ----------------------------------- |
| `-s, --sep` | Delimiter for the PS4G/CSV file.                                                                              | `\t`                                |
| `--start`   | Starting index (inclusive) for slicing the arrays.                                                            | `0`                                 |
| `--end`     | Ending index (exclusive) for slicing the arrays.                                                              | Length of the prediction array      |
| `-o, --out` | Output image file path.                                                                                       | `output.png`                        |
| `--title`   | Custom plot title. If omitted, uses the base filename of the `.npz` plus `[start:end]`, e.g. `CML69 [0:100]`. | Derived from input filename & slice |


## Examples

1. **Basic Run** (full range, default title):

```bash
pixi run impstat \
  --npz data/HMM\_CML69.npz&#x20;
  --ps4g data/CML69.csv
```

This saves `output.png` with title `HMM_CML69 [0:N]`, where `N` is the length of predictions.

2. **Sliced Range & Custom Output**:

```bash
pixi run impstat \
  -n data/HMM_CML69_9_100.npz \
  -p data/CML69.csv \
  --start 50 --end 150 \
  -o results/slice_plot.png \
  --title "CML69 Window 50–150"
````

This loads slices the data between indices 50 and 150, computes mean accuracies, and 
generates a heatmap overlaid with prediction lines. The resulting figure—titled 
“CML69 Window 50–150”—is saved as `results/slice_plot.png`.

