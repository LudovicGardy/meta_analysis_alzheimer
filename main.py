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
import modules.prepare_meta_dataframe as prepare_meta_dataframe
import modules.meta_analysis as meta_analysis

def get_authors_with_multiple_measures(meta_data):
    authors_list = []
    for i in range(len(meta_data["Authors"])):
        authors = meta_data["Authors"][i].split(", ")
        for author in authors:
            if author not in authors_list:
                authors_list.append(author)
    return authors_list

if __name__ == '__main__':

    if "output" not in os.listdir():
        os.mkdir("output")

    input_data = pd.read_csv(open(r'input_data/input_data.csv','rb'))
    studies_with_multiple_measures = get_authors_with_multiple_measures(input_data)
    meta_frame = prepare_meta_dataframe.prepare_meta_dataframe(input_data, studies_with_multiple_measures)  # Write 1 tables in the output/ directory if not exist: meta_frame.csv
    meta_frame_summary, Fail_safe_N, global_scores_table = meta_analysis.meta_analysis(meta_frame)  # Write 1 table in the output/ directory if not exist: global_scores_table.csv
