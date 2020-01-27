# Starting stuff
%load_ext autoreload
%reload_ext autoreload
%autoreload 2

import pyconscious as pc
import numpy as np
import autoreload
from importlib import reload

reload(pc)

def maintest():

  M1 = np.zeros((5, 6, 1000))
  M2 = np.zeros((5, 6, 1000))

  for e in range(5):
    for c in range(6):
      M1[e, c, :] = np.sin(np.arange(c * 15 * e, 1000 + c * 15 * e, 1)) + np.random.normal(0, 0.2, (1, 1, 1000))
      M2[e, c, :] = np.sin(np.arange(c * 15 * e, 1000 + c * 15 * e, 1)) + np.random.normal(0, 0.8, (1, 1, 1000))

  # Test measures
  for i in [M1,M2]:
    print(pc.LZc(i,norm="shuffle_r",concat="space",threshold="median",shuffles=5,ea="mean"))
    print(pc.ACE(i,norm="shuffle_r",threshold="median",shuffles=5,ea="mean"))
    print(pc.SCE(i,norm="shuffle_r",threshold=0.8,shuffles=5,ea="mean",ca="mean"))
    print(pc.stationarity(i,test="adt",ea="mean",ca="mean"))
    print(pc.normality(i,test="adt",ea="mean",ca="mean"))

goal_standard1 = {"LZc":[0.982, 0.981, 0.980, 0.984, 0.981],
                  "ACE":[0.987, 0.998, 1.000, 1.000, 0.999],
                  "SCE":[0.199, 0.201, 0.202, 0.203, 0.205],}
goal_standard2 = {"LZc":[0.987, 0.986, 0.989, 0.988, 0.988],
                  "ACE":[0.998, 0.999, 0.999, 1.001, 0.999],
                  "SCE":[0.733, 0.737, 0.741, 0.737, 0.741],}

maintest()