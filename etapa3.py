"""
Laboratorio 8 - MM3014 Teoria de Probabilidades
Universidad del Valle de Guatemala
Etapa 3: Incorporacion del presupuesto y costo
"""

import numpy as np
import matplotlib.pyplot as plt
import math

# ===========================================================
# PARAMETROS
# ===========================================================
N           = 100       # Numero total de estampas diferentes
S           = 7         # Estampas por sobre
PRECIO      = 9.50      # Precio por sobre individual (Q)
PRESUPUESTO = 1000.0    # Presupuesto total (Q)
R           = 10_000    # Numero de simulaciones
SEED        = 2026      # Semilla para reproducibilidad

# ===========================================================
# SIMULACION - COMPRA CON PRESUPUESTO LIMITADO
# Condicion de parada: gasto + precio > presupuesto  O  album completo
# ===========================================================
np.random.seed(SEED)

completados        = np.zeros(R, dtype=int)
sobres_comprados   = np.zeros(R, dtype=int)
estampas_distintas = np.zeros(R, dtype=int)

for sim in range(R):
    coleccion = set()
    gasto     = 0.0
    sobres    = 0

    while gasto + PRECIO <= PRESUPUESTO and len(coleccion) < N:
        sobre   = np.random.choice(N, size=S, replace=False)
        coleccion.update(sobre)
        gasto  += PRECIO
        sobres += 1

    completados[sim]        = 1 if len(coleccion) == N else 0
    sobres_comprados[sim]   = sobres
    estampas_distintas[sim] = len(coleccion)

# ===========================================================
# RESULTADOS PRINCIPALES
# ===========================================================
prob_completar       = completados.mean()
media_sobres         = sobres_comprados.mean()
mascara_fracaso      = completados == 0
media_distintas_fail = (estampas_distintas[mascara_fracaso].mean()
                        if mascara_fracaso.sum() > 0 else float('nan'))

print("=" * 62)
print("      RESULTADOS - ETAPA 3: Presupuesto y Costo")
print("=" * 62)
print(f"\nParametros: N={N}, S={S}, precio=Q{PRECIO}, presupuesto=Q{PRESUPUESTO:.0f}")
print(f"            R={R:,}, semilla={SEED}")
print("-" * 62)
print(f"  P(completar album | Q{PRESUPUESTO:.0f})       : "
      f"{prob_completar:.4f}  ({prob_completar*100:.2f}%)")
print(f"  E[sobres comprados]                 : {media_sobres:.4f}")
print(f"  E[estampas distintas | fracaso]     : {media_distintas_fail:.4f}")
print(f"  Simulaciones exitosas               : {completados.sum():,} / {R:,}")

# ===========================================================
# PREGUNTAS DE ANALISIS
# ===========================================================

# -- Pregunta 1 ---------------------------------------------
max_sobres  = int(PRESUPUESTO // PRECIO)
min_teorico = math.ceil(N / S)

print("\n-- PREGUNTA 1 " + "-" * 48)
print(f"  Max. sobres con Q{PRESUPUESTO:.0f}         : {max_sobres}")
print(f"  Minimo teorico (ceil(N/S))        : {min_teorico}  (= ceil({N}/{S}))")
print(f"  Estampas teoricas ({max_sobres}x{S})       : {max_sobres * S}"
      f"  {'>='}  N={N}")
suficiente = "Si" if max_sobres >= min_teorico else "No"
print(f"  Suficiente en teoria?             : {suficiente} "
      f"({max_sobres} >= {min_teorico} minimo teorico)")

# -- Pregunta 2: Caja de 104 sobres (Q975) ------------------
SOBRES_CAJA = 104
COSTO_CAJA  = 975.0

np.random.seed(SEED + 1)
exitos_caja = 0
for _ in range(R):
    coleccion = set()
    for _ in range(SOBRES_CAJA):
        sobre = np.random.choice(N, size=S, replace=False)
        coleccion.update(sobre)
    if len(coleccion) == N:
        exitos_caja += 1

prob_caja = exitos_caja / R

print(f"\n-- PREGUNTA 2: Caja de {SOBRES_CAJA} sobres (Q{COSTO_CAJA:.0f}) " + "-" * 22)
print(f"  P(completar | caja {SOBRES_CAJA} sobres)  : "
      f"{prob_caja:.4f}  ({prob_caja*100:.2f}%)")
print(f"  P(completar | sueltos Q{PRESUPUESTO:.0f})  : "
      f"{prob_completar:.4f}  ({prob_completar*100:.2f}%)")
print(f"  Diferencia                        : {(prob_caja - prob_completar)*100:+.2f} pp")
conviene = "Si" if prob_caja > prob_completar else "No, convienen los sueltos"
print(f"  Conviene la caja?                 : {conviene}")

# -- Pregunta 3: Estrategia mixta (caja + sobres sueltos) ---
sueltos_adicionales = int((PRESUPUESTO - COSTO_CAJA) // PRECIO)
costo_mixta         = COSTO_CAJA + sueltos_adicionales * PRECIO
total_mixta         = SOBRES_CAJA + sueltos_adicionales

np.random.seed(SEED + 2)
exitos_mixta = 0
for _ in range(R):
    coleccion = set()
    for _ in range(total_mixta):
        sobre = np.random.choice(N, size=S, replace=False)
        coleccion.update(sobre)
    if len(coleccion) == N:
        exitos_mixta += 1

prob_mixta = exitos_mixta / R

print(f"\n-- PREGUNTA 3: Estrategia mixta (caja + sueltos) " + "-" * 13)
print(f"  Presupuesto restante tras caja    : Q{PRESUPUESTO - COSTO_CAJA:.2f}")
print(f"  Sobres sueltos adicionales        : {sueltos_adicionales}"
      f"  (Q{sueltos_adicionales * PRECIO:.2f})")
print(f"  Total sobres mixta                : {total_mixta}")
print(f"  Costo total mixta                 : Q{costo_mixta:.2f}  (<= Q{PRESUPUESTO:.0f})")
print(f"  P(completar | mixta)              : "
      f"{prob_mixta:.4f}  ({prob_mixta*100:.2f}%)")
print(f"\n  Resumen comparativo:")
print(f"    Solo sueltos  ({max_sobres} sobres, Q{PRESUPUESTO:.0f})  : {prob_completar:.4f}")
print(f"    Solo caja     ({SOBRES_CAJA} sobres, Q{COSTO_CAJA:.0f})  : {prob_caja:.4f}")
print(f"    Caja+sueltos  ({total_mixta} sobres, Q{costo_mixta:.0f})  : {prob_mixta:.4f}  <- optima")
print("=" * 62)

# ===========================================================
# VISUALIZACION: Diagrama de barras - completado vs no completado
# ===========================================================
categorias   = ['Completado', 'No completado']
proporciones = [prob_completar, 1 - prob_completar]
colores      = ['#27ae60', '#c0392b']

fig, ax = plt.subplots(figsize=(8, 6))
bars = ax.bar(categorias, proporciones, color=colores,
              edgecolor='white', linewidth=1.2, width=0.5, zorder=3)

for bar, val in zip(bars, proporciones):
    ax.text(bar.get_x() + bar.get_width() / 2, val + 0.012,
            f"{val:.4f}\n({val*100:.2f}%)",
            ha='center', va='bottom', fontsize=12, fontweight='bold', color='#2c3e50')

ax.set_ylim(0, 1.18)
ax.set_ylabel("Proporcion de simulaciones", fontsize=12)
ax.set_title(
    "Etapa 3 - Album completado vs. no completado  (Presupuesto Q1 000)\n"
    f"N={N} estampas  |  S={S} por sobre  |  Q{PRECIO}/sobre  |  R={R:,} simulaciones",
    fontsize=11, fontweight='bold'
)
ax.grid(axis='y', alpha=0.3, zorder=0)
ax.spines[['top', 'right']].set_visible(False)

plt.tight_layout()
plt.savefig("etapa3_completado_vs_no.png", dpi=150, bbox_inches='tight')
plt.show()
print("\n[OK] Grafica guardada como 'etapa3_completado_vs_no.png'")
