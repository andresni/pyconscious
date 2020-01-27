# -*- coding: utf-8 -*-

import numpy as np
import scipy as sp
import sys

# Used by LZc
def compress(string):
  """
  Takes a string of length n and calculates its theoretical compressability
  according to Lempel Ziv compression (1976).
  """
  d = {}
  w = ''
  i = 1
  for c in string:
    wc = w + c
    if wc in d:
      w = wc
    else:
      d[wc] = wc
      w = c
    i += 1
  return len(d)


def entropy(string):
  """
  Takes a string and calculates the Shannon entropy of it
  """
  string=list(string)
  prob = [ float(string.count(c)) / len(string) for c in dict.fromkeys(list(string)) ]
  entropy = - sum([ p * np.log(p) / np.log(2.0) for p in prob ])
  return entropy

def map2(data):
  ro, co = np.shape(data)
  c = np.zeros(co)
  for t in range(co):
    for j in range(ro):
      c[t] = c[t] + data[j, t] * (2**j)
  return c


def detrend(data):
 """
 Detrend and normalize input data, X a multidimensional time series
 """
 ro, co = np.shape(data)
 Z = np.zeros((ro, co))
 for i in range(ro):
   Z[i, :] = sp.signal.detrend(data[i,:] - np.mean(data[i,:]), axis = 0)
 return Z


def binarize(data, threshold):
 """
 Takes a 2D array of continous data and binarizes it according to threshold, for each channel.
 """
 X = detrend(data)
 ro, co = np.shape(X)
 TH = np.zeros(ro)
 M = np.zeros((ro, co))
 for i in range(ro):
  M[i, :] = abs(sp.signal.hilbert(X[i, :]))
  TH[i] = eval("np.{}(M[i, :])".format(threshold))
  M[i, :] = [1 if l > TH[i] else 0 for l in M[i, :]]
 M = M.astype(int)
 return M


def concatenate(data, concat):
 """
 Takes a 2D array and concatenates it into a string along dimension.
 """
 ro, co = np.shape(data)
 s = ''
 if concat == "time":
   for j in range(ro):
     for i in range(co):
         s += str(data[j, i])
 elif concat == "space":
   for j in range(co):
     for i in range(ro):
      s += str(data[i, j])
 else:
   sys.exit("{} is not a valid argument for 'concat'".format(concat))
 return s


def Psi(data, t):
   '''
   Input: Multi-dimensional time series X
   Output: Binary matrices of synchrony for each series
   '''
   X = detrend(data)
   X = np.angle(sp.signal.hilbert(X))
   ro, co = np.shape(X)
   M = np.zeros((ro, ro - 1, co))
  
   for i in range(ro):
      l = 0
      for j in range(ro):
         if i != j:
            M[i, l] = diff2(X[i], X[j], t)
            l += 1
  
   ce = np.zeros(ro)
  
   for i in range(ro):
      c = map2(M[i])
      ce[i] = entropy(c)
   return ce


def diff2(p1, p2, t):
   '''
   Input: two series of phases
   Output: synchrony time series thereof
   '''
   d = np.array(abs(p1 - p2))
   d2 = np.zeros(len(d))
   for i in range(len(d)):
    if d[i] > np.pi:
     d[i] = 2 * np.pi - d[i]
    if d[i] < t:
     d2[i] = 1
  
   return d2
  