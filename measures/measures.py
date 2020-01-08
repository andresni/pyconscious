# -*- coding: utf-8 -*-

import numpy as np
import scipy as sp
import random
import pylab
#
#from numpy.linalg import *
#from scipy import signal
#from scipy.signal import hilbert
#from scipy.stats import ranksums
#from scipy.io import savemat
#from scipy.io import loadmat
#from random import *
#from itertools import combinations
#from pylab import *

def SCE(data, properties):
  """
  Measure ACE. Takes a 3D array input, outputs aggregate measure
  """
  std_prop = {"e_aggregate": "mean", # mean, std, median, raw
              "norm": "shuffle", # shuffle, max
              "shuffles": 1, # [integer]
              "threshold": 0.8, # [float 0 < x < 1]
              }.update(properties)
  temp = []
  
  for e in data:
    X = detrend(e)
    ro, co = np.shape(X)
    M = Psi(X, std_prop)
    ce = np.zeros(ro)
    norm = entropy(map2(np.random.randint(0, 2, (ro - 1, co))))
    for i in range(ro):
      c = map2(M[i])
      ce[i] = entropy(c)

  return mean(ce)/norm#,ce/norm

def ACE(data, properties):
  """
  Measure ACE. Takes a 3D array input, outputs aggregate measure
  """
  std_prop = {"e_aggregate": "mean", # mean, std, median, raw
              "concat": "raw", # spatial, time
              "norm": "shuffle", # shuffle, max
              "shuffles": 1, # [integer]
              "split": "median" # median, mean
              }.update(properties)
  temp = []

  for e in data:
    X = detrend(e)
    ro, co = np.shape(X)
    M = binarize(X, std_prop)
    E = entropy(map2(M))
    norm = 0
    
    if std_prop["norm"] == "shuffle":   
      for sh in range(std_prop["shuffles"]):
        for i in range(ro):
          random.shuffle(M[i])
        w = entropy(map2(M))
        norm = w if w > norm else norm
    if std_prop["max"]:
      norm = -2**len(e) * 1/2**len(e) * np.log(1/2**len(e)) / np.log(2.0)
    else:
      norm = 1
    temp.append(E / float(norm))
  return eval("np.{}(temp)".format(std_prop["e_aggregate"])) if not std_prop["e_aggregate"] == "raw" else temp
  

def LZc(data, properties):
  """
  Measure LZc. Takes a 3D array input, outputs aggregate measure
  """
  
  std_prop = {"e_aggregate": "mean", # mean, std, median, raw
              "concat": "spatial", # spatial, time
              "norm": "shuffle", # shuffle, max
              "shuffles": 1, # [integer]
              "split": "median" # median, mean
              }.update(properties)
  temp = []
  
  def compress(string):
    d={}
    w = ''
    i=1
    for c in string:
      wc = w + c
      if wc in d:
        w = wc
      else:
        d[wc]=wc
        w = c
      i+=1
    return len(d)    
  
  for e in data:
    X=detrend(e)
    SC=binarize(X, std_prop)
    norm = 0
    
    if std_prop["norm"] == "shuffle":   
      for sh in range(std_prop["shuffles"]):
        M=list(SC)
        random.shuffle(M)
        w=''
        for i in range(len(M)):
          w+=M[i]
        w = compress(w)
        norm = w if w > norm else norm
    if std_prop["max"]:
      norm = np.shape(e)[1] / np.log2(np.shape(e)[1])
    else:
      norm = 1
    temp.append(compress(SC) / float(norm))
  return eval("np.{}(temp)".format(std_prop["e_aggregate"])) if not std_prop["e_aggregate"] == "raw" else temp

# Some functions are shared between the measures.
def entropy(string):
  """
  Takes a string and calculates the entropy of it
  """
  string=list(string)
  prob = [ float(string.count(c)) / len(string) for c in dict.fromkeys(list(string)) ]
  entropy = - sum([ p * np.log(p) / np.log(2.0) for p in prob ])
  return entropy

def map2(data):
  ro,co=np.shape(data)
  c=np.zeros(co)
  for t in range(co):
    for j in range(ro):
      c[t]=c[t]+data[j,t]*(2**j)
  return c

def detrend(data):
 '''
 Detrend and normalize input data, X a multidimensional time series
 '''
 ro, co = np.shape(data)
 Z = np.zeros((ro, co))
 for i in range(ro):
   Z[i, :]=sp.signal.detrend(data[i,:] - np.mean(data[i,:]), axis = 0)
 return Z

def binarize(data, properties):
 '''
 Input: Continuous multidimensional time series
 Output: One string being the binarized input matrix concatenated column-by-column
 '''
 std_prop = {"split": "median", # median, mean
             "concat": "spatial", # spatial, time, raw
             }.update(properties)
 ro, co = np.shape(data)
 TH = np.zeros(ro)
 M = np.zeros((ro, co))
 for i in range(ro):
  M[i, :] = abs(sp.signal.hilbert(data[i, :]))
  TH[i] = np.mean(M[i, :]) if std_prop["split"] == "mean" else np.median(M[i, :])
  M[i, :] = [1 if l > TH[i] else 0 for l in M[i, :]]
 if std_prop["concat"] == "raw":
   return M
 if std_prop["concat"] == "time":
   M = np.transpose(M)
   ro, co = np.shape(data)
 s = ''
 for j in range(co):
  for i in range(ro):
   if M[i, j] > TH[i]:
    s += '1'
   else:
    s += '0'
 return s

def Psi(data, std_prop):
 '''
 Input: Multi-dimensional time series X
 Output: Binary matrices of synchrony for each series
 '''
 def diff2(p1,p2, std_prop):
   '''
   Input: two series of phases
   Output: synchrony time series thereof
   '''
   d = np.array(abs(p1 - p2))
   d2 = np.zeros(len(d))
   for i in range(len(d)):
    if d[i] > np.pi:
     d[i] = 2 * np.pi - d[i]
    if d[i] < std_prop["threshold"]:
     d2[i] = 1
  
   return d2
 
 
 X = np.angle(sp.signal.hilbert(data))
 ro, co = np.shape(X)
 M = np.zeros((ro, ro - 1, co))

 for i in range(ro):
  l = 0
  for j in range(ro):
   if i != j:
    M[i, l] = diff2(X[i], X[j], std_prop)
    l += 1

 return M

