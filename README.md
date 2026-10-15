# AP23 — Programa con AES (ECB vs CTR)

**Autor:** Xavier Margalef Riestra · **Módulo:** MF0489 Semana 2 · **Fecha:** 15/10/2026

Al código base (AES-ECB) le añado una función con AES en modo CTR y comparo tamaños con clave de 128 y 256 bits.

```python
AES_algoritmo_cifrado = AES.new(clave_cifrado, AES.MODE_CTR)
texto_cifrado_ctr = AES_algoritmo_cifrado.encrypt(texto_plano)
nonce = AES_algoritmo_cifrado.nonce   # hace falta para descifrar
```

## Parte 1 — Modo CTR

**¿Qué ocurre si intentas cifrar el texto plano?**

| Modo | Resultado |
|---|---|
| ECB sin padding | ❌ `ValueError: Data must be aligned to block boundary in ECB mode`. AES cifra bloques de 16 bytes |
| CTR | ✅ Cifra sin padding. Genera un keystream y hace XOR, como un cifrado de flujo |

**¿Cuál es el tamaño del texto cifrado?** El mismo que el texto plano. "Hola Bob, nos vemos a las 10" son 28 bytes: en CTR el cifrado son 28 y en ECB con padding, 32.

## Parte 2 — Clave de 256 bits

**¿Diferencias de tamaño entre ECB y CTR?**

| Texto | ECB 128 / 256 | CTR 128 / 256 |
|---|---|---|
| 1 byte | 16 / 16 | 1 / 1 |
| 17 bytes | 32 / 32 | 17 / 17 |
| 28 bytes | 32 / 32 | 28 / 28 |

ECB siempre da un múltiplo de 16 y CTR el mismo tamaño que el texto. La clave no afecta al tamaño porque el bloque es siempre de 128 bits. Con 256 bits AES pasa de 10 a 14 rondas y aguanta más fuerza bruta.

## Decisiones

| Decisión | Motivo |
|---|---|
| CTR en vez de ECB | ECB cifra igual los bloques iguales y deja ver patrones (hay un test que lo comprueba) |
| Nonce aleatorio que genera la librería, guardado para descifrar | Sin él no se descifra, y con la misma clave no se puede repetir |
| Clave de 256 bits con `get_random_bytes` | Las claves salen de un CSPRNG, nunca a mano |
| `pycryptodome==3.24.1` fijada | Instalación reproducible y supply chain controlada |
| Padding con `\x00` del código base | Lo mantengo porque es el del enunciado. Lo correcto es PKCS#7: con ceros no sabes dónde acaba un mensaje que termina en `\x00` |

## Normativa

| Referencia | Relación |
|---|---|
| FIPS 197 · NIST SP 800-38A | AES y sus modos. En CTR el contador no se puede repetir |
| NIST SP 800-38D | AES-GCM = CTR + integridad. Es lo que usa TLS 1.3 |
| NIST SP 800-131A · CNSA 2.0 | 3DES retirado. AES-256 recomendado de cara a la computación cuántica |
| ISO 27001 A.8.24 | Política de criptografía: algoritmo, modo, tamaño de clave y gestión del nonce |

## Ejecución

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python aes_modos.py
python -m unittest -v
```

Dificultades en [`WORKLOG.md`](WORKLOG.md).
