from copy import deepcopy
import random


class Tren:
    def __init__(self, numero_vagones, operacion, matricula):
        self.numero_vagones = numero_vagones
        self.operacion = operacion
        self.matricula = matricula

    def __str__(self):
        return "Número de vagones: " + str(self.numero_vagones) + "\n" + \
            "Muelle de operaciones: " + str(self.operacion) + "\n" + \
            "Matrícula: " + str(self.matricula) + "\n"


def producir_lista_trenes_aleatoria(n, min_vagones, max_vagones):
    lista_trenes = []
    for i in range(n):
        numero_vagones = random.randint(min_vagones, max_vagones)
        operacion = random.choice(["gas", "carbón", "contenedores"])
        lista_trenes.append(Tren(numero_vagones, operacion, i))
    return lista_trenes


def crear_cola_de_trenes(lista_de_trenes):
    auxiliar = lista_de_trenes
    random.shuffle(auxiliar)
    return auxiliar


class Cola_de_trenes(list):
    def __init__(self, lista_de_trenes, create=True):
        if create:
            list.extend(self, crear_cola_de_trenes(lista_de_trenes))
        else:
            list.extend(self, lista_de_trenes)

    def __str__(self):
        cadena = ""
        for i in list(self):
            cadena += (str(i) + "\n")
        return cadena


random.seed(2024)



def trains_mate(indv1, indv2):
    cut = random.randint(0, len(indv1) - 1)

    f_half_new_invd1 = indv1[:cut]
    f_half_new_invd2 = indv1[cut:]

    l_half_new_invd1 = deepcopy(indv2)
    l_half_new_invd2 = []

    for train1 in f_half_new_invd1:
        for train2 in indv2:
            if train1.matricula == train2.matricula:
                for i, t in enumerate(l_half_new_invd1):
                    if train1.matricula == t.matricula:
                        l_half_new_invd1.pop(i)
                        l_half_new_invd2.append(train2)

    new_indv1 = f_half_new_invd1 + l_half_new_invd1
    new_indv2 = f_half_new_invd2 + l_half_new_invd2

    return new_indv1, new_indv2


def train_swap(indivuduo, indpb):
    indivuduo = deepcopy(indivuduo)
    if random.random() < indpb:
        pos1 = random.randint(0, len(indivuduo) - 1)
        pos2 = random.randint(0, len(indivuduo) - 1)

        while pos2 == pos1:
            pos2 = random.randint(0, len(indivuduo) - 1)

        train1 = indivuduo[pos1]
        train2 = indivuduo[pos2]
        indivuduo[pos1] = train2
        indivuduo[pos2] = train1

    return indivuduo,


def tiempo_total(indiv):
    sum = 0
    for tren in indiv:
        sum += tren.numero_vagones

    return sum


def evaluar_cola(individuo):
    muelle_gas = 1
    muelle_carbon = 1
    muelle_contenedores = 1
    id_tren = 0
    t_espera = 0

    for i in range(tiempo_total(individuo)):

        if id_tren < len(individuo):
            if (individuo[id_tren].operacion == "gas" and muelle_gas > 0) | (
                    individuo[id_tren].operacion == "carbón" and muelle_carbon > 0) | (
                    individuo[id_tren].operacion == "contenedores" and muelle_contenedores > 0):
                t_espera += 1

        muelle_gas -= 1
        muelle_carbon -= 1
        muelle_contenedores -= 1

        if id_tren >= len(individuo) and muelle_carbon <= 0 and muelle_contenedores <= 0 and muelle_gas <= 0:
            break

        for _ in range(3):

            if id_tren >= len(individuo):
                break

            if individuo[id_tren].operacion == "carbón" and muelle_carbon <= 0:
                muelle_carbon = individuo[id_tren].numero_vagones
                id_tren += 1
                continue
            if individuo[id_tren].operacion == "contenedores" and muelle_contenedores <= 0:
                muelle_contenedores = individuo[id_tren].numero_vagones
                id_tren += 1
                continue

            if individuo[id_tren].operacion == "gas" and muelle_gas <= 0:
                muelle_gas = individuo[id_tren].numero_vagones
                id_tren += 1
                continue

        continue

    return t_espera - 1,

# Pruebas en las funciones

# Función de mutación

Cola_tren_sin_mut = Cola_de_trenes([Tren(1, "gas", 1), Tren(2, "carbón", 2), Tren(3, "contenedores", 3)], create=False)
Cola_tren_mut = train_swap(Cola_tren_sin_mut, indpb=10.1)

print("PRUEBA MUTACION")
print(Cola_tren_sin_mut)
print(Cola_tren_mut[0])




# Función de cruce

lista_trenes = producir_lista_trenes_aleatoria(10, 1, 10)
padre1 = Cola_de_trenes(lista_trenes)
padre2 = Cola_de_trenes(lista_trenes)

print("PRUEBA CRUCE")
hijos = trains_mate(padre1, padre2)
print(f'Padre1: {padre1}')
print(f'Padre2: {padre2}')
print(f'Primer hijo: {Cola_de_trenes(hijos[0], create=False)}')
print(f'Segundo hijo: {Cola_de_trenes(hijos[1], create=False)}')



# Funcion de aptitud

print("PRUEBA DE EVALUACIÓN")
cola = Cola_de_trenes(producir_lista_trenes_aleatoria(10, 2, 6))
print(f'Unidades de tiempo de espera / aptitud del individuo = {evaluar_cola(cola)[0]}')
print("\n")
print(f'Individuo = {cola}')
print("Traza = Entran trenes 0, 5 y 6, tren 4 espera 4 u; entra 4 y 1 espera 2 u, entra 2 porque 0 ya acabó y 7 espera por 1 durante 4 u.")
print("8 espera 7 por 4 u; 3 y 9 entran porque gas y carbón están libres.")
print("Tiempo de espera total = 14")