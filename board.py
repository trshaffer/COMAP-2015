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


from random import random


class Board:
    def __init__(self):
        self._board = {}
        self.header = {}

    @staticmethod
    def distance(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @staticmethod
    def circle(center, radius):
        quadrant = set()
        for x in range(radius):
            for y in range(radius - x):
                quadrant.add((x, y))
        quadrant.update({(x, -y) for (x, y) in quadrant})
        quadrant.update({(-x, y) for (x, y) in quadrant})
        quadrant.update({(-x, -y) for (x, y) in quadrant})
        return {(x + center[0], y + center[1]) for (x, y) in quadrant}

    def potential(self, at, point):
        if at == point:
            return 0.0
        else:
            #XXX increase this constant to spread farther
            return 5 * self._board[point].infectious /  \
                Board.distance(at, point)

    def strip(self):
        self._board = self.living

    def expose(self, people, *cels):
        for c in cels:
            self._board[c].expose(people)
            self._board[c].flip()

    def infect(self, people, *cels):
        for c in cels:
            self._board[c].infect(people)
            self._board[c].flip()

    def vaccinate(self, people, *cels):
        for c in cels:
            self._board[c].vaccinate(people)
            self._board[c].flip()

    def treat(self, people, *cels):
        for c in cels:
            self._board[c].treat(people)
            self._board[c].flip()

    @property
    def living(self):
        # this is the minimum number of people to cause the cell to be
        # processed. increasing this constant decreases computational
        # workload but ignores some data

        #XXX cutoff for unpopulated cel
        return {k: v for k, v in self._board.items() if v.population >= 1}

    @property
    def infected(self):
        #XXX cutoff for uninfected cell
        return {k: v for k, v in self._board.items() if v.infectious >= 1}

    def tick(self, duration=1):
        for i in range(duration):
            current_living = self.living
            current_infected = self.infected
            for c in current_living:
                self._board[c].tick()
                infection_potential = 0.0
                #XXX max radius of infectivity
                for i in {k: v for k, v in current_infected.items() \
                        if Board.distance(k, c) < 50}:
                    infection_potential += self.potential(c, i)
                #XXX decrease this constant for faster spread
                if random() < infection_potential / 50.0:
                    #XXX proportion of population affected by exposure event
                    self._board[c].expose(0.25 * self._board[c].susceptible)
            for c in current_living:
                self._board[c].flip()
