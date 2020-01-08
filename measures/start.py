# -*- coding: utf-8 -*-
import numpy as np
import quality
import measures

# The main function that will handle the data from here on
def start(data = [], properties = 0):
  # Initial function that takes your data structure
  # and your dictionary of properties.
  # Input: 
  # data = 3D list or numpy array
  # properties = dictionary of parameters
  # Output:
  # value = dictionary containing results and other information (see specifics of measure and parameters)
  
  standard_prop = {"quality_tests": [],
                   "analysis": [], }
  
  # Check if user passed along the required data
  if not len(np.shape(data)) == 3:
    print("""      Input data was not a 3 dimensional structure.
          Please use a 3 dimensional list or numpy array object of
          (epochs, channels, timepoints).""")
    return None
    
  # Check if matrix shape looks correct, prompting to continue if not.
  if not np.shape(data)[1] < np.shape(data)[2] or np.shape(data)[0] < np.shape(data)[2]:
    print("""      Warning, it seems data structure has swapped the
          position of channels, epochs, and timepoints. The proper structure is
          (epochs, channels, timepoints). You're structure is of the shape {}""".format(np.shape(data)))
    if not input("Would you like to continue anyway? y") == "y":
      return None
    
  # Check if properties is dict. If it is, it updates standard properties accordingly
  if not type(properties) is dict:
    print("""      You haven't passed in a dictionary of properties
          for the analysis. Please do so. See documentation.
          At minimum you need a list of analysis or 
          data quality tests to run. 
          For example if running Lempel Ziv complexity:
          properties = {'analysis': ['LZc']}, or if centrality
          properties = {'quality': ['stationarity']}""")
    return None
  else:
    standard_prop.update(properties)
  
  # Now we're ready to run.
  data = np.array(data)
  
  results = {"values": {},
             "quality": {}, }

  if len(standard_prop["quality_tests"]) > 0:
    for test in standard_prop["quality_tests"]:
      try:
        results["quality"][test] = getattr(quality, test)(data, properties)
      except:
        print("Seems like the test: '{}' didn't work. Misspelled perhaps?".format(test))
        return None
      
  if len(standard_prop["analysis"]) > 0:
    for anal in standard_prop["analysis"]:
      try:
        results["values"][anal] = getattr(measures, test)(data, properties)
      except:
        print("Seems like the test: '{}' didn't work. Misspelled perhaps?".format(test))
        return None
        