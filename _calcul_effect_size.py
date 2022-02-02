# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 10:32:49 2018

@author: GARDY

# Note 1
#---------
# Cohen's d is the appropriate effect size measure if two groups have similar 
# standard deviations and are of similar size. Glass' delta, which uses only 
# the standard deviation of the control group, is an alternative measure if 
# each group has a different standard deviation. Hedges' g, which provides a 
# measure of effect size weighted according to the relative size of each 
# sample, is an alternative when there are different sample sizes.

# Note 2
#---------
# Please enter the sample mean (M), sample standard deviation (s) and sample 
# size (n) for each group. Two things to note: (1) if you intend to report 
# Glass's delta, then you need to enter your control group values as Group 1; 
# and (2) if you don't provide values for n, the calculator will still 
# calculate Cohen's d and Glass' delta, but it won't generate a 
# value for Hedges's g.
"""
import numpy as np
from scipy import stats
from scipy.stats import nct

def calculate_pooled_SD(sd_1, sd_2):
    SD_pooled = np.sqrt( (sd_1 ** 2 + sd_2 ** 2) / 2)
    return SD_pooled

def calculate_Cohens_d(mean_1, mean_2, sd_1, sd_2):
    SD_pooled = calculate_pooled_SD(sd_1, sd_2)
    Cohens_d = (mean_2 - mean_1) / SD_pooled
    Cohens_d = round(Cohens_d, 5)
    return(Cohens_d)

def calculate_Glass_delta(mean_1, mean_2, sd):
    SD_controlGroup = sd
    Glass_delta = (mean_2 - mean_1) / SD_controlGroup
    Glass_delta = round(Glass_delta, 5)
    return(Glass_delta)
    
def calculate_Hedges_g(mean_1, mean_2, sd_1, sd_2, size_1, size_2):
    hedge_dict_return = {}
    
    N = size_1 + size_2
    samp1 = (size_1 - 1) *  sd_1 ** 2
    samp2 = (size_2 - 1) *  sd_2 ** 2
    norm = size_1 + size_2 - 2
    SD_weighted = np.sqrt((samp1 + samp2) / norm)
    Hedges_g = (mean_2 - mean_1) / SD_weighted
    Hedges_g = round(Hedges_g, 5)
    if N < 50:
        corrected_Hg = Hedges_g * ( ((N - 3) / (N - 2.25)) * np.sqrt((N - 2) / N) )
        corrected_Hg = round(corrected_Hg, 5)
        hedge_dict_return["Corrected Hedges' g (n < 50)"] =  corrected_Hg
    else:
        hedge_dict_return["Hedges' g (n > 50)"] =  Hedges_g
        
    return(hedge_dict_return)

def calulate_confint_of_effectSize(mean_1, mean_2, sd_1, sd_2, size_1, size_2):

    d = calculate_Hedges_g(mean_1, mean_2, sd_1, sd_2,size_1,size_2)
    d = d[list(d.keys())[0]]    
    
    sigma_d = np.sqrt( ( (size_1 + size_2) / (size_1 * size_2) ) + ( d**2 / (2 * (size_1 + size_2)) ) )
    CI_inf = d - (1.96 * sigma_d)
    CI_sup = d + (1.96 * sigma_d)
    
    CI95_ofCohen = [CI_inf, d, CI_sup]
    
    return(CI95_ofCohen)
    
def calculate_weights(mean_1, mean_2, sd_1, sd_2, size_1, size_2):
    
    d = calculate_Hedges_g(mean_1, mean_2, sd_1, sd_2,size_1,size_2)
    d = d[list(d.keys())[0]]   
    
    # Get variance from sd
    var_d = ( (size_1 + size_2) / (size_1 * size_2) ) + ((d ** 2) / (2*(size_1 + size_2)))
    weight_of_the_study = 1 / var_d
    
    return(var_d, weight_of_the_study)
    
def confidence_interval(mean_1, mean_2, sd_1, sd_2, size_1, size_2):
    
    # Calculations for equal sample sizes
    #-------------------------------------
    if size_1 == size_2:
        df = size_1 - 1
        df_total = df * 2
        n = size_1
        
        tval_2tails = stats.t.ppf(1-0.025, df_total)
        tval_1tail = stats.t.ppf(1-0.05, df_total)
    
        # Get variance from sd
        var_1 = sd_1 ** 2
        var_2 = sd_2 ** 2
        
        # Calculation of the Mean Squared Error
        MSE = (var_1 + var_2) / 2
        
        # Calculation of the standard error of the difference between means
        sigma = np.sqrt( (2 * MSE) / n)
    
        mean_diff = mean_1 - mean_2
        
        # Calculation of the lower and upper limits of the 95% CI
        lower_limit = mean_diff - ( tval_2tails * sigma )
        upper_limit = mean_diff + ( tval_2tails * sigma )

    # Calculations for different sample sizes      
    #-----------------------------------------

    elif size_1 != size_2:
        df_1 = size_1 - 1
        df_2 = size_2 - 1
        df_total = df_1 + df_2
        n = size_1 + size_2

        tval_2tails = stats.t.ppf(1-0.025, df_total)
        tval_1tail = stats.t.ppf(1-0.05, df_total)
    
        # Get variance from sd
        var_1 = sd_1 ** 2
        var_2 = sd_2 ** 2
        
        # Get the some of squares from variance
        SS_1 = var_1 * df_1
        SS_2 = var_2 * df_2
        
        # Get the sum of squares error
        SSE = SS_1 + SS_2
        
        # Calculation of the Mean Squared Error
        MSE = SSE / df_total
        
        # Calculation of the harmonic mean of the saple sizes (nh)
        nh = 2 / ( 1/size_1 + 1/size_2 )
        
        # Calculation of the standard error of the difference between means
        sigma = np.sqrt( (2 * MSE) / nh)
    
        mean_diff = mean_1 - mean_2
        
        # Calculation of the lower and upper limits of the 95% CI
        lower_limit = mean_diff - ( tval_2tails * sigma )
        upper_limit = mean_diff + ( tval_2tails * sigma )
      
    print_interval = ["[lower: {}] [mean: {}] [upper: {}]".format(round(lower_limit,5), round(mean_diff,5), round(upper_limit,5)),[lower_limit, mean_diff, upper_limit]]
    
    return(print_interval)
    
if __name__ == '__main__':

    # Group 1 (Disease)
    sampleMean_1 = 4
    sampleSD_1 = 1
    sampleSize_1 = 3
    
    # Group 2 (Control)
    sampleMean_2 = 3
    sampleSD_2 = 1.414
    sampleSize_2 = 2
    
    Cohens_D = calculate_Cohens_d(sampleMean_1, sampleSD_1, sampleMean_2, sampleSD_2)
    Glass_delta = calculate_Glass_delta(sampleMean_1, sampleMean_2, sampleSD_2)
    Hedges_g = calculate_Hedges_g(sampleMean_1, sampleMean_2, sampleSD_1, sampleSD_2, sampleSize_1, sampleSize_2)
    CI95 = confidence_interval(sampleMean_1, sampleMean_2, sampleSD_1, sampleSD_2, sampleSize_1, sampleSize_2)
    
    note = "\n #----------\n # Note\n #----------\n \n If the results are > 0, the score is higher in the control's goup. \n If the results are < 0, the score is higher in the disease's group."
    print(" \n #----------\n # Results\n #----------\n \n Cohen's d = {} \n Glass's delta = {} \n {} = {} \n 95% CI = {} \n {}".format(Cohens_D, Glass_delta, list(Hedges_g.keys())[0], list(Hedges_g.values())[0], CI95, note))