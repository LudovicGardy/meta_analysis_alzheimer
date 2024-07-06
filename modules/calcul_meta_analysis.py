'''
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
'''

import os
import numpy as np
import pandas as pd
from modules.calcul_random_effect import randomEffect_calculation
from modules.plot_results import plot_data_summary

def export_global_scores(globalScores_table, output_path):
    globalScores_table.to_csv(output_path, index=False)

def calcul_meta_analysis(meta_frame):
    # Filter the global scores
    globalScore_lines = meta_frame["Color"] == "orange"
    globalScores_table = meta_frame[globalScore_lines].copy()
    globalScores_table.index = np.arange(0, len(globalScores_table.index))
    nb_plots = len(globalScores_table["Author"])

    for i in range(nb_plots):
        if "_mean" in globalScores_table.loc[i, "Author"]:
            globalScores_table.loc[i, "Author"] = globalScores_table.loc[i, "Author"].replace("_mean", "")
        globalScores_table.loc[i, "Author"] = globalScores_table.loc[i, "Author"]

    # Get the weight, d and var of each study
    weight_of_studies = []  # W dans le livre
    d_of_studies = []  # Y dans le livre
    var_of_studies = []  # Vy dans le livre

    for i in range(nb_plots):
        if globalScores_table.loc[i, "Color"] == "orange":
            weight_of_studies.append(globalScores_table.loc[i, "Weight"])
            d_of_studies.append(globalScores_table.loc[i, "d"])
            var_of_studies.append(globalScores_table.loc[i, "Var"])

    # Calculate the average effect size (global)
    studies = pd.Series(globalScores_table["Author"], dtype="category").cat.categories
    nb_studies = len(studies)

    # Calculate the random effect model
    randomeffect_model, T_squared, meta_frame, p_val_text, p_val, IC95text, Y_rec, W_rec, Wstar_rec = randomEffect_calculation(
        d_of_studies, weight_of_studies, nb_studies, globalScores_table=globalScores_table
    )

    # Calculate the fail-safe N
    fail_safe_N = calcul_fail_safe_N(globalScores_table, Y_rec, W_rec, Wstar_rec, nb_studies)

    # Comments on the plots
    plot_data_summary(nb_plots, globalScores_table, weight_of_studies, randomeffect_model, nb_studies, T_squared, p_val_text, IC95text, fail_safe_N)

    if "globalScores_table.csv" not in os.listdir("output/"):
        export_global_scores(globalScores_table, r"output/globalScores_table.csv")

    return meta_frame, fail_safe_N, globalScores_table

def calcul_fail_safe_N(globalScores_table, Y_rec, W_rec, Wstar_rec, nb_studies):
    count_failure = 0
    mean_weight = np.mean(globalScores_table["Weight"])
    null_diff = 0
    nb_stud = nb_studies

    failure_pval = randomEffect_calculation(Y_rec, W_rec, nb_stud, Wstar_rec, globalScores_table, init=True)[4]
    while failure_pval < 0.05:
        Y_rec.append(null_diff)
        W_rec.append(mean_weight)
        Wstar_rec.append(mean_weight)
        nb_stud += 1
        count_failure += 1

        failure_pval = randomEffect_calculation(Y_rec, W_rec, nb_stud, Wstar_rec, globalScores_table, init=False)[4]

        print("Count failure... ", count_failure)
        print("p.value... ", failure_pval)
        print("")

    fail_safe_N = count_failure

    return fail_safe_N

# Test
if __name__ == '__main__':
    meta_frame = pd.read_csv(r"output/meta_frame.csv")
    meta_frame, fail_safe_N, globalScores_table = calcul_meta_analysis(meta_frame)
    print(fail_safe_N)
    print(meta_frame)
    print("End of the script")
