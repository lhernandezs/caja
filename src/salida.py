from os import path

class Salida: 
    def __init__(self, mensaje):
        with open(path.join("data", "salida.csv"), mode="a+") as file:
            file.write(str(mensaje) + '\n')

if __name__ == "__main__":
    Salida("Hola.. estamos en septiembre 2024")