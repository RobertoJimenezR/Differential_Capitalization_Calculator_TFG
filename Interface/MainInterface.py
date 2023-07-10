import datetime
import tkinter
from functools import partial
from pydoc import text
from tkinter import Tk, Label, Button, ttk, X, Y, RIGHT, BOTTOM

import dateutil.parser

import CalculationModule.CalculationEngine
import DataImportModule.DataImporter
from Interface.Table import Table


class MainInterface:
    currentSCCE = None

    def __init__(self):
        self.dataimporter: DataImportModule.DataImporter
        self.dataimporter = None
        self.calculationengine: CalculationModule.CalculationEngine
        self.calculationengine = None
        self.CFE = []
        self.dates = []
        self.capitals=[]


        master = Tk()
        self.master = master
        master.title("Calculadora financiera")
        master.geometry()

        barra_de_menus = tkinter.Menu(master)
        self.barra_de_menus = barra_de_menus
        self.main()
        self.calculationengineconfiguration()
        self.dataimportconfiguration()
        master.config(menu=barra_de_menus)

        frameoptions=tkinter.Frame(master)
        Label(frameoptions, text="Tipo de capitalización diferencial:").grid(row=0, column=0, rowspan=1, columnspan=1)
        self.clt = tkinter.StringVar()
        self.clt.set(CalculationModule.CalculationEngine.capitalizationLawType)
        tkinter.OptionMenu(frameoptions, self.clt, *CalculationModule.CalculationEngine.capitalizationLawOptions,
                           command=self.changesclt).grid(row=0, column=1, rowspan=1, columnspan=1)
        self.vsce = tkinter.StringVar(frameoptions)
        self.vsce.set("Aún no ha activado un motor de cálculo")
        Label(frameoptions, textvariable=self.vsce).grid(row=0, column=2, rowspan=1, columnspan=1)
        frameoptions.pack()

        framefunction=tkinter.Frame(master)
        Label(framefunction, text="Función de capital:").grid(row=0, column=0, rowspan=1, columnspan=1)
        self.cexpresion=tkinter.StringVar()
        tkinter.Entry(framefunction,textvariable=self.cexpresion).grid(row=1, column=0, rowspan=1, columnspan=1)
        Label(framefunction, text="Función de tasa de actualización:").grid(row=0, column=1, rowspan=1, columnspan=1)
        self.iexpresion=tkinter.StringVar()
        tkinter.Entry(framefunction,textvariable=self.iexpresion).grid(row=1, column=1, rowspan=1, columnspan=1)
        Label(framefunction, text="Variable:").grid(row=0, column=2, rowspan=1, columnspan=1)
        self.variable = tkinter.StringVar()
        tkinter.Entry(framefunction, textvariable=self.variable).grid(row=1, column=2, rowspan=1, columnspan=1)
        framefunction.pack()


        framelmit=tkinter.Frame(master)
        Label(framelmit, text="Límite inferior:").grid(row=0, column=0, rowspan=1, columnspan=1)
        self.lowerlimit=tkinter.StringVar()
        tkinter.Entry(framelmit,textvariable=self.lowerlimit).grid(row=1, column=0, rowspan=1, columnspan=1)
        Label(framelmit, text="Límite superior:").grid(row=0, column=1, rowspan=1, columnspan=1)
        self.upperlimit=tkinter.StringVar()
        tkinter.Entry(framelmit,textvariable=self.upperlimit).grid(row=1, column=1, rowspan=1, columnspan=1)
        framelmit.pack()

        frameaccion = tkinter.Frame(master)
        self.calculateB=Button(frameaccion, text="Calcular", command=self.calculate, state="disabled")
        self.calculateB.grid(row=0, column=0, rowspan=1, columnspan=1)
        Label(frameaccion, text="Gráfico de evolución del valor:").grid(row=0, column=1, rowspan=1, columnspan=1)
        self.graphicB = Button(frameaccion, text="Mostrar", command=self.showgraphic, state="disabled")
        self.graphicB.grid(row=0, column=2, rowspan=1, columnspan=1)
        frameaccion.pack()

        frameres = tkinter.Frame(master)
        Label(frameres, text="Resultado:").grid(row=12, column=5, rowspan=1, columnspan=1)
        Label(frameres, text="Esxpresión indefinida:").grid(row=13, column=1, rowspan=1, columnspan=1)
        self.IIR = tkinter.StringVar()
        Label(frameres, textvariable=self.IIR).grid(row=14, column=1, rowspan=1, columnspan=1)
        Label(frameres, text="Valor del capital:").grid(row=13, column=10, rowspan=1, columnspan=1)
        self.IDR = tkinter.StringVar()
        Label(frameres, textvariable=self.IDR).grid(row=14, column=10, rowspan=1, columnspan=1)
        frameres.pack()

        framelmitdate = tkinter.Frame(master)
        Label(framelmitdate, text="Fecha final operación:").grid(row=0, column=1, rowspan=1, columnspan=1)
        self.upperdatelimit = tkinter.Entry(framelmitdate)
        self.upperdatelimit.grid(row=1, column=1, rowspan=1, columnspan=1)
        framelmitdate.pack()

        frameaccion2 = tkinter.Frame(master)
        Label(frameaccion2, text="Tabla de capitales:").grid(row=0, column=0, rowspan=1, columnspan=1)
        self.tableB = Button(frameaccion2, text="Calcular", command=self.showvalueevolucion, state="disabled")
        self.tableB.grid(row=0, column=0, rowspan=1, columnspan=1)
        frameaccion.pack()


        self.frametable=tkinter.Frame(master)


    def mainloop(self):
        self.master.mainloop()

    def main(self):
        main = tkinter.Menu(self.barra_de_menus)
        main.add_command(label="Importar datos de EFE", command=self.importdata)
        main.add_command(label="Editar datos de EFE", command=self.editCF)
        main.add_command(label="Editar fechas", command=self.editdates)
        main.add_command(label="Editar capitales", command=self.editcapitals)
        self.barra_de_menus.add_cascade(label="Inicio", menu=main)


    def calculationengineconfiguration(self):
        def changece(ce):
            self.calculationengine = ce
            self.vsce.set("Ha seleccionado " + ce.title)
            self.calculateB.config(state="normal")
            self.graphicB.config(state="normal")
            self.master.update_idletasks()

        ceconfigurationmenu = tkinter.Menu(self.barra_de_menus)
        for a in CalculationModule.CalculationEngine.getSC():
            sc = CalculationModule.CalculationEngine.getISC(a)
            cemenu = tkinter.Menu(ceconfigurationmenu)
            cemenu.add_command(label="Activar", command=partial(changece, sc))
            cemenu.add_command(label="Configurar", command=sc.getConfigurationOptionsWindow)
            ceconfigurationmenu.add_cascade(label=sc.getDescription()[0], menu=cemenu)
            pass
        self.barra_de_menus.add_cascade(label="Configuración motor de cálculo", menu=ceconfigurationmenu)

    def dataimportconfiguration(self):
        def changedi(di):
            self.dataimporter = di

        diconfigurationmenu = tkinter.Menu(self.barra_de_menus)
        for a in DataImportModule.DataImporter.getSC():
            di = DataImportModule.DataImporter.getISC(a)
            dimenu = tkinter.Menu(diconfigurationmenu)
            dimenu.add_command(label="Activar", command=partial(changedi, di))
            dimenu.add_command(label="Configurar", command=di.configurationOptionsWindow)
            diconfigurationmenu.add_cascade(label=di.getDescription()[0], menu=dimenu)
        self.barra_de_menus.add_cascade(label="Configuración importación de datos", menu=diconfigurationmenu)

    def changesclt(self, optionvalue):
        if self.calculationengine is None:
            pass
        else:
            self.calculationengine.capitalizationLawType = optionvalue

    def calculate(self):
        self.calculationengine.init(self.cexpresion.get(), self.iexpresion.get(), self.variable.get())
        self.IIR.set(self.calculationengine.getIndefiniteIntegral())
        self.IDR.set(
            self.calculationengine.getDefiniteIntegral(float(self.lowerlimit.get()), float(self.upperlimit.get())))

    def showgraphic(self):
        """Shows the graphic evolution table"""
        self.calculationengine.init(self.cexpresion.get(), self.iexpresion.get(), self.variable.get())
        self.calculationengine.definiteIntegralGraphic(float(self.lowerlimit.get()), float(self.upperlimit.get()))

    def showvalueevolucion(self):
        """Shows the capital evolution table"""

        data=[]
        if self.capitals.__len__()>0:
            delta = lambda y, d0: (y - d0).days
            try:
                d0 = dateutil.parser.parse(self.capitals[0][1], dayfirst=True)
                df = dateutil.parser.parse(self.upperdatelimit.get(), dayfirst=True)
                d=delta(df, d0)
                for r in self.capitals:
                    lm = r[0]
                    self.calculationengine.init(r[2], self.iexpresion.get(), self.variable.get())
                    data.append([r[0], r[1], r[2],
                                 self.calculationengine.getDefiniteIntegral(
                                     delta(dateutil.parser.parse(r[1], dayfirst=True), d0),d)])
            except Exception as e:
                print("Algún error ha ocurrido con las fechas")
                print(e)
        self.frametable.destroy()
        self.frametable=tkinter.Frame(self.master)
        Table(self.frametable, ["Momento", "Fecha", "Capital aportado", "Valor del capital"], data, self.master)
        self.frametable.pack()
        self.calculationengine.init(self.cexpresion.get(), self.iexpresion.get(), self.variable.get())

    def importdata(self):
        self.dataimporter.importDataWindow()

    def editCF(self):
        """Opens a window that allows you to edit the cash flow"""


        def order():
            saveChangesExit()
            self.editCF()

        def saveChangesExit():
            self.CFE=MainInterface.orderbydate(table.getlistedited(),0)
            master.destroy()

        def saveChangesExitContinue():
            saveChangesExit()
            self.editdates()

        self.CFE=MainInterface.orderbydate(self.dataimporter.getCFEntryList(),0)

        master = tkinter.Toplevel()
        master.title("Editar movimientos de flujo de efectivo")

        frame = tkinter.Frame(master)
        frame.pack(side="top")

        Button(frame, text="Cerrar", command=master.destroy).pack(side=tkinter.RIGHT)
        Button(frame, text="Guardar y cerrar", command=saveChangesExit).pack(side=tkinter.RIGHT)
        Button(frame, text="Guardar y continuar", command=saveChangesExitContinue).pack(side=tkinter.RIGHT)
        Button(frame, text="Ordenar", command=order).pack(side=tkinter.RIGHT)

        frame = tkinter.Frame(master)
        frame.pack(fill=tkinter.BOTH, expand=1)
        table = Table(frame, ["Fecha", "Descripción", "Importe", "Categoría", "Subcategoría"], self.CFE, master=self.master, editablefields=[True, True, True, True, True], readonly=False)

    def editdates(self):
        """Opens a window that allows you to edit the dates"""


        def order():
            saveChangesExit()
            self.editdates()

        def saveChangesExit():
            self.dates=MainInterface.orderbydate(table.getlistedited(),1, True)
            master.destroy()

        def saveChangesExitContinue():
            saveChangesExit()
            self.entrybydate()
            self.editcapitals()

        master = tkinter.Toplevel()
        master.title("Editar fechas")

        frame = tkinter.Frame(master)
        frame.pack(side="top")

        Button(frame, text="Cerrar", command=master.destroy).pack(side=tkinter.RIGHT)
        Button(frame, text="Guardar y cerrar", command=saveChangesExit).pack(side=tkinter.RIGHT)
        Button(frame, text="Guardar y continuar", command=saveChangesExitContinue).pack(side=tkinter.RIGHT)
        Button(frame, text="Ordenar", command=order).pack(side=tkinter.RIGHT)

        frame = tkinter.Frame(master)
        frame.pack(fill=tkinter.BOTH, expand=1)
        table = Table(frame, ["Index", "Fecha"], self.dates, master=self.master, editablefields=[False, True], readonly=False)

    def editcapitals(self):
        """Opens a window that allows you to edit the capitals"""
        def order():
            saveChangesExit()
            self.editcapitals()

        def saveChangesExit():
            self.capitals = MainInterface.orderbydate(table.getlistedited(), 1, True)
            master.destroy()

        def saveChangesExitContinue():
            saveChangesExit()
            nexpr=self.calculationengine.getgeneratecapitalfunction(self.capitals)
            self.cexpresion.set(nexpr[0])
            self.variable.set(nexpr[1])
            self.lowerlimit.set("0")
            self.upperlimit.set(str((dateutil.parser.parse(self.upperdatelimit.get(), dayfirst=True)-nexpr[2]).days))
            self.showvalueevolucion()
            self.calculate()

        master = tkinter.Toplevel()
        master.title("Editar capitales")

        frame = tkinter.Frame(master)
        frame.pack(side="top")

        Button(frame, text="Cerrar", command=master.destroy).pack(side=tkinter.RIGHT)
        Button(frame, text="Guardar y cerrar", command=saveChangesExit).pack(side=tkinter.RIGHT)
        Button(frame, text="Guardar y continuar", command=saveChangesExitContinue).pack(side=tkinter.RIGHT)
        Button(frame, text="Ordenar", command=order).pack(side=tkinter.RIGHT)

        frame = tkinter.Frame(master)
        frame.pack(fill=tkinter.BOTH, expand=1)
        table = Table(frame, ["Index", "Fecha", "Capital"], self.capitals, master=self.master, editablefields=[False, True,True], readonly=False)

    @classmethod
    def orderbydate(cls, data, i, index: bool= False):
        """Sorts the Data list by the date of its records, and indicates the position of the date within the records"""
        data.sort(key=lambda x: dateutil.parser.parse(x[i], dayfirst=True))
        if not index:
            for r in data:
                try:
                    r[i] = dateutil.parser.parse(r[i], dayfirst=True).strftime("%d/%m/%Y")
                except ValueError as e:
                    print("Error capturado en la fecha "+r[i]+"\n"+ e.__str__())
                    data.remove(r)
            return data
        else:
            res=[]
            j=0
            for r in data:
                try:
                    r[i] = dateutil.parser.parse(r[i], dayfirst=True).strftime("%d/%m/%Y")
                    aux=[j]
                    aux.extend(r[1:])
                    j+=1
                    res.append(aux)
                except ValueError as e:
                    print("Error capturado en la fecha " + r[i] + "\n" + e.__str__())
                    data.remove(r)

            return res

    def entrybydate(self):
        """Group cash flows by dates"""
        dates=self.dates
        cfentry=self.CFE
        tcapitals={}
        self.capitals=[]

        interval = lambda x,y, z: dateutil.parser.parse(x, dayfirst=True)<=dateutil.parser.parse(y, dayfirst=True) and dateutil.parser.parse(y, dayfirst=True)<dateutil.parser.parse(z, dayfirst=True)
        if dates.__len__()>=2:
            for i in range(0, dates.__len__()-1):
                s=True
                for j in cfentry:
                    if(interval(dates[i][1], j[0], dates[i+1][1])):

                        if s:tcapitals[i]=float(j[2])
                        else: tcapitals[i]+=float(j[2])
                        s=False

            for k in tcapitals.keys():
                self.capitals.append([k+1, dates[k+1][1], tcapitals[k]])
        return self.capitals