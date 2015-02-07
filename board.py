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

    @staticmethod
    def distance(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def potential(self, at, point):
        return self._board[point].infectious / Board.distance(at, point)

    @property
    def living(self):
        return {k: v for k, v in self._board.items() if v.population >= 1}

    @property
    def infected(self):
        # maybe change if starting from half a case is desirable
        return {k: v for k, v in self._board.items() if v.infectious >= 1}

    def tick(self):
        current_living = self.living
        current_infected = self.infected
        for c in current_living.keys():
            c.tick()
            infection_potential = 0
            for i in current_infected:
                infection_potential += self.potential(c, i)
            c.infect(infection_potential)
        for c in current_living:
            c.flip()
