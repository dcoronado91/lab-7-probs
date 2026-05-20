"""
Laboratorio 7 - MM3014 Teoría de Probabilidades
Universidad del Valle de Guatemala
Etapa 2: Análisis de la probabilidad de éxito en función del número de sobres
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

# ══════════════════════════════════════════════════════════
# PARÁMETROS
# ══════════════════════════════════════════════════════════
N    = 100       # Número total de estampas diferentes
S    = 7         # Estampas por sobre (todas distintas dentro del mismo sobre)
R    = 10_000    # Número de simulaciones por valor de M
SEED = 2026      # Semilla para reproducibilidad

M_values = [20, 25, 30, 35, 40, 45, 50, 60, 70, 80]

# ══════════════════════════════════════════════════════════
# SIMULACIÓN
# Para cada M: comprar exactamente M sobres en R simulaciones
# y registrar si el álbum quedó completo (1) o no (0)
# ══════════════════════════════════════════════════════════
np.random.seed(SEED)

resultados = {}

for M in M_values:
    exitos = 0
    for _ in range(R):
        coleccion = set()
        for _ in range(M):
            sobre = np.random.choice(N, size=S, replace=False)
            coleccion.update(sobre)
        if len(coleccion) == N:
            exitos += 1
    resultados[M] = exitos / R

probabilidades = [resultados[m] for m in M_values]

# ══════════════════════════════════════════════════════════
# TABLA DE RESULTADOS
# ══════════════════════════════════════════════════════════
df = pd.DataFrame({
    "M (sobres)"              : M_values,
    "P(completar | M sobres)" : [round(p, 4) for p in probabilidades],
    "Porcentaje (%)"          : [f"{p*100:.2f}%" for p in probabilidades]
})

print("=" * 55)
print("        TABLA DE RESULTADOS — ETAPA 2")
print("=" * 55)
print(df.to_string(index=False))
print("=" * 55)

# ══════════════════════════════════════════════════════════
# PREGUNTAS DE ANÁLISIS
# ══════════════════════════════════════════════════════════

# ── Pregunta 1: Primer M con P ≥ 50% y P ≥ 90% ──────────
# Extendemos la búsqueda hasta M=120 para encontrar el umbral del 90%
np.random.seed(SEED + 1)
M_extra = list(range(85, 121, 5))
for M in M_extra:
    if M not in resultados:
        exitos = 0
        for _ in range(R):
            coleccion = set()
            for _ in range(M):
                sobre = np.random.choice(N, size=S, replace=False)
                coleccion.update(sobre)
            if len(coleccion) == N:
                exitos += 1
        resultados[M] = exitos / R

todos_M = sorted(resultados.keys())
todas_P = [resultados[m] for m in todos_M]

M_50 = next((m for m, p in zip(todos_M, todas_P) if p >= 0.50), None)
M_90 = next((m for m, p in zip(todos_M, todas_P) if p >= 0.90), None)

print("\n── PREGUNTA 1 ─────────────────────────────────────────")
print(f"  Primer M con P ≥ 50%:  M = {M_50}  →  P̂ = {resultados[M_50]:.4f}")
print(f"  Primer M con P ≥ 90%:  M = {M_90}  →  P̂ = {resultados[M_90]:.4f}")

# ── Pregunta 2: Comparación con la mediana teórica ───────
gamma = 0.5772156649
H_N   = sum(1/k for k in range(1, N + 1))
E_T   = (N / S) * H_N

print("\n── PREGUNTA 2 ─────────────────────────────────────────")
print(f"  H_100  = {H_N:.6f}")
print(f"         ≈ ln(100) + γ  =  {math.log(100):.4f} + {gamma:.4f}  =  {math.log(100)+gamma:.4f}")
print(f"  E[T]   = (N/S) · H_N  =  (100/7) · {H_N:.4f}  =  {E_T:.2f} sobres")
print(f"  Mediana teórica ≈ {E_T:.1f} sobres  (ligeramente menor que la media)")
print(f"  M con P̂ = 50% en sim. =  {M_50} sobres")
print(f"  → Son similares. La mediana < media porque la distribución")
print(f"    de T tiene sesgo positivo (cola larga a la derecha).")

# ── Pregunta 3: Cota de la Unión (Union Bound) ───────────
M_test      = 50
p_falta_una = math.exp(-M_test * S / N)
cota_union  = N * p_falta_una
P_fracaso   = 1 - resultados[M_test]

print("\n── PREGUNTA 3: Union Bound para M = 50 ────────────────")
print(f"  P(falta estampa i) ≈ e^(-MS/N)")
print(f"    = e^(-{M_test}×{S}/{N})  =  e^(-{M_test*S/N})  =  {p_falta_una:.6f}")
print(f"  Cota Union Bound = N · e^(-MS/N)")
print(f"    = {N} × {p_falta_una:.6f}  =  {cota_union:.4f}")
print(f"  P(fracasar) simulación       =  {P_fracaso:.4f}")
print(f"  → La cota ({cota_union:.2f}) > 1, NO es informativa.")
print(f"  Para ser útil necesitamos MS/N > ln(N) ≈ {math.log(N):.2f}")
print(f"  Aquí MS/N = {M_test*S/N:.1f}  <  {math.log(N):.2f}  → cota demasiado laxa.")

# ══════════════════════════════════════════════════════════
# GRÁFICA DE BARRAS
# ══════════════════════════════════════════════════════════
colores = [
    '#c0392b' if p < 0.50 else
    '#27ae60' if p >= 0.90 else
    '#2980b9'
    for p in probabilidades
]

fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(range(len(M_values)), probabilidades,
       color=colores, edgecolor='white', linewidth=1.2,
       width=0.65, zorder=3)

# Líneas de referencia
ax.axhline(0.5, color='#e74c3c', linewidth=2, linestyle='--',
           label='Umbral 50%', zorder=4)
ax.axhline(0.9, color='#f39c12', linewidth=2, linestyle=':',
           label='Umbral 90%', zorder=4)

# Etiquetas encima de cada barra
for i, (m, p) in enumerate(zip(M_values, probabilidades)):
    ax.text(i, p + 0.013, f"{p:.3f}",
            ha='center', va='bottom',
            fontsize=9, fontweight='bold', color='#2c3e50')

# Formato de ejes
ax.set_xticks(range(len(M_values)))
ax.set_xticklabels([str(m) for m in M_values], fontsize=11)
ax.set_ylim(0, 1.12)
ax.set_xlabel("Número de sobres comprados (M)", fontsize=12)
ax.set_ylabel("P̂(completar álbum | M sobres)", fontsize=12)
ax.set_title(
    "Etapa 2 — Probabilidad de completar el álbum en función de M\n"
    f"N={N} estampas  |  S={S} por sobre  |  R={R:,} simulaciones  |  Semilla={SEED}",
    fontsize=12, fontweight='bold'
)

# Leyenda
from matplotlib.patches import Patch
leyenda = [
    Patch(facecolor='#c0392b', label='P < 50%'),
    Patch(facecolor='#2980b9', label='50% ≤ P < 90%'),
    Patch(facecolor='#27ae60', label='P ≥ 90%'),
    plt.Line2D([0], [0], color='#e74c3c', lw=2, ls='--', label='Umbral 50%'),
    plt.Line2D([0], [0], color='#f39c12', lw=2, ls=':',  label='Umbral 90%'),
]
ax.legend(handles=leyenda, loc='upper left', fontsize=10)
ax.grid(axis='y', alpha=0.3, zorder=0)
ax.spines[['top', 'right']].set_visible(False)

plt.tight_layout()
plt.savefig("etapa2_probabilidad_exito.png", dpi=150, bbox_inches='tight')
plt.show()
print("\n[OK] Gráfica guardada como 'etapa2_probabilidad_exito.png'")
