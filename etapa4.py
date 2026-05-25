"""
Laboratorio 8 - MM3014 Teoria de Probabilidades
Universidad del Valle de Guatemala
Etapa 4: Efecto del intercambio de repetidas
"""

import numpy as np
import matplotlib.pyplot as plt

# ===========================================================
# PARAMETROS
# ===========================================================
N      = 100      # Numero total de estampas diferentes
S      = 7        # Estampas por sobre
R      = 10_000   # Simulaciones por configuracion
SEED   = 2026     # Semilla para reproducibilidad
K_vals = [1, 2, 5, 10]   # Valores de K a explorar

# ===========================================================
# FUNCION DE SIMULACION CON INTERCAMBIO
# Cada K repetidas acumuladas se canjean por 1 estampa faltante.
# El intercambio se realiza despues de procesar cada sobre.
# ===========================================================
def simular_con_intercambio(K, max_sobres=None):
    """
    K          : repetidas necesarias para un canje
    max_sobres : limite de sobres a comprar (None = sin limite)
    Retorna    : (sobres_comprados, completo_el_album)
    """
    coleccion = set()
    faltantes = set(range(N))
    repetidas = 0
    sobres    = 0

    while len(coleccion) < N:
        if max_sobres is not None and sobres >= max_sobres:
            break
        sobre = np.random.choice(N, size=S, replace=False)
        sobres += 1
        for e in sobre:
            if e in coleccion:
                repetidas += 1
            else:
                coleccion.add(e)
                faltantes.discard(e)
        # Canjear repetidas acumuladas por estampas faltantes
        while repetidas >= K and faltantes:
            nueva = int(np.random.choice(list(faltantes)))
            coleccion.add(nueva)
            faltantes.discard(nueva)
            repetidas -= K

    return sobres, len(coleccion) == N


# ===========================================================
# PARTE A: Simular hasta completar el album para cada K
# ===========================================================

# Referencia sin intercambio (loop simple, igual que Etapa 1)
np.random.seed(SEED)
sobres_ref = np.zeros(R, dtype=int)
for sim in range(R):
    col = set()
    s   = 0
    while len(col) < N:
        col.update(np.random.choice(N, size=S, replace=False))
        s += 1
    sobres_ref[sim] = s

media_ref = sobres_ref.mean()
std_ref   = sobres_ref.std()

print("=" * 68)
print("      RESULTADOS - ETAPA 4: Intercambio de Repetidas")
print("=" * 68)
print(f"\nParametros: N={N}, S={S}, R={R:,}, semilla={SEED}")
print("\n-- PARTE A: Sobres necesarios para completar el album " + "-" * 14)
print(f"  {'K':>8}  {'Media':>8}  {'Std':>8}  {'Reduccion':>10}")
print(f"  {'-'*8}  {'-'*8}  {'-'*8}  {'-'*10}")
print(f"  {'Sin K':>8}  {media_ref:>8.2f}  {std_ref:>8.2f}  {'--':>10}")

resultados_A = {}
todos_sobres = {'ref': sobres_ref}

for K in K_vals:
    np.random.seed(SEED + K)
    sobres_k = np.zeros(R, dtype=int)
    for sim in range(R):
        sobres_k[sim], _ = simular_con_intercambio(K)
    media_k   = sobres_k.mean()
    std_k     = sobres_k.std()
    reduccion = (media_ref - media_k) / media_ref * 100
    resultados_A[K] = {'media': media_k, 'std': std_k, 'reduccion': reduccion}
    todos_sobres[K] = sobres_k
    print(f"  {f'K={K}':>8}  {media_k:>8.2f}  {std_k:>8.2f}  {reduccion:>9.2f}%")

print("-" * 68)

# -- Pregunta 2 -- ahorro para K=2 -------------------------
ahorro_s = media_ref - resultados_A[2]['media']
ahorro_Q = ahorro_s * 9.50
print("\n-- PREGUNTA 2 " + "-" * 54)
print(f"  K=2 ahorra en promedio     : {ahorro_s:.2f} sobres")
print(f"  Equivalente en quetzales   : Q{ahorro_Q:.2f}  (a Q9.50/sobre)")

# ===========================================================
# VISUALIZACION A: Histogramas superpuestos por K
# ===========================================================
colores_K = {1: '#e74c3c', 2: '#e67e22', 5: '#3498db', 10: '#9b59b6', 'ref': '#2ecc71'}
labels_K  = {1: 'K = 1', 2: 'K = 2', 5: 'K = 5', 10: 'K = 10', 'ref': 'Sin intercambio'}

fig, ax = plt.subplots(figsize=(12, 6))

for key in ['ref', 10, 5, 2, 1]:
    ax.hist(todos_sobres[key], bins=60, alpha=0.55,
            color=colores_K[key], label=labels_K[key],
            edgecolor='none', density=True, zorder=3)

for K in K_vals:
    ax.axvline(resultados_A[K]['media'], color=colores_K[K],
               linewidth=1.5, linestyle='--', zorder=4)
ax.axvline(media_ref, color=colores_K['ref'], linewidth=1.5, linestyle='--', zorder=4)

ax.set_xlabel("Numero de sobres para completar el album", fontsize=12)
ax.set_ylabel("Densidad", fontsize=12)
ax.set_title(
    "Etapa 4A - Distribucion del numero de sobres para distintos K\n"
    f"N={N}  |  S={S}  |  R={R:,} simulaciones  |  Semilla={SEED}",
    fontsize=11, fontweight='bold'
)
ax.legend(fontsize=10)
ax.grid(axis='y', alpha=0.3, zorder=0)
ax.spines[['top', 'right']].set_visible(False)

plt.tight_layout()
plt.savefig("etapa4a_histogramas_K.png", dpi=150, bbox_inches='tight')
plt.show()
print("\n[OK] Grafica guardada como 'etapa4a_histogramas_K.png'")

# ===========================================================
# PARTE B: P(completar album | exactamente M sobres) para cada K
# ===========================================================
M_values = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]

print(f"\n-- PARTE B: P(exito | M sobres exactos) para cada K " + "-" * 15)
print(f"  ({len(K_vals)+1} configuraciones x {len(M_values)} valores de M x {R:,} simulaciones)")

resultados_B = {}

# Referencia sin intercambio
np.random.seed(SEED + 100)
resultados_B['ref'] = []
print("  Procesando Sin K...", end='', flush=True)
for M in M_values:
    exitos = 0
    for _ in range(R):
        col = set()
        for _ in range(M):
            col.update(np.random.choice(N, size=S, replace=False))
        exitos += int(len(col) == N)
    resultados_B['ref'].append(exitos / R)
print(" listo")

for K in K_vals:
    np.random.seed(SEED + 100 + K)
    resultados_B[K] = []
    print(f"  Procesando K={K}...", end='', flush=True)
    for M in M_values:
        exitos = 0
        for _ in range(R):
            _, completado = simular_con_intercambio(K, max_sobres=M)
            exitos += int(completado)
        resultados_B[K].append(exitos / R)
    print(" listo")

# -- Tabla de resultados ------------------------------------
print(f"\n  {'M':>4}" + "".join(f"  {'K='+str(k):>7}" for k in K_vals) + f"  {'Sin K':>7}")
print(f"  {'-'*4}" + "  ------" * (len(K_vals) + 1))
for i, M in enumerate(M_values):
    fila = f"  {M:>4}"
    for K in K_vals:
        fila += f"  {resultados_B[K][i]:>7.4f}"
    fila += f"  {resultados_B['ref'][i]:>7.4f}"
    print(fila)

# -- Umbrales 50%, 75%, 90% por K --------------------------
print("\n-- UMBRALES DE PROBABILIDAD POR K " + "-" * 33)
print(f"  {'K':>7}  {'M->50%':>6}  {'M->75%':>6}  {'M->90%':>6}")
print(f"  {'-'*7}  {'-'*6}  {'-'*6}  {'-'*6}")
for key in K_vals + ['ref']:
    probs = resultados_B[key]
    M50   = next((M_values[i] for i, p in enumerate(probs) if p >= 0.50), '>70')
    M75   = next((M_values[i] for i, p in enumerate(probs) if p >= 0.75), '>70')
    M90   = next((M_values[i] for i, p in enumerate(probs) if p >= 0.90), '>70')
    lbl   = f"K={key}" if key != 'ref' else 'Sin K'
    print(f"  {lbl:>7}  {str(M50):>6}  {str(M75):>6}  {str(M90):>6}")

# -- Pregunta 3 -- analisis puntual M=45 -------------------
if 45 in M_values:
    idx45 = M_values.index(45)
    p10   = resultados_B[10][idx45]
    p5    = resultados_B[5][idx45]
    p1    = resultados_B[1][idx45]
    print("\n-- PREGUNTA 3 (M = 45) " + "-" * 45)
    print(f"  P(exito | K=10, M=45) = {p10:.4f}")
    print(f"  P(exito | K=5,  M=45) = {p5:.4f}   (+{(p5-p10)*100:.2f} pp vs K=10)")
    print(f"  P(exito | K=1,  M=45) = {p1:.4f}   (+{(p1-p5)*100:.2f} pp vs K=5)")

print("=" * 68)

# ===========================================================
# VISUALIZACION B: Grafica de lineas P vs M para cada K
# ===========================================================
fig, ax = plt.subplots(figsize=(11, 6))

for key in ['ref'] + K_vals[::-1]:
    ls = '--' if key == 'ref' else '-'
    ax.plot(M_values, resultados_B[key],
            color=colores_K[key], linewidth=2.2,
            linestyle=ls, marker='o', markersize=5,
            label=labels_K[key], zorder=3)

for umbral, ls_u, col_u in [(0.50, ':', '#e74c3c'),
                              (0.75, '-.', '#e67e22'),
                              (0.90, '--', '#95a5a6')]:
    ax.axhline(umbral, color=col_u, linewidth=1.0, linestyle=ls_u,
               alpha=0.6, label=f'Umbral {int(umbral*100)}%')

ax.set_xlabel("Numero de sobres (M)", fontsize=12)
ax.set_ylabel("P(completar album)", fontsize=12)
ax.set_title(
    "Etapa 4B - Probabilidad de exito vs M para distintos K\n"
    f"N={N}  |  S={S}  |  R={R:,} simulaciones  |  Semilla={SEED}",
    fontsize=11, fontweight='bold'
)
ax.set_ylim(0, 1.05)
ax.legend(fontsize=9, ncol=2, loc='upper left')
ax.grid(alpha=0.3, zorder=0)
ax.spines[['top', 'right']].set_visible(False)

plt.tight_layout()
plt.savefig("etapa4b_prob_vs_M.png", dpi=150, bbox_inches='tight')
plt.show()
print("\n[OK] Grafica guardada como 'etapa4b_prob_vs_M.png'")
