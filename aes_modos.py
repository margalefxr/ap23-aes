# AP23 - Programa con AES (ECB y CTR)
# Xavier Margalef Riestra

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


# Codigo base del enunciado (ECB)
def aes_mode_ecb_basic(texto_plano, clave_cifrado):

    # Cifrado sin padding
    try:
        AES_algoritmo_cifrado = AES.new(clave_cifrado, AES.MODE_ECB)
        AES_algoritmo_cifrado.encrypt(texto_plano)
    except ValueError as e:
        print(f"Error: {e}")

    # Añadir padding al texto plano (bytes nulos)
    texto_plano_padding = texto_plano
    while len(texto_plano_padding) % 16 != 0:
        texto_plano_padding += b"\x00"

    # Cifrado AES modo ECB
    AES_algoritmo_cifrado = AES.new(clave_cifrado, AES.MODE_ECB)
    texto_cifrado_ecb = AES_algoritmo_cifrado.encrypt(texto_plano_padding)
    print(f"Texto cifrado ECB: {texto_cifrado_ecb} (Longitud: {len(texto_cifrado_ecb)} bytes)")
    return texto_cifrado_ecb


# Parte 1: modo CTR (no necesita padding)
def aes_mode_ctr(texto_plano, clave_cifrado):
    AES_algoritmo_cifrado = AES.new(clave_cifrado, AES.MODE_CTR)
    texto_cifrado_ctr = AES_algoritmo_cifrado.encrypt(texto_plano)
    nonce = AES_algoritmo_cifrado.nonce   # hace falta para descifrar
    print(f"Texto cifrado CTR: {texto_cifrado_ctr} (Longitud: {len(texto_cifrado_ctr)} bytes)")

    # Compruebo que se descifra bien con el mismo nonce
    AES_descifrado = AES.new(clave_cifrado, AES.MODE_CTR, nonce=nonce)
    print(f"Descifrado CTR: {AES_descifrado.decrypt(texto_cifrado_ctr)}")
    return texto_cifrado_ctr


if __name__ == "__main__":

    clave_cifrado = b'A\x83\xbeU\xd7\xa9b\x18\x85AN0\xbft\xc3\xab'
    texto_plano = input("Introduce un mensaje para Bob: ").encode()
    print(f"Texto plano: {len(texto_plano)} bytes\n")

    print("--- Parte 1: clave de 128 bits ---")
    aes_mode_ecb_basic(texto_plano, clave_cifrado)
    aes_mode_ctr(texto_plano, clave_cifrado)

    print("\n--- Parte 2: clave de 256 bits ---")
    clave_256 = get_random_bytes(32)
    aes_mode_ecb_basic(texto_plano, clave_256)
    aes_mode_ctr(texto_plano, clave_256)
