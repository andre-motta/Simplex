import numpy as np
from certficates import printOptimalSolution
from certficates import printInvCertificate
from certficates import printUnbCertificate
from certficates import optimalCertificate
from certficates import invCertificate
from certficates import unbCertificate
from certficates import getX
from certficates import getBase
from dual import simplexDual
from primal import simplexPrimal
from primal import truncate
from certficates import isBasicSolution
from primal import buildAuxTableau
import math

result1 = "OPT"
result2 = "OPT"
optimal = [-float('inf'), [], []]
status = True
# region SimplexSolver
epsilon = 0.000001


def isFPI(tableau: np, dimension):
    # checks wether the bases work, if they do work, then it is in FPI
    base = getBase(tableau, dimension)

    if (base == -1).any():
        return False
    return True


def refactorTableau(tableau: np, auxTableau: np):
    newTableau = tableau

    # expands the original tableau
    tableau[0, 0:tableau.shape[1] - 1] = tableau[0, 0:tableau.shape[1] - 1] + auxTableau[0, 0:tableau.shape[1] - 1]

    # the new tableau now uses the values from  the auxiliary tableau in all rows minus C value
    newTableau[1:tableau.shape[0], 0:tableau.shape[1] - 1] = auxTableau[1:tableau.shape[0], 0:tableau.shape[1] - 1]
    # rewrites the B values
    newTableau[..., tableau.shape[1] - 1] = auxTableau[..., auxTableau.shape[1] - 1]

    return newTableau


def pivot(position: list, tableau: np):
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

    #print(tableau)
    #print()


def makeFPI(tableau: np, size):
    slack = np.vstack((np.zeros((1, size[0])), np.identity(size[0])))
    tableau = np.hsplit(tableau, (tableau.shape[1] - 1, tableau.shape[1]))
    tableau = np.hstack((tableau[0], slack, tableau[1]))
    return tableau


def solveSimplex(tableau: np, size):
    # These three lines add the identity matrix to the problem
    # First you set an identity matrix with vstack to the size of your columns 'size[0]'
    # then you split your original simplex as the A matrix and the B column, you then stack it together with your generated slack matrix

    output = open('output.txt', 'w')
    # print("\n\nsolveSimplex")
    # print(tableau)
    #i = 0
    #for x in tableau:
    #    tableau[i] = np.array([truncate(xi) for xi in x])
    #    i += 1
    # print("truncado")
    # print(tableau)
    # print("\n\n")
    # sets standard values for checks
    returnDual = 1
    returnPrimal = 1

    # logical check whether your tableau is in FPI format
    auxBool = isFPI(tableau, size[0])
    # print(tableau)
    # print("\n\nAuxBool")
    # print(auxBool)


    # if in FPI, attempt to apply the DUAL method
    if auxBool:
        print("DUAL")
        returnDual = simplexDual(tableau, size)

    # if Dual was successful,
    # print("returnDual")
    # print(returnDual)
    # print("\n")
    if returnDual == 0:
        printOptimalSolution(getX(tableau, getBase(tableau, size[0]), size[1]), (-1 * tableau[0, tableau.shape[1] - 1]),
                             optimalCertificate(tableau, size[0]), output)
        return "OPT"

    # if Dual was not possible
    if returnDual == 1:
        print("PRIMAL")
        # if in FPI try PRIMAL method
        if auxBool:
            returnPrimal = simplexPrimal(tableau, size)

        # if Primal was not effective or problem is not fully solved yet, attempt Auxiliary Method
        if not isBasicSolution(tableau, size) or returnPrimal == 1:
            print("AUX")
            # print(tableau)
            auxTableau = buildAuxTableau(tableau)
            #print(auxTableau)
            # print()
            returnPrimal = simplexPrimal(auxTableau, size)

            # if the AUX method was sucessful
            if returnPrimal == 0:

                # if sol value is > 0 its not viable
                if auxTableau[0, auxTableau.shape[1] - 1] > 0:
                    printInvCertificate(optimalCertificate(tableau, size[0]) - np.ones(size[0]), output)
                    return "INV"

                # if sol value = 0, refactor the original tableau, get the base, get the canon column and pivot it
                elif auxTableau[0, auxTableau.shape[1] - 1] == 0:
                    tableau = refactorTableau(tableau, auxTableau)
                    canon = getBase(auxTableau, size[0])
                    aux1 = 1
                    print("ORIGINAL")

                    while aux1 <= size[0]:
                        pivot([aux1, canon[aux1 - 1]], tableau)
                        aux1 += 1

        # reattempt the PRIMAL method
        returnPrimal = simplexPrimal(tableau, size)
        # print("RETORNO PRIMAL POS AUX")
        # print(returnPrimal)

        # If PRIMAL was sucessful
        if returnPrimal == 0:
            printOptimalSolution(getX(tableau, getBase(tableau, size[0]), size[1]),
                                 (-1 * tableau[0, tableau.shape[1] - 1]),
                                 optimalCertificate(tableau, size[0]), output)
            return "OPT"

    # Unbounded Certificate
    if returnDual == 2 or returnPrimal == 2:
        printUnbCertificate(unbCertificate(tableau, getBase(tableau, size[0])), output)
        return "UNB"

    # Not valid certificate
    if returnDual == 3 or returnPrimal == 3:
        printInvCertificate(invCertificate(tableau, size[0]), output)
        return "INV"

    return False


# endregion

def almostInt(a):
    c = 1.0000000000000000000000000000000
    global epsilon
    if (a % c != 0):
        b = (a%c)
        #print(b)
        if b < epsilon or b + epsilon >= 1:
            print("True %f" %b)
            return True
        else:
            print("False %f" % b)
            return False
    else:
        print("for a = %f" %a)
        print("True %f" %(a %c))
        return True


def isPI(tableau: np, size):
    partSol = getX(tableau, getBase(tableau, size[0]), size[1])
    #partSol = np.array([float(truncate(xi)) for xi in partSol])
    print("\nPartSol")
    print(partSol)
    #input()
    a = True
    col = -1
    lin = -1
    fv = -1
    for xi in partSol:
        print("xi in partSol")
        if not almostInt(xi):
            a = False
    if a and (partSol >= 0).all():
        print("TUDO INTEIRO POSITIVO")
        print(partSol)
        optimal[1] = partSol
        optimal[2] = optimalCertificate(tableau, size[0])
        return [col, lin, fv, "INT"]
    elif a and (partSol < 0).any():
        print("Tem negativo no B e B todo inteiro!")
        print(partSol)
        return [col, lin, fv, "NEGINT"]
    elif (partSol < 0).any():
        print("Tem negativo no B! E B não é todo inteiro!")
        print(partSol)
        l = [s % 1 for s in partSol]
        m = min(i for i in l if i != 0 and not almostInt(i))
        col = np.where(l == m)[0][0]
        print("COL")
        print(col)
        #gc = input()
        lin = np.transpose((tableau[1:tableau.shape[0], col] == 1).nonzero())
        lin = lin[0][0] + 1
        print("lin")
        print(lin)
        fv = partSol[col]
        returnVL = [lin, col, fv, "NEGNINT"]
        return returnVL
    else:
        print("B positivo! E B não é todo inteiro!")
        print(partSol)
        l = [s % 1 for s in partSol]
        print(l)
        m = min(i for i in l if i != 0 and not almostInt(i))
        col = np.where(l == m)[0][0]
        print("COL")
        print(col)
        gc = input()
        lin = np.transpose((tableau[1:tableau.shape[0], col] == 1).nonzero())
        lin = lin[0][0] + 1
        print("lin")
        print(lin)
        fv = partSol[col]
        returnVL = [lin, col, fv, "NINT"]
        return returnVL


def addBnBRest(tableau: np, tuple, size, type):
    slack = np.zeros((size[0] + 1, 1))
    tableau = np.hsplit(tableau, (tableau.shape[1] - 1, tableau.shape[1]))
    tableau = np.hstack((tableau[0], slack, tableau[1]))
    rest = np.zeros((1, tableau.shape[1]))[0]
    rest[tuple[1]] = 1 if type == '<' else -1
    rest[tableau.shape[1] - 2] = 1
    rest[tableau.shape[1] - 1] = math.floor(tuple[2]) if type == '<' else -1 * math.ceil(tuple[2])
    #print("\nREST")
    #print(rest)
    #print(type)
    #print(tableau[tuple[0], :])
    #print("\n")
    rest = (rest - tableau[tuple[0], :]) if type == '<' else (rest + tableau[tuple[0], :])
    #print("\nREST Pivoteado")
    #print(rest)
    #print("\n")
    tableau = np.vstack((tableau, rest))
    #print("\nTableau Resultante")
    #print(tableau)
    #print("\n")
    # a = input()
    return tableau


def addCutPlanRest(tableau: np, tuple, size):
    slack = np.zeros((size[0] + 1, 1))
    tableau = np.hsplit(tableau, (tableau.shape[1] - 1, tableau.shape[1]))
    tableau = np.hstack((tableau[0], slack, tableau[1]))
    rest = np.zeros((1, tableau.shape[1]))[0]
    print(tuple)
    #input()
    rest = tableau[tuple[0], :].copy()
    print("REST PRE FLOOR")
    print(rest)
    rest = np.floor(rest)
    rest[tableau.shape[1] - 2] = 1
    print("Rest Inicial")
    print(rest)
    rest = (rest - tableau[tuple[0], :])
    print("Rest Pivoteado")
    print(rest)
    tableau = np.vstack((tableau, rest))
    print("New Tableau")
    print(tableau)
    #gc = input()
    return tableau


def pickPivotCutPlan(tableau : np, size):
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
                if ((tableau[aux1, aux2]) < 0 and (tableau[0, aux2]) > 0 and (
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

def branchAndBound(tableau: np, size):
    # if size[0] < 50:
    size1 = size.copy()
    size2 = size.copy()
    tableau1 = tableau.copy()
    tableau2 = tableau.copy()
    global optimal
    global result1
    global result2
    global status
    print("\n\n----------------Branch and Bound Simplex-----------------\n")
    print(tableau1)
    tuple = isPI(tableau1, size)
    if tuple[3] == "INT":
        print("Inteiro")
        if optimal[0] <= (-1 * tableau1[0, tableau1.shape[1] - 1]):
            optimal[0] = (-1 * tableau1[0, tableau1.shape[1] - 1])
    elif tuple[3] == "NEGINT":
        input()
        print("Negative Inteiro")
        print(tableau1)
        print("pos Dual")
        simplexDual(tableau1, size1)
        result1 = solveSimplex(tableau1, size1)
        simplexDual(tableau2, size2)
        result2 = solveSimplex(tableau2, size2)
        print(tableau1)
        branchAndBound(tableau1, size1)
        branchAndBound(tableau2, size2)
    elif tuple[3] == "NEGNINT" and result1 == "OPT":
        print("Negative Nao Inteiro")
        print(tableau1)
        print("pos Dual")
        pos = pickPivotCutPlan(tableau1, size1)
        pivot(pos, tableau1)
        pos = pickPivotCutPlan(tableau2, size2)
        print(tableau1)
        tableau1 = addBnBRest(tableau1, tuple, size1, '<')
        tableau2 = addBnBRest(tableau2, tuple, size2, '>')
        print(tableau1)
        size1[0] += 1
        size2[0] += 1
        print(tuple)
        # gc = input()
        result1 = solveSimplex(tableau1, size1)
        result1 = solveSimplex(tableau1, size2)
        print("Tableau pos solve")
        print(tableau1)
        # gc = input()
        cutPlanSimplex(tableau1, size1)
    elif tuple[3] == "NINT" and (result1 == "OPT" or result2 == "OPT"):
        print("Nao Inteiro <")
        print(tableau1)
        simplexDual(tableau1, size1)
        simplexDual(tableau2, size2)
        print(tableau1)
        tableau1 = addBnBRest(tableau1, tuple, size1, '<')
        tableau2 = addBnBRest(tableau2, tuple, size2, '>')
        size2[0] += 1
        size1[0] += 1
        print(tuple)
        simplexDual(tableau1, size1)
        simplexDual(tableau2, size1)
        result1 = solveSimplex(tableau1, size1)
        result2 = solveSimplex(tableau2, size2)
        print("Tableau pos solve")
        print(tableau1)
        # gc = input()
        branchAndBound(tableau1, size1)
        branchAndBound(tableau2, size2)

def cutPlanSimplex(tableau: np, size):
    # if size[0] < 50:
    size1 = size.copy()
    tableau1 = tableau.copy()
    global optimal
    global result1
    global status
    print("\n\n----------------Cut Plans Simplex-----------------\n")
    print(tableau1)
    tuple = isPI(tableau1, size)
    if tuple[3] == "INT":
        print("Inteiro")
        if optimal[0] <= (-1 * tableau1[0, tableau1.shape[1]-1]):
            optimal[0] = (-1 * tableau1[0, tableau1.shape[1]-1])
    elif tuple[3] == "NEGINT":
        print("Negative Inteiro")
        print(tableau1)
        print("pos Dual")
        simplexDual(tableau1, size1)
        print(tableau1)
        #gc = input()
        cutPlanSimplex(tableau1, size1)
    elif tuple[3] == "NEGNINT" and result1 == "OPT":
        print("Negative Nao Inteiro")
        print(tableau1)
        print("pos Dual")
        pos = pickPivotCutPlan(tableau1, size1)
        pivot(pos, tableau1)
        print(tableau1)
        tableau1 = addCutPlanRest(tableau1, tuple, size1)
        print(tableau1)
        size1[0] += 1
        print(tuple)
        #gc = input()
        result1 = solveSimplex(tableau1, size1)
        print("Tableau pos solve")
        print(tableau1)
        #gc = input()
        cutPlanSimplex(tableau1, size1)
    elif tuple[3] == "NINT" and result1 == "OPT":
        print("Nao Inteiro")
        print(tableau1)
        tableau1 = addCutPlanRest(tableau1, tuple, size1)
        size1[0] += 1
        print(tuple)
        simplexDual(tableau1, size1)
        result1 = solveSimplex(tableau1, size1)
        print("Tableau pos solve")
        print(tableau1)
        #gc = input()
        cutPlanSimplex(tableau1, size1)





        # gc = input()
