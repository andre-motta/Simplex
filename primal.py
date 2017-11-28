import numpy as np
from certficates import checkUnbTableau
from certficates import checkInvTableau
from certficates import isDone
import math as Math


# region SimplexPrimal and Auxiliary
def truncate(f):
    # '''Truncates/pads a float f to n decimal places without rounding'''
    f = round(f, 8)
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, 8)
    i, p, d = s.partition('.')
    return '.'.join([i, (d + '0' * 8)[:8]])

def truncate2(f):
    # '''Truncates/pads a float f to n decimal places without rounding'''
    f = round(f, 3)
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, 3)
    i, p, d = s.partition('.')
    return '.'.join([i, (d + '0' * 3)[:3]])


def pivotP(position: list, tableau: np):
    print("Pivot Primal")
    print(position)
    print(tableau)
    #i = 0
    # for x in tableau:
    #  tableau[i] = np.array([truncate(xi) for xi in x])
    #  i+=1
    # iterates getting the divisions
    tableau[position[0], ...] = tableau[position[0], ...] / tableau[position[0], position[1]]
    aux = 1

    # zeroes the other elements above and below the pivot
    while position[0] - aux >= 0:
        tableau[position[0] - aux, ...] = tableau[position[0] - aux, ...] - tableau[position[0] - aux, position[1]] * \
                                                                            tableau[position[0], ...]
        aux += 1
    aux = 1

    # finishes zeroing the elements < than
    while position[0] + aux < tableau.shape[0]:
        tableau[position[0] + aux, ...] = tableau[position[0] + aux, ...] - tableau[position[0] + aux, position[1]] * \
                                                                            tableau[position[0], ...]
        aux += 1

    print(tableau)
    print()


def simplexPrimal(tableau: np, size):
    # checks wether the tableau is Unbounded
    if checkUnbTableau(tableau):
        return 2
    # checks wether the tableau is not valid
    if checkInvTableau(tableau):
        return 3
    # gets the pivoting position for the Dual method
    position = pickPrimalPivot(tableau)

    if position == [-1, -1]:

        if isDone(tableau):
            return 0
        return 1
    # pivot the position we just picked
    pivotP(position, tableau)
    # recursively apply the PRIMAL method in the pivoted tableau
    return simplexPrimal(tableau, size)


def buildAuxTableau(tableau: np):
    # print("\n---------INSIDE AUX------\n")
    # print(tableau)
    # gets all negative positions on the last column of the tableau (excluding the C row)
    auxArray = np.transpose((tableau[1:tableau.shape[0], tableau.shape[1] - 1] < 0).nonzero())
    auxTableau = tableau.copy()
    # print("\n Aux tableau array ---------------------------------------")
    # print(auxArray)
    # print(auxTableau)
    # print("\n\n\n\n\n")

    aux2 = 0
    # if we have more than 0 rows negate the rows with negative B values
    if auxArray.size > 0:
        while aux2 < auxArray.shape[0]:
            auxTableau[auxArray[0][0] + 1, 0:auxTableau.shape[1]] = \
                np.negative(auxTableau[auxArray[0][0] + 1, 0:auxTableau.shape[1]])
            aux2 += 1

    # creates the identity for the auxiliary with the same process as in the first creation of slack variables
    comp = np.vstack((np.negative(np.ones((1, tableau.shape[0] - 1))), np.identity(tableau.shape[0] - 1)))
    auxTableau = np.hsplit(auxTableau, (auxTableau.shape[1] - 1, auxTableau.shape[1]))
    auxTableau = np.hstack((auxTableau[0], comp, auxTableau[1]))
    # zeroes the last column
    auxTableau[0, 0:tableau.shape[1] - 1] = np.zeros(tableau.shape[1] - 1)
    aux1 = 1

    # finally, for each row we make each row = itself + the first row
    while aux1 < auxTableau.shape[0]:
        auxTableau[0, ...] = auxTableau[0, ...] + auxTableau[aux1, ...]
        aux1 += 1

    return auxTableau


def pickPrimalPivot(tableau: np) -> list:
    # print("PIVOTEANDO PRIMAL")
    # print(tableau)
    # print("\n\n")
    aux1 = 0
    position = [-1, -1]
    cont = 0

    # if the elements of B are not all positive
    if not (tableau[1:tableau.shape[0], tableau.shape[1] - 1] >= 0).all():
        return position

    # while not yet tried every column
    while aux1 < tableau.shape[1] - 1:
        # if the b value is positive
        if tableau[0, aux1] > 0:
            aux2 = 1
            lesser = float("inf")
            # gets the smaller ratio dividing an element by B value in the selected column
            while aux2 < tableau.shape[0]:
                if (tableau[aux2, aux1] > 0 and (tableau[aux2, tableau.shape[1] - 1] / tableau[aux2, aux1] < lesser)):
                    lesser = tableau[aux2, tableau.shape[1] - 1] / tableau[aux2, aux1]
                    position = [aux2, aux1]
                    cont += 1
                aux2 += 1
            # if there was a single iteration
            if cont != 0:
                # print("Position Primal")
                # print(position)
                return position

        aux1 += 1

    return position

# endregion