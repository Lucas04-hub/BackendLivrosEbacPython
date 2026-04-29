import pytest

def test_criar_pokemon():
    pikachu = Pokemon("Pikachu", "Elétrico")
    assert pikachu.nome == "Pikachu"
    assert pikachu.tipo == "Elétrico"
    assert pikachu.nivel == 1

    class Pokemon:
        def __init__(self, nome, tipo):
            self.nome = nome
            self.tipo = tipo
            self.nivel = 1