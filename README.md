## IMPORTANTE

Existen DOS versiones de este Proyecto:
- proyecto.py - Corre en macOS. Si se utiliza con Windows, se encontrarán errores debido a los nombres de los archivos, pues algunos caracteres no son permitidos en Windows
- proyectoWINDOWSver.py - Es la versión de Windows. Trae líneas de código que modifican los nombres para poder ser aceptados/guardados en Windows. Incluye todas las líneas originales de macOS también, pero como comentario para evitar conflictos.

Es importante tomar esto en cuenta a la hora de correr el archivo correspondiente.
Se procesan las siguientes expresiones:
- p
- ~~~p
- (p^q)
- (0=>(ros))
- ~(p^q)
- (p<=>~p)
- ((p=>q)^p)
- (~(p^(qor))os)

Para cada una se puede observar lo siguiente: Análisis Sintáctico, Tokenización, creación de árbol y AFN de su respectiva expresión.