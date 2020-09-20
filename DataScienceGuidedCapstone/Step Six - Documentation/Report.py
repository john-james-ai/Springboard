#%%
# Imports
from collections import OrderedDict
import copy
import pandas as pd
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import scale
from sklearn import __version__ as sklearn_version
from sklearn.model_selection import cross_validate
import statsmodels.api as sm
import os, sys
import warnings
warnings.filterwarnings("ignore")

# Data

#ski_data = pd.read_csv('../../DataScienceGuidedCapstone/data/ski_data_step3_features.csv')
ski_data = pd.read_csv('../DataScienceGuidedCapstone/data/ski_data_step3_features.csv')
big_mountain = ski_data[ski_data.Name == 'Big Mountain Resort']
# This isn't exactly production-grade, but a quick check for development
# These checks can save some head-scratching in development when moving from
# one python environment to another, for example
def get_model():
    model_path = '../DataScienceGuidedCapstone/models/ski_resort_pricing_model.pkl'
    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
    else:
        print("Expected model not found")
    X = ski_data.loc[ski_data.Name != "Big Mountain Resort", model.X_columns]
    y = ski_data.loc[ski_data.Name != "Big Mountain Resort", 'AdultWeekend']        
    model.fit(X,y)
    return model


def plot_compare(feat_name, description, state=None, figsize=(10, 5)):
    """Graphically compare distributions of features.
    
    Plot histogram of values for all resorts and reference line to mark
    Big Mountain's position.
    
    Arguments:
    feat_name - the feature column name in the data
    description - text description of the feature
    state - select a specific state (None for all states)
    figsize - (optional) figure size
    """
    
    plt.subplots(figsize=figsize)
    # quirk that hist sometimes objects to NaNs, sometimes doesn't
    # filtering only for finite values tidies this up
    if state is None:
        ski_x = ski_data[feat_name]
    else:
        ski_x = ski_data.loc[ski_data.state == state, feat_name]
    ski_x = ski_x[np.isfinite(ski_x)]
    plt.hist(ski_x, bins=30)
    plt.axvline(x=big_mountain[feat_name].values, c='r', ls='--', alpha=0.8, label='Big Mountain')
    plt.xlabel(description)
    plt.ylabel('frequency')
    plt.title(description + ' distribution for resorts in market share')
    plt.legend()

def get_rank(feat_name):
    ski_data_sorted = ski_data.sort_values(by=feat_name, ascending=False).reset_index()   
    return ski_data_sorted[ski_data_sorted['Name'] =="Big Mountain Resort"].index.tolist()[0]

def get_ranks():    
    features = ['AdultWeekend', 'vertical_drop', 'Snow Making_ac', 'total_chairs',
                'fastQuads','Runs','LongestRun_mi', 'trams', 'SkiableTerrain_ac']
    ranks = []
    for feature in features:
        ranks.append(get_rank(feature))

    d = {"Features": features, "Ranks": ranks}    
    df = pd.DataFrame(data=d)
    df = df.set_index('Features')
    return df.T

def predict_increase(features, deltas):
    """Increase in modelled ticket price by applying delta to feature.
    
    Arguments:
    features - list, names of the features in the ski_data dataframe to change
    deltas - list, the amounts by which to increase the values of the features
    
    Outputs:
    Amount of increase in the predicted ticket price
    """
    model = get_model()
    X_bm = ski_data.loc[ski_data.Name == "Big Mountain Resort", model.X_columns]    
    bm2 = X_bm.copy()
    for f, d in zip(features, deltas):
        bm2[f] += d
    return model.predict(bm2).item() - model.predict(X_bm).item()

def scenario_1_chart():    
    expected_visitors = 350_000
    runs_delta = [i for i in range(-1, -11, -1)]
    price_deltas = [predict_increase(['Runs'], [delta]) for delta in runs_delta]
    runs_closed = [-1 * r for r in runs_delta] #1
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    fig.subplots_adjust(wspace=0.5)
    ax[0].plot(runs_closed, price_deltas, 'o-')
    ax[0].set(xlabel='Runs closed', ylabel='Change ($)', title='Ticket price')
    revenue_deltas = [5 * expected_visitors * p for p in price_deltas] #2
    ax[1].plot(runs_closed, revenue_deltas, 'o-')
    ax[1].set(xlabel='Runs closed', ylabel='Change ($)', title='Revenue')
    return 

def regression():
    
    features = ['vertical_drop', 'Snow Making_ac',
                'fastQuads','Runs']    
    bias = []
    coef = []
    r_vals = []
    p_vals = []
    se_vals = []
    ci_low = []
    ci_hi = []
    for feature in features:
        # Remove NaN values
        nan_rows = np.isnan(ski_data[feature])
        sd = ski_data[~nan_rows]
        # Extract X, y and add bias to X
        X = np.atleast_2d(sd[feature].to_numpy()).reshape(-1,1)            
        b = np.ones(shape=(len(X),1))        
        X = np.append(b, X, axis=1)        
        y = sd['AdultWeekend']     
        # Fit the model and extract the results
        ols_result = sm.OLS(y, X).fit()        
        bias.append(ols_result.params[0])
        coef.append(ols_result.params[1])        
        r_vals.append(ols_result.rsquared)
        p_vals.append(ols_result.pvalues.x1)
        se_vals.append(ols_result.bse.x1)
        ci_low.append(ols_result.params[1]-2*ols_result.bse.x1) 
        ci_hi.append(ols_result.params[1]+2*ols_result.bse.x1)
    d1 = {'Features':features, 'Intercept': bias, 'Coef': coef, "R2":r_vals, "p-value": p_vals, "Standard Error": se_vals,
         'Lower 95% CI': ci_low, "Upper 95% CI":ci_hi}    

    df1 = pd.DataFrame(data=d1) 
    df1.sort_values(by='Coef', ascending=False, inplace=True)       
    df1 = df1.set_index("Features")

    rev = [r*350000 for r in coef]
    d2 = {'Features': features, 'Coef': coef, 
          'Lower':ci_low, 'Upper':ci_hi, 'Revenue': rev}

    df2 = pd.DataFrame(data=d2) 
    df2.sort_values(by='Coef', ascending=False, inplace=True)       
    df2 = df2.set_index("Features")    
    return df1, df2

#%%

