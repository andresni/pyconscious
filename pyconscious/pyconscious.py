# -*- coding: utf-8 -*-

from . import m_diversity as mdiv
from . import m_quality as mqual
from . import aux_func as aux


def LZc(data, norm = "shuffle_p", concat = "space", threshold = "median", shuffles = 1, ea = "mean"):
  """
  Measure LZc. Takes a 2D/3D array input, outputs aggregate (ea) measure over epochs.
  """
  data = aux.data_check(data)
  return mdiv.LZc(data, norm, concat, threshold, shuffles, ea)


def ACE(data, norm = "shuffle_r", threshold = "median", shuffles = 1, ea = "mean"):
  """
  Measure ACE. Takes a 3D array input, outputs aggregate (ea) measure over epochs
  """
  data = aux.data_check(data)
  return mdiv.ACE(data, norm, threshold, shuffles, ea)


def SCE(data, norm = "shuffle_r", threshold = 0.8, shuffles = 1, ea = "mean", ca = "mean"):
  """
  Measure SCE. Takes a 3D array input, outputs aggregate measure
  """
  data = aux.data_check(data)
  return mdiv.SCE(data, norm, threshold, shuffles, ea, ca)


def stationarity(data, test = "adf", ea = "mean", ca = "mean"):
  """
  Calculates if data satisfies Stationarity.
  Returns p-value(s) where lower means more likely stationary
  condition is satisfied.
  Valid tests to use are:
      'adf' - Augmented Dicky-Fuller test
  """
  data = aux.data_check(data)
  return mqual.stationarity(data, test, ea, ca)

def normality(data, test = "sw", ea = "mean", ca = "mean"):
  """
  Calculates if data is normally distributed or not. Returns
  p-values(s) where lower means more likely normality condition
  is satisfied.
  Valid tests to use are:
      'sw'  - Shapiro Wilks test
      'k2'  - D`Agostino`s K^2 test
      'adt' - Anderson-Darling test
  """
  data = aux.data_check(data)
  return mqual.normality(data, test, ea, ca)
