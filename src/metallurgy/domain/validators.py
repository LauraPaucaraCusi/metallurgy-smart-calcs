def validar_positivo(nombre: str, valor: float) -> None:
    if valor <= 0:
        raise ValueError(f"{nombre} debe ser mayor que 0")


def validar_no_negativo(nombre: str, valor: float) -> None:
    if valor < 0:
        raise ValueError(f"{nombre} no puede ser negativo")
