IMT2230-Proyecto_2-Creacion-de-page-rank — Red de confianza Bitcoin OTC

En este proyecto se aplico el algoritmo de **PageRank** sobre la red real [Bitcoin OTC](http://konect.cc/networks/soc-sign-bitcoinotc/), una red dirigida, ponderada y firmada que registra las calificaciones de confianza (de -10 a +10) que se dan entre si los usuarios de la plataforma [bitcoin-otc.com](https://bitcoin-otc.com/) al momento de comerciar Bitcoins de forma directa, sin pasar por un exchange centralizado.

Buscamos usar PageRank no solo como una medida de popularidad, sino como una herramienta para rastrear si existe un nucleo de usuarios de alta confianza dentro de una plataforma anonima, y si este algoritmo es capaz de identificar a sus miembros mas centrales.

Este trabajo fue elaborado por:

| Nombre del Alumno | Cuenta de GitHub |
| :--- | :--- |
| Esteban Cortes | [@esteban78009](https://github.com/esteban78009) |
| Sebastian Pinochet | [@sebastian18931](https://github.com/sebastian18931) |

Para la ejecucion de este proyecto se debe de correr en python, recomendamos usar python 3.11 o superior junto con la descarga de las siguientes librerias :

- numpy
- networkx
- matplotlib
- seaborn
- pandas
- scipy

Ademas que se debe de hacer uso de la red de archivos que se encuentra, tanto en este github, como respetando nuestro sistemas de ruta y descargandola en la siguiente pagina([soc-sign-bitcoinotc](http://konect.cc/networks/soc-sign-bitcoinotc/)) 

## Descripcion de la red

Cada nodo de la red representa a un usuario (comprador o vendedor) registrado en la plataforma, y cada arista dirigida representa la calificación que un usuario le da a otro luego de una transacción, con un peso entre -10 (estafa/desconfianza total) y +10 (confianza total). La red cuenta con 5.881 nodos y 35.592 aristas.

## Hipotesis

Nuestra hipótesis que guio este proyecto es la siguiente:

Planteamos que los usuarios con mayor rating promedio recibido no están distribuidos de forma aleatoria en la red, sino que forman uno o varios clústeres de confianza densamente interconectados entre si. A partir de esto esperábamos que:

1. Los nodos con mayor PageRank coincidieran en gran medida con los nodos de alto rating promedio positivo.
2. El subgrafo inducido por los nodos de alto PageRank tuviera una densidad interna notablemente mayor a la densidad global de la red.
3. Los pesos promedio de las aristas dentro de este cluster fueran mas positivos que los de las aristas mixtas (cluster-resto de la red).

Esta hipotesis se basa en la logica de los sistemas de reputacion: en una plataforma donde el anonimato impide conocer al otro de antemano, los traders confiables tienden a calificarse mutuamente de forma positiva y recurrente, formando una comunidad cohesionada que el PageRank deberia poder revelar como el nucleo central de la red.

Se relatan nuestros metodos de mejor manera en el archivo main.ipynb, sin embargo, como resumen de la tecnica usada:

### Construccion de la Matriz de Google

A partir del grafo dirigido se construyo la matriz de hipervinculos $H$, donde cada columna representa la distribucion de salida de un nodo. Los nodos colgantes (sin aristas de salida) se repararon reemplazando su columna por el vector uniforme $\mathbf{1}/n$, obteniendo asi la matriz columna-estocastica $S$. Finalmente se construyo la Matriz de Google:

$$G = \alpha S + \frac{1-\alpha}{n}\mathbf{1}\mathbf{1}^T$$

usando $\alpha = 0.85$, el valor estandar de la industria que equilibra la influencia de la estructura del grafo con el salto aleatorio que garantiza la convergencia.

### Calculo del PageRank

El vector de PageRank se calculo resolviendo el problema de valor propio $G\mathbf{r} = \mathbf{r}$ mediante iteracion de potencias, partiendo del vector uniforme $\mathbf{r}^{(0)} = \mathbf{1}/n$ e iterando hasta que el error $\|\mathbf{r}^{(k+1)} - \mathbf{r}^{(k)}\|_1 < 10^{-10}$, verificando ademas que la convergencia siguiera una razon geometrica aproximada a $\alpha$.

### Explicacion del metodo

Al no contar la red con metadatos mas alla del id de cada usuario (por tratarse de una plataforma anonima), se construyeron atributos propios a partir del rating promedio recibido por cada nodo y la fraccion de calificaciones negativas recibidas, lo que permitio clasificar a los usuarios en categorias de confianza (alto, neutral, sospechoso) y asi poder interpretar el ranking obtenido y compararlo con la estructura del subgrafo inducido por los nodos de mayor PageRank.

### Resultados

Si bien recomendamos leer el informe (proyecto_page_rank.pdf) y consultar el notebook main.ipynb para obtener mas detalle de esto mismo, se pudo observar que dos de las tres predicciones de nuestra hipotesis se confirmaron: la densidad interna del top-PageRank supero ampliamente a la densidad global de la red y los pesos promedio de las aristas intra-cluster resultaron notablemente mas positivos que los de las aristas mixtas. El coeficiente de clustering local del top-PageRank fue, en cambio, menor al promedio global, lo cual se explica por la presencia de nodos tipo "hub" altamente conectados. En conjunto, esto respalda que el PageRank logra identificar un nucleo de confianza dentro de la red de Bitcoin OTC, compuesto casi en su totalidad por usuarios de categoria neutral o de alto rating, con los nodos sospechosos practicamente ausentes de dicho nucleo.




