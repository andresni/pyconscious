# -*- coding: utf-8 -*-

import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
     name='isitconscious',  
     version='0.1',
     scripts=['isitconscious'] ,
     author="Andre Sevenius Nilsen",
     author_email="sevenius.nilsen@gmail.com",
     description="A package of measures of consciousness",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/andresni/isitconscious",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     python_requires = '>=3.2',
 )