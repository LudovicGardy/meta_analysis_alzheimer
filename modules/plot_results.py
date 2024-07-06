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

from matplotlib.markers import MarkerStyle
import matplotlib.pyplot as plt
import pandas as pd

def plot_data_summary(nb_plots, globalScores_table, weight_of_studies, randomeffect_model, nb_studies, T_squared, p_val_text, IC95text, fail_safe_N):    

    ### Plot data
    f,ax = plt.subplots(figsize=(15, 15+1))
    plt.xticks(fontsize=10+4)
    ax.axvline(0, color = "red", linestyle = "--", linewidth = 1)
    ax.set_xlim(-4,10)
    #f.suptitle("Effect sizes and Random Effet Model", fontsize=14, fontweight='bold')
    ax.set_ylabel("Studies", fontsize=14+4)
    ax.set_xlabel("Score", fontsize=14+4)
    
    sizes_dict = {"orange": 20, "black": 5}
    width_dict = {"orange": 2, "black": 0.7}
    markers_dict = {"orange": "D", "black": "o"}
    
    for i in range(0, nb_plots):
        ax.plot([globalScores_table["CI95inf"][i],globalScores_table["CI95sup"][i]],[i,i], color = "dimgrey", linewidth = width_dict[globalScores_table["Color"][i]], zorder = 1)
        ax.scatter(globalScores_table["d"][i], [i], color = "black", s = sizes_dict[globalScores_table["Color"][i]], marker = markers_dict[globalScores_table["Color"][i]], zorder = 2)
        ax.text(-3.8, i, globalScores_table["Author"][i], fontsize=10+4)
        N_subjects = int(round(globalScores_table["MCI_size"][i],0))+ int(round(globalScores_table["Control_size"][i],0))
        ax.text(4, i, "{} ({}; {})".format(N_subjects,int(round(globalScores_table["MCI_size"][i],0)), int(round(globalScores_table["Control_size"][i],0))), fontsize = 10+4)
        ax.text(6, i, "{}".format("%.2f" % round(globalScores_table["d"][i],2)), fontsize=10+4)
        ax.text(6.5, i, "({}; {})".format("%.2f" % round(globalScores_table["CI95inf"][i],2), "%.2f" % round(globalScores_table["CI95sup"][i],2)), fontsize=10+4)   

    for i in range(0, nb_plots):        
        if globalScores_table["Color"][i] == "orange":
            w = round(globalScores_table["Weight"][i],2)
            w_pcent = (round(globalScores_table["Weight"][i],2) * 100) / sum(weight_of_studies)
            ax.text(8.5, i, "{}".format("%.2f" % round(w,2)), fontsize=10+4)
            ax.text(9.1, i, "({})".format("%.2f" % round(w_pcent,2)), fontsize=10+4)

    ax.text(-3.8, (nb_plots + 2), "Authors. Date [ref]", fontweight='bold', fontsize = 10+4)
    ax.text(4, (nb_plots + 2), "N (MCI; Ctrl)", fontweight='bold', fontsize = 10+4)    
    ax.text(6, (nb_plots + 2), "Effect size (95% CI)", fontweight='bold', fontsize = 10+4)
    ax.text(8.5, (nb_plots + 2), "Weights (%)", fontweight='bold', fontsize = 10+4)
    ax.text(-3.8, -5, "Random effects model", fontweight='bold', bbox={'facecolor':'lightgray', 'alpha':0.5, 'pad':5}, fontsize = 10+4)
    ax.set_ylim(-7, nb_plots + 5)

    t = MarkerStyle(marker="d")
    t._transform = t.get_transform().rotate_deg(90)
    ax.scatter(randomeffect_model, -5, s = 400, marker = t, color = "crimson")
    print("mean effect size = {}".format(randomeffect_model))
    
    # figuresubtitle
    #ax.set_title("Nb studies = {} // Tau squared = {} // {} // {} // Fail Safe N = {}".format(nb_studies, round(T_squared,3), p_val_text, IC95text, fail_safe_N))
    print("Nb studies = {} | Tau squared = {} | {} | {} | Fail Safe N = {}".format(nb_studies, round(T_squared,3), p_val_text, IC95text, fail_safe_N))

    ax.get_yaxis().set_ticks([])
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    
    nb_plots, globalScores_table, weight_of_studies, randomeffect_model, nb_studies, T_squared, p_val_text, IC95text, fail_safe_N = 10, pd.read_csv(r"output/globalScores_table.csv"), [0.1, 0.2, 0.3, 0.4], 0.5, 4, 0.6, 0.7, 0.8, 0.9
    plot_data_summary(nb_plots, globalScores_table, weight_of_studies, randomeffect_model, nb_studies, T_squared, p_val_text, IC95text, fail_safe_N)
