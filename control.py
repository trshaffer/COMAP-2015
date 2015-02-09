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


import csv
import uuid
import formats.esri


history = []
snapshots = []
name = str(uuid.uuid4())

sierra = formats.esri.import_population('sierraleone.txt')
print('imported map data')

sierra.patient_zero((369, 284))

#TODO apply vaccines
print('initial conditions set up')

def go(month):
    for day in range(30):
        sierra.tick()
        history.append({
            'day': day + (30 * month),
            'susceptible': sierra.susceptible,
            'exposed': sierra.exposed,
            'infectious': sierra.infectious,
            'recovered': sierra.recovered,
            'cases': sierra.cases,
            'deaths': sierra.deaths})
        print('%d, %d' % (month, day))
    formats.esri.export_cases('cases-%s-%d.txt' % (name, month), sierra)
    formats.esri.export_deaths('deaths-%s-%d.txt' % (name, month), sierra)
    print('dumped snapshots')

def log_history():
    with open('history-%s.csv' % name, 'w', newline='') as csvfile:
        logwriter = csv.DictWriter(csvfile,
            ['day', 'susceptible', 'exposed', 'infectious', 'recovered',
             'cases', 'deaths'])
        logwriter.writeheader()
        for r in history:
            logwriter.writerow(r)
    print('wrote history')
