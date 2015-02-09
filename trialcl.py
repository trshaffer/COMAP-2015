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


import control
import board

try:
    control.go(0)

    for e in board.Board.circle((411, 205), 5):
        control.sierra.vaccinate(200, e)
    for e in board.Board.circle((329, 164), 5):
        control.sierra.vaccinate(200, e)
    for e in board.Board.circle((239, 274), 5):
        control.sierra.vaccinate(200, e)
    for e in board.Board.circle((236, 156), 5):
        control.sierra.vaccinate(200, e)

    with open('treated-%s.txt' % control.name, 'w') as f:
        f.write('%f\n' % control.sierra.treated)

    for i in range(1, 4):
        control.go(i)

finally:
    control.log_history()
