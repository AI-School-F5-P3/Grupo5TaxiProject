import tkinter as tk

ventana = tk.Tk()

ventana.title("Cronómetro en Tkinter")           


etiqueta = tk.Label(ventana, text='0.00', font=("Arial",30))    

def actualizar_temporizador():
    tiempo = float(etiqueta["text"])
    tiempo += 0.05
    etiqueta["text"] = f"{tiempo:.2f}"
    ventana.after(50, actualizar_temporizador)

boton_iniciar = tk.Button(ventana, text = "Iniciar",command = (actualizar_temporizador),
                        font =(15))

boton_iniciar.pack()

ventana.mainloop()