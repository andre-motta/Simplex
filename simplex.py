__author__ = "Andre Lustosa Cabral de Paula Motta"
__copyright__ = "Open Source"
__credits__ = ["Andre Motta"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Andre Motta"
__email__ = "andre.motta@dcc.ufmg.br"
__status__ = "Delivered"
__lastedit__ = "15:58:41 BRST - 23 October 2017 ------ Added Comments to Code"
__created__ = "14:22:33 BRST - 31 September 2017"


import numpy as np
from ast import literal_eval
from simplexsolver import makeFPI
from simplexsolver import solveSimplex
from simplexsolver import cutPlanSimplex
from simplexsolver import branchAndBound
from simplexsolver import optimal
from simplexsolver import result1
from primal import truncate2
from certficates import printIntSolution







global optimal
np.set_printoptions(precision=12)
# region OpenFile
op = open('output.txt', 'w')
fp = open('simplex.txt', 'r')
line0 = fp.readline()
line1 = fp.readline()
line2 = fp.readline()
line3list = []
line3 = fp.readline()
# endregion

#region Generate Variables
line3list.extend(literal_eval(line3.strip()))
simplex = np.asarray(line3list, dtype=float)
size = [int(line1), int(line2)]
funcOption = int(line0)
# endregion
global result1
#region 'Main'
simplex = makeFPI(simplex, size)
print("\n---------------- INÍCIO RELAXAÇÃO LINEAR ---------------------\n")
result1 = solveSimplex(simplex, size)
print("\n\n\n---------------- FIM RELAXAÇÃO LINEAR ------------------------\n")
if (funcOption == 0) and result1 =="OPT":
  cutPlanSimplex(simplex, size)
elif result1 == "OPT":
  branchAndBound(simplex, size)
#endregion
#printIntSolution(optimal[1], optimal[0], optimal[2])
if optimal[1] != []:
  a = 0
  for i in optimal[1]:
      optimal[1][a] = truncate2(i)
      a+=1
  printIntSolution(optimal[1], truncate2(optimal[0]), optimal[2])
else:
  print("não achou sol inteira")