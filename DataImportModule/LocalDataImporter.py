import tkinter
from tkinter.filedialog import askopenfilename
from tkinter import Label, Button, ttk
import dateutil.parser
import pandas
from DataImportModule import DataImporter


class LocalDataImporter(DataImporter):
    title = "Importar datos local"
    description = "Desde csv"

    def __init__(self):
        self.map = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}
        self.delimiter = ";"
        self.CFEntry = []

    def configurationoptionswindow(self) -> None:
        di = self

        class ConfInterface:
            def __init__(self):
                master = tkinter.Toplevel()
                self.master = master
                master.title("Configuración importador de datos local")
                Label(master, text="Posiciones de los campos en la fila del CSV (comenzando en 0):").grid(row=0,
                                                                                                          column=0,
                                                                                                          rowspan=1,
                                                                                                          columnspan=1)

                Label(master, text="Fecha:").grid(row=1, column=0, rowspan=1, columnspan=1)
                self.dateposition = tkinter.IntVar(master, value=di.map[0])
                tkinter.Entry(master, textvariable=self.dateposition).grid(row=1, column=1, rowspan=1, columnspan=1)

                Label(master, text="Descripción:").grid(row=1, column=2, rowspan=1, columnspan=1)
                self.descriptionposition = tkinter.IntVar(master, value=di.map[1])
                tkinter.Entry(master, textvariable=self.descriptionposition).grid(row=1, column=3, rowspan=1,
                                                                                  columnspan=1)

                Label(master, text="Importe:").grid(row=1, column=4, rowspan=1, columnspan=1)
                self.amountposition = tkinter.IntVar(master, value=di.map[2])
                tkinter.Entry(master, textvariable=self.amountposition).grid(row=1, column=5, rowspan=1, columnspan=1)

                Label(master, text="Categoría:").grid(row=1, column=6, rowspan=1, columnspan=1)
                self.categoryposition = tkinter.IntVar(master, value=di.map[3])
                tkinter.Entry(master, textvariable=self.categoryposition).grid(row=1, column=7, rowspan=1, columnspan=1)

                Label(master, text="Subcategoría:").grid(row=1, column=8, rowspan=1, columnspan=1)
                self.subcategoryposition = tkinter.IntVar(master, value=di.map[4])
                tkinter.Entry(master, textvariable=self.subcategoryposition).grid(row=1, column=9, rowspan=1,
                                                                                  columnspan=1)

                Label(master, text="Delimitador:").grid(row=2, column=3, rowspan=1, columnspan=1)
                self.delimiter = tkinter.Entry(master)
                self.delimiter.grid(row=2, column=4, rowspan=1, columnspan=1)

                Button(master, text="Guardar cambios y cerrar", command=self.savechangesexit).grid(row=3, column=10,
                                                                                                   rowspan=1,
                                                                                                   columnspan=1)
                Button(master, text="Cerrar", command=master.destroy).grid(row=3, column=11, rowspan=1, columnspan=1)

            def savechangesexit(self):
                di.map = {0: self.dateposition.get(), 1: self.descriptionposition.get(),
                          2: self.amountposition.get(),
                          3: self.categoryposition.get(), 4: self.subcategoryposition.get()}
                if self.delimiter.get() != "":
                    di.delimiter = self.delimiter.get()
                self.master.destroy()

        ConfInterface()

    def importdatawindow(self):
        file_name = askopenfilename()
        df = pandas.read_csv(file_name, delimiter=self.delimiter, header=None)
        self.CFEntry = []
        categories = []
        subcategories = []
        for r in df.to_numpy():
            self.CFEntry.append([r[self.map[0]], r[self.map[1]], r[self.map[2]], r[self.map[3]], r[self.map[4]]])
            if not (r[self.map[3]] in categories):
                categories.append(r[self.map[3]])
            if not (r[self.map[4]] in subcategories):
                subcategories.append(r[self.map[4]])

        di = self

        class CFfilter:
            def __init__(self):
                master = tkinter.Toplevel()
                self.master = master
                master.title("Importar movimientos de flujo de efectivo")

                Label(master, text="Filtro de fecha:").grid(row=0, column=0, rowspan=1, columnspan=1)

                Label(master, text="Desde:").grid(row=1, column=0, rowspan=1, columnspan=1)
                self.date0 = tkinter.Entry(master)
                self.date0.grid(row=1, column=1, rowspan=1, columnspan=1)

                Label(master, text="hasta:").grid(row=1, column=2, rowspan=1, columnspan=1)
                self.date1 = tkinter.Entry(master)
                self.date1.grid(row=1, column=3, rowspan=1, columnspan=1)

                Label(master, text="Filtro categoría:").grid(row=2, column=0, rowspan=1, columnspan=1)
                self.category = tkinter.Variable(value=categories)
                self.LBcategory = tkinter.Listbox(master, listvariable=self.category, height=5,
                                                  selectmode=tkinter.MULTIPLE, exportselection=0,
                                                  xscrollcommand=ttk.Scrollbar(master,
                                                                               orient=tkinter.HORIZONTAL).set,
                                                  yscrollcommand=ttk.Scrollbar(master, orient=tkinter.VERTICAL).set,
                                                  activestyle="dotbox")
                self.LBcategory.grid(row=2, column=1, rowspan=1, columnspan=1)
                self.LBcategory.selection_set(0, tkinter.END)

                Label(master, text="Filtro subcategoría:").grid(row=2, column=2, rowspan=1, columnspan=1)
                self.subcategory = tkinter.Variable(value=subcategories)
                self.LBsubcategory = tkinter.Listbox(master, listvariable=self.subcategory, height=5,
                                                     selectmode=tkinter.MULTIPLE, exportselection=0,
                                                     xscrollcommand=ttk.Scrollbar(master,
                                                                                  orient=tkinter.HORIZONTAL).set,
                                                     yscrollcommand=ttk.Scrollbar(master, orient=tkinter.VERTICAL).set,
                                                     activestyle="dotbox")
                self.LBsubcategory.grid(row=2, column=3, rowspan=1, columnspan=1)
                self.LBsubcategory.selection_set(0, tkinter.END)

                Button(master, text="Importar", command=self.importdata).grid(row=3, column=11,
                                                                              rowspan=1,
                                                                              columnspan=1)
                Button(master, text="Cerrar", command=master.destroy).grid(row=3, column=12, rowspan=1, columnspan=1)

            def importdata(self):
                aux = []
                selectedcategories = []
                for i in self.LBcategory.curselection():
                    selectedcategories.append(self.LBcategory.get(i))
                selectedsubcategories = []
                for i in self.LBsubcategory.curselection():
                    selectedsubcategories.append(self.LBsubcategory.get(i))

                # Filtrar con fechas capturando errores
                try:
                    d0 = dateutil.parser.parse(self.date0.get())
                    try:
                        d1 = dateutil.parser.parse(self.date1.get())
                        for r in di.CFEntry:
                            try:
                                d = dateutil.parser.parse(r[0])
                                if (d0 <= d) & (d <= d1) & \
                                        (r[3] in selectedcategories) & (r[4] in selectedsubcategories):
                                    aux.append(r)
                            except ValueError as e:
                                print(
                                    "Error capturado en la fecha " + r[0] + " en el fichero de origen\n" + e.__str__())
                    except ValueError as e:
                        print(
                            "Error capturado en la fecha " + self.date1.get() + " en la fecha superior de filtro\n" +
                            e.__str__())
                        if self.date1.get() == "":
                            for r in di.CFEntry:
                                try:
                                    d = dateutil.parser.parse(r[0])
                                    if (d0 <= d) & \
                                            (r[3] in selectedcategories) & (
                                            r[4] in selectedsubcategories):
                                        aux.append(r)
                                except ValueError as e:
                                    print("Error capturado en la fecha " + r[
                                        0] + " en el fichero de origen\n" + e.__str__())

                except ValueError as e:
                    print(
                        "Error capturado en la fecha " + self.date0.get() + " en la fecha inferior de filtro\n" +
                        e.__str__())
                    if self.date0.get() == "":
                        try:
                            d1 = dateutil.parser.parse(self.date1.get())
                            for r in di.CFEntry:
                                try:
                                    d = dateutil.parser.parse(r[0])
                                    if (d <= d1) & \
                                            (r[3] in selectedcategories) & (
                                            r[4] in selectedsubcategories):
                                        aux.append(r)
                                except ValueError as e:
                                    print("Error capturado en la fecha " + r[
                                        0] + " en el fichero de origen\n" + e.__str__())

                        except ValueError as e:
                            print(
                                "Error capturado en la fecha " + self.date1.get() + " en la fecha superior de filtro\n"
                                + e.__str__())
                            if self.date1.get() == "":
                                for r in di.CFEntry:
                                    try:
                                        dateutil.parser.parse(r[0])
                                        if (r[3] in selectedcategories) & (
                                                r[4] in selectedsubcategories):
                                            aux.append(r)
                                    except ValueError as e:
                                        print("Error capturado en la fecha " + r[
                                            0] + " en el fichero de origen\n" + e.__str__())

                di.CFEntry = aux
                self.master.destroy()

        CFfilter()

    def getcfentrylist(self) -> [[]]:
        return self.CFEntry

    def getdescription(self):
        return self.title, self.description
