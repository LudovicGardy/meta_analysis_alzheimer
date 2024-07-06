from scipy.stats import norm
import numpy as np

def randomEffect_calculation(d,w,k,wstar = [], globalScores_table = [], init = True):
    # Estimating Q
    if init == True:
        W = globalScores_table["Weight"]
        Y = globalScores_table["d"]
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
        
    for i in range(0,len(globalScores_table["Var"])):
        Wstar_list.append(1 / (np.array(globalScores_table["Var"][i]) + T_squared))
        
    data_temp = globalScores_table.assign(W_star = Wstar_list)
        
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

    p_val_text = p_value
    if p_value > 0.001 :
        p_val_text = "p.value = {}".format(round(p_value,5))
    else:
        p_val_text = "p value < 0.001"
        
    IC95text = "95% CI = [{}; {}]".format(IC95total_inf, IC95total_sup)
        
    return(Mstar, T_squared,data_temp, p_val_text, p_value, IC95text, list(Y), list(W), list(Wstar))