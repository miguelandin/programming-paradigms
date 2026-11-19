import tkinter

window = tkinter.Tk()
window.title("Calc")
window.option_add("*Font", "Arial 32")

calc_input: str = ""
calc_out = tkinter.Label(window, text=calc_input, bg="#77767b")
calc_out.grid(row=0, column=0, columnspan=4, sticky="nsew")


def strAppend(value: str):
    global calc_input
    calc_input += value
    calc_out.config(text=calc_input)


def calculate():
    global calc_input
    try:
        calc_input = str(eval(calc_input))
        calc_out.config(text=calc_input)
    except Exception as e:
        calc_input = ""
        calc_out.config(text=e.__str__())


def clear():
    global calc_input
    calc_input = ""
    calc_out.config(text=calc_input)


for i in range(10):
    btn = tkinter.Button(
        window,
        text=str(i),
        bg="#c64600",
        activebackground="#ffa348",
        command=lambda val=str(i): strAppend(val)
    )
    if i == 0:
        btn.grid(row=4, column=0, sticky="nsew")
    else:
        btn.grid(row=(i - 1) // 3 + 1, column=(i - 1) % 3, sticky="nsew")

btn = tkinter.Button(window, text="+", command=lambda val="+": strAppend(val),
                     bg="#c64600", activebackground="#ffa348")
btn.grid(row=1, column=3, sticky="nsew")

btn = tkinter.Button(window, text="-", command=lambda val="-": strAppend(val),
                     bg="#c64600", activebackground="#ffa348")
btn.grid(row=2, column=3, sticky="nsew")

btn = tkinter.Button(window, text="*", command=lambda val="*": strAppend(val),
                     bg="#c64600", activebackground="#ffa348")
btn.grid(row=3, column=3, sticky="nsew")

btn = tkinter.Button(window, text="/", command=lambda val="/": strAppend(val),
                     bg="#c64600", activebackground="#ffa348")
btn.grid(row=4, column=3, sticky="nsew")

btn = tkinter.Button(window, text="C", command=clear,
                     bg="#c64600", activebackground="#ffa348")
btn.grid(row=4, column=1, sticky="nsew")

btn = tkinter.Button(window, text="=", command=calculate,
                     bg="#c64600", activebackground="#ffa348")
btn.grid(row=4, column=2, sticky="nsew")

for c in range(4):
    window.columnconfigure(c, weight=1)
for r in range(5):
    window.rowconfigure(r, weight=1)

window.mainloop()
