from typing import Callable


def dog(yrs: float):
    return yrs*7


def cat(yrs: float):
    return yrs*5


def fish(yrs: float):
    return yrs*12


year_transform: dict[str, Callable[[float], float]] = {
    "perro": dog, "gato": cat, "pez": fish}


def pets_age(animal: str, years: float):
    return year_transform[animal](years)


print(pets_age("pez", 12))
