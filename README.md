# COMAP-2015

Since I'm going to be out tomorrow, I'll try to give some
instructions on using the core functionality. You'll need
a recent Python interpreter.
- Clone or download the repo from Github
- Open a terminal in the package folder
  with `cd path/to/COMAP-2015`
- Assuming you want to import map data, run `python` and then
  `>>> import formats.esri`
- The `import_population` function takes a filename for the
  map data and returns a new grid. You'll need to assign it
  to a variable:
  `>>> population = formats.esri.import_population('hello.txt')`
- I didn't have time to implement infection and disease masks,
  so you can just enter infections manually with coordinates:
  `>>> population.living[84, 80]._infectious['front'] = 5`
- To make it go for one timestep, call `>>> population.tick()`
- To remove cells with too few people and possibly save time
  on computations, call `>>> population.strip()`
- Once you have something, you can export by passing the whole
  grid to `>>> output_population("filename.txt", population)`.
  There is also `output_casualties` with the same usage.
  I have the Ebola turned waaaaay up, so you'll need to tweak
  the parameters. It should be mostly multiplying constants.
  I marked some places in the source code you might want to change.
  I gave them two hash signs by the right margin.
