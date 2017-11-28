import numpy as np


# region OptimalFucntions

def getBase(tableau: np, dimension):
    # gets all positions in the first row where value is zero
    auxArray = np.transpose((tableau[0, 0:tableau.shape[1] - 1] == 0).nonzero())
    # sets an array with the size of the dimension (number of columns)
    base = np.full(dimension, -1)

    # if the zeroes are < dimension something is wrong and we do not have a base
    if auxArray.size < dimension:
        return base

    aux1 = 0
    # for eah column
    while aux1 < auxArray.shape[0]:
        # we check wether in that specific column there are exaclty One 1 and the rest of the elements are zeroes
        if (np.transpose((tableau[1:tableau.shape[0], auxArray[aux1][0]] == 1).nonzero()).size == 1 and np.transpose(
                (tableau[1:tableau.shape[0], auxArray[aux1][0]] == 0).nonzero()).size == tableau[1:tableau.shape[0],
                                                                                         0].size - 1) and \
                        base[
                            np.transpose((tableau[1:tableau.shape[0], auxArray[aux1][0]] == 1).nonzero())[0][0]] == - 1:
            # if yes this will be one of the bases
            base[np.transpose((tableau[1:tableau.shape[0], auxArray[aux1][0]] == 1).nonzero())[0][0]] = auxArray[aux1][
                0]
        aux1 += 1

    return base


def optimalCertificate(tableau: np, lin):
    certificate = np.negative(tableau[0, tableau.shape[1] - (lin + 1):tableau.shape[1] - 1])
    return certificate


def isBasicSolution(tableau, size):
    # gets the lien from the tableau that contains the X vector
    solX = getX(tableau, getBase(tableau, size[0]), tableau.shape[1] - 1)

    # if all the values are GEQ 0 it is a basic solution
    if (solX >= 0).all():
        return True
    return False


def isDone(tableau):
    # if C <= 0 (Reversed logic because I only realized I had been doing it backwards too far into this)
    if (tableau[0, 0:tableau.shape[1] - 1] <= 0).all():

        # if vector B >= 0 its Done.
        if (tableau[1:tableau.shape[0], tableau.shape[1] - 1] >= 0).all():
            return True
    return False


def getX(tableau: np, base: np, col):
    aux1 = 0
    print("\n------getX------\n")
    # creates a vector with the size of the X vector.
    solX = np.full(tableau.shape[1] - 1, 0, dtype=np.float)

    # copies the x vector from the tableau into the Solution vector.
    # print(tableau[:, tableau.shape[1]-1])
    # print(solX)
    while aux1 < base.shape[0]:
        # print(aux1)
        # print(base.shape[0])
        solX[base[aux1]] = tableau[aux1 + 1, tableau.shape[1] - 1]
        aux1 += 1

    # returns the solution Vector
    # print(solX)
    return solX[0:col]


def printOptimalSolution(sol_o: np, val_ob, certificate: np, op):
    print("Solução ótima x = {0}, com valor objetivo {1}, e certificado y = {2}".format(sol_o, val_ob, certificate))


def printIntSolution(sol_o: np, val_ob, certificate: np):
    print("Solução inteira x = {0}, com valor objetivo {1}, e certificado y = {2}".format(sol_o, val_ob, certificate))


# endregion



# region InviavelFunctions
def invCertificate(tableau: np, lin):
    aux = 1
    certificate = np.full(lin, -1)

    while aux < tableau.shape[0]:
        # if the values for the variables are all negative and the B value is positive or vice versa for any given row...
        if (((tableau[aux, 0:tableau.shape[1] - 1] <= 0).all() and (
                    tableau[aux, 0:tableau.shape[1] - 1] != 0).any() and (tableau[aux, tableau.shape[1] - 1] > 0)) or
                ((tableau[aux, 0:tableau.shape[1] - 1] >= 0).all() and (
                            tableau[aux, 0:tableau.shape[1] - 1] != 0).any() and (
                    tableau[aux, tableau.shape[1] - 1] < 0))):
            certificate = tableau[aux, tableau.shape[1] - (lin + 1):tableau.shape[1] - 1]
        aux += 1

    return certificate


def checkInvTableau(tableau: np):
    aux = 1
    while aux < tableau.shape[0]:
        # if the val    ues for the variables are all negative and the B value is positive or vice versa for any given row...
        if (((tableau[aux, 0:tableau.shape[1] - 1] <= 0).all() and (tableau[aux, 0:tableau.shape[1] - 1] != 0).any() and
                 (tableau[aux, tableau.shape[1] - 1] > 0)) or ((tableau[aux, 0:tableau.shape[1] - 1] >= 0).all() and
                                                                   (tableau[aux,
                                                                    0:tableau.shape[1] - 1] != 0).any() and (
            tableau[aux, tableau.shape[1] - 1] < 0))):
            return True

        aux += 1

    return False


def printInvCertificate(certificate: np, op):
    print("PL inviável, aqui está um certificado {}".format(certificate))


# endregion


# region UnboundedFucntions
def unbCertificate(tableau: np, base: np):
    aux1 = 0
    certificate = np.full(tableau.shape[1] - 1, 0, dtype=np.float)

    while aux1 < base.shape[0]:
        certificate[base[aux1]] = - tableau[aux1 + 1, getUnbCol(tableau)]
        aux1 += 1

    certificate[getUnbCol(tableau)] = 1
    return certificate


def getUnbCol(tableau: np):
    aux = 0
    while aux < tableau.shape[1]:
        # if all variables in a column are <= 0 and at least one is not 0 and the corresponding C element is > 0
        if (((tableau[1:tableau.shape[0], aux] <= 0).all() and (tableau[1:tableau.shape[0], aux] != 0).any() and
                 (tableau[0, aux] > 0))):
            return aux
        aux += 1


def checkUnbTableau(tableau: np):
    aux = 0
    while aux < tableau.shape[1]:
        # if all variables in a column are <= 0 and at least one is not 0 and the corresponding C element is > 0
        if (((tableau[1:tableau.shape[0], aux] <= 0).all() and (tableau[1:tableau.shape[0], aux] != 0).any() and
                 (tableau[0, aux] > 0))):
            return True

        aux += 1

    return False


def printUnbCertificate(certificate: np, op):
    print("PL ilimitada, aqui está um certificado {}".format(certificate))
    # endregion