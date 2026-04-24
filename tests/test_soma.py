import pytest

def soma(a,b):
    return a+b

def test_soma_dois_numeros1():
    resultado = soma(10,15)
    print(resultado)
    assert resultado == 25

def test_soma_dois_numeros2():
    resultado = soma(10,15)
    print(resultado)
    assert resultado == 20
