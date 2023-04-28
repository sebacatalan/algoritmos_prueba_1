import re

# Usar expresiones regulares para extraer los nombres de las variables de la función objetivo
#funcion= input("Ingrese la función objetivo (2x1 + 3x2): Z= ")
funcion="2x1 + 3x2"
variables=re.findall(r"(-?\d*)\s*[xX]1\s*[+-]\s*(\d*)\s*[xX]2",funcion)
""" n=int(input("Cuantas restricciones son: "))
restricciones=[]
for i in range(n):
    a=input("Ingresa la restriccion Nº"+str(i+1)+" : ")
    lado_der=input("Ingresa el lado derecho de la restriccion Nº"+str(i+1)+" :")
    restr=re.findall(r"(-?\d*)\s*[xX]1\s*[+-]\s*(\d*)\s*[xX]2",a)
    restr.append(lado_der)
    restricciones.append(restr)
 """
matriz=[]
cant=len(variables)
print(cant)
for variable in variables:
    for i in range(cant):
        matriz.append(int(variable[i]))
        matriz.append(int(variable[i+1]))

print(matriz)