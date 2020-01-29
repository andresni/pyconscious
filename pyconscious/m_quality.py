# -*- coding: utf-8 -*-

from . import functions as func
import numpy as np
import sys
import statsmodels as stm
import statsmodels.tsa.stattools as sts
import scipy.stats as ss
import random


def stationarity(data, test, ea, ca):
  """
  Calculates if data satisfies stationarity with Ad-Fuller test
  """
  temp = []
  for e in data:
    t = []
    for c in e:
      t.append(sts.adfuller(c)[1])
    try:
      temp.append(eval("np.{}(t)".format(ca)))
    except AttributeError:
      print("'{}' is an invalid value for 'ca', using 'mean'.".format(ca))
      temp.append(np.mean(t))
  try:
    return eval("np.{}(temp)".format(ea)) if not ea == "raw" else temp
  except AttributeError:
    print("'{}' is an invalid value for 'ea', using 'mean'.".format(ea))
    return np.mean(temp)

def normality(data, test, ea, ca):
  """
  Calculates if data follows a gaussian/normal distribution
  """
  temp = []
  for e in data:
    t = []
    for c in e:
        if test == "sw":
            t.append(1 - ss.shapiro(c)[1])
        elif test == "k2":
            t.append(1 - ss.normaltest(c)[1])
        else:
            sys.exit("'{}' is an invalid parameter for 'test'. Exiting.".format(test))
    try:
      temp.append(eval("np.{}(t)".format(ca)))
    except AttributeError:
      print("'{}' is an invalid value for 'ca', using 'mean'.".format(ca))
      temp.append(np.mean(t))
  try:
    return eval("np.{}(temp)".format(ea)) if not ea == "raw" else temp
  except AttributeError:
    print("'{}' is an invalid value for 'ea', using 'mean'.".format(ea))
    return np.mean(temp)