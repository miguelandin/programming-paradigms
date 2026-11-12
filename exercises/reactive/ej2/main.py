from reactivex import from_, observable

list1 = [1, 2, 3, 4, 5, 6]

observable = from_(list1)

observable.subscribe(
    on_next=(lambda v: print(f"Recibido: {v}")))
on_completed=(lambda:print("Terminado")))
on_error()
)
