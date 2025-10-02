def especial(primero: int, segundo: int, **kwargs) -> int:
    for key, value in kwargs.items():
        print(f"{key}: {value}")    
    return primero + segundo * 2        

print(especial(1, 2, tercero=3, cuarto=4, quinto="valor"))
