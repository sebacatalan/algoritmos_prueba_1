import re

# Usar expresiones regulares para extraer los nombres de las variables de la función objetivo
#funcion= input("Ingrese la función objetivo (2x1 + 3x2): Z= ")
#tipo=input("Es Maximización(max) o Minimización(min): ")
tipo="min"
funcion="2x1 + 3x2"
variables=re.findall(r"(-?\d*)\s*[xX]1\s*[+-]\s*(\d*)\s*[xX]2",funcion)
n=int(input("Cuantas restricciones son: "))

def funcionobjt(variables_z,tipo,n):
    matriz=[]#inicio la matriz
    rest=[]
    Z="Z"
    canti=len(variables_z)#tomo el largo de las variables z que en realidad son  las entradas de x1 y x2
    if tipo=="max":#si es maximizacion
        algo=["DV","Z","X1","X2"]
        for i in range(n):
            h="H"+str(i+1)
            algo.append(h)
        algo.append("LD")
        matriz.append(algo)
        var_z=[]#inicio la lista donde estaran las variables de z
        var_z.append(Z)
        var_z.append(1)#agregamos el 1 que corresponde a z en la lista
        for variable in variables_z:#recorro variablez
            for i in range(canti):#este ciclo es para transformar en negativo los coeficientes de x1 y x2
                x1=int(variable[i])#aqui guardo el valor x1 en la variables x1
                x2=int(variable[i+1])#lo mismo pero con x2
                var=[]
                var.append(x1)
                var.append(x2)
                rest.append(var)
                var_z.append(-x1)#meto las variables en la lista, pero en negativo
                var_z.append(-x2)
                for i in range(n+1):#esto es para agregar las holguras el +1 es por el lado derecho
                    var_z.append(0)#agrego las holguras y el lado derecho
        matriz.append(var_z)#meto la lista dentro de otra
        for i in range(n):#ahora hago un ciclo que se repite dependiendo de la cantidad de restricciones que ingrese el usuario
            a=input("Ingresa la restriccion Nº"+str(i+1)+" : ")
            variables=re.findall(r"(-?\s*\d+)\s*[xX]1\s*([+-]\s*\d+)\s*[xX]2",a)  #basicamente es para detectar los valores de x1 y x2
            #tambien detecta  si es negativo o positivo el numero   
            lado_derecho=re.findall(r"(<=|>=)\s*(-?\d+)",a)#aqui revisamos el lado derecho
            coeficientes = [int(var[0].replace(" ","")) if var[0] else 1 for var in variables]#aqui  reemplazamos por  1 si no se entrego ningun numero  alrededor de un x1 o x2
            coeficientes.insert(0, 0)#ingreso el valor que tendrian las restriccioenes en su columna z
            H="H"+str(i+1)
            coeficientes.insert(0, H)
            coeficientes.append(int(variables[-1][1].replace(" ","")))#agrega el valor como entero y con el signo que deberia tener  dentro de la restriccion
            todas_las_restricciones=[int(var[0].replace(" ","")) if var[0] else 1 for var in variables]
            todas_las_restricciones.append(int(variables[-1][1].replace(" ","")))#agrega el valor como entero y con el signo que deberia tener  dentro de la restriccion
            for j in range(n):#este ciclo for es para rellenar los 0 y 1 de las holguras
                if i==j:#si es la holgura 1, en la restriccion 1 se  agrega un 1
                    coeficientes.append(1)
                else:
                    coeficientes.append(0)#si no se cumple agrega un 0
            for restriccion in lado_derecho:#ciclo for para agregar el lado derecho a la lista
                operador, valor = restriccion
                valor = int(valor)#el valor pasa a ser entero
                if operador == "<=":#si se cumple que este era el operador
                    coeficientes.append(valor)#se agrega el lado derecho
                    todas_las_restricciones.append("<=")
                    todas_las_restricciones.append(valor)
                elif operador == ">=":
                    coeficientes.append(valor)
                    todas_las_restricciones.append(">=")
                    todas_las_restricciones.append(valor)
            matriz.append(coeficientes)#imprime la matriz
            rest.append(todas_las_restricciones)
    elif tipo=="min":
        algo=["DV","Z","X1","X2"]
        for i in range(n):
            if i%2==0:
                num_E=0
                h="E"+str(num_E+1)
                algo.append(h)
            else:
                num_A=0
                h="A"+str(num_A+1)
                algo.append(h)
        algo.append("LD")
        matriz.append(algo)
        var_z=[]
        cant=4+2*n
        for i in range(cant):
            if i==0:
                var_z.append(-1)
            elif i>2 and i%2==0:
                var_z.append(1)
            else:
                var_z.append(0)
        var_z.insert(0,Z)
        matriz.append(var_z)
        c=0
        d=1
        for variable in variables_z:#recorro variablez
            for i in range(canti):#este ciclo es para transformar en negativo los coeficientes de x1 y x2
                x1=int(variable[i])#aqui guardo el valor x1 en la variables x1
                x2=int(variable[i+1])#lo mismo pero con x2
                var=[]
                var.append(x1)
                var.append(x2)
                rest.append(var)
        for i in range(n):
            a=input("Ingresa la restriccion Nº"+str(i+1)+" : ")
            variables=re.findall(r"(-?\s*\d+)\s*[xX]1\s*([+-]\s*\d+)\s*[xX]2",a)     
            lado_derecho=re.findall(r"(<=|>=)\s*(-?\d+)",a)
            coeficientes = [int(var[0].replace(" ","")) if var[0] else 1 for var in variables]
            coeficientes.insert(0, 0)
            A="A"+str(i+1)
            coeficientes.insert(0, A)
            coeficientes.append(int(variables[-1][1].replace(" ","")))
            todas_las_restricciones=[int(var[0].replace(" ","")) if var[0] else 1 for var in variables]
            todas_las_restricciones.append(int(variables[-1][1].replace(" ","")))#agrega el valor como entero y con el signo que deberia tener  dentro de la restriccion
            for j in range(2*n):#este ciclo for es para rellenar los 0 y 1 de las holguras:#si es la holgura 1, en la restriccion 1 se  agrega un 1
                if j==i+c:
                    coeficientes.append(-1)
                elif j==i+d:
                    coeficientes.append(1)
                else:
                    coeficientes.append(0)#si no se cumple agrega un 0
            for restriccion in lado_derecho:
                operador, valor = restriccion
                valor = int(valor)
                if operador == "<=":#si se cumple que este era el operador
                    coeficientes.append(valor)#se agrega el lado derecho
                    todas_las_restricciones.append("<=")
                    todas_las_restricciones.append(valor)
                elif operador == ">=":
                    coeficientes.append(valor)
                    todas_las_restricciones.append(">=")
                    todas_las_restricciones.append(valor)
            matriz.append(coeficientes)
            rest.append(todas_las_restricciones)
            c+=1
            d+=1
    return matriz , rest

listas, restricc=funcionobjt(variables,tipo,n)

for i in range(n+2):
    print(listas[i])

for i in range(n+1):
    print(restricc[i])

 