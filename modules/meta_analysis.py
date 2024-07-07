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
from modules.calculate_random_effect import calculate_random_effect
from modules.plot_results import plot_meta_analysis

def export_global_scores(global_scores_table, output_path):
    global_scores_table.to_csv(output_path, index=False)

def meta_analysis(meta_frame):
    '''
    This function calculates the meta-analysis of the global scores. It filters the global scores, calculates 
    the average effect size, the fail-safe N, and the comments on the plots.
    '''

    # Filter the global scores
    globalScore_lines = meta_frame["Color"] == "orange"
    global_scores_table = meta_frame[globalScore_lines].copy()
    global_scores_table.index = np.arange(0, len(global_scores_table.index))
    nb_plots = len(global_scores_table["Author"])

    for i in range(nb_plots):
        if "_mean" in global_scores_table.loc[i, "Author"]:
            global_scores_table.loc[i, "Author"] = global_scores_table.loc[i, "Author"].replace("_mean", "")
        global_scores_table.loc[i, "Author"] = global_scores_table.loc[i, "Author"]

    # Get the weight, d and var of each study
    weight_of_studies = []  # W in Borenstein's book
    d_of_studies = []  # Y in Borenstein's book
    var_of_studies = []  # Vy in Borenstein's book

    for i in range(nb_plots):
        if global_scores_table.loc[i, "Color"] == "orange":
            weight_of_studies.append(global_scores_table.loc[i, "Weight"])
            d_of_studies.append(global_scores_table.loc[i, "d"])
            var_of_studies.append(global_scores_table.loc[i, "Var"])

    # Calculate the average effect size (global)
    studies = pd.Series(global_scores_table["Author"], dtype="category").cat.categories
    nb_studies = len(studies)
    
    random_effect_results = calculate_random_effect(np.array(d_of_studies), np.array(weight_of_studies), np.array(var_of_studies), nb_studies)
    fail_safe_N = calculate_fail_safe_N(d_of_studies, weight_of_studies, var_of_studies, nb_studies, global_scores_table)
    
    # Comments on the plots
    plot_meta_analysis(nb_plots, global_scores_table, weight_of_studies, random_effect_results.Mstar, nb_studies, random_effect_results.T_squared, random_effect_results.p_val_text, random_effect_results.IC95text, fail_safe_N)

    if "global_scores_table.csv" not in os.listdir("output/"):
        export_global_scores(global_scores_table, r"output/global_scores_table.csv")

    return meta_frame, fail_safe_N, global_scores_table

def calculate_fail_safe_N(d_of_studies, weight_of_studies, var_of_studies, nb_studies, global_scores_table):
    '''
    The fail safe N is the number of studies with null effect size that would be needed to make the p-value of 
    the random effect model greater than 0.05. It is a measure of the robustness of the meta-analysis. In other 
    words, it represents the number of studies that would be needed to make the meta-analysis not significant.
    '''

    # Initial p-value
    random_effect_results = calculate_random_effect(np.array(d_of_studies), np.array(weight_of_studies), np.array(var_of_studies), nb_studies)
    Wstar = random_effect_results.Wstar
    failure_pval = random_effect_results.p_value

    count_failure = 0
    # Add studies with null effect size until the p-value is greater than 0.05
    while failure_pval < 0.05:  
        null_diff = 0
        mean_weight = np.mean(global_scores_table["Weight"])  # simulating the weight of the new 'null study' using the mean weight of real studies
        
        d_of_studies.append(null_diff)
        weight_of_studies.append(mean_weight)
        Wstar.append(mean_weight)
        nb_studies += 1
        count_failure += 1

        random_effect_results = calculate_random_effect(np.array(d_of_studies), np.array(weight_of_studies), np.array(var_of_studies), nb_studies, Wstar)
        failure_pval = random_effect_results.p_value

        print("Count failure... ", count_failure)
        print("p.value... ", failure_pval)
        print("")

    fail_safe_N = count_failure

    return fail_safe_N

if __name__ == '__main__':
    meta_frame = pd.read_csv(r"output/meta_frame.csv")
    meta_frame, fail_safe_N, global_scores_table = meta_analysis(meta_frame)
    print(fail_safe_N)
    print(meta_frame)
    print("End of the script")
