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

import pandas as pd
import modules.reshape_dataframe as reshape_dataframe
import modules.calcul_meta_analysis as calcul_meta_analysis

def get_authors_list(meta_data):
    authors_list = []
    for i in range(len(meta_data["Authors"])):
        authors = meta_data["Authors"][i].split(", ")
        for author in authors:
            if author not in authors_list:
                authors_list.append(author)
    return authors_list

if __name__ == '__main__':
    meta_data = pd.read_csv(open(r'data/Data_meta.csv','rb'))
    meta_data.head                  

    studies_with_multiple_measures = get_authors_list(meta_data)
    meta_frame = reshape_dataframe.reshape_dataframe(meta_data, studies_with_multiple_measures)
    meta_frame_summary, Fail_safe_N = calcul_meta_analysis.calcul_meta_analysis(meta_frame)

