# Python plotter for xplot (.xpl) files

This is a basic implementation of (a subset of) the xplot .xpl format
using matplotlib. It is specifically targeted at drawing TCPTrace time
sequence graphs.

The native xplot is of course a lot faster than matplotlib, but this
makes it possible to take full advantage of matplotlib's styling and
exporting features.

Only tested on Python 3.5 and matplotlib 1.5. May eat your children;
will definitely eat your RAM (a 600 second time sequence diagram eats
~1.5 GB of RAM).

License: GPLv3.

## Usage
```
python xplot.py <filename>.xpl
```
