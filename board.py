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

    # taxicab distance is the easiest to work with here
    @staticmethod
    def distance(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # when infecting or vaccinating areas, this function might come in handy
    # to cover regions
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

    # the potential used here is inspired by electrostatic potential. the idea
    # is that an infected cell increases the potential (I love the ambiguity
    # of the English language) for nearby cells to be exposed to the disease.
    # a more intensely infected cell should be more likely to infect others,
    # and this effect should drop off with distance. the function used here
    # was chosen to be most intense near the source, drop off somewhat
    # quickly, and approach zero.
    def potential(self, at, point):
        if at == point:
            return 0.0
        else:
            #XXX increase this constant to spread farther
            return 5 * self._board[point].infectious /  \
                Board.distance(at, point)

    # if the gameboard has VERY sparsely populated areas, this method can
    # remove cells to save on computation. this is likely a bad idea, though.
    def strip(self):
        self._board = self.living

    # these methods should be used to interact with the board
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

    # this is the minimum number of people to cause the cell to be
    # processed. increasing this constant decreases computational
    # workload but ignores some data
    @property
    def living(self):
        #XXX cutoff for unpopulated cel
        return {k: v for k, v in self._board.items() if v.population >= 1}

    @property
    def infected(self):
        #XXX cutoff for uninfected cell
        return {k: v for k, v in self._board.items() if v.infectious >= 1}

    # summary info
    @property
    def susceptible(self):
        return sum([c.susceptible for c in self._board.values()])

    @property
    def exposed(self):
        return sum([c.exposed for c in self._board.values()])

    @property
    def infectious(self):
        return sum([c.infectious for c in self._board.values()])

    @property
    def recovered(self):
        return sum([c.recovered for c in self._board.values()])

    @property
    def cases(self):
        return sum([c.cases for c in self._board.values()])

    @property
    def deaths(self):
        return sum([c.deaths for c in self._board.values()])

    @property
    def treated(self):
        return sum([c.treated for c in self._board.values()])

    @property
    def population(self):
        return sum([c.population for c in self._board.values()])

    @property
    def initial_population(self):
        return sum([c.initial_population for c in self._board.values()])

    # this is the heart of the program.
    def tick(self, duration=1):
        for i in range(duration):
            # cache the dict comprehensions to avoid filtering every
            # time something happens
            current_living = self.living
            current_infected = self.infected
            for c in current_living:
                # apply the SEIR model now since it overwrites the backbuffer
                self._board[c].tick()
                infection_potential = 0.0
                # to keep computations tractable, limit the distance at which
                # infected neighbors can affect the current cell
                #XXX max radius of infectivity
                for i in {k: v for k, v in current_infected.items() \
                        if Board.distance(k, c) < 50}:
                    infection_potential += self.potential(c, i)
                # here we set the likelihood of an exposure. if neighbors have
                # too much infection, it's guaranteed. we scale the infection
                # potential down and compare to a uniform random value. if the
                # potential is low (or the constant is large), nothing happens.
                # if the scaled value goes above one, exposure is guaranteed.
                #XXX decrease this constant for faster spread
                if random() < infection_potential / 50.0:
                    #XXX proportion of population affected by exposure event
                    self._board[c].expose(0.25 * self._board[c].susceptible)
            for c in current_living:
                self._board[c].flip()
