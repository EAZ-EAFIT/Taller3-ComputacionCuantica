# Taller 3 Computación Cuántica Universidad EAFIT
### Esteban Álvarez Zuluaga

---
## Descripción
El presente programa permite la ejecución del algoritmo de Grover de busqueda para el caso general de multiples valores. Recibe como parametro una lista de elementos, que corresponden a los indices de respuesta a un problema de busqueda, o los valores donde f(x) = 1 para una funcion $\\{1, 0\\}^n$ -> $\\{0,1\\}$. El programa genera una grafica del circuito cuántico utilizado, asi como el resultado de una simulación de multiples ejecuciones del algoritmo, donde se evidencia que las más probables son las respuesta esperada.
## Instalación
Descargar Python 3.11.9 y las dependencias expuestas en `requirements.txt`.
Si se utiliza pip, se puede usar el comando:
   ```bash
  pip install -r requirements.txt
```
## Ejecución
Para ejecutar, se puede correr el siguiente comando, con los numeros que se busquen.
   ```bash
  python Grovers_algorithm.py <search_answer_1> <search_answer_2> ... <search_answer_n>
```
