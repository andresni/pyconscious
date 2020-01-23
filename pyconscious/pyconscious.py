# -*- coding: utf-8 -*-

import numpy as np
import sys
from . import functions as m
import statsmodels as stm
import statsmodels.tsa.stattools as sts
import random


def data_check(data = []):
  """
  Initial function that checks your data structure
  Input a 2D/3D list or numpy array.
  Output is a 3D numpy array if data is approved.
  """ 
 
  if len(np.shape(data)) == 2:
    print("""
          Padding 2D to 3D array.
          """)
    data = np.array([data])

  elif not len(np.shape(data)) == 3:
    sys.exit("""
             Input data has the wrong dimensionality. The
             correct dimenstionality is [epochs, channels, timepoints],
             or [channels, timepoints].
             """)
    
  # Check if matrix shape looks correct, prompting to continue if not.
  if not np.shape(data)[1] < np.shape(data)[2] or not np.shape(data)[0] < np.shape(data)[2]:
    if not input("""
                 Warning! It seems data structure has swapped the
                 position of channels, epochs, and/or timepoints. The proper structure is
                 [epochs, channels, timepoints]. You're structure is of the shape {}. 
                 Would you like to continue anyway (y/n)?
                 """.format(np.shape(data))) == "y":
        sys.exit("""
                 You didn't want to continue.
                 """)
      
  if not all(isinstance(x, (int, float)) for z in data for y in z for x in y):
    sys.exit("""
             Seems like your data is not entirely consisting of int/float. Please check.
             """)

  return np.array(data)

def LZc(data, norm = "shuffle_p", concat = "space", threshold = "median", shuffles = 1, ea = "mean"):
  """
  Measure LZc. Takes a 2D/3D array input, outputs aggregate (ea) measure over epochs.
  """  
  data = data_check(data)
  temp = []
  N = 1  
  for e in data:
    e = m.binarize(e, threshold)
    SC = m.concatenate(e, concat)
    if norm == "shuffle_p":
      for sh in range(shuffles):
        w = m.compress("".join(random.sample(SC,len(SC))))
        N = w if w > N else N
    elif norm == "max":
      M = [0, 0]
      for i in range(1,len(SC)):
        M[0] += (i*2**i) - (2**i - 1)
        M[1] += 2**i
        if M[0] - len(SC) >= len(SC):
          N = M[1] - ((M[0] - len(SC))/float(i))
          break
    elif norm == "shuffle_r":
      for sh in range(shuffles):
        w = m.compress([str(np.random.randint(0,2)) for i in range(len(SC))])
        N = w if w > N else N

    temp.append(m.compress(SC) / float(N))
  return eval("np.{}(temp)".format(ea)) if not ea == "raw" else temp
  
def ACE(data, norm = "shuffle_r", threshold = "median", shuffles = 1, ea = "mean"):
  """
  Measure ACE. Takes a 3D array input, outputs aggregate (ea) measure over epochs
  """
  data = data_check(data)
  temp = []
  N = 1
  for e in data:
    e = m.binarize(e, threshold)
    E = m.entropy(m.map2(e))
    if norm == "shuffle_p":   
      for sh in range(shuffles):
        for i in range(len(e)):
          random.shuffle(e[i])
        w = m.entropy(m.map2(e))
        N = w if w > N else N
    elif norm == "max":
      N = -2**len(e) * 1/2**len(e) * np.log(1/2**len(e)) / np.log(2.0)
    elif norm == "shuffle_r":
      for sh in range(shuffles):
        w = m.entropy(m.map2(np.random.randint(0, 2, np.shape(e))))
        N = w if w > N else N
    temp.append(E / float(N))
  return eval("np.{}(temp)".format(ea)) if not ea == "raw" else temp

def SCE(data, norm = "shuffle_r", threshold = 0.8, shuffles = 1, ea = "mean", ca = "mean"): 
  """
  Measure SCE. Takes a 3D array input, outputs aggregate measure
  """
  data = data_check(data)
  temp = []
  N = 1
  for e in data:
    ro, co = np.shape(e)
    E = m.Psi(e, threshold)
    if norm == "shuffle_p":   
      for sh in range(shuffles):
        for i in range(ro):
          random.shuffle(e[i])
        w = eval("np.{}(Psi(e, threshold))".format(ca))
        N = w if w > N else N
    elif norm == "max":
      N = -2**len(e) * 1/2**len(e) * np.log(1/2**len(e)) / np.log(2.0)
    elif norm == "shuffle_r":
      for sh in range(shuffles):
        w = m.entropy(m.map2(np.random.randint(0, 2, (ro-1,co))))
        N = w if w > N else N
    temp.append(eval("np.{}(E)".format(ca)) / float(N))
  return eval("np.{}(temp)".format(ea)) if not ea == "raw" else temp



def centrality(data, ea = "mean", ca = "mean"):
  """
  Calculates if data satisfies Centrality with Ad-Fuller test
  """
  temp = []
  for e in data:
    t = []
    for c in e:
      t.append(sts.adfuller(c)[1])
    temp.append(eval("np.{}(t)".format(ca)))
  return eval("np.{}(temp)".format(ea)) if not ea == "raw" else temp
