COMAP-2015
==========

*Problem A*

Megan Chambers, Tim Shaffer, Eric Shehadi

formats.esri
------------
- `import_population(filepath)` Load an ASCII map data file and return a
  new `Board` with the given susceptible population
- `export_population(filepath, pop_map)` Write the given `Board` to the
  specified path in ASCII format to be read by GIS software
- `export_cases(filepath, pop_map)`
- `export_deaths(filepath, pop_map)`

Board
-----
Locations are specified as 2-tuples, e.g. `(10, 20)`
- `tick()` Update the populations on the board according to the hybrid model.
  In addition to the changes described in `Cel.tick()`, spread the infection
  around to neighbors.
- `distance(a, b)` Return the taxicab distance between points `a` and `b`
- `circle(center, radius)` Return a set of points with `center` and `radius`
- `strip()` Remove cells not considered to be living
- `expose(howmany, *cels)` Expose `howmany` as described in
  `Cel.expose(howmany)` the location(s) given by `*cels`
- `infect(howmany, *cels)`
- `vaccinate(howmany, *cels)`
- `treat(howmany, *cels)`
- `susceptible` Total number of __Susceptible__ people on the board
- `exposed`
- `infectious`
- `recovered`
- `cases` See `Cel.cases`
- `population`
- `initial_population`
- `deaths`
- `treated`

Cel
---
- `tick()` Update the populations of the cell according to the SEIR model
- `expose(howmany)` Move at most `howmany` people from __Susceptible__ to
  __Exposed__
- `infect(howmany)` Move at most `howmany` people from __Susceptible__ to
    __Infectious__
- `vaccinate(howmany)` Move at most `howmany` people from
  __Susceptible__ to __Recovered__ and update the count of treated individuals
- `treat(howmany)` Move at most `howmany` people from __Exposed__ to
  __Recovered__ and update the count of treated individuals
- `susceptible` The number of __Susceptible__ people in the cell
- `exposed`
- `infectious`
- `recovered`
- `population` Total number of people currently alive in the cell, i.e.
  the sum of __Susceptible__ + __Exposed__ + __Infectious__ + __Recovered__
- `initial_population` The number of people in the `Cel` at its creation
- `deaths` The number of people that have died since the `Cel` was created,
  i.e. `initial_population` - `population`
- `treated` The number of people tho received a vaccination or treatment,
- `cases` The cumulative number of people who have contracted the disease in
  the cell, i.e. `infectious` + `recovered` + `deaths` - `treated`
- `basic_reproduction_number`
- `effective_reproduction_number`
