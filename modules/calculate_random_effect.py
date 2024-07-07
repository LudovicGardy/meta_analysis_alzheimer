from scipy.stats import norm
import numpy as np
import pandas as pd
from dataclasses import dataclass

@dataclass
class RandomEffectResults:
    Mstar: float
    T_squared: float
    data_temp: pd.DataFrame
    p_val_text: str
    p_value: float
    IC95text: str
    Y: list
    W: list
    Wstar: list

def calculate_random_effect(d, w, k, wstar=[], global_scores_table=[], init=True):
    '''
    Parameters
    ----------
    d : list
        List of effect sizes of each study.
    w : list
        List of weights of each study : 1 / (variance of effect size).
    k : int
        Number of studies.
    wstar : list, optional
        List of weights of each study : 1 / (variance of effect size).
    global_scores_table : pd.DataFrame, optional
        Table of effect sizes, weights, variances and other informations.
    init : bool, optional
        If True, the function is called for the first time. The global_scores_table is used to calculate the random effect model. 
        If False, the function is called to calculate the fail-safe N. The global_scores_table is not used.
    '''

    
    # Estimating Q
    if init:
        W = global_scores_table["Weight"]
        Y = global_scores_table["d"]
    else:
        W = w
        Y = d
        
    W = np.array(W)
    Y = np.array(Y)
        
    df = k - 1
        
    WY = W * Y

    W_squared = W ** 2
    Ysquared = Y ** 2
    W_Ysquared = W * Ysquared
        
    Q = sum(W_Ysquared) - ((sum(WY) ** 2) / sum(W))
        
    # Estimating C
    C = sum(W) - (sum(W_squared) / sum(W))
        
    # Estimating T^2
    T_squared = (Q - df) / C      
        
    # Estimating New Weights (Random weights instead of fixed)
    Wstar_list = []
        
    for i in range(0,len(global_scores_table["Var"])):
        Wstar_list.append(1 / (np.array(global_scores_table["Var"][i]) + T_squared))
        
    data_temp = global_scores_table.assign(W_star = Wstar_list)
        
    # Estimating the global effect size with random model
    if init == True:
        Wstar = data_temp["W_star"]
    else:
        Wstar = wstar
        
    Wstar = np.array(Wstar)
        
    Wstar_Y = Wstar * Y
        
    Mstar = sum(Wstar_Y) / sum(Wstar)
                
    # Estimating the p_value
    V_Mstar = 1 / sum(Wstar)
        
    SE_Mstar = np.sqrt(V_Mstar)
        
    Z = Mstar / SE_Mstar
        
    fi = norm.cdf(abs(Z)) 
        
    p_value = 2 * (1 - fi)

    # Estimating 95% CI
    IC95total_inf = round(Mstar - 1.96 * SE_Mstar, 3)
    IC95total_sup = round(Mstar + 1.96 * SE_Mstar, 3)

    if p_value > 0.001 :
        p_val_text = "p.value = {}".format(round(p_value,5))
    else:
        p_val_text = "p value < 0.001"
        
    IC95text = "95% CI = [{}; {}]".format(IC95total_inf, IC95total_sup)
        
    random_effect_results = RandomEffectResults(Mstar, T_squared, data_temp, p_val_text, p_value, IC95text, list(Y), list(W), list(Wstar))

    return random_effect_results


if __name__ == '__main__':
    d,w,k,wstar = [0.5, 0.6, 0.7, 0.8], [0.1, 0.2, 0.3, 0.4], 4, [0.1, 0.2, 0.3, 0.4]
    global_scores_table = pd.DataFrame({"Var": [0.1, 0.2, 0.3, 0.4]})
    init = False

    random_effect_results = calculate_random_effect(d,w,k,wstar,global_scores_table,init)
    print(random_effect_results)

    failure_pval = random_effect_results.p_value
    print(f"failure p.value... {failure_pval}")