# Paradigmas de Programación — Práctica 1: Programación funcional
El código de cada ejercicio está en su `main.py` correspondiente:

| Parte | Ejercicio | Fichero | Funciones |
|---|---|---|---|
| 1 | Palíndromos | `part-1/1/main.py` | `is_palindrome`, `palindromes` |
| 1 | Suma de cuadrados | `part-1/2/main.py` | `square_sum` |
| 1 | Factorial | `part-1/3/main.py` | `factorial` |
| 1 | Estudiantes aprobados | `part-1/4/main.py` | `has_passed`, `filter_students` |
| 2 | haveibeenpwned | `part-2/main.py` | `text_to_dict`, `Ption`, `Color`, `paint`, `PARSERS`, `ApiResponse`, `get_api_data`, `manage_data`, `get_error`, `get_passwd_info`, `parse_domain_breach`, `get_domain_info`, `sha1`, `ntlm` y bloque principal |

---

## Parte 1

### Ejercicio 1 — Palíndromos

En este ejercicio se han creado dos funciones.

#### `is_palindrome(word: str) -> bool`

```python
def is_palindrome(word: str) -> bool:
    palindrome = True
    o: int = 0
    e: int = len(word) - 1

    while o != e:
        if word[o] != word[e]:
            palindrome = False
            break
        o += 1
        e -= 1

    return palindrome
```

Recibe un string (la palabra) y devuelve un booleano que indica si es palíndromo. Para ello crea dos índices que recorren la palabra: `o`, que empieza en la posición 0, y `e`, que empieza en la última posición (`len(word) - 1`). Mientras ambos índices no coincidan (es decir, hasta llegar al centro de la palabra), el bucle `while` compara letra a letra los dos extremos de la palabra y acerca los índices hacia el centro. Si en alguna de estas comparaciones las letras no coinciden, la variable que se devolverá, `palindrome`, pasa a ser `False` y se sale del bucle con `break`.

#### `palindromes(words: list[str]) -> list[bool]`

```python
def palindromes(words: list[str]) -> list[bool]:
    return list(map(is_palindrome, words))
```

Recibe una lista de strings y devuelve una lista de `True`/`False` indicando cuáles son palíndromos. Simplemente aplica `map` con la función `is_palindrome` sobre la lista de palabras y convierte el resultado en una lista.

`map` es una función de orden superior: recibe otra función (`is_palindrome`) como argumento y la aplica a cada elemento del iterable, sin necesidad de escribir un bucle. Como `map` devuelve un iterador perezoso, se convierte en lista con `list()`.

---

### Ejercicio 2 — Suma de cuadrados

#### `square_sum(num: int) -> int`

```python
def square_sum(num: int) -> int:
    return sum(map(lambda x: x**2, range(1, num)))
```

Devuelve la suma de los cuadrados de los números que genera `range(1, num)`. Para ello se hace lo siguiente:

1. Se crea un iterable con `range(1, num)`, que será el parámetro iterable de `map()`.
2. Se define una función lambda (función anónima) que eleva al cuadrado cada valor del iterable.
3. El resultado del `map()` se pasa a la función `sum()`, que suma todos los valores del iterable.

Toda la función es una única expresión que compone `range`, `map` y `sum`, sin variables intermedias ni bucles.

---

### Ejercicio 3 — Factorial

#### `factorial(num: int) -> int`

```python
from functools import reduce


def factorial(num: int) -> int:
    return reduce(lambda x, y: x*y, range(1, num+1))
```

Calcula el factorial de un número entero. Para ello se usa la función `reduce` de `functools`, que aplica una función de dos argumentos sobre los elementos de un iterable de forma acumulativa, reduciéndolo a un único valor.

Como función se le pasa una lambda que multiplica el valor acumulado (`x`) por el siguiente valor (`y`), y como iterable `range(1, num+1)`, es decir, los números de 1 a `num`. Por ejemplo, para `num = 5` se calcula `((((1 · 2) · 3) · 4) · 5) = 120`.

---

### Ejercicio 4 — Estudiantes aprobados

En este ejercicio se han creado dos funciones para filtrar, de una lista de diccionarios, los estudiantes que tienen una media igual o superior a 6.

#### `has_passed(student: dict[str, Any]) -> bool`

```python
def has_passed(student: dict[str, Any]) -> bool:
    scores = student["calificaciones"]
    return sum(scores)/len(scores) >= 6
```

Recibe un estudiante (un diccionario) y selecciona de él la lista de calificaciones. Con ella calcula la media: suma todos sus valores con `sum()` y los divide entre la longitud de la lista con `len()`. Si el resultado es igual o superior a 6 devuelve `True`; en caso contrario, `False`.

Es una función pura: no modifica el diccionario que recibe y, para la misma entrada, siempre devuelve el mismo resultado.

#### `filter_students(students: list[dict[str, Any]]) -> list[dict[str, Any]]`

```python
def filter_students(students: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return list(filter(has_passed, students))
```

Devuelve un `filter` de la lista de estudiantes usando la función anterior, `has_passed`, como función evaluadora, y lo convierte en lista para obtener la lista filtrada de estudiantes.

`filter` es una función de orden superior que se queda solo con los elementos para los que la función evaluadora devuelve `True`. No modifica la lista original, sino que genera una nueva.

Con la lista de ejemplo del enunciado, el resultado es el siguiente:

| Estudiante | Calificaciones | Media | `has_passed` |
|---|---|---|---|
| Juan | 7, 8, 6, 5 | 6,50 | `True` |
| Ana | 9, 6, 8 | 7,67 | `True` |
| Pedro | 4, 5, 3 | 4,00 | `False` |
| Maria | 10, 9, 9 | 9,33 | `True` |
| Luis | 3, 2, 5 | 3,33 | `False` |

---

## Parte 2 — Script haveibeenpwned

El script permite dos modos de funcionamiento: comprobación de contraseñas (con hash SHA1 o NTLM) y comprobación de dominios. Para cumplir con el paradigma de programación funcional se ha dividido en muchas funciones pequeñas, cada una con una única responsabilidad. El flujo general es:

```
argumentos (argparse) → [hash de la contraseña] → get_api_data → ApiResponse → manage_data → callback de éxito o de error → print
```

Uso del script:

```bash
pip install -r requirements.txt

python main.py -p              # contraseña con hash SHA1
python main.py -p --ntlm       # contraseña con hash NTLM (formato Windows)
python main.py -d <dominio>    # dominio
```

En el modo contraseña, la contraseña se pide por teclado sin mostrarla en pantalla.

A continuación se describe cada función (y objeto) y su uso.

### 1. `text_to_dict(text: str) -> dict[str, Any]`

```python
def text_to_dict(text: str) -> dict[str, Any]:
    return dict(map(lambda item: (item[0], int(item[1])), map(lambda line: line.split(":"), text.splitlines())))
```

Recibe el string que devuelve la API cuando se consultan contraseñas filtradas. Ese texto tiene una línea por hash, con el formato `SUFIJO:VECES`. La función lo transforma en un diccionario encadenando dos `map`:

1. `text.splitlines()` divide el texto en líneas.
2. El primer `map` aplica `line.split(":")` a cada línea, devolviendo un nuevo iterable con el sufijo del hash y el contador separados.
3. El segundo `map` convierte cada par en una tupla `(sufijo, int(veces))`.
4. `dict()` construye el diccionario, donde el sufijo del hash de la contraseña es la clave y el número de veces que se ha filtrado es el valor.

### 2. `Ption(StrEnum)`

```python
class Ption(StrEnum):
    PasswdNTLM = "https://api.pwnedpasswords.com/range/{}?mode=ntlm"
    PasswdSHA1 = "https://api.pwnedpasswords.com/range/{}"
    Domain = "https://haveibeenpwned.com/api/v3/breaches?Domain={}"
```

La clase `Ption` es un `StrEnum`, lo que significa que sus miembros (`PasswdNTLM`, `PasswdSHA1`, `Domain`) contienen como string la URL de la petición a la API a la que hace referencia su nombre. Las llaves `{}` de cada URL se sustituyen después por el argumento de la consulta (prefijo del hash o dominio).

La ventaja de usar esto en lugar de un diccionario es que es estático: sus valores no se pueden modificar durante la ejecución, y además cada miembro tiene un tipo propio (`Ption`), lo que permite usarlo como tipo de parámetro y como clave del diccionario `PARSERS`.

### 3. `Color(StrEnum)`

```python
class Color(StrEnum):
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    PURPLE = "\033[95m"
    RESET = "\033[0m"
```

Es lo mismo que la clase anterior, pero en este caso se definen los códigos de escape ANSI de los colores, para pasarlos a la función `paint` junto a un string y que la salida de la terminal tenga colores.

### 4. `paint(text: str, color: Color) -> str`

```python
def paint(text: str, color: Color) -> str:
    return f"{color}{text}{Color.RESET}"
```

Simplifica el repetitivo proceso de escribir strings con color: devuelve el texto rodeado por el código del color y el código `RESET`, para que el color no se extienda al resto de la salida. No imprime nada, solo devuelve un nuevo string.

### 5. `PARSERS`

```python
PARSERS: dict[Ption, Callable[[str], Any]] = {
    Ption.PasswdNTLM: text_to_dict,
    Ption.PasswdSHA1: text_to_dict,
    Ption.Domain: json.loads,
}
```

Es un diccionario cuya clave es de tipo `Ption` (el tipo de petición) y cuyo valor es una función (`Callable`). Se usa para transformar los datos que se reciben de la API según el tipo de consulta que se haga. Esto es necesario porque la API devuelve texto plano en las consultas de contraseñas (que se transforma con `text_to_dict`) y JSON en las consultas de dominios (que se transforma con `json.loads`).

Las funciones se guardan en el diccionario como cualquier otro valor (funciones de primera clase), de modo que `get_api_data` elige el parser adecuado sin necesidad de condicionales.

### 6. `ApiResponse(NamedTuple)`

```python
class ApiResponse(NamedTuple):
    ok: bool
    data: Any = None
    error: str | None = None
```

Con esta clase de tipo `NamedTuple` se define el tipo de objeto que devuelven las consultas que se hacen a la API: un indicador de éxito (`ok`), los datos ya transformados (`data`) y, en su caso, el mensaje de error (`error`). Es buena práctica crear esta clase porque la API no devuelve un objeto estandarizado, por lo que sería muy complicado de manejar si hay muchos casos de uso. Al ser una `NamedTuple`, el objeto es inmutable.

### 7. `get_api_data(petition: Ption, arg: str) -> ApiResponse`

```python
def get_api_data(petition: Ption, arg: str) -> ApiResponse:
    response = requests.get(petition.format(arg))

    if response.ok:
        return ApiResponse(ok=True, data=PARSERS[petition](response.text))
    else:
        return ApiResponse(ok=False, error=f"Error: {response.status_code}")
```

Esta función es la que hace la petición a la API. Recibe un objeto de tipo `Ption` para elegir el tipo de petición y un argumento de tipo string que se pasa junto a la petición (prefijo del hash de la contraseña o dominio). Gracias a la función `.format(arg)` se sustituyen las llaves de las URL que contiene `Ption` por el string correspondiente.

Después, dependiendo de la respuesta (`response.ok`), se crea una instancia de `ApiResponse` y se devuelve:

- Si la petición tiene éxito, `ok=True` y en `data` los datos transformados con el parser que corresponde a la petición en `PARSERS`.
- Si no, `ok=False` y en `error` un mensaje con el código de estado HTTP.

### 8. `manage_data(data: ApiResponse, on_succes: Callable, on_error: Callable) -> str`

```python
def manage_data(data: ApiResponse, on_succes: Callable, on_error: Callable) -> str:
    if data.ok:
        return on_succes(data.data)
    else:
        return on_error(data.error)
```

Recibe un objeto de tipo `ApiResponse` y dos callbacks: uno para el caso en que `data.ok` sea verdadero, que maneja los datos de éxito, y otro para manejar el mensaje de error de la respuesta. Es una función de orden superior: no sabe qué hace cada callback, solo decide cuál ejecutar, por lo que la misma función sirve para los dos modos del script.

### 9. `get_error(error: str) -> str`

```python
def get_error(error: str) -> str:
    return paint(f"[!] {error}", Color.RED)
```

Es un callback que devuelve el mensaje de error pintado de rojo y precedido de una exclamación.

### 10. `get_passwd_info(data: dict[str, Any], passwd: str) -> str`

```python
def get_passwd_info(data: dict[str, Any], passwd: str) -> str:
    breach = data.get(passwd[5:])
    if breach:
        return paint(f"Password breached {breach} times", Color.RED)
    else:
        return paint("Password not breached", Color.GREEN)
```

Es el callback que se usa en las peticiones de contraseñas filtradas. Recibe el diccionario creado con `text_to_dict` y el hash completo de la contraseña (`passwd`), y busca en el diccionario el sufijo del hash (`passwd[5:]`, es decir, todo lo que va después de los 5 caracteres del prefijo enviado a la API). Si lo encuentra, devuelve en rojo el número de veces que se ha filtrado; si no, devuelve en verde que la contraseña no se ha filtrado.

Como `manage_data` llama al callback de éxito con un único argumento (los datos), en el bloque principal se usa `functools.partial` para fijar de antemano el argumento `passwd`: `partial(get_passwd_info, passwd=passwd)` genera una nueva función que solo necesita recibir los datos (aplicación parcial).

### 11. `parse_domain_breach(data: dict[str, Any]) -> str`

```python
def parse_domain_breach(data: dict[str, Any]) -> str:
    title = paint(data.get("Title", ""), Color.CYAN)
    breach_date = paint(data.get("BreachDate", ""), Color.PURPLE)
    description = paint(data.get("Description", ""), Color.RED)

    return f"Title: {title}\n Breach date: {breach_date}\n Description: {description}"
```

Recibe un diccionario con una de las filtraciones que devuelve la API sobre un dominio y devuelve parte de su información en un string: el título (`Title`), la fecha de la filtración (`BreachDate`) y la descripción (`Description`), cada uno pintado de un color. Se usa `.get()` con un string vacío por defecto para que no falle si falta algún campo.

### 12. `get_domain_info(data: list[dict[str, Any]]) -> str`

```python
def get_domain_info(data: list[dict[str, Any]]) -> str:
    if (data):
        return "\n\n".join(map(parse_domain_breach, data))
    else:
        return paint("No breaches found", Color.GREEN)
```

Es el callback que se usa cuando se hace una petición de tipo `Ption.Domain`. Recibe una lista de diccionarios con las filtraciones (data breaches) registradas para el dominio. Esta lista se pasa por un `map` con la función `parse_domain_breach` y, con el iterable de salida, se junta todo en un único string con `.join()`, separando cada filtración con una línea en blanco. Si la lista está vacía (el dominio no tiene filtraciones registradas), devuelve en verde que no se han encontrado filtraciones.

### 13. `sha1(raw_passwd: str) -> str`

```python
def sha1(raw_passwd: str) -> str:
    return SHA1.new(raw_passwd.encode(
        "utf-8")).hexdigest().upper()
```

Convierte un string a su hash SHA1 (usando la librería `pycryptodome`): codifica la contraseña en UTF-8, calcula el hash y lo devuelve en hexadecimal y en mayúsculas.

### 14. `ntlm(raw_passwd: str) -> str`

```python
def ntlm(raw_passwd: str) -> str:
    return MD4.new(raw_passwd.encode(
        "utf-16le")).hexdigest().upper()
```

Convierte un string a su hash NTLM, que consiste en aplicar MD4 sobre la contraseña codificada en UTF-16LE. Igual que `sha1`, lo devuelve en hexadecimal y en mayúsculas.

Las dos funciones tienen la misma firma (`str → str`), por lo que son intercambiables en el bloque principal.

### 15. Bloque principal (`main`)

```python
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data Breach Checker")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-p", "--password", action="store_true",
                       help="Check if password has been leaked")

    group.add_argument(
        "-d", "--domain", help="Check if domain had a data breach")

    parser.add_argument("--ntlm", action="store_true",
                        help="Use NTLM  instead of SHA1")

    args = parser.parse_args()

    if args.password:
        hasher, endpoint = (ntlm, Ption.PasswdNTLM) if args.ntlm else (
            sha1, Ption.PasswdSHA1)
        passwd = hasher(getpass("Password: "))
        print(manage_data(get_api_data(endpoint, passwd[:5]), partial(
            get_passwd_info, passwd=passwd), get_error))
    elif args.domain:
        print(manage_data(get_api_data(Ption.Domain,
              args.domain), get_domain_info, get_error))
```

En el main se manejan las flags del script con la librería `argparse`:

- Un grupo de argumentos mutuamente excluyente y obligatorio para elegir el modo: `-p`/`--password` (comprobación de contraseña) o `-d`/`--domain` seguido del dominio a comprobar.
- La flag opcional `--ntlm`, para usar NTLM en lugar de SHA1.

**Modo contraseña.** Según la flag `--ntlm`, se elige la pareja formada por la función de hash y el endpoint: `(ntlm, Ption.PasswdNTLM)` o `(sha1, Ption.PasswdSHA1)`. La función de hash se guarda en la variable `hasher` como un valor más y se llama después para calcular el hash de la contraseña, que se pide con `getpass` para que no se muestre en pantalla. A la API solo se le envían los 5 primeros caracteres del hash (`passwd[:5]`), de modo que ni la contraseña ni su hash completo salen del equipo. Por último, se llama a `manage_data` con la respuesta de `get_api_data`, el callback `partial(get_passwd_info, passwd=passwd)` y el callback `get_error`, y se imprime el resultado.

**Modo dominio.** Se llama a `manage_data` con la respuesta de `get_api_data(Ption.Domain, args.domain)` y los callbacks `get_domain_info` y `get_error`, y se imprime el resultado.

---

## Resumen de conceptos de programación funcional aplicados

| Concepto | Dónde se aplica |
|---|---|
| Funciones de orden superior (`map`, `filter`, `reduce`) | `palindromes`, `square_sum`, `factorial`, `filter_students`, `text_to_dict`, `get_domain_info` |
| Funciones lambda | `square_sum`, `factorial`, `text_to_dict` |
| Funciones como valores (primera clase) | `PARSERS`; selección de `hasher` en el bloque principal |
| Callbacks | `manage_data` con `get_passwd_info`, `get_domain_info` y `get_error` |
| Aplicación parcial | `partial(get_passwd_info, passwd=passwd)` |
| Composición de funciones | `sum(map(...))`, `dict(map(map(...)))`, `manage_data(get_api_data(...), ...)` |
| Inmutabilidad | `ApiResponse` (`NamedTuple`), `Ption` y `Color` (`StrEnum`) |
| Funciones puras | `has_passed`, `paint`, `text_to_dict`, `parse_domain_breach`, `sha1`, `ntlm` |
