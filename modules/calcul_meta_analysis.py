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

import numpy as np
import pandas as pd

import sys
sys.path.append(r"F:\GardyL\Python\Alzheimer_meta_analysis")
from modules._calcul_random_effect import randomEffect_calculation
from modules._plot_results import plot_data_summary

def calcul_meta_analysis(meta_frame):

    ### zzz
    globalScore_lines = meta_frame["Color"] == "orange"
    globalScores_table = meta_frame[globalScore_lines]
    globalScores_table.index = np.arange(0,len(globalScores_table.index))     
    nb_plots = len(globalScores_table["Author"])   

    for i in range(0, nb_plots):
        if "_mean" in globalScores_table["Author"][i]:
            globalScores_table["Author"][i] = globalScores_table["Author"][i].replace("_mean", "")
        globalScores_table["Author"][i] = globalScores_table["Author"][i]

    ### Get the individual weight of the studies (not each task but studies)
    weight_of_studies = [] # W in book
    d_of_studies = [] # Y in book
    var_of_studies = [] # Vy in  

    for i in range(0, nb_plots):
        if globalScores_table["Color"][i] == "orange":
            weight_of_studies.append(globalScores_table["Weight"][i])
            d_of_studies.append(globalScores_table["d"][i])
            var_of_studies.append(globalScores_table["Var"][i])
           
    ### Calculate the mean (global) effect size
    # count studies
    studies = pd.Series(globalScores_table["Author"], dtype = "category").cat.categories
    count_means = 0
    for i in studies:
        if "mean" in i:
            count_means += 1
    nb_studies = len(studies)

    ### Export for archives
    #globalScores_table.to_excel(r"F:\GardyL\Python\Alzheimer_meta_analysis\output\globalScores_table.xlsx", index = False)


    ### zzz
    randomeffect_model, T_squared, meta_frame, p_val_text, p_val, IC95text, Y_rec, W_rec, Wstar_rec = randomEffect_calculation(d_of_studies,weight_of_studies,nb_studies,globalScores_table =  globalScores_table)    

    ### Calcul fail safe N
    fail_safe_N = calcul_fail_safe_N(globalScores_table, Y_rec, W_rec, Wstar_rec, nb_studies)

    ### Info for plots
    plot_data_summary(nb_plots, globalScores_table, weight_of_studies, randomeffect_model, nb_studies, T_squared, p_val_text, IC95text, fail_safe_N)

    return(meta_frame, fail_safe_N)

def calcul_fail_safe_N(globalScores_table, Y_rec, W_rec, Wstar_rec, nb_studies):

    count_failure = 0
    mean_weight = np.mean(globalScores_table["Weight"])
    null_diff = 0
    nb_stud = nb_studies

    failure_pval = randomEffect_calculation(Y_rec,W_rec,nb_stud, Wstar_rec, globalScores_table, init = True)[4]
    while failure_pval < 0.05:
        Y_rec.append(null_diff)
        W_rec.append(mean_weight)     
        Wstar_rec.append(mean_weight)
        nb_stud += 1
        count_failure += 1
                
        failure_pval = randomEffect_calculation(Y_rec, W_rec, nb_stud, Wstar_rec, globalScores_table, init = False)[4]
        
        print("Count failure... ",count_failure)
        print("p.value... ",failure_pval)
        print("")
        
    fail_safe_N = count_failure    

    return(fail_safe_N)

