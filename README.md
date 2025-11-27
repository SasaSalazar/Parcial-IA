# Parcial — NL to PDDL (Web UI) VERSION 2


Esta es la **Versión 2** del proyecto.  
Contiene mejoras importantes sobre la versión 1, incluyendo:

- Extracción más precisa de objetos.  
- Mejor manejo de secuencias lógicas.  
- Precondiciones y efectos más consistentes.  
- Modelo PDDL más adecuado para planificadores automáticos.

pero aun tiene errores no es perfecta.

Es la versión **recomendada** para la evaluación.

---


# ⚠️ Instrucciones obligatorias para ejecutar correctamente

## 1. Solo usar esta versión de manera aislada  
Por favor evite tener dos versiones del proyecto descargadas al mismo tiempo.

Flask puede fallar si detecta archivos duplicados, rutas repetidas o múltiples aplicaciones relacionadas.

## 2. Si ya probó la versión 1

Debe hacer lo siguiente ANTES de probar esta versión:

1. Cerrar toda ventana donde Flask haya estado corriendo.  
2. Eliminar la carpeta completa de `Parcial-IA` previamente descargada.  
3. Clonar únicamente esta rama.  
4. Ejecutar Flask desde aquí.

## 3. Cada versión está en una rama separada  
- No mezclar archivos entre ramas.  
- No mover archivos de una versión a otra.  
- No combinar carpetas.
- No respirar >:c.

---

# Cómo clonar exactamente esta versión

```
git clone --branch version-2 --single-branch https://github.com/TU_USUARIO/Parcial-IA.git
cd Parcial-IA
```
-O descarga directamente el .zip en github depensiendo de la rama/version que desees probar.

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

-En terminal: carpeta parcial-inteligencia artificial

-pip install flask requests flask-cors

-python app.py

-Abre en navegador: http://127.0.0.1:5000

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
