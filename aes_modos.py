"""
AP23 - Programa con AES: modo ECB frente a modo CTR, clave de 128 y 256 bits
Autor: Xavier Margalef Riestra

  - cifrar_ecb()            -> codigo base del enunciado (ECB + padding con bytes nulos)
  - cifrar_ctr()            -> Parte 1: AES en modo CTR
  - descifrar_ctr()         -> comprobacion de ida y vuelta
  - Parte 2                 -> mismo proceso con clave de 256 bits

La clave de 128 bits es la del enunciado (dato publico del ejercicio).
La de 256 bits se genera con get_random_bytes (CSPRNG).
"""

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

CLAVE_128 = b'A\x83\xbeU\xd7\xa9b\x18\x85AN0\xbft\xc3\xab'   # enunciado (16 bytes)


def cifrar_ecb_sin_padding(texto_plano: bytes, clave: bytes) -> str:
    """Intenta ECB sin padding. Devuelve el error de la libreria si el texto no mide multiplo de 16."""
    try:
        AES.new(clave, AES.MODE_ECB).encrypt(texto_plano)
        return "OK (el texto ya media un multiplo de 16 bytes)"
    except ValueError as e:
        return f"Error: {e}"


def cifrar_ecb(texto_plano: bytes, clave: bytes) -> bytes:
    """ECB con padding de bytes nulos hasta multiplo de 16 (como en el codigo del enunciado)."""
    texto_padding = texto_plano
    while len(texto_padding) % 16 != 0:
        texto_padding += b"\x00"
    return AES.new(clave, AES.MODE_ECB).encrypt(texto_padding)


def cifrar_ctr(texto_plano: bytes, clave: bytes) -> tuple[bytes, bytes]:
    """
    Parte 1: AES en modo CTR. No necesita padding porque convierte AES en un
    cifrado de flujo. Devuelve (nonce, cifrado): el nonce se genera aleatorio
    (8 bytes) y hay que guardarlo junto al cifrado para poder descifrar.
    """
    cipher = AES.new(clave, AES.MODE_CTR)
    return cipher.nonce, cipher.encrypt(texto_plano)


def descifrar_ctr(nonce: bytes, texto_cifrado: bytes, clave: bytes) -> bytes:
    """Regenera el mismo keystream (misma clave y nonce) y descifra."""
    return AES.new(clave, AES.MODE_CTR, nonce=nonce).decrypt(texto_cifrado)


def comparar(texto_plano: bytes, clave: bytes, etiqueta: str) -> None:
    """Cifra con ECB y CTR y muestra los tamanos."""
    print(f"\n== {etiqueta}: clave de {len(clave) * 8} bits ==")
    print(f"ECB sin padding : {cifrar_ecb_sin_padding(texto_plano, clave)}")
    ecb = cifrar_ecb(texto_plano, clave)
    nonce, ctr = cifrar_ctr(texto_plano, clave)
    print(f"ECB con padding : {len(ecb)} bytes -> {ecb.hex()}")
    print(f"CTR             : {len(ctr)} bytes -> {ctr.hex()} (nonce {nonce.hex()})")
    # if y no assert: los assert se desactivan con python -O
    if descifrar_ctr(nonce, ctr, clave) != texto_plano:
        raise SystemExit("ERROR: el descifrado CTR no devuelve el texto original")
    print("Descifrado CTR  : OK")


if __name__ == "__main__":
    texto_plano = input("Introduce un mensaje para Bob: ").encode("utf-8")
    print(f"Texto plano: {len(texto_plano)} bytes")

    comparar(texto_plano, CLAVE_128, "PARTE 1")
    comparar(texto_plano, get_random_bytes(32), "PARTE 2")
