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


# for explanation of parameters, see http://is.gd/aeMk9q (if it's up...)


class Cel:
    def __init__(self, susceptible=0, exposed=0, infectious=0, recovered=0):
        self.front_buffer = "front"
        self.back_buffer = "back"
        self.timestep = 1 # probably measured in days

        self.initial_population = susceptible + exposed + \
            infectious + recovered

        self._susceptible = {}
        self._susceptible[self.front_buffer] = susceptible
        self._susceptible[self.back_buffer] = susceptible

        self._exposed = {}
        self._exposed[self.front_buffer] = exposed
        self._exposed[self.back_buffer] = exposed

        self._infectious = {}
        self._infectious[self.front_buffer] = infectious
        self._infectious[self.back_buffer] = infectious

        self._recovered = {}
        self._recovered[self.front_buffer] = recovered
        self._recovered[self.back_buffer] = recovered

        self.transmission_rate = 0.45
        self.fatality_rate = 0.48

        # DO NOT set these to 0
        self.incubation_duration = 5.3
        self.infectiousness_duration = 5.61

    @property
    def constants(self):
        return {'transmission_rate': self.transmission_rate,
                'fatality_rate': self.fatality_rate,
                'incubation_duration': self.incubation_duration,
                'infectiousness_duration': self.infectiousness_duration}

    @property
    def stats(self):
        return {'susceptible': self.susceptible,
                'exposed': self.exposed,
                'infectious': self.infectious,
                'recovered': self.recovered,
                'initial_population': self.initial_population,
                'population': self.population}

    def tick(self):
        self._susceptible[self.back_buffer] = self.susceptible + \
            (self.timestep * self.susceptible_change)
        self._exposed[self.back_buffer] = self.exposed + \
            (self.timestep * self.exposed_change)
        self._infectious[self.back_buffer] = self.infectious + \
            (self.timestep * self.infectious_change)
        self._recovered[self.back_buffer] = self.recovered + \
            (self.timestep * self.recovered_change)

    def flip(self):
        self.front_buffer, self.back_buffer = \
            self.back_buffer, self.front_buffer

    def expose(self, quantity):
        victims = min(quantity, self.susceptible)
        self._susceptible[self.back_buffer] -= victims
        self._exposed[self.back_buffer] += victims

    def infect(self, quantity):
        victims = min(quantity, self.susceptible)
        self._susceptible[self.back_buffer] -= victims
        self._infectious[self.back_buffer] += victims

    def vaccinate(self, quantity):
        victims = min(quantity, self.susceptible)
        self._susceptible[self.back_buffer] -= victims
        self._recovered[self.back_buffer] += victims

    def treat(self, quantity):
        victims = min(quantity, self.exposed)
        self._exposed[self.back_buffer] -= victims
        self._recovered[self.back_buffer] += victims

    @property
    def susceptible(self):
        return self._susceptible[self.front_buffer]

    @property
    def exposed(self):
        return self._exposed[self.front_buffer]

    @property
    def infectious(self):
        return self._infectious[self.front_buffer]

    @property
    def recovered(self):
        return self._recovered[self.front_buffer]

    @property
    def population(self):
        return self.susceptible + self.exposed + \
            self.infectious + self.recovered

    @property
    def casualties(self):
        return self.infectious + self.initial_population - \
            self.population

    @property
    def basic_reproduction_number(self):
        return self.transmission_rate * self.infectiousness_duration

    @property
    def effective_reproduction_number(self):
        try:
            return self.transmission_rate * self.susceptible * \
                   self.infectiousness_duration / self.population
        except ZeroDivisionError:
            return 0.0

    @property
    def susceptible_change(self):
        try:
            return -self.transmission_rate * self.susceptible * \
                   self.infectious / self.population
        except ZeroDivisionError:
            return 0.0

    @property
    def exposed_change(self):
        try:
            return (self.transmission_rate * self.susceptible * \
                    self.infectious / self.population) - \
                    (self.exposed / self.incubation_duration)
        except ZeroDivisionError:
            return 0.0

    @property
    def infectious_change(self):
        return (self.exposed / self.incubation_duration) - \
               (self.infectious / self.infectiousness_duration)

    @property
    def recovered_change(self):
        return (1 - self.fatality_rate) * \
               self.infectious / self.infectiousness_duration
