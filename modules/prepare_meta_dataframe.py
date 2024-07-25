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

import os

import numpy as np
import pandas as pd

import modules.calculate_effect_size as calculate_effect_size


def calculate_meta_data(mean1, mean2, sd1, sd2, size1, size2, effect_size_method):
    CI95 = calculate_effect_size.calulate_confint_of_effect_size(
        mean1, mean2, sd1, sd2, size1, size2, effect_size_method
    )
    Weight = calculate_effect_size.calculate_weights(
        mean1, mean2, sd1, sd2, size1, size2, effect_size_method
    )
    return {
        "CI95inf": CI95[0],
        "d": CI95[1],
        "CI95sup": CI95[2],
        "Weight": Weight[1],
        "Var": Weight[0],
    }


def prepare_meta_dataframe(
    input_data, studies_with_multiple_measures, effect_size_method
):
    meta_dict = {
        "Author": [],
        "CI95inf": [],
        "d": [],
        "CI95sup": [],
        "Weight": [],
        "Var": [],
        "MCI_size": [],
        "Control_size": [],
        "MMSE_score": [],
        "Color": [],
    }

    for i in range(len(input_data["MCI_Mean"])):
        if not (
            np.isnan(input_data["MCI_Mean"][i])
            or np.isnan(input_data["Control_Mean"][i])
            or np.isnan(input_data["MCI_SD"][i])
            or np.isnan(input_data["Control_SD"][i])
            or np.isnan(input_data["MCI_size"][i])
            or np.isnan(input_data["Control_size"][i])
        ):
            effect_data = calculate_meta_data(
                input_data["MCI_Mean"][i],
                input_data["Control_Mean"][i],
                input_data["MCI_SD"][i],
                input_data["Control_SD"][i],
                input_data["MCI_size"][i],
                input_data["Control_size"][i],
                effect_size_method,
            )

            meta_dict["Author"].append(input_data["Authors"][i])
            meta_dict["CI95inf"].append(effect_data["CI95inf"])
            meta_dict["d"].append(effect_data["d"])
            meta_dict["CI95sup"].append(effect_data["CI95sup"])
            meta_dict["Weight"].append(effect_data["Weight"])
            meta_dict["Var"].append(effect_data["Var"])
            meta_dict["MCI_size"].append(input_data["MCI_size"][i])
            meta_dict["Control_size"].append(input_data["Control_size"][i])
            meta_dict["MMSE_score"].append(input_data["MMSE_score"][i])
            meta_dict["Color"].append(
                "orange"
                if input_data["Authors"][i] not in studies_with_multiple_measures
                else "black"
            )

    meta_frame = pd.DataFrame(meta_dict)

    ### Add means for multiple measures
    for study in studies_with_multiple_measures:
        indices = meta_frame.index[meta_frame["Author"] == study].tolist()
        if indices:
            meta_dict["Author"].append(study + "_mean")
            meta_dict["CI95inf"].append(meta_frame.loc[indices, "CI95inf"].mean())
            meta_dict["d"].append(meta_frame.loc[indices, "d"].mean())
            meta_dict["CI95sup"].append(meta_frame.loc[indices, "CI95sup"].mean())
            meta_dict["Weight"].append(meta_frame.loc[indices, "Weight"].mean())
            meta_dict["Var"].append(meta_frame.loc[indices, "Var"].mean())
            meta_dict["MCI_size"].append(meta_frame.loc[indices, "MCI_size"].mean())
            meta_dict["Control_size"].append(
                meta_frame.loc[indices, "Control_size"].mean()
            )
            meta_dict["MMSE_score"].append(meta_frame.loc[indices, "MMSE_score"].mean())
            meta_dict["Color"].append("orange")

    meta_frame = pd.DataFrame(meta_dict)
    meta_frame = meta_frame.sort_values(by="Weight", ascending=True).reset_index(
        drop=True
    )

    if "meta_frame.csv" not in os.listdir("output/"):
        meta_frame.to_csv("output/meta_frame.csv", index=False)

    return meta_frame
