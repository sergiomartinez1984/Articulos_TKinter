from tkinter import *
import articulos

def main():
    raiz = Tk()
    raiz.title("Tienda de informatica")
    raiz.iconbitmap("computer_pc_10894.ico")
    raiz.config(bg="#303031")
    raiz.geometry("643x373")
    raiz.resizable(0, 0)
    articulos.App(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()