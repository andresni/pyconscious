# -*- coding: utf-8 -*-

import statsmodels as stm
import numpy as np

# This is a function list of various data quality measures.

def stationarity(data, properties):
  std_prop = {"e_aggregate": "mean", # mean, std, median, max, min
              "c_aggregate": "mean", # mean, std, median, max, min, raw
              }.update(properties)
  temp = []
  for e in data:
    t = []
    for c in e:
      t.append(stm.tsa.stattools.adfuller(c)[1])
    temp.append(eval("np.{}(t)".format(std_prop["c_aggregate"])))
  return eval("np.{}(temp)".format(std_prop["aggregate"]))
  