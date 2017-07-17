
#essentials
import csv
import pandas as pd
import numpy as np
import string
import sklearn
from sklearn.pipeline import Pipeline
import time
import tensorflow as tf
import pickle
from sklearn.externals import joblib 

from sklearn.neural_network import MLPClassifier
from patsy import dmatrices
from sklearn import metrics
import random
import logging
from tqdm import tqdm
from functools import reduce
from operator import add

#preprocessing
from sklearn.preprocessing import MinMaxScaler,OneHotEncoder, normalize,LabelEncoder, FunctionTransformer, scale,StandardScaler
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn import metrics
from patsy import dmatrices
from sklearn.feature_selection import RFECV,SelectKBest, f_classif,f_regression,mutual_info_regression, RFE, chi2
from sklearn.decomposition import PCA
import scipy.stats as stats

data = pd.read_csv('lendingclubraw.csv', sep =',')
data.head(5)

#target variable
overallgoal = 2 # classification
encoder = LabelEncoder()
columnnames = list(data)
coldict = {}
colcount = 1
for i in columnnames:
    coldict[i] = colcount
    colcount += 1
coldict_sort = sorted(coldict.items(), key=lambda x:x[1])
print coldict_sort
targetvar = 9 # target variable - column number
targetvar2 = coldict.keys()[coldict.values().index(targetvar)]
print targetvar2

#check missing values in each column
data.isnull().sum()/len(data)*100

#discard unnecessary features
def discard_vars(data):
    discardyesno = raw_input('Do you want to discard any variables? y/n: ').lower()
    if discardyesno == 'y':
        columnnames = list(data)
        coldict = {}
        colcount = 1
        discardcol = []
        for i in columnnames:
            coldict[i] = colcount
            colcount += 1
        coldict_sort = sorted(coldict.items(), key=lambda x:x[1])
        for j,k in coldict_sort:
            print k, j
        discard = raw_input('Input numbers of variables to discard: -separate with comma- ')
        discard = discard.split(',')
        for i in discard:
            i = int(i)-1
            discardcol.append(data.iloc[:,i].name)
        data = data.drop(discardcol, axis = 1)
        print 'Done'
    return data

data = discard_vars(data) # y;  1,2,10,11,16,19,22,23,46,48,49

def settings(data):
    binary = 0
    regression = 0
    if len(data.ix[:,targetvar2].unique()) == 2:
        binary = 1
    else:
        type_target = data.ix[:,targetvar2].dtype
        if type_target == 'float64':
            regression = 1
    settings = {'goal':overallgoal, 'binary': binary, 'regression': regression}
    print "settings saved..."
    return settings

settings = settings(data)

# Check Missing Values - col wise, then row-wise
def remove_inc_variables(data, pct):
    col_to_keep = []
    print "Total Vars Start:", len(data.columns)
    for i in range(len(data.columns)):
        if (float(data.iloc[:,i].isnull().sum().tolist()) / float(len(data.index))) > pct:
            print str(data.iloc[:,i].name) + " Removing | NAs: " + str(round(float(data.iloc[:,i].isnull().sum().tolist()) / float(len(data.index)),2))
        else:
            print str(i+1), str(data.iloc[:,i].name) + " OK to keep"+ " | NAs: " + str(round(float(data.iloc[:,i].isnull().sum().tolist()) / float(len(data.index)),2))
            col_to_keep.append(i)
    data_nona = data.iloc[:,col_to_keep]
    print "Total Vars End:", len(data_nona.columns)
    return data_nona

# select whether to delete, interpolation to handle rows with NAs
def na_handling(data, arg):
    if arg == 1:
        data_nona = data.dropna()
        if (len(data_nona.index) == len(data.index)):
            print 'no NAs'
        else:
            print 'remaining decreased to ' + str(len(data_nona.index)) + ' from ' + str(len(data.index))
    elif arg == 2:
        data_nona = data.interpolate()
        # if time series, method='quadratic'
        # if values approximating a cumulative distribution function, method = 'pchip'
        # if goal of smooth plotting, method='akima'
        data_nona = data_nona.dropna() #drop all rows that were not imputed
        print 'remaining decreased to ' + str(len(data_nona.index)) + ' from ' + str(len(data.index))
    else:
        print 'arg = 1 or 2'
        print 'call function again'
    return data_nona

data_nona = remove_inc_variables(data,.1)
data_nona = na_handling(data_nona,1)


def is_categorical(array_like):
    return array_like.dtype.name == 'category'

def is_object(array_like):
    return array_like.dtype.name == 'object'

#separate numerics and non numerics
def sep_types(data_nona):
    #index_init = range(0,len(data_nona.columns))
    data_numeric = pd.DataFrame()
    data_object = pd.DataFrame()
    for i in range(0,len(data_nona.columns)):
        if is_categorical(data_nona.iloc[:,i]) == True:
            data_object[data_nona.iloc[:,i].name] = data_nona.iloc[:,i]
        elif is_object(data_nona.iloc[:,i]) == True:
            data_object[data_nona.iloc[:,i].name] = data_nona.iloc[:,i]
        else:
            data_numeric[data_nona.iloc[:,i].name] = data_nona.iloc[:,i]
    return data_object, data_numeric

#move categories into the allobjects dataframe
def move_cat(data_numeric, data_allobjects):
    dropcols = []
    for i in range(0, len(data_numeric.columns)):
        #print data_numeric.iloc[:,i].dtype
        if len(data_numeric.iloc[:,i].unique()) == 2:
            print data_numeric.iloc[:,i].dtype
            if data_numeric.ix[:,i].unique()[0] == 0:
                if data_numeric.ix[:,i].unique()[1] == 1:
                    print data_numeric.ix[:,i].name, data_numeric.ix[:,i].dtype
                    #data_numeric.ix[:,i] = data_numeric.ix[:,i].astype('category')
                    print data_numeric.ix[:,i].name,data_numeric.ix[:,i].dtype
                    data_allobjects[data_numeric.ix[:,i].name] = data_numeric.ix[:,i]
                    dropcols.append(data_numeric.ix[:,i].name)

    data_numeric = data_numeric.drop(dropcols, axis = 1)
    return data_numeric, data_allobjects


def num_handle(data_numeric):
    for i in range(0, len(data_numeric.columns)):
        #print column name and normal test value
        p = stats.normaltest(data_numeric.iloc[:,i]) #tests normality of column
        col_name = data_numeric.columns[i]
        print col_name,p[1]
        if p[1] < 0.055:
            print "Not a normal distribution: " + str(data_numeric.iloc[:,i].name)
            column_data = data_numeric.iloc[:,i].reshape(-1,1)
            #log transformations
            log_transformer = FunctionTransformer(np.log10)
            log_col = log_transformer.fit_transform(column_data)
            #ln transformations
            ln_transformer = FunctionTransformer(np.log)
            ln_col = ln_transformer.fit_transform(column_data)
            #sqrt tranformation
            sqrt_transformer = FunctionTransformer(np.sqrt)
            sqrt_col = sqrt_transformer.fit_transform(column_data)
            print "Transform complete: ",str(data_numeric.iloc[:,i].name)
            
                        #compare transformations
            plog = stats.skew(log_col, bias = False)
            pln = stats.skew(ln_col, bias = False)
            psqrt = stats.skew(sqrt_col, bias = False)

            transform_dict = {'plog':abs(plog), 'pln':abs(pln),'psqrt':abs(psqrt)}
            trans_min = min(transform_dict, key=transform_dict.get)
            
            file_name = col_name+'.pkl'
            print file_name
            if trans_min == 'plog':
                joblib.dump(log_transformer, file_name) 
                data_numeric.iloc[:,i] = log_transformer.transform(column_data)
                
            elif trans_min == 'pln':
                joblib.dump(ln_transformer, file_name) 
                data_numeric.iloc[:,i] = ln_transformer.transform(column_data)
            elif trans_min == 'psqrt':
                joblib.dump(sqrt_transformer, file_name) 
                data_numeric.iloc[:,i] = sqrt_transformer.transform(column_data)
            else:
                pass
            print "Best transform: " + str(trans_min)
    return data_numeric


def cat_handle(data_allobjects):
    dummifycol = []
    dropifycol = []
    data_unused = pd.DataFrame()
    print data_allobjects.head(5)
    columnnames = list(data_allobjects)
    coldict = {}
    colcount = 1
    
    for i in columnnames:
        coldict[i] = colcount
        colcount += 1
    coldict_sort = sorted(coldict.items(), key=lambda x:x[1])
    print coldict_sort
    
    dropify = raw_input('Input numbers of variables to drop: -separate with comma- na if none ')
    if dropify == 'na':
        pass
    else:
        dropify = dropify.split(',')
        
    dummify = raw_input('Input numbers of variables to dummify: -separate with comma- ')
    dummify = dummify.split(',')
    
    print "Start creating dummy variables"
    for i in dummify:
        i = int(i)-1
        dummifycol.append(data_allobjects.iloc[:,i].name)
    #df = data_allobjects[dummifycol].copy()
    for i in dummifycol:
        filename = i+'.npy'
        le = LabelEncoder() #object
        data_allobjects[i] = le.fit_transform(data_allobjects[i]) 
        np.save(filename,le.classes_)# if multiple columns in table
    

        
    print "Start droppping variables"
    if dropify == 'na':
        pass
    else:
        for i in dropify:
            i = int(i)-1
            dropifycol.append(data_allobjects.iloc[:,i].name)
            data_unused[data_allobjects.iloc[:,i].name] = data_allobjects.iloc[:,i]
    for i in dummifycol:
        print i
        data_allobjects = pd.get_dummies(data_allobjects, prefix = str(i), columns = [i])
        #need to remove one dummy column to accommodate for all 0s
        # get list of all dummy vars from i   
        dummy_i = [col for col in data_allobjects.columns if i in col]
        #drop the 1st of the list
        data_allobjects = data_allobjects.drop(dummy_i[0], axis = 1)
    print "Dummified"
        
    data_allobjects = data_allobjects.drop(dropifycol, axis = 1)
    
    print "Dropified"
    return data_allobjects,data_unused


data_nona2 = data_nona #refresh variable
data_object, data_numeric = sep_types(data_nona2) ###
data_allobjects = data_object #contains all the non-numerics
data_numeric, data_allobjects = move_cat(data_numeric, data_allobjects) ###
data_numeric = num_handle(data_numeric) ###

data_allobjects, data_unused = cat_handle(data_allobjects) #9; 1,3,4,5,6,7,8,10,11
#not dummifying the target variable

data_allobjects.head(5)

data_combine = pd.concat([data_allobjects,data_numeric], axis = 1)
allcols = list(data_combine)
targetcols = []
for i in allcols:
    if i.startswith(targetvar2):
        targetcols.append(i)

finalcols = list(data_combine.columns.values)
for i in targetcols:
    finalcols.pop(finalcols.index(i))

#column header cleaning and arrangement
data_combine = data_combine[finalcols+targetcols]
data_combine.columns = data_combine.columns.str.replace(" ", "_")
data_combine.columns = data_combine.columns.str.replace("(", "_")
data_combine.columns = data_combine.columns.str.replace(")", "_")
data_combine.columns = data_combine.columns.str.replace("__", "_")
data_combine.columns = data_combine.columns.str.replace("-", "_")

data_combine.head(5)

########## genetic algorithm

#creating the formula for the algorithm
allcols = list(data_combine)
dontinclude = ['grade']

finalfeatures = []
for i in allcols:
    if i in dontinclude:
        pass
    else:
        finalfeatures.append(i)
form = '+'.join(finalfeatures)
form = 'grade'+'~'+form
form

data_combine['grade'].unique()

#encode the target variable into labels 
le = sklearn.preprocessing.LabelEncoder()
le.fit(data_combine['grade'].unique())
list(le.classes_)
data_combine['grade'] = le.transform(data_combine['grade'])

data_combine.head(5)

#split data
y,x = dmatrices(form, data_combine, return_type = 'dataframe')
y = np.ravel(y)
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x,y,test_size = 0.3, random_state = 0)
