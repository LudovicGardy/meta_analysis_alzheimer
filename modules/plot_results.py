"""
Creation date: 2018, August
Author: L. Gardy
E-mail: ludovic.gardy@cnrs.fr
Encoding: UTF-8

Related publication
--------------------
Title: A meta-analysis of semantic memory in prodromal Alzheimer’s Disease.
Authors: Joubert S., Gardy L., Didic M., Rouleau I., Barbeau E.J.
Journal: Neuropsychology Review, 31(2): 221-232, 2021.
DOI: https://doi.org/10.1007/s11065-020-09453-5
"""

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.markers import MarkerStyle


def plot_meta_analysis(
    nb_plots: int,
    global_scores_table: pd.DataFrame,
    weight_of_studies: list,
    randomeffect_model_result: float,
    nb_studies: int,
    T_squared: float,
    p_val_text: str,
    IC95text: str,
    fail_safe_N: int,
):
    fig, ax = plt.subplots(figsize=(15, 16))
    plt.xticks(fontsize=14)
    ax.axvline(0, color="red", linestyle="--", linewidth=1)
    ax.set_xlim(-4, 10)
    ax.set_ylabel("Studies", fontsize=18)
    ax.set_xlabel("Score", fontsize=18)

    sizes_dict = {"orange": 20, "black": 5}
    width_dict = {"orange": 2, "black": 0.7}
    markers_dict = {"orange": "D", "black": "o"}

    for i in range(nb_plots):
        row = global_scores_table.iloc[i]
        ax.plot(
            [row["CI95inf"], row["CI95sup"]],
            [i, i],
            color="dimgrey",
            linewidth=width_dict[row["Color"]],
            zorder=1,
        )
        ax.scatter(
            row["d"],
            [i],
            color="black",
            s=sizes_dict[row["Color"]],
            marker=markers_dict[row["Color"]],
            zorder=2,
        )
        ax.text(-3.8, i, row["Author"], fontsize=14)
        N_subjects = int(round(row["MCI_size"], 0)) + int(round(row["Control_size"], 0))
        ax.text(
            4,
            i,
            f"{N_subjects} ({int(round(row['MCI_size'], 0))}; {int(round(row['Control_size'], 0))})",
            fontsize=14,
        )
        ax.text(6, i, f"{row['d']:.2f}", fontsize=14)
        ax.text(6.5, i, f"({row['CI95inf']:.2f}; {row['CI95sup']:.2f})", fontsize=14)

    total_weight = sum(weight_of_studies)
    for i in range(nb_plots):
        if global_scores_table["Color"][i] == "orange":
            weight = round(global_scores_table["Weight"][i], 2)
            weight_percent = (weight * 100) / total_weight
            ax.text(8.5, i, f"{weight:.2f}", fontsize=14)
            ax.text(9.1, i, f"({weight_percent:.2f})", fontsize=14)

    header_y = nb_plots + 2
    ax.text(-3.8, header_y, "Authors. Date [ref]", fontweight="bold", fontsize=14)
    ax.text(4, header_y, "N (MCI; Ctrl)", fontweight="bold", fontsize=14)
    ax.text(6, header_y, "Effect size (95% CI)", fontweight="bold", fontsize=14)
    ax.text(8.5, header_y, "Weights (%)", fontweight="bold", fontsize=14)

    ax.text(
        -3.8,
        -5,
        "Random effects model",
        fontweight="bold",
        bbox={"facecolor": "lightgray", "alpha": 0.5, "pad": 5},
        fontsize=14,
    )
    ax.set_ylim(-7, nb_plots + 5)

    t = MarkerStyle(marker="d")
    t._transform = t.get_transform().rotate_deg(90)
    ax.scatter(randomeffect_model_result, -5, s=400, marker=t, color="crimson")

    print(f"mean effect size = {randomeffect_model_result}")
    print(
        f"Nb studies = {nb_studies} | Tau squared = {round(T_squared, 3)} | {p_val_text} | {IC95text} | Fail Safe N = {fail_safe_N}"
    )

    ax.get_yaxis().set_ticks([])

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    table = pd.read_csv(r"output/global_scores_table.csv")
    nb_plots = table.shape[0]
    weight_of_studies = [0.1, 0.2, 0.3, 0.4]  # Example weights
    effect_size = 0.5
    nb_studies = 4
    T_squared = 0.6
    p_val_text = "p value < 999"
    IC95text = "95% CI = [888; 999]"
    fail_safe_N = 999
    plot_meta_analysis(
        nb_plots,
        table,
        weight_of_studies,
        effect_size,
        nb_studies,
        T_squared,
        p_val_text,
        IC95text,
        fail_safe_N,
    )
