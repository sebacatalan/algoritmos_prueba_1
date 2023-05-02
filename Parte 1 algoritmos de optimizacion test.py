import re
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, solve

restricciones = ['x1 + x2 <= 700','5x1+8x2<=5000']
objetivo = 'max z = 0.08x1 + 0.1x2' #funciuon de prueba

#------------------------------------- FUNCION OBJETIVO------------------------------------------

# objetivo = input("Ingrese la función objetivo: ")


# Extraer los coeficientes de la función objetivo
coeficientes_objetivo = re.findall(r'\b\d*x\d*\b', objetivo)
coef_obj_dict = {}
for coef in coeficientes_objetivo:
    valor = coef.replace("x1", "").replace("x2", "").replace("*", "")
    valor = int(valor) if valor else 1
    if "x1" in coef:
        coef_obj_dict["x1"] = valor
    elif "x2" in coef:
        coef_obj_dict["x2"] = valor
    # coef_obj_dict["z"] = 0 if coef_obj_dict.get("z") is None else coef_obj_dict.get("z")
    
valor2 = 0

#Definir la ecuacion de la recta correspondiente
m = coef_obj_dict['x1']
b = coef_obj_dict['x2'] *valor2
z = lambda x1: m * x1 + b


# Crear una función de la forma z = ax + by + c
# def crear_funcion(coef_dict):
#     a = coef_dict.get("x1", 0)
#     b = coef_dict.get("x2", 0)
#     c = coef_dict.get("z", 0)
#     return lambda x: (-a*x + c)/b if b != 0 else np.nan

print(coef_obj_dict)

#-------------------------------------------- RESTRICCIONES ----------------------------------


# restricciones = ["0x1 + 2x2 >= 12", "3x1 - 2x2 <= 18","8x1 + 9x2 <= 7","x1 + x2 <=4"]
# restricciones = []
# while True:
#     restriccion = input("Ingrese una restricción (o escriba 'fin' si terminó): ")
#     if restriccion == "fin":
#         break
#     restricciones.append(restriccion)

# Crear el diccionario principal
diccionario_restricciones = {}

for i, restriccion in enumerate(restricciones):
    # Crear un diccionario para cada restricción
    coeficientes = re.findall(r'\b\d*x\d*\b', restriccion)
    coef_dict = {}
    for coef in coeficientes:
        valor = coef.replace("x1", "").replace("x2", "").replace("*", "")
        valor = int(valor) if valor else 1
        if "x1" in coef:
            coef_dict["x1"] = valor
        elif "x2" in coef:
            coef_dict["x2"] = valor
    
    # Obtener el signo y el término independiente
    signo = "<="
    if ">=" in restriccion:
        signo = ">="
    elif "<=" in restriccion:
        signo = "<="
    termino_independiente = re.findall(r'(?<=[<=>])\s*-?\d+', restriccion)
    termino_independiente = int(termino_independiente[0]) if termino_independiente else 0
    
    # Agregar el signo y el término independiente al diccionario
    coef_dict["signo"] = signo
    coef_dict["termino_independiente"] = termino_independiente
    
    # Agregar el diccionario de coeficientes al diccionario principal
    diccionario_restricciones[f"restriccion_{i+1}"] = coef_dict

print(diccionario_restricciones)
# print(diccionario_restricciones["restriccion_2"]['x1'])
    
    

#coeficientes de la funcion objetivo
# coeficientes = re.findall(r'\d+', objetivo)
# coeficientes = [int(c) for c in coeficientes]
# print('coef',coeficientes)



#si es max o min
if "max" in objetivo:
    signo = -1  
    print('max')
else:
    signo = 1 
    print('min')


#------------------------------------ Grafica --------------------------------------

# Grafica restriccion
fig, ax = plt.subplots()
# Definir la función que grafica una restricción
def plot_restriccion(coeficientes, termino_independiente, signo):
    x1 = [-2000, 2000] # Rango de valores para la variable x1
    x2 = [(termino_independiente - coeficientes[0] * x1[0]) / coeficientes[1],
          (termino_independiente - coeficientes[0] * x1[1]) / coeficientes[1]]
    plt.plot(x1, x2, label=f'{coeficientes[0]}x1 + {coeficientes[1]}x2 {signo} {termino_independiente}')
    if coeficientes[0] == 0:
        x = termino_independiente / coeficientes[1]
        y = 0
    elif coeficientes[1] == 0:
        x = 0
        y = termino_independiente / coeficientes[0]
    else:
        x = termino_independiente / coeficientes[0]
        y = termino_independiente / coeficientes[1]
    
    # Agregar texto con las coordenadas de la intersección
    plt.annotate(f'({x:.2f}, 0)', xy=(x, 0), xytext=(5, -10), textcoords='offset points')
    plt.annotate(f'(0, {y:.2f})', xy=(0, y), xytext=(-30, 5), textcoords='offset points')
    
    
#Cambia el tamano del grafico
    plt.ylim(0, 1000)
    plt.xlim(0, 1000)
    

#Funcion que encuentra el punto donde las restricciones se intersectan hecho con sympy
# def encontrar_punto_corte(r1,r2):
#     x1, x2 = symbols('x1 x2')
#     eq1 = r1['x1']*x1 + r1['x2']*x2 - r1['termino_independiente']
#     eq2 = r2['x1']*x1 + r2['x2']*x2 - r2['termino_independiente']
#     sol = solve((eq1,eq2),(x1,x2))
#     punto_corte = (sol[x1], sol[x2])
#     return punto_corte

#Punto de corte manual

def encontrar_punto_de_corte(restriccion1, restriccion2):
    a1, b1, c1 = restriccion1['x1'], restriccion1['x2'], restriccion1['termino_independiente']
    a2, b2, c2 = restriccion2['x1'], restriccion2['x2'], restriccion2['termino_independiente']
    
    if a1*b2 - a2*b1 == 0:
        return None  # Las restricciones son paralelas
    
    x = (b2*c1 - b1*c2) / (a1*b2 - a2*b1)
    y = (a1*c2 - a2*c1) / (a1*b2 - a2*b1)
    
    return x, y

def encontrar_todos_los_puntos(diccionario_restricciones):
    puntos_de_corte = []
    restricciones = list(diccionario_restricciones.values())
    for i in range(len(restricciones)):
        for j in range(i + 1, len(restricciones)):
            punto_de_corte = encontrar_punto_de_corte(restricciones[i], restricciones[j])
            if punto_de_corte is not None:
                puntos_de_corte.append(punto_de_corte)
    return puntos_de_corte

def verificar_factibilidad(punto, diccionario_restricciones):
    for restriccion in diccionario_restricciones.values():
        if restriccion['signo'] == "<=":
            if punto[0]*restriccion['x1'] + punto[1]*restriccion['x2'] > restriccion['termino_independiente']:
                return False
        elif restriccion['signo'] == ">=":
            if punto[0]*restriccion['x1'] + punto[1]*restriccion['x2'] < restriccion['termino_independiente']:
                return False
        elif restriccion['signo'] == "==":
            if punto[0]*restriccion['x1'] + punto[1]*restriccion['x2'] != restriccion['termino_independiente']:
                return False
    return True


#colorear





puntos_de_corte = encontrar_todos_los_puntos(diccionario_restricciones)
print('puntos de corte: ',puntos_de_corte)



# factible = verificar_factibilidad((2,6),diccionario_restricciones)
# print(factible)


# xd = encontrar_punto_corte(diccionario_restricciones['restriccion_1'],diccionario_restricciones['restriccion_2'])
# print('punto de corte:',xd)




#prueba del punto de corte (da (2,6))
# print(encontrar_punto_corte(diccionario_restricciones["restriccion_1"],diccionario_restricciones["restriccion_2"]))


#NOTA: Tambien se puede solventar manualmente, primero identificando las restricciones que se intersectan y luego
# despejando alguno de los x (x1 por ejemplo) para poder obtener x2 en un sistema de ecuaciones




#======================================= TESTEO ==========================================
# Ejemplo de cómo llamar a la función plot_restriccion de forma manual

# plot_restriccion([diccionario_restricciones['restriccion_2']['x1'],
#                   diccionario_restricciones['restriccion_2']['x2']],
#                  diccionario_restricciones['restriccion_2']['termino_independiente'],
#                  diccionario_restricciones["restriccion_2"]['signo'])
# # print(diccionario_restricciones["restriccion_2"]['x1'])

#=========================================================================================



#Graficamos todas las restricciones
for restriccion in diccionario_restricciones.values():
    plot_restriccion([restriccion['x1'], restriccion['x2']], restriccion['termino_independiente'], restriccion['signo'])
    # Graficamos los puntos de corte
    for i, punto in enumerate(puntos_de_corte):
        ax.plot(punto[0], punto[1],'ro')
        ax.annotate(f'({punto[0]:.2f}, {punto[1]:.2f})', (punto[0], punto[1]), textcoords='offset points', xytext=(5,5))

        

#Grafica la funcion objetivo
x = [0, max(10, max(ax.get_xlim()))]
y = [(coef_obj_dict["x2"] * i - coef_obj_dict["x1"]) / coef_obj_dict["x1"] for i in x]
ax.plot(x, y, label="Funcion Objetivo")

#pintar la region factible
    

    # Configurar los límites de los ejes x e y
plt.xlim(0, 1130)
plt.ylim(0, 1130)



plt.legend()
plt.show()








