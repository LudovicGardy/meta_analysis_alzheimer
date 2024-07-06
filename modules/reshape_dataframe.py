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
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import modules.calcul_effect_size as calcul_effect_size

### New data frame for plots
def shorter_dataframe(meta_data):

    nb_plots = len(meta_data["MCI_Mean"])

    meta_dict = {"Author": [],"CI95inf": [], "d": [], "CI95sup": [], "Weight" : [], 
                    "Var" : [], "MCI_size" : [], "Control_size" : [], "MMSE_score" : [], 
                    "Task_difficulty" : [], "NamingVsSemantic" : []}
        
    for i in range(0,nb_plots):
        if not np.isnan(meta_data["MCI_Mean"][i]) and not np.isnan(meta_data["Control_Mean"][i]) and not np.isnan(meta_data["MCI_SD"][i]) and not np.isnan(meta_data["Control_SD"][i]) and not np.isnan(meta_data["MCI_size"][i]) and not np.isnan(meta_data["Control_size"][i]):
            if meta_data["Way"][i] == 1:
                CI95 = calcul_effect_size.calulate_confint_of_effectSize(meta_data["MCI_Mean"][i], meta_data["Control_Mean"][i], meta_data["MCI_SD"][i], meta_data["Control_SD"][i], meta_data["MCI_size"][i], meta_data["Control_size"][i])
                Weight = calcul_effect_size.calculate_weights(meta_data["MCI_Mean"][i], meta_data["Control_Mean"][i], meta_data["MCI_SD"][i], meta_data["Control_SD"][i], meta_data["MCI_size"][i], meta_data["Control_size"][i])
                meta_dict["Author"].append(meta_data["Authors"][i])
                meta_dict["CI95inf"].append(CI95[0])
                meta_dict["d"].append(CI95[1])
                meta_dict["CI95sup"].append(CI95[2])   
                meta_dict["Weight"].append(Weight[1])
                meta_dict["Var"].append(Weight[0])
                meta_dict["MCI_size"].append(meta_data["MCI_size"][i])
                meta_dict["Control_size"].append(meta_data["Control_size"][i])
                meta_dict["MMSE_score"].append(meta_data["MMSE_score"][i])
                meta_dict["Task_difficulty"].append(meta_data["Task_difficulty"][i])
                meta_dict["NamingVsSemantic"].append(meta_data["NamingVsSemantic"][i])
            elif meta_data["Way"][i] == 2:
                CI95 = calcul_effect_size.calulate_confint_of_effectSize(meta_data["Control_Mean"][i], meta_data["MCI_Mean"][i], meta_data["Control_SD"][i], meta_data["MCI_SD"][i], meta_data["Control_size"][i], meta_data["MCI_size"][i])
                Weight = calcul_effect_size.calculate_weights(meta_data["Control_Mean"][i], meta_data["MCI_Mean"][i], meta_data["Control_SD"][i], meta_data["MCI_SD"][i], meta_data["Control_size"][i], meta_data["MCI_size"][i])
                meta_dict["Author"].append(meta_data["Authors"][i])
                meta_dict["CI95inf"].append(CI95[0])
                meta_dict["d"].append(CI95[1])
                meta_dict["CI95sup"].append(CI95[2])
                meta_dict["Weight"].append(Weight[1])
                meta_dict["Var"].append(Weight[0])
                meta_dict["MCI_size"].append(meta_data["MCI_size"][i])
                meta_dict["Control_size"].append(meta_data["Control_size"][i])
                meta_dict["MMSE_score"].append(meta_data["MMSE_score"][i])
                meta_dict["Task_difficulty"].append(meta_data["Task_difficulty"][i])
                meta_dict["NamingVsSemantic"].append(meta_data["NamingVsSemantic"][i])

    meta_frame_temp = pd.DataFrame(meta_dict)

    if "meta_frame_temp.csv" not in os.listdir("output/"):
        meta_frame_temp.to_csv("output/meta_frame_temp.csv", index=False)
        
    return meta_dict, meta_frame_temp

def reshape_dataframe(meta_data, studies_with_multiple_measures):
    '''
    This function reshapes the dataframe to be used in the meta-analysis. Some authors have multiple measures, so we calculate the mean of these measures.
    '''
        
    meta_dict, meta_frame_temp = shorter_dataframe(meta_data)
   
    ### Add means for multiple measures   
    for i in studies_with_multiple_measures:
        meta_dict["Author"].append(i + "_mean")
        meta_dict["CI95inf"].append(np.mean(meta_frame_temp["CI95inf"][meta_frame_temp["Author"] == i]))
        meta_dict["d"].append(np.mean(meta_frame_temp["d"][meta_frame_temp["Author"] == i]))
        meta_dict["CI95sup"].append(np.mean(meta_frame_temp["CI95sup"][meta_frame_temp["Author"] == i]))
        meta_dict["Weight"].append(np.mean(meta_frame_temp["Weight"][meta_frame_temp["Author"] == i]))
        meta_dict["Var"].append(np.mean(meta_frame_temp["Var"][meta_frame_temp["Author"] == i]))
        meta_dict["MCI_size"].append(np.mean(meta_frame_temp["MCI_size"][meta_frame_temp["Author"] == i]))
        meta_dict["Control_size"].append(np.mean(meta_frame_temp["Control_size"][meta_frame_temp["Author"] == i]))
        meta_dict["MMSE_score"].append(np.mean(meta_frame_temp["MMSE_score"][meta_frame_temp["Author"] == i]))
        meta_dict["Task_difficulty"].append("NaN")
        meta_dict["NamingVsSemantic"].append("NaN")
        
    meta_frame = pd.DataFrame(meta_dict)    
    meta_frame = meta_frame.drop(["Task_difficulty", "NamingVsSemantic"], axis = 1)
    meta_frame = meta_frame.sort_values(by = 'Weight', ascending = True)
    meta_frame.index = range(0,len(meta_frame["Author"]))    

    ### Add a color column  
    meta_frame = meta_frame.assign(Color = np.repeat("Nan", len(meta_frame["Author"])))
    
    for count, auth in enumerate(meta_frame["Author"]):
        if auth in studies_with_multiple_measures and "mean" not in auth:
            meta_frame.loc[count, "Color"] = "black"
        else:
            meta_frame.loc[count, "Color"] = "orange"

    if "meta_frame.csv" not in os.listdir("output/"):
        meta_frame.to_csv("output/meta_frame.csv", index=False)

    return(meta_frame)