matriz=[["VB","Z","x1","x2","E1","A1","E2","A2","E3","A3","LD"],
        ["Z",-1,0,0,0,1,0,1,0,1,0],
        ["A1",0,60,60,-1,1,0,0,0,0,300],
        ["A2",0,12,6,0,0,-1,1,0,0,36],
        ["A3",0,10,30,0,0,0,0,-1,1,90]]

def suma_res(matriz,n):
    for j in range(1,n+2):
        for i in range(2,len(matriz[0])):
            if i >= 2 and i <= 3 or i==4+(n*2):
                matriz[1][i]=matriz[1][i]-matriz[j][i]
    for i in range(2,len(matriz[0])):
        if i>=4 and i<4+(n*2):
            if matriz[1][i]==0:
                matriz[1][i]=1
            elif matriz[1][i]==1:
                matriz[1][i]=0
    return matriz

def x1_x2_menor(matriz,n):
    menor=0
    for i in range(2,(2*n)+4):
        matriz[1][i]
        if matriz[1][i] < menor:# 0 > -3
            menor=matriz[1][i]
            indice=i
    return indice

def obtener_columna(matriz,indice,n):
    var=0
    for i in range(2,len(matriz)):
        if matriz[i][-1]>var:
            var=matriz[i][-1]
    for i in range(2,len(matriz)):
        if matriz[i][indice]>0:
            piv=round(matriz[i][-1]/matriz[i][indice],3)
            if  var>piv:
                var=piv
                ind=i
    return ind

def divide_la_fial_piv(matriz,indice,fila,pivote,n):
    LDI=matriz[0][indice]
    copia_fila=matriz[fila][:]
    for i in range(1,2*n+5):
        num=(copia_fila[i]/pivote)
        matriz[fila][i]=num
    matriz[fila][0]=LDI
    return matriz

def ultima_parte(matriz,indice,fila,n):
    copia_fila=matriz[fila][:]
    for i in range(1,len(matriz)):
        if i != fila:#para no tomar en  cuenta a la fila pivote
            Num=copia_fila[indice]*matriz[i][indice]
            for j in range(1,5+(2*n)):
                matriz[i][j]=matriz[i][j]- copia_fila[j]*Num
    for fila in matriz:
        for i in range(len(fila)):
            if isinstance(fila[i], (int, float)):
                fila[i] = round(fila[i], 3)
    return matriz

cont=0
n=3
matriz=(suma_res(matriz,n))
print(matriz)
while cont!=1:
    for j in range(2,len(matriz[0])):
        if matriz[1][-1]==0:
            cont+=1
            break
        else:
            for i in range(n):
                indice=(x1_x2_menor(matriz,n))
                fila=(obtener_columna(matriz,indice,n))
                div=(divide_la_fial_piv(matriz,indice,fila,matriz[fila][indice],3))
                ma=(ultima_parte(matriz,indice,fila,n))
                matriz=ma
                for j in range(3+2):
                    print(matriz[j])
                print("---------------------------------------------------------------------")

a=6
col_del=[6]
for i in range(n-1):
    a+=2
    col_del.append(a)

col_del = [i - 1 for i in col_del]
for fila in matriz:
    for j in sorted(col_del, reverse=True):
        del fila[j]

for j in range(len(matriz)):
    print(matriz[j])

restricc=[[0.12,0.15],[3,4]]

def min_fase_2(matriz,restricciones):
    r=restricciones[0]
    j=0
    for i in range(2,4):        
        matriz[1][i]=r[j]
        j+=1
    return matriz

matriz=(min_fase_2(matriz,restricc))

