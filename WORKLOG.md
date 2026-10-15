# WORKLOG — AP23 Programa con AES

## Pasos

| # | Paso | Resultado |
|---|---|---|
| 1 | Leer las lecciones de DES, 3DES y AES (modos ECB, CBC, CFB, OFB y CTR) | Base teórica |
| 2 | Ejecutar el código base sin padding | `ValueError: Data must be aligned to block boundary in ECB mode` |
| 3 | `cifrar_ctr()` y `descifrar_ctr()` | Cifrado del mismo tamaño que el texto; ida y vuelta OK |
| 4 | Repetir con clave de 256 bits | Mismos tamaños que con 128 |
| 5 | Pruebas con `unittest` | 6/6 OK |

## Decisiones (por qué A y no B)

| Decisión | Elegido (A) | Descartado (B) | Motivo |
|---|---|---|---|
| Clave de 256 bits | `get_random_bytes(32)` | Escribirla a mano | Una clave tiene que salir de un CSPRNG |
| Nonce CTR | El que genera la librería, devuelto con el cifrado | Fijo en el código | Un nonce fijo se repetiría en cada ejecución con la misma clave |
| Padding | Bytes nulos, como el código base | PKCS#7 | Se mantiene el código del enunciado; se documenta que lo correcto es PKCS#7 |
| Verificaciones | `if` + `SystemExit` | `assert` | `assert` se desactiva con `python -O` |
| Dependencia | `pycryptodome==3.24.1` fijada | Sin versión | Instalación reproducible y control de supply chain |

## Dificultades

| ID | Dificultad | Solución |
|---|---|---|
| D-01 | "¿Qué ocurre si intentas cifrar el texto plano?" no dice en qué modo | Se responde para los dos: en ECB sin padding da error y en CTR funciona |
| D-02 | El código base usa `input()`, así que no se puede probar automáticamente tal cual | La lógica va en funciones que se prueban sin teclado; `input()` solo en `__main__` |
| D-03 | En CTR, sin guardar el nonce no se puede descifrar | `cifrar_ctr()` devuelve `(nonce, cifrado)` |
| D-04 | El padding con bytes nulos es ambiguo si el mensaje termina en `\x00` | Documentado; la alternativa es PKCS#7 |
