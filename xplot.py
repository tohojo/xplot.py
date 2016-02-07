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
           "blue": "#386cb0",
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

    # Similarly as for makers, we keep lines mapped by colour and try to combine
    # them if we have several line segments that share points
    lines = {}
    def add_line(col,parts):
        x1,y1,x2,y2 = map(float, parts[1:])
        if not col in lines:
            lines[col] = [([x1,x2],[y1,y2])]
        else:
            found = False
            for l in lines[col][-5:]:
                if l[0][-1] == x1 and l[1][-1] == y1:
                    l[0].append(x2)
                    l[1].append(y2)
                    found = True
                    break
            if not found:
                lines[col].append(([x1,x2],[y1,y2]))

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
            add_line(col,parts)

        # Text above or to the right specifies coordinates with the string on
        # the next line
        elif parts[0] in ("atext","rtext","ltext"):
            text = next(fp).strip()
            x,y = map(float, parts[1:3])
            kwargs = {'ha': 'center', 'va':'center', 'color': COLOURS[col],
                      'textcoords':'offset points'}
            theta=0
            offset = (0,5)
            if len(parts) == 4 and parts[3] in COLOURS:
                kwargs['color'] = COLOURS[parts[3]]
            if parts[0] == "rtext":
                kwargs['ha'] = 'left'
                offset = (2,0)
            elif parts[0] == "ltext":
                kwargs['ha'] = 'right'
                offset = (-2,0)
            t = ax.annotate(text,(x,y),offset,**kwargs)

        # Markers are specified as 'marker x y'
        elif parts[0] in MARKERS.keys():
            add_marker(col,MARKERS[parts[0]],parts)

        # We are done, let's draw
        elif line == "go":
            break
        else:
            print("Unknown: %s" % line)

    # Draw the lines
    for c,ll in lines.items():
        for x,y in ll:
            ax.plot(x,y,lw=1,c=COLOURS[c])
    # Draw the markers
    for (c,m),(x,y) in markers.items():
        ax.plot(x,y,ls="",marker=m,markeredgecolor=COLOURS[c],markerfacecolor='none',markersize=4)
    ax.autoscale_view()
    pyplot.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: xplot.py <filename>.xpl\n")
        sys.exit(1)
    plot_xplot(sys.argv[1])
