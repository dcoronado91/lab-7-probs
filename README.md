# Laboratorios 7, 8 y 9 — MM3014 Teoría de Probabilidades
## Simulación Monte Carlo: Álbum Panini FIFA 2026

**Curso:** MM3014 Teoría de Probabilidades  
**Universidad del Valle de Guatemala**  
**Autores:** Angel Sanabria (24725) · Derek Coronado (24732)  
**Semilla global:** `np.random.seed(2026)` / `np.random.default_rng(2026)`

---

## Descripción general

Simulación de Monte Carlo aplicada al problema del coleccionista (_coupon collector problem_) usando como contexto el álbum de estampas Panini del Mundial FIFA 2026. Los laboratorios 7 y 8 usan un álbum simplificado N=100 estampas, S=7 por sobre; el laboratorio 9 escala al álbum real N=980.

Los laboratorios avanzan progresivamente:

| Lab | Etapa | Tema |
|-----|-------|------|
| 7 | 1 | Simulación básica: sobres necesarios para completar |
| 7 | 2 | Probabilidad de éxito en función del número de sobres M |
| 8 | 3 | Restricción de presupuesto y comparación de estrategias |
| 8 | 4 | Mecanismo de intercambio de repetidas (K repetidas → 1 nueva) |
| 9 | 5 | Álbum real N=980: costo, presupuesto, estrategias, intercambio y sensibilidad |

---

## Estructura del Proyecto

```
lab-probs/
├── laboratorio7_panini.ipynb          # Notebook Lab 7 (Etapas 1 y 2)
├── etapa1.py                          # Script Etapa 1
├── etapa2.py                          # Script Etapa 2
├── etapa2_probabilidad_exito.png      # Gráfica Etapa 2
├── laboratorio8_panini.ipynb          # Notebook Lab 8 (Etapas 3 y 4)
├── etapa3.py                          # Script Etapa 3
├── etapa4.py                          # Script Etapa 4
├── etapa3_completado_vs_no.png        # Gráfica Etapa 3 — completó vs. no completó
├── etapa3_comparacion_estrategias.png # Gráfica Etapa 3 — comparación de estrategias
├── etapa4a_histogramas_K.png          # Gráfica Etapa 4A — histogramas por K
├── etapa4b_prob_vs_M.png              # Gráfica Etapa 4B — P(completar) vs M por K
├── etapa4_rendimiento_marginal_K.png  # Gráfica Etapa 4 — rendimiento marginal
├── laboratorio9_panini.ipynb          # Notebook Lab 9 (Etapa 5)
├── etapa5.py                          # Script Etapa 5 — álbum real N=980
├── pregunta1.png                      # Distribución de sobres para completar N=980
├── pregunta2.png                      # P(completar) según presupuesto
├── pregunta3.png                      # Estrategia óptima cajas + sueltos con Q10,000
├── pregunta4.png                      # Efecto del intercambio K=5
├── pregunta5.png                      # Sensibilidad al tamaño del sobre S
└── README.md                          # Este archivo
```

---

## Laboratorio 7

### Etapa 1 — Simulación básica

**Parámetros:** N=100, S=7, R=10,000, semilla=2026

Simula cuántos sobres se necesitan para completar el álbum sin restricciones.

- Media y desviación estándar de sobres necesarios
- Media y desviación estándar de estampas repetidas
- Comparación con el valor esperado teórico $E[T] = \frac{N}{S} \cdot H_N \approx 74.04$
- Histograma de distribución de sobres
- Análisis del coeficiente de variación (~32%)

### Etapa 2 — Probabilidad de éxito

**M evaluados:** 20, 25, 30, 35, 40, 45, 50, 60, 70, 80 sobres · R=10,000 por M

Estima $P(\text{completar} \mid M \text{ sobres})$ para distintos valores de M.

- Gráfica de barras con umbrales P=50% y P=90%
- Identificación de umbrales: M para superar 50% y 90%
- Comparación mediana Etapa 1 vs. umbral 50% Etapa 2
- Evaluación de cota teórica (union bound) para M=50

**Resultados esperados:**

| Métrica | Valor |
|---|---|
| Media sobres (simulada) | ~74 sobres |
| Media repetidas | ~418 estampas |
| E[T] teórico | 74.04 sobres |
| P > 50% desde | M ≥ 70 sobres |
| P > 90% desde | M ≥ 80 sobres |

---

## Laboratorio 8

### Etapa 3 — Incorporación del presupuesto y costo

| Parámetro | Valor |
|---|---|
| Precio por sobre | Q 9.50 |
| Presupuesto total | Q 1,000 |
| Simulaciones | R = 10,000 |
| Semilla | 2026 |

Simula la compra secuencial de sobres hasta agotar el presupuesto o completar el álbum.

- $P(\text{completar} \mid Q1{,}000)$
- Número esperado de sobres comprados
- Estampas distintas promedio en simulaciones fallidas
- Gráfica: proporción completó vs. no completó

**Preguntas de análisis:**
1. Máximo de sobres comprables (105) vs. mínimo teórico (`ceil(100/7)` = 15)
2. Caja de 104 sobres a Q 975: comparación de probabilidad con sueltos
3. Estrategia mixta (caja + sueltos adicionales) para maximizar P dentro de Q 1,000

**Resultados esperados:**

| Estrategia | Sobres | Costo | P(completar) |
|---|---|---|---|
| Sueltos con Q 1,000 | 105 | Q 997.50 | ~simulado |
| Caja sola | 104 | Q 975.00 | ~similar |
| Caja + 2 sueltos | 106 | Q 994.00 | ~mayor |

### Etapa 4 — Efecto del intercambio de repetidas

> **Regla de canje:** cada K estampas repetidas acumuladas se intercambian por 1 estampa nueva elegida entre las faltantes. El canje se aplica tras cada sobre.

| Parámetro | Valores |
|---|---|
| K (tasa de canje) | 1, 2, 5, 10 |
| R por configuración | 10,000 |
| M (Parte B) | 20, 25, 30, …, 70 |

**Parte A — Sobres hasta completar:**
- Media, std y reducción porcentual respecto al caso sin canje por cada K
- Ahorro en quetzales (a Q 9.50/sobre)
- Histogramas superpuestos

**Parte B — P(completar | M) por K:**
- Gráfica de líneas con curva de referencia sin canje
- Umbrales 50%, 75% y 90% para cada K
- Rendimiento marginal ampliado (K = 1, 2, 3, 4, 5, 7, 10)

**Resultados esperados:**

| K | Reducción aprox. | Ahorro (Q) |
|---|---|---|
| 10 | ~5–10% | ~Q 35–70 |
| 5 | ~15–25% | ~Q 100–165 |
| 2 | ~30–40% | ~Q 200–265 |
| 1 | ~40–50% | ~Q 265–335 |

---

## Laboratorio 9

### Etapa 5 — Álbum real del Mundial 2026 (N=980)

> Escala la simulación al álbum oficial Panini del Mundial FIFA 2026: **980 estampas distintas**, **7 estampas por sobre**, precio Q 9.50/sobre, caja de 104 sobres a Q 975.

| Parámetro | Valor |
|---|---|
| N (estampas distintas) | 980 |
| S (estampas por sobre) | 7 |
| Precio por sobre | Q 9.50 |
| Precio por caja (104 sob.) | Q 975 |
| Semilla | 2026 |

La implementación usa arrays booleanos de NumPy (`np.zeros(N, dtype=bool)`) en lugar de conjuntos Python para garantizar eficiencia con N=980.

---

#### Pregunta 1 — ¿Cuántos sobres y cuánto dinero para completar el álbum?

**R = 500 simulaciones**

Estima la distribución del número de sobres necesarios para coleccionar las 980 estampas. Compara la media simulada con el valor teórico $E[T] = \frac{N}{S} \cdot H_N$.

**Resultados:**

| Métrica | Valor |
|---|---|
| E[sobres] simulado | ~1,037–1,040 |
| E[T] teórico | 1,045.1 |
| Costo esperado | ~Q 9,850–9,880 |
| Mediana | ~1,000–1,010 sobres |
| Percentil 90 | ~1,255–1,283 sobres |

---

#### Pregunta 2 — ¿Con qué presupuesto hay ≥ 50%, 75% y 90% de probabilidad?

**R = 300 simulaciones por punto · presupuestos Q4,000 a Q14,000**

Barre distintos presupuestos y estima la fracción de simulaciones que completan el álbum con ese gasto.

**Resultados:**

| Umbral | Presupuesto mínimo |
|---|---|
| P ≥ 50% | Q 10,000 |
| P ≥ 75% | Q 11,000 |
| P ≥ 90% | Q 12,000–12,500 |

---

#### Pregunta 3 — Con Q10,000, ¿qué combinación cajas + sueltos maximiza P(completar)?

**R = 300 simulaciones por combinación · 11 estrategias (0–10 cajas)**

Para cada número de cajas compradas primero, calcula cuántos sueltos adicionales caben en Q10,000 y simula la probabilidad de completar.

**Resultado:** la combinación de **7 cajas + sueltos adicionales** (~334 sueltos, total ~1,062 sobres) maximiza P ≈ 0.65.

---

#### Pregunta 4 — ¿Cuánto ahorra el intercambio K=5 en sobres y quetzales?

**R = 300 simulaciones · K = 5**

Aplica el mecanismo de canje (5 repetidas → 1 estampa nueva) y compara el número medio de sobres con y sin intercambio.

**Resultados:**

| Escenario | Sobres promedio | Costo aprox. |
|---|---|---|
| Sin intercambio | ~1,053 | ~Q 10,000 |
| Con K=5 | ~281 | ~Q 2,670 |
| **Ahorro** | **~773 sobres** | **~Q 7,340 (73%)** |

---

#### Pregunta 5 — ¿Cómo cambia el costo al variar el tamaño del sobre S (5 a 9)?

**R = 300 simulaciones por valor de S**

Evalúa cómo el número de estampas por sobre afecta el costo total esperado, manteniendo N=980 fijo.

**Resultados:**

| S | E[sobres] | Costo aprox. | vs S=7 |
|---|---|---|---|
| 5 | ~1,456 | ~Q 13,830 | referencia |
| 6 | ~1,209 | ~Q 11,490 | referencia |
| 7 | ~1,066 | ~Q 10,125 | base |
| 8 | ~908 | ~Q 8,625 | −14.8% |
| 9 | ~816 | ~Q 7,750 | −23.5% |

---

## Teoría

**Valor esperado teórico (coupon collector con sobres de S items):**

$$E[\text{sobres}] = \frac{N}{S} \cdot H_N, \quad H_N = \sum_{k=1}^{N}\frac{1}{k} \approx \ln N + \gamma$$

con $\gamma \approx 0.5772$ (constante de Euler-Mascheroni).

| Álbum | N | S | $H_N$ | $E[\text{sobres}]$ | $E[\text{repetidas}]$ |
|---|---|---|---|---|---|
| Simplificado (Labs 7–8) | 100 | 7 | ≈ 5.187 | ≈ 74.04 | ≈ 418.25 |
| Real Mundial 2026 (Lab 9) | 980 | 7 | ≈ 7.314 | ≈ 1,045.1 | ≈ 6,371 |

**Costo efectivo por estampa nueva vía canje:**

$$C_{\text{canje}}(K) = K \cdot \frac{Q\,9.50}{7}$$

---

## Requisitos

```bash
pip install numpy matplotlib jupyter
```

## Ejecución

```bash
# Laboratorio 7
python etapa1.py
python etapa2.py
jupyter notebook laboratorio7_panini.ipynb

# Laboratorio 8
python etapa3.py
python etapa4.py
jupyter notebook laboratorio8_panini.ipynb

# Laboratorio 9
python etapa5.py
jupyter notebook laboratorio9_panini.ipynb
```