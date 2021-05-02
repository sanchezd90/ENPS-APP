# ENPS APP
Esta es una app para realizar evaluaciones neuropsicológicas y acceder a la información de evaluaciones previas. Esta es una versión de muestra, la original y más completa está en producción en un sitio privado. 

Esta versión está corriendo en Heroku [https://enps.herokuapp.com/enps]

Esta versión solo cuenta con la posibilidad de realizar una evaluación con la tarea RAVLT. RAVLT es una tarea de memoria verbal que requiere que el evaluado recuerde una lista de palabras que se le leen a través varios ensayos. Esta app permite registrar las respuestas, calificarlas y obtener un puntaje para cada ensayo basado en valores normativos. 

Cada una de las evaluaciones se almacenan en una base de datos (MongoBD) y pueden ser retomadas en cualquier momento. Para eso la app cuenta con un explorador básico de evaluaciones realizadas. 

El proyecto original contempla la inclusión de varias pruebas más y la posibilidad de generar un informe de evaluación. Además permitirá eliminar o editar registros a usuarios con el rol indicado. 
