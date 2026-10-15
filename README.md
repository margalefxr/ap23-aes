# AP23 — Programa con AES (ECB vs CTR)

**Autor:** Xavier Margalef Riestra · **Módulo:** MF0489 Semana 2 · **Fecha:** 15/10/2026

## Resumen

| | |
|---|---|
| **Objetivo** | Añadir al código base (AES-ECB) una función con AES en modo CTR, comparar tamaños y repetir con clave de 256 bits |
| **Resultado** | Completado. 6/6 pruebas OK |
| **Observación** | ECB necesita padding y deja ver patrones; CTR no necesita padding pero exige no repetir nunca el nonce |

**Preguntas de la tarea:**

| Parte | Pregunta | Respuesta corta |
|---|---|---|
| 1 | ¿Qué ocurre si intentas cifrar el texto plano? | En ECB sin padding da error; en CTR se cifra directamente |
| 1 | ¿Cuál es el tamaño del texto cifrado resultante? | En CTR, igual que el texto plano |
| 2 | ¿Diferencias de tamaño entre ECB y CTR con clave de 256 bits? | Las mismas que con 128: la clave no cambia el tamaño del cifrado |

## Parte 1 — AES en modo CTR

`cifrar_ctr()` en `aes_modos.py`:

```python
cipher = AES.new(clave, AES.MODE_CTR)            # nonce aleatorio de 8 bytes
return cipher.nonce, cipher.encrypt(texto_plano)
```

**¿Qué ocurre si intentas cifrar el texto plano?**

| Modo | Sin padding | Por qué |
|---|---|---|
| ECB (código base) | ❌ `ValueError: Data must be aligned to block boundary in ECB mode` | AES cifra bloques de 16 bytes; si el texto no mide un múltiplo de 16, ECB no puede |
| CTR | ✅ Se cifra sin problema | CTR cifra un contador y hace XOR con el texto: funciona como un cifrado de flujo, a cualquier longitud |

**¿Cuál es el tamaño del texto cifrado?** En CTR, **exactamente el del texto plano**. Ejemplo con "Hola Bob, nos vemos a las 10" (28 bytes):

| Modo | Texto plano | Texto cifrado |
|---|---|---|
| ECB con padding | 28 bytes | **32 bytes** (rellena hasta el siguiente múltiplo de 16) |
| CTR | 28 bytes | **28 bytes** |

CTR genera un **nonce** aleatorio que hay que guardar junto al cifrado, porque sin él no se puede descifrar. No es secreto, pero con la misma clave no se puede repetir nunca: generaría el mismo keystream (el mismo fallo que vi en la PE 89.1 con ChaCha20).

## Parte 2 — Clave de 256 bits

La clave pasa de 16 a 32 bytes, generada con `get_random_bytes(32)`.

**¿Qué diferencias hay en el tamaño del cifrado entre ECB y CTR?**

| Texto plano | ECB (128) | ECB (256) | CTR (128) | CTR (256) |
|---|---|---|---|---|
| 1 byte | 16 | 16 | 1 | 1 |
| 16 bytes | 16 | 16 | 16 | 16 |
| 17 bytes | 32 | 32 | 17 | 17 |
| 28 bytes | 32 | 32 | 28 | 28 |

- **ECB:** el cifrado siempre es múltiplo de 16 bytes, porque hay que rellenar el último bloque.
- **CTR:** el cifrado mide lo mismo que el texto.
- **La clave no influye en el tamaño:** AES siempre trabaja con bloques de 128 bits. Con clave de 256 bits lo que cambia es el número de rondas (10 → 14) y la resistencia a fuerza bruta.

## Comparativa de modos

| | ECB | CTR |
|---|---|---|
| Padding | Necesario | No |
| Tamaño del cifrado | Múltiplo de 16 | Igual al texto |
| Bloques iguales → cifrado igual | ❌ Sí, revela patrones (probado en `test_ecb_revela_patrones`) | ✅ No |
| Necesita IV/nonce | No | Sí, único por mensaje |
| Paralelizable | Sí | Sí, cifrado y descifrado |
| Integridad | ❌ | ❌ (hace falta GCM) |

**Padding del código base:** rellena con bytes nulos (`\x00`). Funciona para el ejercicio, pero si el mensaje original termina en `\x00` no se puede saber dónde acaba. Lo estándar es PKCS#7 (`Crypto.Util.Padding.pad`).

## Normativa y uso actual

| Referencia | Qué dice |
|---|---|
| FIPS 197 | Estándar AES: bloque de 128 bits, claves de 128, 192 o 256 |
| NIST SP 800-38A | Define los modos ECB, CBC, CFB, OFB y CTR; en CTR el contador no puede repetirse con la misma clave |
| NIST SP 800-38D | AES-GCM: CTR + autenticación. Es lo que se usa en TLS 1.3 |
| NIST SP 800-131A | Triple DES ya no se permite para cifrar desde 2024 → AES |
| CNSA 2.0 (NSA) | Exige AES-256: con computación cuántica (Grover), AES-128 se queda en ~64 bits efectivos |
| ISO 27001 A.8.24 / ENS | Política de criptografía: algoritmo, modo, longitud de clave y gestión de nonces y claves |

En la práctica: **ECB no se usa para datos reales**, CTR solo como base, y lo que se despliega es **AES-256-GCM** (cifrado + integridad).

## Pruebas

| Prueba | Qué comprueba |
|---|---|
| `test_ecb_sin_padding_falla` | ECB sin padding da el error de alineación |
| `test_ctr_mismo_tamano_que_el_texto` | CTR: cifrado = texto, con 128 y 256 bits |
| `test_ecb_redondea_a_multiplo_de_16` | ECB: 1→16, 16→16, 17→32, 100→112, con 128 y 256 bits |
| `test_ctr_ida_y_vuelta` | Se descifra correctamente con el nonce guardado |
| `test_ctr_nonce_distinto_cada_vez` | Mismo mensaje dos veces → nonce y cifrado distintos |
| `test_ecb_revela_patrones` | Dos bloques iguales dan el mismo cifrado en ECB |

## Cómo ejecutarlo

```bash
python3 -m venv .venv && source .venv/bin/activate   # Windows: python -m venv .venv  y  .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python aes_modos.py          # pide el mensaje para Bob
python -m unittest -v        # 6 pruebas
```

Proceso, decisiones y dificultades en [`WORKLOG.md`](WORKLOG.md).

```
ap23-aes/
├── README.md
├── WORKLOG.md
├── aes_modos.py
├── test_aes_modos.py
└── requirements.txt     ← pycryptodome==3.24.1
```
