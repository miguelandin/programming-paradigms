from typing import Any, Optional

from reactivex import create
from reactivex.abc import DisposableBase, ObserverBase, SchedulerBase
from reactivex.disposable import Disposable


def generator(
    observer: ObserverBase[Any], scheduler: Optional[SchedulerBase] = None
) -> DisposableBase:
    observer.on_next("Hola")
    observer.on_next("Adios")
    observer.on_completed()
    return Disposable()


observable = create(generator)

subs = observable.subscribe(on_next=lambda v: print(f"Recibido: {v}"))
