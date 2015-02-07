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


class Board:
    def __init__(self):
        self._board = {}
        self.header = {}

    @staticmethod
    def distance(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def potential(self, at, point):
        if at == point:
            return 0
        else:
            # this could be multiplied by a constant, squared, etc.
            # the infectious part is the number of infectious people at some
            # point and distance is that point's distance
            return self._board[point].infectious / Board.distance(at, point) ##

    def strip(self):
        self._board = self.living

    @property
    def living(self):
        # this is the minimum number of people to cause the cell to be
        # processed. increasing this constant decreases computational
        # workload but ignores some data
        return {k: v for k, v in self._board.items() if v.population >= 1}   ##

    @property
    def infected(self):
        # same as above
        return {k: v for k, v in self._board.items() if v.infectious >= 1}   ##

    def tick(self):
        current_living = self.living
        current_infected = self.infected
        for c in current_living.keys():
            self._board[c].tick()
            infection_potential = 0.0
            for i in current_infected:
                infection_potential += self.potential(c, i)
            self._board[c].infect(infection_potential)
        for c in current_living:
            self._board[c].flip()
