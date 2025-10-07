# =============================================================
# Actividad 2.1. Red Neuronal Hopfield 
# Omar Arias Zepeda A00830966
# =============================================================

#convertir a a -1 
def leer_patron_txt(nombre_archivo):
    patron = []
    with open(nombre_archivo, "r") as f:
        for linea in f:
            linea = linea.strip()
            for c in linea:
                patron.append(1 if c == "1" else -1)
    return patron

# Producto externo vector x vector^T
def producto_externo(vector):
    n = len(vector)
    M = [[0]*n for _ in range(n)]
    for i in range(n):
        vi = vector[i]
        for j in range(n):
            M[i][j] = vi * vector[j]
    return M

# Suma de matrices A + B
def sumar_matrices(A, B):
    n = len(A)
    for i in range(n):
        Ai, Bi = A[i], B[i]
        for j in range(n):
            Ai[j] += Bi[j]
    return A

# Multiplicación vector x matriz M
def producto_vector_matriz(fila, M):
    n = len(fila)
    res = [0]*n
    for j in range(n):
        s = 0
        for k in range(n):
            s += fila[k] * M[k][j]
        res[j] = s
    return res

# Escalón con desempate por valor previo
def funcion_escalon(previo, x):
    salida = []
    for i in range(len(x)):
        if x[i] > 0:
            salida.append(1)
        elif x[i] < 0:
            salida.append(-1)
        else:
            salida.append(previo[i])  
    return salida

# fucnion comparar para hopfield 
def Comparar(U_inicial, M, max_pasos=100):
    U = U_inicial[:]
    pasos = 0
    while pasos < max_pasos:
        print(f"\nIteración {pasos}:")
        print("U =", U)
        z = producto_vector_matriz(U, M)
        U_nuevo = funcion_escalon(U, z)
        print("U nuevo =>", U_nuevo)
        if U_nuevo == U:
            print(f"\nConvergencia alcanzada en {pasos} pasos")
            return U_nuevo, pasos
        U = U_nuevo
        pasos += 1
    print(f"\nNo convergió en {max_pasos} pasos (devuelvo último estado).")
    return U, pasos

def ver16x16(vec):
    for r in range(16):
        fila = vec[r*16:(r+1)*16]
        print(''.join('1' if v==1 else '0' for v in fila))

# Distancia de Hamming
def hamming(a, b):
    return sum(1 for x, y in zip(a, b) if x != y)


# ENTRENAMIENTO
# =============================================================
archivos_entrenamiento = ["suma.txt", "resta.txt", "multiplicacion.txt", "division.txt", "igual.txt"]

patrones = []
for nombre in archivos_entrenamiento:
    v = leer_patron_txt(nombre)
    patrones.append((nombre, v))

N = len(patrones[0][1])  
M = [[0]*N for _ in range(N)]
for _, v in patrones:
    M = sumar_matrices(M, producto_externo(v))
# Normalizar por N 
for i in range(N):
    Mi = M[i]
    for j in range(N):
        Mi[j] /= N
    Mi[i] = 0


#Prueba con un patrón leído de archivo
# =============================================================

archivo_prueba = "prueba.txt"  
print(f"\nProbando con el patrón leído de archivo: {archivo_prueba}\n")
U0 = leer_patron_txt(archivo_prueba)


print("\nCadena ORIGINAL:")
print(U0)

print("Patrón ORIGINAL:")
ver16x16(U0)

# Ejecutar Hopfield con impresiones por iteración
estado_final, pasos = Comparar(U0, M, max_pasos=10)

print("\nCadena RECONOCIDA:")
print(estado_final)

print("\nPatrón RECONOCIDO:")
ver16x16(estado_final)

# Comparar con patrones entrenados
distancias = [(nombre, hamming(estado_final, v)) for nombre, v in patrones]
distancias.sort(key=lambda x: x[1])
mejor_nombre, _ = distancias[0]
print(f"\n Símbolo detectado: {mejor_nombre}")
