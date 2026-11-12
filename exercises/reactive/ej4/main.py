from reactivex import operators as ops
from reactivex import of

observable = of(22, 35, 28, 40)


t_obersvable = observable.pipe(
    ops.filter(lambda t: t > 30),
    ops.map(lambda t: f"ALERTA: {t}ºC")
)

sub = t_obersvable.subscribe(lambda a: print(a))

sub.dispose()
