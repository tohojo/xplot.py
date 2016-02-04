## -*- coding: utf-8 -*-
##
## xplot.py
##
## Author:   Toke Høiland-Jørgensen (toke@toke.dk)
## Date:      4 February 2016
## Copyright (c) 2016, Toke Høiland-Jørgensen
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import matplotlib
matplotlib.use("Qt4Agg")
from matplotlib import pyplot, markers
from matplotlib.lines import Line2D
from matplotlib.transforms import Affine2D

# Mapping of xplot colours; these are from colorbrewer2.org
COLOURS = {"white":"#1b9e77",
           "black": "#666666",
           "orange": "#a6761d",
           "green": "#66a61e",
           "yellow": "#e6ab02",
           "red": "#d95f02",
           "purple": "#7570b3",
}

# Mapping xplot markers to matplotlib markers
MARKERS = {'darrow': markers.CARETDOWN,
           'uarrow': markers.CARETUP,
           'box': 's',
           'dot': '.',
           'utick': markers.TICKUP,
           'dtick': markers.TICKDOWN,
           'htick': '_',
           'diamond': 'D'}

def plot_xplot(filename):
    fp = open(filename, "r")
    fig = pyplot.figure()
    ax = fig.gca()
    col = "black"

    # Strategy for markers: Collect all markers of the same style and colour in
    # a list which is then plotted using axes.plot() at the end. This dict and
    # helper function does that.
    markers = {}
    def add_marker(col,m,parts):
        if len(parts) == 4 and parts[3] in COLOURS:
            col = parts[3]
        k = col,m
        x,y = map(float,parts[1:3])
        if k in markers:
            markers[k][0].append(x)
            markers[k][1].append(y)
        else:
            markers[k] = ([x],[y])

    # Parse the xplot command lines
    for line in fp:
        line = line.strip()
        parts = line.split()
        if line.startswith("timeval"):
            # This just sets a data type; we don't care
            pass

        # title, xlabel and ylabel has the value on the following line
        elif line == "title":
            fig.suptitle(next(fp).strip())
        elif line == "xlabel":
            ax.set_xlabel(next(fp).strip())
        elif line == "ylabel":
            ax.set_ylabel(next(fp).strip())

        # A colour name on a line sets the current colour
        elif line in COLOURS:
            col = line

        # Lines are defined as 'line x1 y1 x2 y2'
        elif parts[0] == "line":
            x1,y1,x2,y2 = map(float, parts[1:])
            ax.add_line(Line2D([x1,x2],[y1,y2],c=COLOURS[col],lw=1))

        # Text above or to the right specifies coordinates with the string on
        # the next line
        elif parts[0] in ("atext","rtext"):
            text = next(fp)
            x,y = map(float, parts[1:])
            kwargs = {'ha': 'center', 'va':'center', 'color': COLOURS[col]}
            if parts[0] == "rtext":
                # We translate the 'rtext' to have the text be to the right
                # instead of above. Values are simply arrived at by trial and
                # error.
                trans = Affine2D.identity().translate(6,-8)
                kwargs['transform']=ax.transData+trans
            t = ax.text(x,y,text,**kwargs)

        # Markers are specified as 'marker x y'
        elif parts[0] in MARKERS.keys():
            add_marker(col,MARKERS[parts[0]],parts)

        # We are done, let's draw
        elif line == "go":
            break
        else:
            print("Unknown: %s" % line)

    # Draw the markers
    for (c,m),(x,y) in markers.items():
        ax.plot(x,y,ls="",marker=m,markeredgecolor=COLOURS[c],markerfacecolor='none',markersize=4)
    ax.autoscale_view()
    pyplot.show()

if __name__ == "__main__":
    plot_xplot(sys.argv[1])
