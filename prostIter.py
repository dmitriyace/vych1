# приведенные к нормальной форме данные
a = [[13.2, 1.9, 2.3], [0.8, -7.3, -0.7], [0.5, -1.4, -9.6]]
b = [5.12, 5.2, 1.5]
# ограничитель
epsilon = 0.0001


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
        ds.append(abs(prevX[j]-newX[j]))
        prevX[j]=newX[j]
    for d in ds:
        if d < epsilon:
            contWhile = False
    i = 0

    ds.clear()
for x in prevX:
    print(x)
