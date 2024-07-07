from scipy.stats import norm
import numpy as np
import pandas as pd
from dataclasses import dataclass
from numpy.typing import NDArray
from typing import List

@dataclass
class RandomEffectResults:
    Mstar: float
    T_squared: float
    p_val_text: str
    p_value: float
    IC95text: str
    Wstar: list

def calculate_random_effect(Y:NDArray, W:NDArray, var:NDArray, k:int, wstar:List=[]):
    '''
    Parameters
    ----------
    d : NDArray
        List of effect sizes of each study included in the meta analysis.
    w : NDArray
        List of weights of each study included in the meta analysis: 1 / (variance of effect size).
    var : NDArray
        List of variance of effect sizes of each study included in the meta analysis.
    k : int
        Number of studies.
    wstar : list, optional
        List of weights of each study : 1 / (variance of effect size).
    '''
                
    freedom_degrees = k - 1
        
    WY = W * Y

    W_squared = W ** 2
    Ysquared = Y ** 2
    W_Ysquared = W * Ysquared
        
    Q = sum(W_Ysquared) - ((sum(WY) ** 2) / sum(W))
        
    # Estimating C
    C = sum(W) - (sum(W_squared) / sum(W))
        
    # Estimating T^2
    T_squared = (Q - freedom_degrees) / C      
        
    # Estimating New Weights (Random weights instead of fixed)
    if len(wstar) == 0:
        Wstar_list = list(wstar)
        for i in range(0,len(var)):
            Wstar_list.append(1 / (np.array(var[i]) + T_squared))
        Wstar = np.array(Wstar_list)
    else:
        Wstar = np.array(wstar)
                    
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
        
    random_effect_results = RandomEffectResults(Mstar, T_squared, p_val_text, p_value, IC95text, list(Wstar))

    return random_effect_results


if __name__ == '__main__':
    d,w,var,k = [0.1, 0.2, 0.3, 0.4], [1, 2, 3, 4], [10, 20, 30, 40], 4

    random_effect_results = calculate_random_effect(np.array(d),np.array(w),np.array(var),k)
    print(random_effect_results)

    failure_pval = random_effect_results.p_value
    print(f"failure p.value... {failure_pval}")