Para hacer la parte dos de la actividad se han usado muchas funciones para cumplir con el paradigma de programación funcional. A continuación enumeramos cada función (y objeto) y su uso:

1. `text_to_dict`: Recibe un string que será lo que devuelve la API cuando solicitas contraseñas leakeadas. Con este string se pasa por el primer map convirtiendolo en un iterable usando `.striplines()`, devolviendo un nuevo iterable que divide cada linea con `.split(':')`. Con este segundo iterable de salida se pasa por un segundo map que lo convierte en un diccionario donde la hash de la contraseña es la clave, y el número de veces leakeado como valor.

2. `Ption(StrEnum)`: La clase `Ption` es un `StrEnum` lo que significa que de esta clase, las variables definidas (`PasswdSHA1`, `Domain`) contienen strings de urls que hagan las peticiones a las que se asemeja su nombre a la API. La gracia de usar esto en lugar de un diccionario es que es estático y más rápido.

3. `Color(StrEnum)`: Es lo mismo que la clase anterior pero en este caso se definen colores para pasarlos a la función paint junto a un string para que la salida de la terminal tenga colores.

4. `paint`: Simplifica el repetitivo proceso de escribir strings con color.

5. `PARSERS`: Es un diccionario de clave tipo `Ption` (el tipo de petición) y valor Callable. Este diccionario lo usaremos para transformar los datos que recibimos del request de la API según el tipo de consulta que hagamos. Esto es necesario ya que la API puede devolver un `.txt` o un `.json` dependiendo de la consulta.

6. `ApiResponse(NamedTuple)`: Con esta clase de tipo NamedTuple definimos el tipo de objeto que devolverá las consultas que hagamos la con la API. Es buena práctica crear esta clase ya que la API no devuelve un objeto estandarizádo, por lo que sería muy complicado de manejar si hay muchos casos de uso.

7. `get_api_data`: Esta función es la que hace el request a la API; recibe un objeto de tipo PTion para elegir el tipo de petición y un argumento de tipo string para pasarlo junto a la petición (contraseña, dominio...). Gracias a la función `.format(arg)` podemos sustituir las llaves de las urls que contiene `Ption` por el string que queramos. Después, dependiendo de las respuesta (`.ok`), se creará una instancia de la clase `ApiResponse` y se devolverá este mismo.

8. `manage_data`: Manage data recibe un objeto de tipo `ApiResponse` y dos callbacks, uno en el que la `respuesta.ok` sea verdadera para manejar sus datos de éxito, y otra para manejar el mensaje de error de las respuesta.

9. `get_error`: Es un callback que devuelve el mensaje de error pintado de rojo y con una exclamación.

10. `get_passwd_info`: Es el callback que se usaría cuando se llama a las peticiones de contraseñas leakeadas. Recibe el diccionario creado con `text_to_dict`, busca en el diccionario la contraseña que tenemos en el parámetro `passwd`. Si la encuentra o no devuelve un string según el caso.

11. `parse_domain_breach`: Recibe un diccionario con la respuesta de la API sobre los leakeos de dominios y devuelve cierta información de esta en un string.

12. `get_domain_info`: Callback que se usa cuando se hace una petición de tipo `Ption.Domain`. Recibe una lista de diccionarios con data breaches registrados. Este iterador lo pasa por un map con la función `parse_domain_breach`. Después con el iterable de salida se junta todo en un string con `.join()`.

13. `sha1`: Convierte un string a hash en sha1.

14. `ntlm`: Convierte un string a hash en ntlm.

15. `main`: En el main se manejan las flags del script con la librería `argparse`.
