# Parcial — NL to PDDL (Web UI) VERSION 1

Esta es la **Versión 1** del proyecto.  
Es funcional y genera correctamente `domain.pddl` y `problem.pddl`, pero utiliza un modelo más simple que la Versión 2.


# ⚠️ Instrucciones muy importantes para evitar errores

Por favor siga estas indicaciones textualmente para evitar conflictos al ejecutar Flask:

## 1. Solo pruebe **una versión del proyecto a la vez**  
No descargue o mantenga dos carpetas distintas del proyecto en el mismo computador.

Flask detecta conflictos cuando existen dos copias del mismo proyecto o dos aplicaciones similares.

## 2. Si desea probar otra versión (p. ej. version-2)
Debe hacer esto EXACTAMENTE:

1. **Cerrar** cualquier ventana de terminal que esté ejecutando Flask.  
2. **Eliminar por completo** la carpeta actual del proyecto.  
3. **Clonar o descargar nuevamente dependiendo de la version deseada por rama** la otra rama que desee probar.  
4. Ejecutar Flask desde esa nueva carpeta.

## 3. No mezclar ramas  
Por favor **no mezclar archivos** entre versiones.  
Cada rama representa un estado distinto del proyecto.

---

# Cómo clonar esta versión exactamente

```
git clone --branch version-1 --single-branch https://github.com/SasaSalazar/Parcial-IA.git
cd Parcial-IA
```


## Requisitos
- Python 3.8+
- pip install flask requests flask-cors

## Estructura
- app.py
- pddl_generator.py
- templates/index.html
- static/style.css
- output/ (se crea automáticamente)

## Ejecutar
1. En terminal: carpeta parcial-inteligencia artificial

pip install flask requests flask-cors
python app.py

2. Abre en navegador: http://127.0.0.1:5000

## Uso
- Escribe una instrucción (ES o EN), pulsa *Generar PDDL*.
- Verás `domain.pddl` y `problem.pddl` en la página.
- Puedes descargar ambos desde los enlaces.
- Pulsando *Generar + Obtener plan (remoto)* pedirá un plan al solver público planning.domains.


## Notas

- El botón Generar + Obtener Plan Remoto NO funciona. Estoy viendo cómo arreglarlo, pero por el momento no funciona, así que no lo pruebes.

- Profe, por favor colocar las frases que te muestro a continuación, similares, parecidas, o idealmente las mismas. Por favor, no le pongas cosas raras. Profe, no sea malo, se lo suplico.: cubre muchos casos típicos (buy/make/clean/go/neutralize).

- 1. Nivel básico (acciones simples)

dominios pequeños xd:

“El robot debe recoger una manzana de la mesa.”

“El agente debe ir al cuarto y encender la luz.”

“El robot debe llevar un libro desde la mesa hasta la estantería.”

“El agente debe abrir la puerta del dormitorio.”

“El robot debe tomar una llave y usarla para abrir un cofre.”

- 2. Nivel intermedio 

acciones con condiciones:

“El robot debe preparar té, pero solo después de hervir el agua en la tetera.”

“El agente debe cargar una batería antes de activar el dron.”

“El robot debe construir un juguete, pero necesita todas las piezas primero.”

“El agente debe arreglar la máquina, pero debe tener un destornillador.”

“El robot debe entregar un paquete, pero primero tiene que encontrarlo.”

- 3. Nivel avanzado (secuencias más largas o lógicas)

“El robot debe cocinar pasta: llenar la olla, hervir el agua y luego añadir la pasta.”

“El agente debe rescatar a un gato: localizarlo, acercarse, levantarlo y volver con él al punto inicial.”

“El robot debe limpiar una habitación: recoger basura, barrer el piso y vaciar el cubo.”

“El agente debe reparar un generador: quitar la tapa, reemplazar la pieza dañada y cerrar la tapa.”

“El robot debe montar una tienda de campaña: armar las estacas, colocar la tela y tensar las cuerdas.”

4. Nivel narrativo 

Posee cierto yo no sé cuá:

“El androide debe recuperar un chip de memoria perdido y cargarlo en su núcleo.”

“El agente debe infiltrarse en el laboratorio y robar un archivo codificado.”

“El robot debe sellar una fuga de plasma antes de que el reactor se inestabilice.”

“El androide debe encontrar una flor marchita y revivirla con un líquido nutritivo.”

“El agente debe salvar a un niño: localizarlo, liberarlo y llevarlo a un lugar seguro.”
