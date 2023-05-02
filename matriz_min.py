import re 

funcion= input("Ingrese la función objetivo (2x1 + 3x2): Z= ")
tipo="min"
#funcion="2x1 + 3x2"
restricc=[]
variables=re.findall(r"(-?\d+(?:,\d{1,2})?)\s*[xX]1\s*[+-]\s*(-?\d+(?:,\d{1,2})?)\s*[xX]2",funcion)
for valor in variables[0]:
    restricc.append(float(valor.replace(",", ".")))

n=int(input("Cuantas restricciones son: "))

def funcionobjt(variables_z,tipo,n):
    matriz=[]#inicio la matriz
    rest=[]
    Z="Z"
    canti=len(variables_z)#tomo el largo de las variables z que en realidad son  las entradas de x1 y x2
    if tipo=="min":
        algo=["VB","Z","X1","X2"]
        num_E=0
        num_A=0
        for i in range(n*2):#basicamente agrega a la matriz dependiendo de las restricciones los E1, E2 ,...E*n
            if i%2==0:
                h="E"+str(num_E+1)
                algo.append(h)
                num_E+=1
            else:
                h="A"+str(num_A+1)#lo mismo pero con los A
                algo.append(h)
                num_A+=1
        algo.append("LD")#agrega el LD
        matriz.append(algo)
        var_z=[]
        cant=4+2*n
        for i in range(cant):#todo esto es para agregar los -1, 1 y 0 del metodo
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
    return matriz

matriz=funcionobjt(variables,tipo,n)#guarda la matriz generada
for j in range(len(matriz)):
    print(matriz[j])
print("--------",restricc,"---------")
def suma_res(matriz,n):#esta funcion suma las restricciones en x1, x2 y LD, ademas de que haces lo ajustes pertinentes para dejar la fila z correctamente
    for j in range(1,n+2):
        for i in range(2,len(matriz[0])):
            if i >= 2 and i <= 3 or i==4+(n*2):
                matriz[1][i]=matriz[1][i]-matriz[j][i]
    for i in range(2,len(matriz[0])):
        if i>=4 and i<len(matriz[0]):
            if matriz[1][i]==0:
                matriz[1][i]=1
            elif matriz[1][i]==1:
                matriz[1][i]=0
    return matriz

def x1_x2_menor(matriz,n):#busca el numero mas negativo en la fila z, el cual se debe eliminar y almacena su columna
    menor=0
    for i in range(2,len(matriz[0])-1):
        matriz[1][i]
        if matriz[1][i] < menor:# 0 > -3
            menor=matriz[1][i]
            indice=i
    return indice

def obtener_columna(matriz,indice,n):#aqui mediante el indice anterior se busca la fila pivote
    var=0
    for i in range(2,len(matriz)):
        if matriz[i][-1]>var:
            var=matriz[i][-1]#este es un agregado como no quiero ingresar una variable pues no se cuales seran los limites de los numero busco el numero mas grande del lado derecho
    for i in range(2,len(matriz)):
        if matriz[i][indice]>0:
            piv=round(matriz[i][-1]/matriz[i][indice],3)#almacena la fila de el numero mas pequeño resultante de dividir el lado derecho por el numero en la columna indice
            if  var>piv:#utilizo ese numero grande para compararlo con el resultado de la fila e indice pivote
                var=piv
                ind=i
    return ind

def divide_la_fial_piv(matriz,indice,fila,pivote,n):#aqui se divide esa fila pivote por el numero pivote para hacer un 1 en esa columna
    LDI=matriz[0][indice]
    copia_fila=matriz[fila][:]
    for i in range(1,len(matriz[0])):
        num=(copia_fila[i]/pivote)
        matriz[fila][i]=num
    matriz[fila][0]=LDI
    return matriz

def ultima_parte(matriz,indice,fila,n):#aqui lo que hacemos es una vez modificada la fila la usamos para hacer 0 hacia arriba y hacia abajo de esta misma
    copia_fila=matriz[fila][:]
    for i in range(1,len(matriz)):
        if i != fila:#para no tomar en  cuenta a la fila pivote
            Num=copia_fila[indice]*matriz[i][indice]
            for j in range(1,len(matriz[0])):
                matriz[i][j]=matriz[i][j]- copia_fila[j]*Num
    for fila in matriz:
        for i in range(len(fila)):
            if isinstance(fila[i], (int, float)):
                fila[i] = round(fila[i], 3)
    return matriz

cont=0
matriz=(suma_res(matriz,n))
for j in range(len(matriz)):
    print(matriz[j])
print("----------------------------------------------")
while cont!=1:#este ciclo terminara cuando ocurra el if
    for j in range(2,len(matriz[0])):
        if matriz[1][-1]==0:#el metodo de dos fases termina cuando el LD de la fila es 0
            cont+=1
            break
        else:#mientras tanto se seguira ejecutando 
            for i in range(n):
                indice=(x1_x2_menor(matriz,n))
                fila=(obtener_columna(matriz,indice,n))
                div=(divide_la_fial_piv(matriz,indice,fila,matriz[fila][indice],3))
                ma=(ultima_parte(matriz,indice,fila,n))
                matriz=ma
                for j in range(n+2):
                    print(matriz[j])
                print("---------------------------------------------------------------------")

a=6
col_del=[6]#inicia en 6 ya que ahi esta el A1 y va aumentando hasta n-1 pues solo hara 2 iteaciones 
for i in range(n-1):
    a+=2#pues parte del indice 6, luego 8 y termina en 9 esas son las columnas de A1,A2 y A3
    col_del.append(a)#aqui se guardan las columnas a eliminar 

col_del = [i - 1 for i in col_del]#escogo el 6 que ahi se ubicaria el A1 lo elimino y paso al siguiente asi sucesivamente
for fila in matriz:
    for j in sorted(col_del, reverse=True):
        del fila[j]

for j in range(len(matriz)):#imprimo la nueva matriz
    print(matriz[j])

def min_fase_2(matriz,restricciones):#empieza la fase 2
    j=0
    for i in range(2,4):        
        matriz[1][i]=restricciones[j]#integro los valores x1 y x2 ingresados dentro de la matriz
        j+=1
    return matriz

def menor_x(matriz):#uno busca el numero mas pequeño de la fila z mientras que el otro el mas negativo y lo almacena en en a y b respectivamente
    a=0
    b=0
    for i in range(2,len(matriz[0])):
        if matriz[1][i]>0:
            a=matriz[1][i]
        elif matriz[1][i]<0:
            b=matriz[1][i]
    return a,b

def x1_x2_menor_dos(matriz,n):#podria haber hecho lo mismo que en otra funcion anterior pero no lo quise hacer XD
    menor=1000000000000
    indice=0
    for i in range(2,len(matriz)-1):
        matriz[1][i]
        if matriz[1][i] < menor and matriz[1][i]!=0:# 0 > -3
            menor=matriz[1][i]
            indice=i#busca la columna mas grande de la fila z para utilizarlo en la segunda fase
    return indice

print("-------------------------------------------------")
matriz=(min_fase_2(matriz,restricc))
for j in range(len(matriz)):
    print(matriz[j])

f=n#un variable cualquiera para romper el ciclo
while f==n:
    a,b=menor_x(matriz)#obtengo los numeros menores
    if matriz[1][2]==0 and matriz[1][3]==0:#en la segunda fase se busca que se hgan 0 en x1 y x2 en la fila z
        if b<0 and b!=matriz[1][-1]:#aqui digo que si el numero mas negativo es menor a 0 se siga ejecutando, pero si tambien debe ser distinto del LD
            print("-----------------------------")#pues si eso pasara no habria ningun numero negarivo en la fila z
            indice=x1_x2_menor_dos(matriz,n)
            fila=obtener_columna(matriz,indice,n)
            div=divide_la_fial_piv(matriz,indice,fila,matriz[fila][indice],n)
            ma=ultima_parte(matriz,indice,fila,n)
            matriz=ma
            for j in range(n+2):
                print(ma[j])
        elif b>=0 or matriz[1][-1]==b:#para que se rompa el ciclo el numero mas pequeño debe ser <= 0 o tambien haber encontrado la el numero de la columna del LD
            break
    elif matriz[1][2]!=0 or matriz[1][3]!=0:#para que se hagan 0 en x
                    print("-----------------------------")
                    indice=x1_x2_menor_dos(matriz,n)
                    fila=obtener_columna(matriz,indice,n)
                    div=divide_la_fial_piv(matriz,indice,fila,matriz[fila][indice],n)
                    ma=ultima_parte(matriz,indice,fila,n)
                    matriz=ma
                    for j in range(n+2):
                        print(ma[j])
    else:
            break

print("----------------------------    A     -------------------------------")