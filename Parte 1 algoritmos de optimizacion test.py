import re
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog


# objetivo = input("Ingrese la función objetivo: ")
objetivo = 'max z = 3x1 + 5x2' #funciuon de prueba



restricciones = ["4x1 + 5x2 >= 5", "6x1 - 7x2 <= 10", "8x1 + 9x2 <= 7"] # restriccion de prueba

for restriccion in restricciones:
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
    
    print(coef_dict)

    
    
    
    
    
# while True:
#     restriccion = input("Ingrese una restricción (o escriba 'fin' si terminó): ")
#     if restriccion == "fin":
#         break
#     restricciones.append(restriccion)

#coeficientes de la funcion objetivo
coeficientes = re.findall(r'\d+', objetivo)
coeficientes = [int(c) for c in coeficientes]
print('coef',coeficientes)





# Definir la función que grafica una restricción
def plot_restriccion(coeficientes, termino_independiente, signo):
    x1 = [0, 10] # Rango de valores para la variable x1
    x2 = [(termino_independiente - coeficientes[0] * x1[0]) / coeficientes[1],
          (termino_independiente - coeficientes[0] * x1[1]) / coeficientes[1]]
    plt.plot(x1, x2, label=f'{coeficientes[0]}x1 + {coeficientes[1]}x2 {signo} {termino_independiente}')
    plt.ylim(0, 10)
    plt.xlim(0, 10)

# Ejemplo de cómo llamar a la función plot_restriccion
plot_restriccion([2, 3], 15, '<=')
plt.legend()
plt.show()








#si es max o min
if "max" in objetivo:
    signo = -1  
    print('max')
else:
    signo = 1 
    print('min')

A = []
b = []
coeficientes_restriccion = []
#coeficientes de las restricciones
for restriccion in restricciones:
    coef = re.findall(r'[\+\-]?\d+', restriccion)
    coef = [int(c) for c in coef]
    A.append(coef[:-1])
    b.append(coef[-1])
    coeficientes_restriccion.append(coef)
# print('restriccion A:',A)
# print('restriccion B:',b)
# print('coeficientes restricciones: ',coeficientes_restriccion)

# restricciones signos
signos = []
for restriccion in restricciones:
    if "<=" in restriccion:
        signos.append(-1)  # Restricción <=
    elif ">=" in restriccion:
        signos.append(1)   # Restricción >=
    else:
        raise ValueError("Restricción no válida")


# # Dibujar las restricciones
# plt.figure(figsize=(8,8))
# x1 = np.linspace(0, 10, 100)  # Rango de valores de x1
# for i in range(len(restricciones)):
#     ecuacion = A[i][0]*x1 + A[i][1]*(-1)
#     plt.plot(x1, ecuacion/b[i], label=f"Restricción {i+1}")

# plt.xlim(0, 10)
# plt.ylim(0, 10)
# plt.xlabel('x1')
# plt.ylabel('x2')
# plt.title('Restricciones')
# plt.legend()
# plt.grid()
# plt.show()







