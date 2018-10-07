import random, sys, numpy as np, fileinput, logging;

# приведенные к нормальной форме данные
a = [[13.2, 1.9, 2.3], [0.8, -7.3, -0.7], [0.5, -1.4, -9.6]]
b = [5.12, 5.2, 1.5]
# ограничитель
epsilon = 0.0000001


def count_solution(a, b, epsilon):
    # получим величину матрицы
    eqSize = a.__len__()
    print(eqSize)
    # массив для хранения предыдущих х
    # заполним его нулями перед началом работы метода ПИ. newX - массив новых значений х
    prevX = []
    newX = []
    for i in range(eqSize):
        prevX.append(0)
        newX.append(0)

    # массив для хранения разницы значений newX и prevX
    ds = []
    # счетчик для обработки уравнений, переменная выхода из цикла while
    i = 0
    contWhile = True
    # переменная для хранения суммы коэффициентов, помноженных на предыдущие значение х
    sumQs = 0
    # цикл обработки уравнений МПИ
    while (contWhile):
        for eq in a:
            # получим массив коэффициентов не при текущем x и сумму коэффициентов, помноженных на х
            for j in range(len(eq)):
                if j != i:
                    sumQs += eq[j] * prevX[j] * (-1)
                else:
                    currentQ = eq[j]
            # посчитаем текущий икс с прошлым значением и получим следующий вариант
            newX[i] = (b[i] + sumQs) / currentQ
            i += 1
            sumQs = 0
        for j in range(len(newX)):
            ds.append(abs(prevX[j] - newX[j]))
            prevX[j] = newX[j]
        for d in ds:
            if d < epsilon:
                contWhile = False
        i = 0

        ds.clear()
    for x in prevX:
        print(x)


################################

def genCoeffs(size):
    coeffs = list()
    for row in range(size):
        rowList = list()
        sumQ = 0
        for col in range(size):
            if row == col:
                rowList.append(0)
            else:
                e = float(random.randint(-100,100))/10
                rowList.append(e)
                sumQ+=abs(e)
        eDiagonal = float(random.randint(-1000,1000))/10
        while abs(eDiagonal) < sumQ:
            delta = sumQ - abs(eDiagonal) + random.randint(5,25)
            if eDiagonal > 0:
                eDiagonal+=delta
            else:
                eDiagonal-=delta
        rowList[row] = eDiagonal

        coeffs.append(rowList)
    return np.matrix(coeffs, dtype='float')

def genB(size):
    bList = list()
    for b in range(size):
        bList.append(float(random.randint(-100,100))/10)
    return np.matrix(bList, dtype='float')

def createRandomCoeffs():
    size = random.randint(1,20)
    coeffs = genCoeffs(size)
    b = genB(size)
    approx = 0.001
    print(coeffs, b, approx)
    return coeffs, b, approx

def readMatrix(rawInput=""):
    matrix = None
    try:
        size = int(input("enter matrix size\n"))
    except:
        print("you must have typed in integer value!")
        exit(0)
    print("enter coefficients")
    for i in range(size):
        rawInput += input()
    # if (rawInput == ""):
    #     for line in fileinput.input():
    #         rawInput += line
    try:
        matrix = np.matrix(rawInput, dtype='float')
    except (ValueError, SyntaxError) as err:
        logging.info('Can''t read the matrix. Error: {}'.format(err))
        print('use only digits, columns should be separated by ";"')

    return matrix


def validCoeffs(coeffs):
    row, col = coeffs.shape  # !
    if row != col:
        print("Matrix should be squared")
        return False
    if np.linalg.det(coeffs) == 0:
        print("Determinant mustn't be 0")
        return False
    return True


def validBs(matrixB, coeffSize):
    bIsValid = (matrixB.shape == (1, coeffSize)) or (matrixB.shape == coeffSize, 1)
    if not bIsValid:
        print("B must be the same size as matrix")
    return bIsValid


def makeDiagonal(coeffs, b):
    for i in range(b.size):
        for j in range(i + 1, b.size):
            logging.info("\n {} >= sum({}) - {}".format(coeffs[j, i], coeffs[j], coeffs[j, i]))

            absSum = 0
            for row in coeffs[j]:
                for e in range(row.size):
                    absSum += abs(row.item(e))

            if (abs(coeffs.item(j, i)) >= (absSum - abs(coeffs.item(j, i)))):
                coeffs[j], coeffs[i] = coeffs[i].copy(), coeffs[j].copy()
                b[0, j], b[0, i] = b[0, i].copy(), b[0, j].copy()

            logging.info("\n new coefficients:\n{}".format(coeffs))
            logging.info("\n new B:\n{}\n".format(b))

    for i in range(b.size):
        absSum = 0
        for row in coeffs[i]:
            for e in range(row.size):
                absSum += abs(row.item(e))
        if abs(coeffs.item(i, j)) < (absSum - abs(coeffs.item(i, i))):
            return None, None

    logging.info("\nDiagonals:\nMatrix\n{}\nB\n{}\n".format(coeffs, b))
    return coeffs, b


##################################

def readInput():

    coeffs = readMatrix()
    if coeffs is None:
        exit(-1)
    print("Your matrix:\n{}".format(coeffs))
    logging.info("\nMatrix:\n{}".format(coeffs))
    if not validCoeffs(coeffs):
        exit(-2)

    print("Enter B coefficients")
    b = readMatrix()
    if b is None:
        exit(-1)
    print("B's:\n{}".format(b))
    if not validBs(b, coeffs.shape(0)):
        exit(-2)
    if (b.shape[0] != 1):
        logging.info("Transposing B")
        b = b.getT()
    coeffsDiagonaled, bDiagonaled = makeDiagonal(coeffs, b)
    if coeffsDiagonaled is None or bDiagonaled is None:
        print("Can't make diagonal matrix")
        exit(-3)

    print("What approximation should we use?")
    try:
        approx = float(input())
    except ValueError as err:
        logging.info("Enter correct approximation. We caught: {}".format(err))
        print("Approximation value fail")

    return (coeffsDiagonaled, bDiagonaled, approx)




def reafFromFile(filename):
    with open(filename) as file:
        lines = file.readlines()

    approx = None
    try:
        coefStart = lines.index("Coeffs:\n")
        coefEnd = lines.index("B:\n")
        coefStr = ""
        for line in range(coefStart+1, coefEnd):
            coefStr+=(lines[line])

        bStart = coefEnd
        bEnd = lines.index("Epsilon:\n")
        bStr = ""
        for line in range(bStart+1, bEnd):
            bStr += (lines[line])

        approx = float(lines[bEnd+1])
    except ValueError as err:
        print("Incorrect file")
        logging.info("Error: {}".format(err))
        exit(-4)

    coeffs,b = (readMatrix(coefStr), readMatrix(bStr))
    if coeffs is None or b is None:
        exit(-1)
    if not validCoeffs(coeffs) or not validBs(b, coeffs.shape[0]):
        exit(-2)

    coeffsDiagonaled, bDiagonaled = makeDiagonal(coeffs, b)
    if coeffsDiagonaled is None or bDiagonaled is None:
        print("Diagonal coefficients trouble")
        exit(-3)

    return (coeffsDiagonaled, bDiagonaled)



def countSolution(coeffs, b, approx):
    n = b.size
    x = b.copy()
    logging.info("\n X:\n{}".format(x))
    iterationsCount = 0
    delta = list()
    while True:
        iterationsCount += 1
        max_delta = 0
        prevX = x.copy()
        for row in range(n):
            xNew = b[0, row]
            for col in range(n):
                if col != row:
                    logging.info("\n new temporary xs: {} -= {} * {}".format(xNew, coeffs[row,col], prevX[0,col]))
                    xNew -= (coeffs[row, col] * prevX[0, col])
                xNew/=coeffs[row,row]
                logging.info("\n new X: {}".format(xNew))
                x[0,row] = xNew

                logging.info("\n Delta: {}".format(abs(xNew-prevX[0,row])))
                max_delta = max(max_delta, abs(xNew - prevX[0, row]))
                solutionFound = max_delta < approx

        logging.info("\nNew x:\n{}\n".format(x))
        delta.append(max_delta)
        if solutionFound:
            break
    return (x, iterationsCount, delta)


if __name__ == "__main__":
    logging.basicConfig(filename="log.log",
                        format='%(asctime)-15s %(funcName)s %(message)s',
                        level=logging.DEBUG)
    if len(sys.argv) > 1:
        if sys.argv[1] == "rand":
            coeffs, b, approx = createRandomCoeffs()
        elif sys.argv[1] == "file":
            if len(sys.argv) == 3:
                try:
                    coeffs, b, approx = reafFromFile(sys.argv[2])
                except  FileNotFoundError:
                    print("file not found")
                    exit(1)
            else:
                print("you must write filename")
                exit(0)
        else:
            print("run program with 'random' param er without params")
            exit(0)
    else:
        coeffs, b, approx = readInput()

    answer, iterations, delta = countSolution(coeffs, b, approx)
    print("answer:\n{}".format(answer))
    print("iterations: {}".format(iterations))
    print("Deltas: {}".format(delta))