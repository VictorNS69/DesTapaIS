Este documento resumirá **las normas de calidad** que acordemos. Todos podemos aportar.

- **NO SE PUSHEA A MASTER SIN PR (pull request)**: Siempre se ha de crear una **nueva branch** y hacer una PR. Otro miembro (que no sea el de la PR) tiene que revisar el código. Pueden hacer varios una revisión. A la hora de hacer la PR pone quien la tiene que revisar. Aunque Víctor llevará el control del repositorio.
- Los **commits** tienen que ser identificativos y claros para la persona que no ha trabajado en ese commit. No son válidos commits estilo _"funciona", "fix", "no se que poner"_, etc. Si se ha testeado la función suma, el commit podrá ser del estilo _"testeada función suma"_. Si se quiere, se puede poner tanta información como se desee en el commit, ya que no hay un máximo de caracteres.
- Si se **cierra un issue** en un commit, hay que añadir al commit lo siguiente: `Closes #nº_issue`. Para más información pinchar [aquí](https://help.github.com/en/articles/closing-issues-using-keywords). 

_Echadle un ojo que es muy interesante saber usar esta característica_. **OJO!** Esto **solo cierra issues** no tarjetas. También, el **issue no se cerrará hasta que se haga el merge** pero eso se hará automáticamente una vez se apruebe la PR.
- Puede haber tarjetas (en el board/proyecto) que no esten asignadas a issue, pero **la mayoría de tarjetas estarán relacionadas a un issue**.
- Los documentos, para que sean más faciles de hacer entre todos estarán en [Drive](https://drive.google.com/drive/folders/11TI6JH4CGTRb-80Cpk__9QrWz_RezDju?usp=sharing). Aún así, los documentos finales en versión _PDF_ seguramente si los subamos a git.
- El repositorio tiene que estar **bien estructurado** con sus carpetas y subcarpetas (tantas como sea necesario)
- Por si es necesario, [aquí](https://www.markdownguide.org/) teneis una guía de Markdown (los .md).
- **Si alguien está trabajando en un issue, se lo tiene que asignar** (barra lateral derecha, asignar).

### Cómo crear Issues
_Aunque Víctor intentará ser el que cree todos los issues, puede darse el caso de que el resto necesite crear un issue. Si es así, seguid las instrucciones de aquí._

Desde la web de Github, ir al apartado _Issues_ y ahí escribir un título descriptivo y una buena descripción (si es un issue sencillo de entender con el título, no hará falta descripción.

También hay que añadir en la barra lateral derecha la siguiente información:
- **Labels**: Etiquetas que se consideren necesarias. Como mínimo debería estar la etiqueta del "encargado" de la tarea.
- **Projects**: Asignar siempre el proyecto de _"Práctica ISII"_.
- **Milestone**: Asignar la fecha límite a la que haga referencia dicho Issue. Si no es específica de ninguna milestone, asignar la primera disponible.

**NOTAS**:
- Si se considera necesario, **se pueden crear más** _labels_ y _tags_. En principio no es necesario crear ninguna nueva _milestone_ pero puede darse el caso.
- **Se pueden crear tantos issues como se desee**. Un **issue se transforma automáticamente en tarjeta del board**. Así que no creéis un issue y una tarjeta. 
- **Si la tarea se considera que no necesita crear un issue**, entonces solo hay que crear la tarjeta en el board.
- Si existe una tarjeta y se desea pasar a issue, se puede hacer desde el board en una de las opciones. Tras hacer eso tendrías que añadir los campos mencionados arriba.
### Cómo hacer una Pull Request (PR)
Básicamente **hay que hacer lo mismo que en la creación de issues**, salvo que aquí no es necesario asignarsela (_Assignees_) a nadie. En cambio, **se necesita mínimo una persiona como _Reviewer_**. Una vez aprobado el cambio por ese Reviewer (u otra persona que haga revisión) se podrá mergear.

**NOTA:** No sé si es obligatorio que Víctor haga revisión para poder mergear

Una vez cerrada y mergeada la PR, **la rama se borrará automáticamente**.
### Cerrar issues
Como he mencionado antes, la mejor manera para que todo funcione correctamente es añadir en el mensaje de commit alguna palabra clave de [aquí](https://help.github.com/en/articles/closing-issues-using-keywords). Pero si por algún motivo no se ha hecho así, o no hay commit que cierre esa issue, se puede cerrar de manera manual desde la pestaña issues.
### Cómo trabajar con ramas
Podéis crear la rama de dos maneras. 

1. Desde el propio GitHub donde pone "Branch:master" clickar y escribir el nombre de la rama. Esto creará la rama en el repositorio y tendréis que hacer `git pull` para tenerla en local.

2. Desde la línea de comandos escribiendo `git checkout -b nombre_rama` una vez eso, hay que pushear la rama. Al hacer `git push` dará un error con un mensaje, el comando de ese mensaje es el que tenéis que ejecutar para pushear la rama al repositorio remoto.

**Nota**: Para mayor comodidad, **el nombre de la rama se deberá identificar con el issue en el que se está trabajando**.

Se pueden tener tantas ramas a la vez como se desee.

Para que sea más facil ver en el terminal en que rama estáis, podéis hacer lo que dice [este gist](https://gist.github.com/VictorNS69/f86527dd094fac13466b61527338438b) que hice yo. Despues de hacerlo, tenéis que hacer `source ~/.bashrc`.

También, para saber en que rama estás trabajando sin hacer lo que dice el gist, en el terminal escribid `git branch`.
