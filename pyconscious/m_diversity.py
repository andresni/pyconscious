# -*- coding: utf-8 -*-

from . import functions as func
import numpy as np
import sys
import random

def LZc(data, norm = "shuffle_p", concat = "space", threshold = "median", shuffles = 1, ea = "mean"):
  """
  Measure LZc. Takes a 2D/3D array input, outputs aggregate (ea) measure over epochs.
  """
  temp = []
  N = 0
  for e in data:
    e = func.binarize(e, threshold)
    SC = func.concatenate(e, concat)
    if norm == "shuffle_p":
      for sh in range(shuffles):
        w = func.compress("".join(random.sample(SC,len(SC))))
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
        w = func.compress([str(np.random.randint(0,2)) for i in range(len(SC))])
        N = w if w > N else N
    else:
      sys.exit("'{}' is not a valid argument for 'norm'".format(norm))

    temp.append(func.compress(SC) / float(N))
  try:
    return eval("np.{}(temp)".format(ea)) if not ea == "raw" else temp
  except AttributeError:
    print("'{}' is an invalid value for 'ea', using 'mean'.".format(ea))
    return np.mean(temp)

def ACE(data, norm = "shuffle_r", threshold = "median", shuffles = 1, ea = "mean"):
  """
  Measure ACE. Takes a 3D array input, outputs aggregate (ea) measure over epochs
  """
  temp = []
  N = 0
  for e in data:
    e = func.binarize(e, threshold)
    E = func.entropy(func.map2(e))
    if norm == "shuffle_p":
      for sh in range(shuffles):
        for i in range(len(e)):
          random.shuffle(e[i])
        w = func.entropy(func.map2(e))
        N = w if w > N else N
    elif norm == "max":
      N = -2**len(e) * 1/2**len(e) * np.log(1/2**len(e)) / np.log(2.0)
    elif norm == "shuffle_r":
      for sh in range(shuffles):
        w = func.entropy(func.map2(np.random.randint(0, 2, np.shape(e))))
        N = w if w > N else N
    else:
      sys.exit("'{}' is not a valid argument for 'norm'".format(norm))
    temp.append(E / float(N))
  try:
    return eval("np.{}(temp)".format(ea)) if not ea == "raw" else temp
  except AttributeError:
    print("'{}' is an invalid value for 'ea', using 'mean'.".format(ea))
    return np.mean(temp)

def SCE(data, norm = "shuffle_r", threshold = 0.8, shuffles = 1, ea = "mean", ca = "mean"):
  """
  Measure SCE. Takes a 3D array input, outputs aggregate measure
  """
  temp = []
  N = 0
  for e in data:
    ro, co = np.shape(e)
    E = func.Psi(e, threshold)
    if norm == "shuffle_p":
      for sh in range(shuffles):
        for i in range(ro):
          random.shuffle(e[i])
        try:
          w = eval("np.{}(func.Psi(e, threshold))".format(ca))
        except AttributeError:
          print("'{}' is an invalid value for 'ca', using 'mean'.".format(ca))
          w = np.mean(func.Psi(e, threshold))
        N = w if w > N else N
    elif norm == "max":
      N = -2**len(e) * 1/2**len(e) * np.log(1/2**len(e)) / np.log(2.0)
    elif norm == "shuffle_r":
      for sh in range(shuffles):
        w = func.entropy(func.map2(np.random.randint(0, 2, (ro-1,co))))
        N = w if w > N else N
    else:
      sys.exit("'{}' is not a valid argument for 'norm'".format(norm))
    try:
      temp.append(eval("np.{}(E)".format(ca)) / float(N))
    except AttributeError:
      print("'{}' is an invalid value for 'ca', using 'mean'.".format(ca))
      temp.append(np.mean(E) / float(N))
  try:
    return eval("np.{}(temp)".format(ea)) if not ea == "raw" else temp
  except AttributeError:
    print("'{}' is an invalid value for 'ea', using 'mean'.".format(ea))
    return np.mean(temp)

