# ProblemRandomizer

## Resumen 

Este es un módulo de python que permite de manera conveniente crear bancos aleatorios de preguntas (enfocado a preguntas de los cursos básicos universitarios de matemáticas) de manera local, a partir de un archivo Json en donde puede incluir fórmulas matemáticas en formato LaTeX, en un archivo zip que se puede importar directamente a Blackboard. Las preguntas pueden ser de tipo Opción múltiple, Ensayo, Respuesta numérica, Rellenar los espacios en blanco y Respuesta de archivo. 

Idealmente este puede ser útil para superar las limitaciones y el lento funcionamiento del editor de preguntas de Blackboard, ya que este además permite generar diferentes versiones de una misma pregunta (con su respectiva respuesta), de manera que se puede obtener fácilmente suficientes versiones distintas de un mismo exámen (como para que cada estudiante tenga un examen diferente al de los demás compañeros al momento de aplicar la prueba). 

## Dependencias

Este paquete requiere tener instalado en su equipo python3, python-lxml, python-image, imagemagick, sympy, scipy y LaTeX. Se puede instalar estos fácilmente en ubuntu de la siguiente manera:

```
sudo apt-get install python-lxml python-image imagemagick  python-sympy 
```

¡Este también debería funcionar en Windows! (Aunque hasta la fecha se desconoce una manera no desesperante de lograr esto.)

## Cómo usarlo (Python3)

Basta con correr el programa ProblemRandomizer.py desde la linea de comandos pasando como parámetro la ruta, ya sea absoluta o local, del archivo Json que contiene la información de los conjuntos de preguntas a generar. Por ejemplo, al correr `python3 ProblemRandomizer.py example_0.json` se generará un archivo con nombre _Examen 0.zip_ el cual contiene varios conjuntos de preguntas, donde cada uno corresponde a distintas versiones de la misma pregunta. A su vez este archivo zip contiene unos archivos html con los cuales puede visualizar desde su navegador los conjuntos de preguntas generados previo a la carga de estos a Blackboard.

Se incluyen 4 archivos Json que sirven de ejemplo para el funcionamiento de cada tipo de pregunta, cada uno genera un archivo zip el cual se puede cargar a Blackboard siguiendo la opción de Cargar prueba en la sección de Pruebas disponible en el menú de Herramientas del curso en la parte correspondiente a Pruebas, sondeos y conjuntos (estos quedan cargados como conjuntos de preguntas listos para importar a sus pruebas). Los archivos Json deben seguir un formato que especifica no sólo el contenido, sino el tipo y la cantidad de versiones de cada pregunta. 

## Cómo funciona

El proyecto consta de 3 módulos python: **ProblemRandomizer.py, RandomMathObjects.py y MyBlackboardQuiz.py**

Los últimos 2 son esenciales para el correcto funcionamiento del módulo principal, ya que el segundo es el que se encarga de generar muestras aleatorias de diversas variables aleatorias correspondientes a distintos objetos matemáticos, mientras que el último se encarga de crear el archivo zip que contiene los archivos con el formato correcto para cargar las preguntas a Blackboard. 

Este último corresponde a una versión aumentada del módulo _BlackboardQuiz.py_ obtenida del proyecto [BlackboardQuizMaker](https://github.com/toastedcrumpets/BlackboardQuizMaker).
