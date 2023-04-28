def holgura_rentable(funcion):
    n=len(funcion)
    numero=0
    for i in range(n):
        if i>=3:
            a=n-1
            if i<a:
                if funcion[i] > numero:
                    numero=funcion[i]