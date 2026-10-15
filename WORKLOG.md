# WORKLOG — AP23

| # | Paso | Resultado |
|---|---|---|
| 1 | Ejecutar el código base sin padding | Error de alineación en ECB |
| 2 | `aes_mode_ctr()`, con comprobación de descifrado | Cifrado del mismo tamaño que el texto; descifra bien |
| 3 | Repetir con clave de 256 bits | Mismos tamaños que con 128 |
| 4 | 3 pruebas con `unittest` | 3/3 OK |

## Dificultades

| Dificultad | Solución |
|---|---|
| "¿Qué ocurre si intentas cifrar el texto plano?" no dice en qué modo | Respondo para los dos: ECB da error y CTR funciona |
| El código base usa `input()` y así no se puede probar automáticamente | La lógica va en funciones; `input()` solo en `__main__` |
| Sin guardar el nonce de CTR no se puede descifrar | Guardo `AES_algoritmo_cifrado.nonce` y lo paso al descifrar |
