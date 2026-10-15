# Pruebas del AP23
# Ejecutar: python -m unittest -v

import unittest
from Crypto.Random import get_random_bytes
from aes_modos import aes_mode_ecb_basic, aes_mode_ctr

clave_128 = get_random_bytes(16)
clave_256 = get_random_bytes(32)


class TestAES(unittest.TestCase):

    def test_ctr_mismo_tamano(self):
        for clave in (clave_128, clave_256):
            self.assertEqual(len(aes_mode_ctr(b"x" * 28, clave)), 28)

    def test_ecb_multiplo_de_16(self):
        for clave in (clave_128, clave_256):
            self.assertEqual(len(aes_mode_ecb_basic(b"x" * 28, clave)), 32)

    def test_ecb_deja_ver_patrones(self):
        # dos bloques iguales dan el mismo cifrado
        cifrado = aes_mode_ecb_basic(b"A" * 32, clave_128)
        self.assertEqual(cifrado[:16], cifrado[16:])


if __name__ == "__main__":
    unittest.main()
