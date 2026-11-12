from reactivex import of
from reactivex import operators as ops


observable = of('Hola', 'Adiós')

operator1 = ops.map(lambda s: s.upper())
operator2 = ops.map(lambda s: f"En mayúscula: {s}")

t_obsersvable = observable.pipe(operator1, operator2)

t_obsersvable.subscribe(lambda v: print(f"Recibido: {v}"))
