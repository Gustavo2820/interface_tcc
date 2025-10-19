from random import randint,seed
from itertools import product
from copy import copy

def funcObj(qtd):
    i=0
    lista = []
    while i<3:
        lista.append(randint(1, 9))
        i += 1
    return tuple(lista)

def otim():
    seed(1)
    tam = 6
    combinations = list(product([True, False], repeat=tam))
    combinations = combinations[:-1]

    combs = [combinations[0]]
    objs = [funcObj(tam)]
    todascombs = copy(combinations)
    todosobs = copy(objs)

    for combination in combinations[1:]:
        obj = funcObj(tam)
        todosobs.append(obj)

        i = 0
        menor = True
        while (i < len(combs)):
            # if obj[0] < objs[i][0] or obj[1] < objs[i][1] or obj[2] < objs[i][2]:
            menor = menor and (obj[0] < objs[i][0] or obj[1] < objs[i][1] or obj[2] < objs[i][2])

            if (obj[0] < objs[i][0] and obj[1] < objs[i][1] and obj[2] < objs[i][2]
                or obj[0] == objs[i][0] and obj[1] < objs[i][1] and obj[2] < objs[i][2]
                or obj[0] < objs[i][0] and obj[1] == objs[i][1] and obj[2] < objs[i][2]
                or obj[0] < objs[i][0] and obj[1] < objs[i][1] and obj[2] == objs[i][2]
                or obj[0] == objs[i][0] and obj[1] == objs[i][1] and obj[2] < objs[i][2]
                or obj[0] == objs[i][0] and obj[1] < objs[i][1] and obj[2] == objs[i][2]
                or obj[0] < objs[i][0] and obj[1] == objs[i][1] and obj[2] == objs[i][2]
            ):
                combs.pop(i)
                objs.pop(i)
                i -= 1
            i += 1

        if menor:
            combs.append(combination)
            objs.append(obj)

    print(f"Todos combinations: {todascombs}, Tam:{len(todascombs)}")
    print(f"Todos objs: {todosobs}, Tam:{len(todosobs)}")
    print(f"Combinations final: {combs}, Tam:{len(combs)}")
    print(f"Objs final: {objs}, Tam:{len(objs)}")


otim()
