# Welcome to this readme
"Many measures reside in here. Pass a 3D matrix, and grab a beer"

This package is a package of measures to calculate "consciousness". That is,
it will include measures that have been used in previous research to give a single
value to characterize a whole state of consciousness such as awake, anesthesia,
hallucinations, sleep, coma, etc.

---

To install:

pip[3] install [--user] git+https://github.com/andresni/pyconscious.git

To use:

import pyconscious

result = pyconscious.LZc(data, **kwargs)

---

Input data is 2D/3D matrix of continuous data in the format [channels, timepoints],
or [epochs, channels, timepoints].

**kwargs depends on the method used but standard parameters are provided based on literature.

Documentation is currently limited, including which measures are included and
exactly which parameters they take (and allowed values). Use tab-completion.
If invalid parameters are passed, you'll be notified, mostly.