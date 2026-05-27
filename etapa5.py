"""
Laboratorio 9 - MM3014 Teoria de Probabilidades
Universidad del Valle de Guatemala
Etapa 5: Simulacion del album real  (N=980, Mundial 2026)
"""

import numpy as np
import matplotlib.pyplot as plt

# ===========================================================
# PARAMETROS GLOBALES  (album real Mundial 2026)
# ===========================================================
N           = 980       # Total de estampas diferentes
S           = 7         # Estampas por sobre
PRECIO      = 9.50      # Precio sobre individual (Q)
PRECIO_CAJA = 975.0     # Precio caja 104 sobres (Q)
SOBRES_CAJA = 104       # Sobres por caja
SEED        = 2026

# R reducido frente a etapas anteriores: N=980 es mas costoso.
# Se usan arrays booleanos numpy en lugar de sets para mayor velocidad.

print("=" * 65)
print("   ETAPA 5 - Album real  N=980, S=7, semilla=2026")
print("=" * 65)


# ===========================================================
# FUNCIONES AUXILIARES  (optimizadas con arrays numpy bool)
# ===========================================================

def sim_completar(S_val=S):
    """Simula hasta completar el album. Retorna sobres usados."""
    count = 0
    col   = np.zeros(N, dtype=bool)
    s     = 0
    while count < N:
        st    = np.random.choice(N, size=S_val, replace=False)
        nuevas = ~col[st]
        col[st] = True
        count  += int(nuevas.sum())
        s      += 1
    return s


def sim_presupuesto(budget):
    """Simula con presupuesto fijo. Retorna True si completo el album."""
    count = 0
    col   = np.zeros(N, dtype=bool)
    gasto = 0.0
    while gasto + PRECIO <= budget and count < N:
        st    = np.random.choice(N, size=S, replace=False)
        nuevas = ~col[st]
        col[st] = True
        count  += int(nuevas.sum())
        gasto  += PRECIO
    return count == N


def sim_exactos(total_sobres):
    """Compra exactamente total_sobres. Retorna True si completo."""
    count = 0
    col   = np.zeros(N, dtype=bool)
    for _ in range(total_sobres):
        if count == N:
            break
        st    = np.random.choice(N, size=S, replace=False)
        nuevas = ~col[st]
        col[st] = True
        count  += int(nuevas.sum())
    return count == N


def sim_intercambio(K):
    """Simula hasta completar con intercambio K:1. Retorna sobres usados."""
    col       = np.zeros(N, dtype=bool)
    count     = 0
    repetidas = 0
    sobres    = 0
    while count < N:
        st     = np.random.choice(N, size=S, replace=False)
        nuevas = ~col[st]
        col[st] = True
        n_new  = int(nuevas.sum())
        count     += n_new
        repetidas += S - n_new
        sobres    += 1
        while repetidas >= K and count < N:
            falt = np.where(~col)[0]
            if len(falt) == 0:
                break
            nueva = int(np.random.choice(falt))
            col[nueva] = True
            count     += 1
            repetidas -= K
    return sobres


# ===========================================================
# PREGUNTA 1
# Cuantos sobres se necesitan en promedio para completar el
# album del Mundial 2026 (N=980, S=7), y cuanto cuesta eso?
# Se muestra la distribucion simulada vs el valor teorico
# del Coupon Collector generalizado: E[T] = (N/S) * H_N.
# ===========================================================
R_P1 = 500
np.random.seed(SEED)

sobres_p1 = np.array([sim_completar() for _ in range(R_P1)])
media_p1  = sobres_p1.mean()
std_p1    = sobres_p1.std()
H_N       = sum(1/k for k in range(1, N + 1))
E_teo     = (N / S) * H_N

print(f"\n-- PREGUNTA 1 " + "-" * 51)
print(f"   Cuantos sobres y cuanto dinero para completar N=980?")
print(f"-" * 65)
print(f"  R={R_P1}  |  E[sobres]={media_p1:.1f} (std={std_p1:.1f})  "
      f"|  E[T]teorico={E_teo:.1f}")
print(f"  Costo esperado : Q{media_p1*PRECIO:,.2f}")
print(f"  Mediana        : {int(np.percentile(sobres_p1,50))} sobres"
      f"  ->  Q{int(np.percentile(sobres_p1,50))*PRECIO:,.0f}")
print(f"  Percentil 90   : {int(np.percentile(sobres_p1,90))} sobres"
      f"  ->  Q{int(np.percentile(sobres_p1,90))*PRECIO:,.0f}")

fig, ax = plt.subplots(figsize=(11, 5))
ax.hist(sobres_p1, bins=40, color='#3498db', edgecolor='none', alpha=0.82, zorder=3)
ax.axvline(media_p1, color='#e74c3c', lw=2.2, linestyle='-',
           label=f'Media = {media_p1:.0f} sobres  (Q{media_p1*PRECIO:,.0f})')
ax.axvline(E_teo, color='#27ae60', lw=2.2, linestyle='--',
           label=f'E[T] teorico = {E_teo:.0f}')
ax.set_xlabel("Sobres necesarios para completar el album", fontsize=12)
ax.set_ylabel("Frecuencia", fontsize=12)
ax.set_title(
    "P1 - Distribucion de sobres para completar el album del Mundial 2026\n"
    f"N={N}, S={S}, R={R_P1}",
    fontsize=11, fontweight='bold'
)
ax.legend(fontsize=10)
ax.grid(axis='y', alpha=0.3, zorder=0)
ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig("pregunta1.png", dpi=150, bbox_inches='tight')
plt.show()
print("[OK] pregunta1.png guardado")


# ===========================================================
# PREGUNTA 2
# A partir de que presupuesto se alcanza >= 50%, 75% y 90%
# de probabilidad de completar el album real?
# Se simula P(completar) para presupuestos de Q4000 a Q14000.
# ===========================================================
R_P2         = 300
presupuestos = list(range(4000, 14001, 1000))   # 11 puntos
prob_p2      = []

np.random.seed(SEED + 10)
print(f"\n-- PREGUNTA 2 " + "-" * 51)
print(f"   Con que presupuesto hay >= 50%, 75% y 90% de P?")
print(f"-" * 65)
print(f"  R={R_P2} por punto  |  Calculando...", end='', flush=True)

for budget in presupuestos:
    exitos = sum(int(sim_presupuesto(budget)) for _ in range(R_P2))
    prob_p2.append(exitos / R_P2)

print(" listo")

B50 = next((b for b, p in zip(presupuestos, prob_p2) if p >= 0.50), None)
B75 = next((b for b, p in zip(presupuestos, prob_p2) if p >= 0.75), None)
B90 = next((b for b, p in zip(presupuestos, prob_p2) if p >= 0.90), None)

for b, p in zip(presupuestos, prob_p2):
    marca = (" <- 50%" if b == B50 else
             " <- 75%" if b == B75 else
             " <- 90%" if b == B90 else "")
    print(f"  Q{b:,}  ->  {p*100:.1f}%{marca}")

print(f"  P>=50%: Q{B50:,}" if B50 else "  P>=50%: fuera de rango", end="  |  ")
print(f"P>=75%: Q{B75:,}" if B75 else "P>=75%: fuera de rango", end="  |  ")
print(f"P>=90%: Q{B90:,}" if B90 else "P>=90%: fuera de rango")

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot([b/1000 for b in presupuestos], prob_p2,
        color='#2980b9', lw=2.2, marker='o', markersize=6, zorder=3)
for u, cu, lu in [(0.50,'#e74c3c','50%'),(0.75,'#e67e22','75%'),(0.90,'#27ae60','90%')]:
    ax.axhline(u, color=cu, lw=1.3, linestyle='--', alpha=0.75, label=f'Umbral {lu}')
ax.set_xlabel("Presupuesto (miles de Q)", fontsize=12)
ax.set_ylabel("P(completar album)", fontsize=12)
ax.set_title(
    "P2 - Probabilidad de completar el album segun presupuesto\n"
    f"N={N}, S={S}, R={R_P2} por punto",
    fontsize=11, fontweight='bold'
)
ax.set_ylim(0, 1.05)
ax.legend(fontsize=10)
ax.grid(alpha=0.3, zorder=0)
ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig("pregunta2.png", dpi=150, bbox_inches='tight')
plt.show()
print("[OK] pregunta2.png guardado")


# ===========================================================
# PREGUNTA 3
# Con Q10,000, que combinacion de cajas (104 sob, Q975) y
# sobres sueltos (Q9.50) maximiza P(completar el album)?
# Se evaluan de 0 a 10 cajas usando el resto en sueltos.
# ===========================================================
R_P3    = 300
PRES_P3 = 10_000.0

np.random.seed(SEED + 20)
print(f"\n-- PREGUNTA 3 " + "-" * 51)
print(f"   Con Q10,000, cajas + sueltos: cual combo es mejor?")
print(f"-" * 65)
print(f"  R={R_P3} por estrategia  |  Calculando...", end='', flush=True)

estrategias, probs_p3, labels_p3 = [], [], []
for nc in range(0, 11):
    costo_c = nc * PRECIO_CAJA
    if costo_c > PRES_P3:
        break
    ns    = int((PRES_P3 - costo_c) // PRECIO)
    tot   = nc * SOBRES_CAJA + ns
    costo = costo_c + ns * PRECIO
    estrategias.append((nc, ns, tot, costo))
    exitos = sum(int(sim_exactos(tot)) for _ in range(R_P3))
    probs_p3.append(exitos / R_P3)
    labels_p3.append(f"{nc}C+{ns}S\n({tot})")

print(" listo")

mejor = int(np.argmax(probs_p3))
print(f"  {'Cajas':>5}  {'Sueltos':>7}  {'Total':>6}  {'Costo':>8}  {'P':>7}")
print(f"  {'-'*5}  {'-'*7}  {'-'*6}  {'-'*8}  {'-'*7}")
for i, ((nc, ns, tot, cst), p) in enumerate(zip(estrategias, probs_p3)):
    m = "  <- mejor" if i == mejor else ""
    print(f"  {nc:>5}  {ns:>7}  {tot:>6}  Q{cst:>7,.0f}  {p:>7.4f}{m}")

cols_p3 = ['#27ae60' if i == mejor else '#3498db' for i in range(len(probs_p3))]
fig, ax = plt.subplots(figsize=(max(9, len(probs_p3)*1.1), 5))
bars = ax.bar(range(len(probs_p3)), probs_p3, color=cols_p3,
              edgecolor='white', lw=1.1, width=0.7, zorder=3)
for bar, p in zip(bars, probs_p3):
    ax.text(bar.get_x()+bar.get_width()/2, p+0.005,
            f"{p:.3f}", ha='center', va='bottom', fontsize=8, fontweight='bold')
ax.set_xticks(range(len(labels_p3)))
ax.set_xticklabels(labels_p3, fontsize=8)
ax.set_ylim(0, 1.12)
ax.set_ylabel("P(completar album)", fontsize=12)
ax.set_title(
    "P3 - P(completar) segun estrategia con Q10,000  (C=caja, S=suelto)\n"
    f"N={N}, S={S}, R={R_P3}  |  Verde = estrategia optima",
    fontsize=10, fontweight='bold'
)
ax.grid(axis='y', alpha=0.3, zorder=0)
ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig("pregunta3.png", dpi=150, bbox_inches='tight')
plt.show()
print("[OK] pregunta3.png guardado")


# ===========================================================
# PREGUNTA 4
# Cuanto reduce el intercambio K=5 el numero esperado de
# sobres y el gasto para completar el album real?
# Histogramas superpuestos sin intercambio vs con K=5.
# ===========================================================
R_P4 = 300
K_P4 = 5

np.random.seed(SEED + 30)
sobres_sinK = np.array([sim_completar() for _ in range(R_P4)])

print(f"\n-- PREGUNTA 4 " + "-" * 51)
print(f"   Cuanto ahorra el intercambio K={K_P4} en sobres y Q?")
print(f"-" * 65)
print(f"  R={R_P4}  |  Simulando K={K_P4}...", end='', flush=True)
np.random.seed(SEED + 31)
sobres_conK = np.array([sim_intercambio(K_P4) for _ in range(R_P4)])
print(" listo")

m_sin = sobres_sinK.mean()
m_con = sobres_conK.mean()
ahorro_s = m_sin - m_con
print(f"  Sin intercambio : {m_sin:.1f} sobres  ->  Q{m_sin*PRECIO:,.0f}")
print(f"  Con K={K_P4}         : {m_con:.1f} sobres  ->  Q{m_con*PRECIO:,.0f}")
print(f"  Ahorro          : {ahorro_s:.1f} sobres  =  Q{ahorro_s*PRECIO:,.0f}"
      f"  ({ahorro_s/m_sin*100:.1f}%)")

bins4 = np.linspace(min(sobres_sinK.min(), sobres_conK.min()),
                    max(sobres_sinK.max(), sobres_conK.max()), 45)
fig, ax = plt.subplots(figsize=(11, 5))
ax.hist(sobres_sinK, bins=bins4, color='#9b59b6', alpha=0.6, density=True,
        label=f'Sin intercambio  (media={m_sin:.0f})', zorder=3)
ax.hist(sobres_conK, bins=bins4, color='#e74c3c',  alpha=0.6, density=True,
        label=f'K={K_P4}  (media={m_con:.0f})', zorder=3)
ax.axvline(m_sin, color='#9b59b6', lw=2, linestyle='--', zorder=4)
ax.axvline(m_con, color='#e74c3c', lw=2, linestyle='--', zorder=4)
ax.set_xlabel("Sobres para completar el album", fontsize=12)
ax.set_ylabel("Densidad", fontsize=12)
ax.set_title(
    f"P4 - Efecto del intercambio K={K_P4} sobre el numero de sobres\n"
    f"N={N}, S={S}, R={R_P4}  |  Ahorro: {ahorro_s:.0f} sob = Q{ahorro_s*PRECIO:,.0f}",
    fontsize=11, fontweight='bold'
)
ax.legend(fontsize=10)
ax.grid(axis='y', alpha=0.3, zorder=0)
ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig("pregunta4.png", dpi=150, bbox_inches='tight')
plt.show()
print("[OK] pregunta4.png guardado")


# ===========================================================
# PREGUNTA 5
# Como cambia el numero esperado de sobres si el tamano del
# sobre S varia entre 5 y 9 estampas (N=980 fijo)?
# Muestra cuanto mas barato o caro seria el album segun el
# tamano de sobre que decida usar Panini.
# ===========================================================
R_P5     = 300
S_values = [5, 6, 7, 8, 9]
medias_5 = []
stds_5   = []

np.random.seed(SEED + 40)
print(f"\n-- PREGUNTA 5 " + "-" * 51)
print(f"   Como cambia el costo al variar S (5 a 9) con N=980?")
print(f"-" * 65)
print(f"  R={R_P5} por valor de S")

for Sv in S_values:
    arr = np.array([sim_completar(S_val=Sv) for _ in range(R_P5)])
    medias_5.append(arr.mean())
    stds_5.append(arr.std())

ref7 = medias_5[S_values.index(7)]
print(f"  {'S':>3}  {'E[sobres]':>10}  {'Std':>7}  {'Costo Q':>10}  {'vs S=7':>9}")
print(f"  {'-'*3}  {'-'*10}  {'-'*7}  {'-'*10}  {'-'*9}")
for Sv, m, d in zip(S_values, medias_5, stds_5):
    diff = "referencia" if Sv == 7 else f"{((m-ref7)/ref7*100):+.1f}%"
    print(f"  {Sv:>3}  {m:>10.1f}  {d:>7.1f}  Q{m*PRECIO:>8,.0f}  {diff:>9}")

cols5 = ['#e74c3c','#e67e22','#3498db','#27ae60','#9b59b6']
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(S_values, medias_5, color=cols5, edgecolor='white',
              lw=1.1, width=0.6, zorder=3)
ax.errorbar(S_values, medias_5, yerr=stds_5,
            fmt='none', color='#2c3e50', capsize=6, lw=1.8, zorder=4)
for bar, m in zip(bars, medias_5):
    ax.text(bar.get_x()+bar.get_width()/2, m + max(stds_5)*0.08,
            f"{m:.0f}", ha='center', va='bottom', fontsize=10, fontweight='bold')
ax.set_xlabel("Estampas por sobre (S)", fontsize=12)
ax.set_ylabel("Sobres esperados para completar", fontsize=12)
ax.set_title(
    "P5 - Sobres esperados segun el tamano del sobre S  (N=980)\n"
    f"R={R_P5}  |  Barras de error = 1 desv. est.",
    fontsize=11, fontweight='bold'
)
ax.set_xticks(S_values)
ax.grid(axis='y', alpha=0.3, zorder=0)
ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig("pregunta5.png", dpi=150, bbox_inches='tight')
plt.show()
print("[OK] pregunta5.png guardado")

print("\n" + "=" * 65)
print("  Graficas generadas:")
print("  pregunta1.png  Distribucion sobres para completar N=980")
print("  pregunta2.png  P(completar) segun presupuesto")
print("  pregunta3.png  Estrategia optima cajas+sueltos con Q10,000")
print("  pregunta4.png  Efecto del intercambio K=5")
print("  pregunta5.png  Sensibilidad al tamano del sobre S")
print("=" * 65)
