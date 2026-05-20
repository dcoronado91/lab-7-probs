import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# LABORATORIO 7 - MM3014 Teoría de Probabilidades
# Etapa 1: Simulación básica con álbum reducido
# ============================================================

# Semilla para reproducibilidad
np.random.seed(2026)

# Parámetros
N = 100   # Número total de estampas diferentes
S = 7     # Estampas por sobre (todas distintas dentro del mismo sobre)
R = 10000 # Número de simulaciones

# ============================================================
# SIMULACIÓN
# ============================================================

sobres_totales    = np.zeros(R, dtype=int)
repetidas_totales = np.zeros(R, dtype=int)

for sim in range(R):
    coleccion = np.zeros(N, dtype=bool)  # arreglo booleano de estampas obtenidas
    sobres    = 0
    repetidas = 0

    while coleccion.sum() < N:
        # Comprar un sobre: S estampas distintas entre sí (replace=False)
        nuevas = np.random.choice(N, size=S, replace=False)
        sobres += 1
        for estampa in nuevas:
            if coleccion[estampa]:
                repetidas += 1
            else:
                coleccion[estampa] = True

    sobres_totales[sim]    = sobres
    repetidas_totales[sim] = repetidas

# ============================================================
# RESULTADOS A CALCULAR
# ============================================================

media_sobres    = sobres_totales.mean()
std_sobres      = sobres_totales.std()
media_repetidas = repetidas_totales.mean()
std_repetidas   = repetidas_totales.std()

# Mínimo teórico sin repetidas: ceil(N/S)
minimo_teorico = int(np.ceil(N / S))  # = 15

# Probabilidad de necesitar más de 30 sobres
prob_mas_30 = (sobres_totales > 30).mean()

# Valor esperado teórico (Coupon Collector con sobres de S estampas)
H_N       = sum(1/k for k in range(1, N+1))   # H_100 exacto
E_teorico = (N / S) * H_N

# ============================================================
# IMPRESIÓN DE RESULTADOS
# ============================================================

print("=" * 55)
print("  LABORATORIO 7 - ETAPA 1: Resultados")
print("=" * 55)
print(f"\nParámetros: N={N}, S={S}, R={R}, semilla=2026")

print(f"\n{'─'*55}")
print(f"  SOBRES NECESARIOS PARA COMPLETAR EL ÁLBUM")
print(f"{'─'*55}")
print(f"  Media muestral          : {media_sobres:.4f}")
print(f"  Desviación estándar     : {std_sobres:.4f}")
print(f"  Valor esperado teórico  : {E_teorico:.4f}")

print(f"\n{'─'*55}")
print(f"  ESTAMPAS REPETIDAS")
print(f"{'─'*55}")
print(f"  Media muestral          : {media_repetidas:.4f}")
print(f"  Desviación estándar     : {std_repetidas:.4f}")

print(f"\n{'─'*55}")
print(f"  ANÁLISIS DE UMBRALES")
print(f"{'─'*55}")
print(f"  Mínimo teórico sin reps : {minimo_teorico} sobres  (= ceil(100/7))")
print(f"  P(sobres > 30)          : {prob_mas_30:.4f}  ({prob_mas_30*100:.2f}%)")

print(f"\n{'─'*55}")
print(f"  PREGUNTAS DE ANÁLISIS")
print(f"{'─'*55}")
print(f"  1. Mínimo sin repetidas : {minimo_teorico} sobres")
print(f"     ¿Alguna sim usó exactamente {minimo_teorico}? "
    f"{'Sí' if (sobres_totales == minimo_teorico).any() else 'No'}")
print(f"  2. H_100 exacto         : {H_N:.6f}")
print(f"     H_100 ~ ln(100)+y    : {np.log(100)+0.5772:.6f}")
print(f"     E[T] teórico         : {E_teorico:.4f} sobres")
print(f"     Media simulación     : {media_sobres:.4f} sobres")
print(f"  3. E[repetidas] teórico : {E_teorico*S - N:.4f}")
print(f"     Media rep. simulación: {media_repetidas:.4f}")
print(f"  4. CV (std/media)       : {std_sobres/media_sobres:.4f}  "
    f"({'alta' if std_sobres/media_sobres > 0.2 else 'baja'} variabilidad)")
print("=" * 55)

# ============================================================
# VISUALIZACIÓN: Histograma
# ============================================================

fig, ax = plt.subplots(figsize=(12, 6))

ax.hist(sobres_totales, bins=60, color='steelblue', edgecolor='white',
        linewidth=0.5, alpha=0.85, label='Distribución simulada')

ax.axvline(media_sobres, color='crimson', linewidth=2.2, linestyle='-',
        label=f'Media muestral = {media_sobres:.2f}')

ax.axvline(minimo_teorico, color='darkorange', linewidth=2.2, linestyle='--',
        label=f'Mínimo teórico = {minimo_teorico}  (ceil(N/S))')

ax.axvline(E_teorico, color='forestgreen', linewidth=2.2, linestyle=':',
        label=f'E[T] teórico = {E_teorico:.2f}')

ax.set_xlabel('Número de sobres necesarios', fontsize=13)
ax.set_ylabel('Frecuencia', fontsize=13)
ax.set_title('Etapa 1 - Distribución del número de sobres para completar el álbum\n'
            f'(N=100 estampas, S=7 por sobre, R=10 000 simulaciones, semilla=2026)',
            fontsize=13)
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('etapa1_histograma.png', dpi=150)  # se guarda en la misma carpeta del script
plt.show()
print("\nHistograma guardado como 'etapa1_histograma.png'")