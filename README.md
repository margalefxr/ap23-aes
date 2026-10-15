# AP23 — Programa con AES (ECB vs CTR)

**Autor:** Xavier Margalef Riestra · **Módulo:** MF0489 Semana 2 · **Fecha:** 15/10/2026

Partiendo del código base (AES-ECB), añado una función con AES en modo CTR y comparo tamaños con clave de 128 y 256 bits.

```python
cipher = AES.new(clave, AES.MODE_CTR)            # nonce aleatorio de 8 bytes
return cipher.nonce, cipher.encrypt(texto_plano)
```

## Parte 1 — Modo CTR

**¿Qué ocurre si intentas cifrar el texto plano?**

| Modo | Resultado |
|---|---|
| ECB sin padding | ❌ `ValueError: Data must be aligned to block boundary in ECB mode` (AES cifra bloques de 16 bytes) |
| CTR | ✅ Cifra sin padding: genera un keystream y hace XOR, como un cifrado de flujo |

**¿Cuál es el tamaño del texto cifrado?** Igual que el texto plano. Con "Hola Bob, nos vemos a las 10" (28 bytes), el cifrado CTR mide 28 bytes y el ECB con padding, 32.

## Parte 2 — Clave de 256 bits

**¿Diferencias de tamaño entre ECB y CTR?**

| Texto | ECB 128 / 256 | CTR 128 / 256 |
|---|---|---|
| 1 byte | 16 / 16 | 1 / 1 |
| 17 bytes | 32 / 32 | 17 / 17 |
| 28 bytes | 32 / 32 | 28 / 28 |

ECB siempre ocupa un múltiplo de 16 y CTR lo mismo que el texto. **La clave no cambia el tamaño:** el bloque siempre es de 128 bits; con 256 bits solo pasan de 10 a 14 rondas y aumenta la resistencia a fuerza bruta.

## Decisiones

| Decisión | Por qué |
|---|---|
| CTR antes que ECB | ECB cifra igual los bloques iguales y deja ver patrones (lo comprueba un test) |
| Nonce aleatorio, devuelto con el cifrado | Hace falta para descifrar y no puede repetirse con la misma clave |
| Clave de 256 bits con `get_random_bytes` | Las claves salen de un CSPRNG, no se escriben a mano |
| `pycryptodome==3.24.1` fijada | Instalación reproducible y control de supply chain |
| Se mantiene el padding con `\x00` del código base | Es el del enunciado; lo correcto sería PKCS#7, porque con ceros no se sabe dónde acaba un mensaje que termina en `\x00` |

## Normativa

| Referencia | Qué aplica aquí |
|---|---|
| FIPS 197 · NIST SP 800-38A | AES y sus modos; en CTR el contador no puede repetirse |
| NIST SP 800-38D | En producción se usa AES-GCM (CTR + integridad), como en TLS 1.3 |
| NIST SP 800-131A · CNSA 2.0 | 3DES retirado; AES-256 recomendado frente a la computación cuántica |
| ISO 27001 A.8.24 | Política de criptografía: algoritmo, modo, tamaño de clave y gestión del nonce |

## Ejecutar

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python aes_modos.py
python -m unittest -v
```

Dificultades encontradas en [`WORKLOG.md`](WORKLOG.md).
