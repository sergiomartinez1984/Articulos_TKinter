from tkinter import *
from tkinter import ttk
from tkinter import messagebox as MessageBox
import csv

#Mensajes de Advertencia para que el usurio sepa lo que esta haciendo
def noExiste(var):
    var_s = str(var)
    MessageBox.showinfo("Articulo no encontrado", var_s+ ' '+ "no existe")

def write_name():
    MessageBox.showinfo("Articulo no encontrado", "Tienes que insertar un nombre")

def write_contact():
    MessageBox.showinfo("Escribe un nombre de Articulo", "Debes escribir un Articulo para usar la opcion \"Añadir Articulo\"")

def delete_message(name):
    var_name = str(name)
    if var_name =='':
        write_name()
    else:
        search = MessageBox.askquestion("Eliminar Articulo", "¿Esta seguro de que desea eliminar este Articulo?\n"+var_name)
        if search == "yes":
            return True
        else:
            return False

def modify_message(contact):
    var_nombre = str(contact[0])
    var_referencia = str(contact [1])
    var_precio = str(contact[2])
    search = MessageBox.askquestion("Modificar Articulo", "Desea modificar este Articulo: \n"+"Nombre: "+var_nombre+"\nReferencia: "+var_referencia+"\nPrecio: "+var_precio)
    if search == "yes":
        return True
    else:
        return False


class App():
    def __init__(self, raiz):
        self.window = raiz

#Menu desplegable con dos opciones

        barraMenu = Menu(self.window)
        self.window.config(menu = barraMenu)
        filemenu = Menu(barraMenu, tearoff = 0, bg="Light Blue")
        filemenu.add_command(label = "Todos los articulos", command = lambda: mostrar_articulos(), font=("Aldrich", "9", "bold"))
        filemenu.add_command(label="Cerrar tienda", command = lambda: raiz.destroy(), font = ("Aldrich", "9", "bold"))
        barraMenu.add_cascade(label="Opciones", menu=filemenu)

#------Paneles donde estan alojados el panel de contactos y el panel de informacion

        panelInfo = LabelFrame(self.window, bg = "purple")
        panelInfo.place(x=1, y=200, width=640, height=50)

        panelContactos = LabelFrame(self.window, bg="#303031")
        panelContactos.grid(row=0, column=0,sticky=N)


#------Cuadros de texto del panel de informacion

        Label(panelInfo, text = 'Nombre', bg="white", font=("Aldrich", "11", "normal")).grid(row=0, column=0)
        inbox_nombre = Entry(panelInfo, font=("Aldrich", "11", "normal"), width = 28)
        inbox_nombre.grid(row=1, column=0)
        inbox_nombre.focus()

        Label(panelInfo, text='Referencia', bg="white", font=("Aldrich", "11", "normal")).grid(row=0, column=1)
        inbox_referencia = Entry(panelInfo, font=("Aldrich", "11", "normal"), width=30)
        inbox_referencia.grid(row=1, column=1)

        Label(panelInfo, text='Precio', bg="white", font=("Aldrich", "11", "normal")).grid(row=0, column=2)
        inbox_precio = Entry(panelInfo, font=("Aldrich", "11", "normal"), width=20)
        inbox_precio.grid(row=1, column=2)

# ------Botones pricipales de nuestra aplicacion, para insertar,modificar y borrar,etc...


        btAdd = Button(raiz, command=lambda: agregar(), text='Añadir articulo', width=19)
        btAdd.configure(bg="orange", cursor='hand2',font=("Aldrich", "9", "normal"))
        btAdd.place(x=3, y=165, width=100, height=30)

        btBuscar = Button(raiz, command=lambda: buscar(), text='Buscar', width=19)
        btBuscar.configure(bg="orange", cursor='hand2', font=("Aldrich", "9", "normal"))
        btBuscar.place(x=103, y=165, width=100, height=30)

        btLimpiar = Button(raiz, command=lambda: limpiar(), text='Vaciar Almacen', width=19)
        btLimpiar.configure(bg="orange", cursor='hand2', font=("Aldrich", "9", "normal"))
        btLimpiar.place(x=203, y=165, width=100, height=30)

        btModificar = Button(raiz, command=lambda: modificar(), text='Modificar articulos',width=19)
        btModificar.configure(bg="orange", cursor='hand2', font=("Aldrich", "8", "normal"))
        btModificar.place(x=303, y=165, width=100, height=30)

        btMostrar = Button(raiz, command=lambda: mostrar_articulos(), text='Mostrar articulos', width=19)
        btMostrar.configure(bg="orange", cursor='hand2', font=("Aldrich", "8", "normal"))
        btMostrar.place(x=403, y=165, width=100, height=30)

        btEliminar = Button(raiz, command=lambda: eliminar(), text='Eliminar', width=19,heigh = 5)
        btEliminar.configure(bg="red",fg="white", cursor='hand2', font=("Aldrich", "11", "normal"))
        btEliminar.place(x=503, y=165, width=138, height=30)

#------Combo Box para la busqueda o modificacion de un articulo,se podra buscar o modificar tanto por nombre,referencia o precio

        Label(raiz, text = 'Buscar/Modificar', bg="purple",font=("Aldrich", "10", "normal")).place(x=2, y=260, width=138, height=30)
        combo = ttk.Combobox(raiz, state='readonly', width=17, justify='center', font=("Aldrich", "10", "normal"))
        combo["values"] = ['Nombre', 'Referencia', 'precio']
        combo.place(x=2, y=270, width=138, height=30)
        combo.current(0)

#------Tabla de Articulos donde se muestra la infromacion de los articulos que hay en la tienda--------

        self.tree=ttk.Treeview(panelContactos, heigh = 5, columns=("uno","dos"))
        self.tree.grid(padx = 10, pady = 5, row = 0, column = 0,sticky=N)
        self.tree.heading("#0", text='Nombre', anchor=CENTER)
        self.tree.heading("uno", text='Referencia', anchor=CENTER)
        self.tree.heading("dos", text='Precio', anchor=CENTER)

#-------Para el scroll de la tabla de los articulos,cuando hay demasiados se activa el scroll,si no permanece desactivado

        scrollVert = Scrollbar(panelContactos, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollVert.set)
        scrollVert.grid(row=0, column=1, sticky="nsew")

        scroll_x = Scrollbar(panelContactos, command=self.tree.xview, orient=HORIZONTAL)
        self.tree.configure(xscrollcommand=scroll_x.set)
        scroll_x.grid(row=2, column=0, columnspan=1, sticky="nsew")


#----------nuestros metodos

        def _limpiar_texto():
            inbox_nombre.delete(0,"end")
            inbox_referencia.delete(0, "end")
            inbox_precio.delete(0, "end")

        def _limpiar_lista():
            tree_list = self.tree.get_children()
            for item in tree_list:
                self.tree.delete(item)

        def _vista_csv():
            with open('articulos_list.csv', 'r') as f:
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    nombre = str(row[0])
                    referencia = str(row[1])
                    precio = str(row[2])
                    self.tree.insert("", 0, text = nombre, values = (referencia, precio))

        def _guardar(nombre, referencia, precio):
            g_nom = nombre
            g_ref = referencia
            g_pre = precio
            with open('articulos_list.csv', 'a') as f:
                writer = csv.writer(f, lineterminator ='\r', delimiter = ',')
                writer.writerow((g_nom, g_ref, g_pre))

        def _buscar(var_inbox, possition):
            list = []
            s_var_inbox = str(var_inbox)
            var_possition = int(possition)
            with open('articulos_list.csv', 'r') as f:
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    if s_var_inbox == row[var_possition]:
                        list = [row[0], row[1], row[2]]
                        break
                    else:
                        continue
            return list

        def _check(answer, var_search):
            list_answer = answer
            var_search = var_search
            if list_answer == []:
                noExiste(var_search)
            else:
                name = str(list_answer[0])
                surname = str(list_answer[1])
                phone = str(list_answer[2])
                self.tree.insert("", 0, text = "------------------------------", values = ("------------------------------", "------------------------------"))
                self.tree.insert("", 0, text = name, values = (surname, phone))
                self.tree.insert("", 0, text = "Resultados nombres", values = ("Resultados referencias", "Resultados precio"))

        def _check1(answer, var_search):
            val_modify = answer
            var = var_search
            if val_modify == []:
                noExiste(var)
            else:
                VentanaModificar(self.window, val_modify)


#-------Metodos de accion de los botones.
#-------Estos metodos son pasados a nuestros botones

        def agregar():
            nombre = inbox_nombre.get()
            referencia = inbox_referencia.get()
            precio = inbox_precio.get()
            articulo_check = [nombre, referencia, precio]
            if articulo_check == ['','','']:
                write_contact()
            else:
                if nombre == '':
                    nombre = '<Default>'
                if referencia == '':
                    referencia = '<Default>'
                if precio == '':
                    precio = '<Default>'
                _guardar(nombre, referencia, precio)
                self.tree.insert("", 0, text="------------------------------", values=("------------------------------", "------------------------------"))
                self.tree.insert("", 0, text=str(nombre), values=(str(referencia), str(precio)))
                self.tree.insert("", 0, text="Nuevo nombre añadido", values=("Nueva referencia añadido", "Nuevo precio añadido"))
                self.tree.insert("", 0, text="------------------------------", values=("------------------------------", "------------------------------"))
            articulo_check = []
            _limpiar_texto()

        def buscar():
            answer = []
            var_search = str(combo.get())
            if var_search == 'Nombre':
                var_inbox = inbox_nombre.get()
                possition = 0
                answer = _buscar(var_inbox, possition)
                _check(answer, var_search)
            elif var_search == 'Referencia':
                var_inbox = inbox_referencia.get()
                possition = 1
                answer = _buscar(var_inbox, possition)
                _check(answer, var_search)
            else:
                var_inbox = inbox_precio.get()
                possition = 2
                answer = _buscar(var_inbox, possition)
                _check(answer, var_search)

        def modificar():
            answer = []
            var_search = str(combo.get())
            if var_search == 'Nombre':
                var_inbox = inbox_nombre.get()
                possition = 0
                answer = _buscar(var_inbox, possition)
                _check1(answer, var_search)
            elif var_search == 'Referencia':
                var_inbox = inbox_referencia.get()
                possition = 1
                answer = _buscar(var_inbox, possition)
                _check1(answer, var_search)
            else:
                var_inbox = inbox_precio.get()
                possition = 2
                answer = _buscar(var_inbox, possition)
                _check1(answer, var_search)
            _limpiar_texto()

        def mostrar_articulos():
            _vista_csv()


        def eliminar():
            nom = str(inbox_nombre.get())
            a = delete_message(nom)
            if a == True:
                with open('articulos_list.csv', 'r') as f:
                    reader = list(csv.reader(f))
                with open('articulos_list.csv', 'w') as f:
                    writer = csv.writer(f, lineterminator ='\r', delimiter=',')
                    for i, row in enumerate(reader):
                        if nom != row[0]:
                            writer.writerow(row)
            limpiar()
            mostrar_articulos()

        def limpiar():
            _limpiar_texto()
            _limpiar_lista()

#------Nueva clase para la ventana modificar articulo,
#------Aparecera una nueva ventana,una vez pulsemos a modificar un articulo

class VentanaModificar():

    def __init__(self, raiz, val_modify):
        self.raiz_window = raiz
        self.val_modify = val_modify
        self.nombre = str(self.val_modify[0])
        self.referencia = str(self.val_modify[1])
        self.precio = str(self.val_modify[2])

        window_modify = Toplevel(self.raiz_window)
        window_modify.title("Modificar Articulo")
        window_modify.configure(bg = "#87CEFA")
        window_modify.geometry("615x130")
        window_modify.resizable(0,0)

        panel_texto = LabelFrame(window_modify, bg = "#87CEFA")
        panel_texto.grid(row=0, column=0)

        bt_panel_texto = LabelFrame(window_modify, bg = "#87CEFA")
        bt_panel_texto.grid(row=2, column=0)

#------Dialogo de confirmacion para la modificacion del articulo

        Label(panel_texto, text = "¿Quieres modificar este articulo?", bg = "#87CEFA", font = ("Alrich", "11", "normal")).grid(row = 0, column = 0, columnspan = 3)
        Label(panel_texto, text = self.nombre, bg ="#87CEFA", font = ("Alrich", "11", "normal")).grid(row = 1, column = 0)
        Label(panel_texto, text = self.referencia, bg ="#87CEFA", font = ("Alrich", "11", "normal")).grid(row = 1, column = 1)
        Label(panel_texto, text = self.precio, bg ="#87CEFA", font = ("Alrich", "11", "normal")).grid(row = 1, column = 2)

#------Cuadros de texto de la ventana modificar

        Label(panel_texto, text = "Introduce un nuevo Nombre", bg = "#87CEFA",font = ("Alrich", "11", "normal")).grid(row = 2, column = 0)
        nombre = Entry(panel_texto, font = ("Alrich", "11", "normal"), width=25)
        nombre.grid(row = 3, column = 0)
        nombre.focus()

        Label(panel_texto, text="Introduce una nueva Referencia", bg="#87CEFA", font=("Alrich", "11", "normal")).grid(row=2, column=1)
        ape = Entry(panel_texto, font=("Alrich", "11", "normal"), width=25)
        ape.grid(row=3, column=1)

        Label(panel_texto, text="Introduce un nuevo Precio", bg="#87CEFA", font=("Alrich", "11", "normal")).grid(row=2,column=2)
        tlf = Entry(panel_texto, font=("Alrich", "11", "normal"), width=25)
        tlf.grid(row=3, column=2)

#-------Botones de la nueva ventana de modificar

        btOk = Button(bt_panel_texto, command = lambda: si(), text = "Si", width = 10)
        btOk.configure(bg = "#90EE90", cursor = 'hand2',font=("Alrich", "11", "normal"))
        btOk.grid(row = 1, column = 0, padx = 2, pady = 3, sticky = W + E)

        btNo = Button(bt_panel_texto, command = window_modify.destroy, text = "No",width = 10, bg = "yellow", cursor = 'hand2')
        btNo.configure(bg = "#90EE90", cursor = 'hand2', font=("Alrich", "11", "normal"))
        btNo.grid(row = 1, column = 1, padx = 2, pady = 3, sticky = W + E)

        btCancel = Button(bt_panel_texto, command = window_modify.destroy, text = "Cancelar", width = 10, bg = "green", cursor = 'hand2')
        btCancel.configure(bg = "#90EE90", cursor = 'hand2', font=("Alrich", "11", "normal"))
        btCancel.grid(row = 1, column = 2, padx = 2, pady = 3, sticky = W + E)

#--------Funciones de los botones

        def si():
            articulo = self.val_modify
            nombre_nuevo = nombre.get()
            ref_nueva = ape.get()
            pre_nuevo = tlf.get()
            a = modify_message(articulo)
            if a == True:
                _eliminar_antiguo(articulo[0])
                _agregar_nuevo(nombre_nuevo, ref_nueva, pre_nuevo)
            window_modify.destroy()

        def _agregar_nuevo(nombre, referencia, precio):
            g_nombre = nombre
            g_ref = referencia
            g_pre = precio
            with open('articulos_list.csv', 'a') as f:
                writer = csv.writer(f, lineterminator ='\r', delimiter=',')
                writer.writerow((g_nombre,g_ref,g_pre))

        def _eliminar_antiguo(nombre_antiguo):
            nombre = nombre_antiguo
            with open('articulos_list.csv', 'r') as f:
                reader = list(csv.reader(f))
            with open('articulos_list.csv', 'w') as f:
                writer = csv.writer(f, lineterminator ='\r', delimiter=',')
                for i, row in enumerate(reader):
                    if nombre != row[0]:
                        writer.writerow(row)






