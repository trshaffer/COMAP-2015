# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# based on the specification at http://is.gd/EBJeXy and some guesswork

from board import Board
from cel import Cel


# this function handles all exports involving writing a grid into an ASCII
# file with ESRI headers. the particulars of the data to be written are
# handled by a selector function.
def _export_board(filepath, pop_map, selection):
    with open(filepath, 'w') as f:
        # the key-value pairs stored in the Board are written out first.
        # the order probably doesn't match that of the file imported.
        for e in pop_map.header:
            f.write('%s %s\n' % (e, pop_map.header[e]))
        # use the dimensions from the header to walk over the grid
        for y in range(int(pop_map.header['nrows'])):
            for x in range(int(pop_map.header['ncols'])):
                # if there is no entry, just use the NODATA value
                try:
                    f.write('%f' % selection(pop_map._board[x, y]))
                except KeyError:
                    f.write(pop_map.header['NODATA_value'])
                if x < int(pop_map.header['ncols']) - 1:
                    f.write(' ')
            f.write('\n')

# these guys just abstract member access to pass it around
def population_exporter(cel):
    return cel.population

def cases_exporter(cel):
    return cel.cases

def deaths_exporter(cel):
    return cel.deaths

# these are the public functions
def population_importer(val):
    return Cel(susceptible = float(val))

def export_population(filepath, pop_map):
    _export_board(filepath, pop_map, population_exporter)

def export_cases(filepath, pop_map):
    _export_board(filepath, pop_map, cases_exporter)

def export_deaths(filepath, pop_map):
    _export_board(filepath, pop_map, deaths_exporter)

# this reads in an ESRI map file and feeds the data into a new Board
def import_population(filepath):
    pop_map = Board()

    with open(filepath) as f:
        pop_data = f.readlines()

    # first, parse the header.
    # the entries go into a dict in the Board
    while pop_data[0].strip()[0].isalpha():
        header_line = pop_data.pop(0).split()
        pop_map.header[header_line[0]] = header_line[1]
    pop_cells = ' '.join(pop_data).split()

    # assuming the dimensions in the header are correct, just walk along and
    # dump the values into a Board
    for y in range(int(pop_map.header['nrows'])):
        for x in range(int(pop_map.header['ncols'])):
            c = pop_cells.pop(0)
            # only add a Cel if there's actual data in the map file
            if c != pop_map.header['NODATA_value']:
                pop_map._board[x, y] = Cel(susceptible=float(c))
    return pop_map
