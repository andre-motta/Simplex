import numpy as np
from certficates import checkUnbTableau
from certficates import checkInvTableau
from certficates import isDone


# region SimplexDual

def pivotD(position: list, tableau: np):
    # iterates getting the divisions
    print("Pivot Dual")
    print(position)
    print(tableau)
    #a = input()
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


def simplexDual(tableau: np, size):
    # checks wether the tableau is Unbounded
    if checkUnbTableau(tableau):
        return 2
    # checks wether the tableau is not valid
    if checkInvTableau(tableau):
        return 3

    # gets the pivoting position for the Dual method
    position = pickDualPivot(tableau)

    # default value for no position
    if position == [-1, -1]:
        # if no position and its done returns 0
        if isDone(tableau):
            return 0
        return 1
    # pivot the position we just picked
    pivotD(position, tableau)
    # recursively apply the DUAL method in the pivoted tableau
    return simplexDual(tableau, size)


def pickDualPivot(tableau: np) -> list:
    aux1 = 1
    position = [-1, -1]
    cont = 0
    # while not yet passed through all rows
    # print("\ntableau dual simplex\n")

    while aux1 < tableau.shape[0]:

        # if the element in B is negative for this row
        if tableau[aux1, tableau.shape[1] - 1] < 0:
            # print("\naux1 encontrado")
            # print(aux1)
            aux2 = 0
            lesser = float("inf")

            # for each element in the row
            while aux2 < tableau.shape[1] - 1:

                # if the position is negative, and the C value is negative and the element / C is smaller then lesser swap lesser (do it for all elements)
                if ((tableau[aux1, aux2]) < 0 and (tableau[0, aux2]) < 0 and (
                        tableau[0, aux2] / tableau[aux1, aux2] < lesser)):
                    lesser = tableau[0, aux2] / tableau[aux1, aux2]
                    position = [aux1, aux2]
                    cont += 1

                aux2 += 1
            # if there was at least one iteration
            if cont != 0:
                # print("Position Dual")
                # print(position)
                # print(tableau)
                # print("\n")
                return position

        aux1 += 1

    return position

# endregion
