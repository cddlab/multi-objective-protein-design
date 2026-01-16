import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scienceplots  # noqa: F401
import glob
from natsort import natsorted

plt.style.use(['science', 'nature'])


def first_front_only(values1, values2):
    assert len(values1) == len(values2) and len(values1) > 0
    n = len(values1)
    dominated = np.zeros(n, int)
    front = []

    for p in range(n):
        for q in range(n):
            if (values1[q] < values1[p] and values2[q] <= values2[p]) or \
               (values1[q] <= values1[p] and values2[q] < values2[p]):
                dominated[p] += 1
        if dominated[p] == 0:
            front.append(p)

    assert len(front) > 0
    return front


csv_files = natsorted(glob.glob('./data/*.csv'))

palette = sns.color_palette([
        "#3819e6",
        '#3cb44b',
        '#ffe119',
        "#8fc800",
        '#f58231',
        '#911eb4',
        "#72efef",
        '#f032e6',
        "#208181",
        "#edbe89",
        "#A82929",
        "#4D4D08",
        "#323297",
        "#6C736D",
        "#2F1111",
        "#bd4b1a",
        "#435cd8",
        '#9a6324',
        "#d2b720",
        "#63d7cf",
        "#da157e",
        '#6a3d9a',
        '#d2f53c',
        "#736056",
        "#ed1717",
        "#da8530",
        "#60f471",
        "#d55897",
    ]
)[:len(csv_files)]

plt.rcParams["font.size"] = 25
plt.figure(figsize=(9, 6))

for col, path in zip(palette, csv_files):
    print(f"Processing {path}")
    df = pd.read_csv(path)
    cols = {c.lower(): c for c in df.columns}
    tm, wt, seq = cols['negative_tm_score'], cols['recovery'], cols['query_sequence']
    df = df[df[wt] >= 0]
    df = df[df[tm] <= 0]
    df = df.drop_duplicates(subset=seq, keep='first')

    vals1, vals2 = df[tm].to_numpy(), df[wt].to_numpy()
    idx = first_front_only(vals1, vals2)
    pareto = np.atleast_2d(df.iloc[idx][[tm, wt]].to_numpy())
    pareto = pareto[np.argsort(pareto[:, 0])]

    base = os.path.basename(path)
    label = os.path.splitext(base)[0]
    plt.plot(
        pareto[:, 0], pareto[:, 1], 'o-', ms=4, lw=1.5,
        alpha=0.8, color=col
    )

plt.xlabel(r'$\mathrm{f}_{\text{structure}}$')
plt.ylabel(r'$\mathrm{f}_{\text{recovery}}$')
plt.tick_params(labelsize=12)
plt.tight_layout()
# plt.savefig("./plot/fig3.png", dpi=300)
plt.show()