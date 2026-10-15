"""Pruebas del AP23. Ejecutar desde esta carpeta: python -m unittest -v"""

import unittest

from Crypto.Random import get_random_bytes

from aes_modos import CLAVE_128, cifrar_ctr, cifrar_ecb, cifrar_ecb_sin_padding, descifrar_ctr

CLAVE_256 = get_random_bytes(32)


class TestAES(unittest.TestCase):

    def test_ecb_sin_padding_falla(self):
        self.assertIn("aligned to block boundary", cifrar_ecb_sin_padding(b"Hola Bob", CLAVE_128))

    def test_ctr_mismo_tamano_que_el_texto(self):
        for clave in (CLAVE_128, CLAVE_256):
            for n in (1, 8, 16, 17, 100):
                _, cifrado = cifrar_ctr(b"x" * n, clave)
                self.assertEqual(len(cifrado), n)

    def test_ecb_redondea_a_multiplo_de_16(self):
        for clave in (CLAVE_128, CLAVE_256):
            for n, esperado in ((1, 16), (16, 16), (17, 32), (100, 112)):
                self.assertEqual(len(cifrar_ecb(b"x" * n, clave)), esperado)

    def test_ctr_ida_y_vuelta(self):
        for clave in (CLAVE_128, CLAVE_256):
            nonce, cifrado = cifrar_ctr("Hola Bob, ¿qué tal?".encode(), clave)
            self.assertEqual(descifrar_ctr(nonce, cifrado, clave).decode(), "Hola Bob, ¿qué tal?")

    def test_ctr_nonce_distinto_cada_vez(self):
        n1, c1 = cifrar_ctr(b"mismo mensaje", CLAVE_128)
        n2, c2 = cifrar_ctr(b"mismo mensaje", CLAVE_128)
        self.assertNotEqual(n1, n2)
        self.assertNotEqual(c1, c2)

    def test_ecb_revela_patrones(self):
        cifrado = cifrar_ecb(b"A" * 32, CLAVE_128)
        self.assertEqual(cifrado[:16], cifrado[16:])   # bloques iguales -> cifrado igual


if __name__ == "__main__":
    unittest.main()
