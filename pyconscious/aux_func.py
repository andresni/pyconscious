# -*- coding: utf-8 -*-

import numpy as np
import sys

def data_check(data = []):
  """
  Initial function that checks your data structure
  Input a 2D/3D list or numpy array (2D padded to 3D)
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

  if not all(isinstance(x, (int, np.float32, np.float64)) for z in data for y in z for x in y):
    sys.exit("""
             Seems like your data is not entirely consisting of int/float. Please check.
             """)

  return np.array(data)