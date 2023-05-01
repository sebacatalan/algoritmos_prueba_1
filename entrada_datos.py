import re

# Usar expresiones regulares para extraer los nombres de las variables de la función objetivo
funcion= input("Ingrese la función objetivo (2x1 + 3x2): Z= ")
tipo=input("Es Maximización(max) o Minimización(min): ")
#tipo="min"
#funcion="2x1 + 3x2"
variables=re.findall(r"(-?\d*)\s*[xX]1\s*[+-]\s*(\d*)\s*[xX]2",funcion)
n=int(input("Cuantas restricciones son: "))

def funcionobjt(variables_z,tipo,n):
    matriz=[]#inicio la matriz
    rest=[]
    Z="Z"
    canti=len(variables_z)#tomo el largo de las variables z que en realidad son  las entradas de x1 y x2
    if tipo=="max":#si es maximizacion
        algo=["VB","Z","X1","X2"]
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
        algo=["VB","Z","X1","X2"]
        num_E=0
        num_A=0
        for i in range(n*2):
            if i%2==0:
                h="E"+str(num_E+1)
                algo.append(h)
                num_E+=1
            else:
                h="A"+str(num_A+1)
                algo.append(h)
                num_A+=1
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

def x1_x2_menor(matriz):
    menor=0
    for i in range(2,(len(matriz[0]))):
        matriz[1][i]
        if matriz[1][i] < menor:# 0 > -3
            menor=matriz[1][i]
            indice=i
    return indice

def obtener_columna(matriz,indice,n):
    var=0
    for i in range(2,len(matriz)):#para no tener errores estableci que  el valor mas grande del LD tomaria el valor de var
        if matriz[i][-1]>var:#para no tener que estar cambiandolo constantemente
            var=matriz[i][-1]
    for i in range(2,len(matriz)):#asi que al momento de comparar para encontrar el valor mas pequeño de las columnas de cada fila solo se almacenase el mas pequeño
        if matriz[i][indice]>0:#
            piv=matriz[i][-1]/matriz[i][indice]
            if  var>piv:
                var=piv
                ind=i#almacenamos su indice
    return ind

def divide_la_fial_piv(matriz,indice,fila,pivote,n):
    LDI=matriz[0][indice]#aqui es para agregar el x1 o x2 segun la columna pivote 
    copia_fila=matriz[fila][:]#copio todos los valores de la fila pivote
    for i in range(1,n+5):#parto de 1 pues en la posicion 0 esta el h1, h2 o h3
        matriz[fila][i]=copia_fila[i]/pivote#divido la fila por el pivote y ya tendria mi fila  para pivotear hacia arrina y hacia abajo
    matriz[fila][0]=LDI#al lado izquierdo
    return matriz#retorno la matriz con sus modificaciones

def ultima_parte(matriz,indice,fila,n):
    copia_fila=matriz[fila][:]#almacena esa lista dentro de copia_fila
    for i in range(1,len(matriz)):#parto de 1 pues en la posicion 0 estarian los valores de las columnas
        if i != fila:#para no tomar en  cuenta a la fila pivote
            Num=copia_fila[indice]*matriz[i][indice]#almacena en num el 1 que debe dar una vez modificada la matriz multiplicado por fila en la que va el ciclo y su respectivo indice
            for j in range(1,n+5):#parte de 1 para no  tomar los str de h1,h2 y h3 hasta n que serian restricciones y 5 por (VB,z,x1,x2,LD)
                matriz[i][j]=matriz[i][j]- copia_fila[j]*Num#le restamos la copia sehun el indice de la fila por el respectivo numero que iria en la fila pivote
    for fila in matriz:
        for i in range(len(fila)):
            if isinstance(fila[i], (int, float)):
                fila[i] = round(fila[i], 3)
    return matriz

def menor(matriz):
    a=0.000000000000000001
    for i in range(2,len(matriz[0])):
        if matriz[1][i]<0:
            a=matriz[1][i]
    return a

matriz, restricc=funcionobjt(variables,tipo,n)

copia = matriz
#-------------------------------------------------------------
# aqui hacemos la copia de la matriz ingresada par utilizarla mas adelante
filas = len(matriz) # copia de matriz original
columnas = len(matriz[0])
c_ma = []

for i in range(filas):
    fila = []
    for j in range(columnas):
        fila.append(matriz[i][j])
    c_ma.append(fila) # nombre de la copia
#-------------------------------------------------------------
f=n
if tipo=="max":
    for j in range(n+2):
        print(copia[j])
    while n==f:
        a=menor(copia)
        if a<=-1:
            print("-----------------------------")
            indice=x1_x2_menor(copia)
            fila=obtener_columna(copia,indice,n)
            div=divide_la_fial_piv(copia,indice,fila,copia[fila][indice],n)
            ma=ultima_parte(copia,indice,fila,n)
            matriz=ma
            for j in range(n+2):
                print(ma[j])
        else:
            f+=1
            break

#calculamos la holgura rentable apartando la fila N°1
piv = matriz
funi= piv[1]
def holgura_rentable(funi):
    n=len(funi)
    numero=0
    indice = 0
    for i in range(n):
        if i>3:
            if i < n-1:
                if funi[i] > numero:
                    indice = i
                    numero=funi[i] 
    return numero, indice # nos retorna el valor y la posicion de la holgura
print(holgura_rentable(funi))

print("------------------------------------------------------------------------------------\n")
#------------------------------------
# aqui lo que hacemos es preparar el indice dado antes para 
# compararlo con los valores de la columna [0] 
ind = indice-3
indice2 = matriz[ind]
in_mat = indice2[0]
#------------------------------------
#en este if comprobamos que valor que da el indice para comparar en que fila debemos aumentar 
#en 1 el ultimo valor
if in_mat == "x1":
    c_ma[2][-1] += 1

elif in_mat == "x2":
    c_ma[3][-1] += 1

else:
    lo= []
    for fila in range(1,len(c_ma)):
        if c_ma[fila][0] == in_mat:
            lo = c_ma[fila]
            break
    lo[-1] += 1

""" for i in range(len(c_ma)): # solo es para comprobar si el cambio se efectua de manera correcta
    for j in range(len(c_ma[0])):
        print(c_ma[i][j], end='\t') """
#---------------------------------------------------------------------------------------
# en proceso, aqui debe ejecutar el metodo gauss con la matriz ya modificada aunque aun no lo hace
for j in range(n+2):
    print(c_ma[j])
while n==f:
    a=menor(c_ma)
    if a<=-1:
        print("-----------------------------")
        indice=x1_x2_menor(c_ma)
        fila=obtener_columna(c_ma,indice,n)
        div=divide_la_fial_piv(c_ma,indice,fila,c_ma[fila][indice],n)
        ma=ultima_parte(c_ma,indice,fila,n)
        matriz=ma
        for j in range(n+2):
            print(ma[j])
    else:
        f+=1
        break



""" for j in range(n+2):
    print(c_ma[j])
for i in range(2):
    print("-----------------------------")
    indice=x1_x2_menor(c_ma)
    fila=obtener_columna(c_ma,indice,n)
    div=divide_la_fial_piv(c_ma,indice,fila,c_ma[fila][indice],n)
    ma=ultima_parte(c_ma,indice,fila,n)
    matriz=ma
    for j in range(3+2):
        print(ma[j])

f1 = matriz[1] 
  """