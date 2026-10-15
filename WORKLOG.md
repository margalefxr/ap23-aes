# WORKLOG — AP23

| # | Paso | Resultado |
|---|---|---|
| 1 | Ejecutar el código base sin padding | Error de alineación en ECB |
| 2 | `cifrar_ctr()` y `descifrar_ctr()` | Cifrado del mismo tamaño que el texto; ida y vuelta OK |
| 3 | Repetir con clave de 256 bits | Mismos tamaños que con 128 |
| 4 | 6 pruebas con `unittest` | 6/6 OK |

## Dificultades

| Dificultad | Solución |
|---|---|
| "¿Qué ocurre si intentas cifrar el texto plano?" no dice en qué modo | Respondo para los dos: ECB da error y CTR funciona |
| El código base usa `input()` y así no se puede probar automáticamente | La lógica va en funciones; `input()` solo en `__main__` |
| Sin guardar el nonce de CTR no se puede descifrar | `cifrar_ctr()` devuelve `(nonce, cifrado)` |
