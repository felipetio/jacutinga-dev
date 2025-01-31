
def fahrenheit_para_celsius(fahrenheit: float) -> float:
    """"
    Transforma uma tempetatura de Fahrenheit para celsius
    """
    celsius = (fahrenheit - 32) * 5 / 9
    return celsius



def kelvin_para_celsius(kelvin: float) -> float:
    """
    Transforma uma temperatura de Kelvin para Celsius
    """
    celsius = kelvin - 273.15
    return celsius

