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
import sys

sys.path.append(r"F:\GardyL\Python\Alzheimer_meta_analysis")
import reshape_dataframe
import calcul_meta_analysis

if __name__ == '__main__':
    
    authors_list = ["Joubert et al. 2010","Langlois et al. 2016", "Ahmed et al. 2008", "Joubert et al. 2008", "Gonzalez-Estévez et al. 2004", 
                    "Barbeau et al. 2012", "Leyhe et al. 2010", "Clague et al. 2011", "Gardini et al. 2015", "Benoit et al. 2017",
                    "Seidenberg et al. 2009", "Vogel et al. 2005", "Rodriguez-Ferreiro et al. 2012", "Smith JC et al. 2013", "Borg et al. 2010"]    

    meta_data = pd.read_excel(open(r'F:\GardyL\Python\Alzheimer_meta_analysis\Data_meta.xlsx','rb'))
    meta_data.head                  

    meta_frame = reshape_dataframe.reshape_dataframe(meta_data, authors_list)
    meta_frame_summary, Fail_safe_N = calcul_meta_analysis.calcul_meta_analysis(meta_frame)

