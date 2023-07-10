import tkinter
from tkinter import Label, Button

import dateutil.parser
import sympy.plotting.plot
from sympy import *

from CalculationModule import CalculationEngine


class LocalCalculationEngine(CalculationEngine):
    title = "Motor de cálculo local"
    description = "Utiliza Sympy"
    conds = "none"

    def __init__(self, capitalfunction: str, interestfunction: str, variable: str, capitalizationlawtype: str):
        super().__init__(capitalfunction, interestfunction, variable, capitalizationlawtype)

    def getindefiniteintegral(self) -> str:
        if self.capitalizationlawtype == "Simple":
            return self.capitalfunction + "+" + str(
                integrate("(" + self.capitalfunction + ")*(" + self.interestfunction + ")", Symbol(self.variable),
                          conds=self.conds))
        ie = str(integrate(self.interestfunction, (Symbol(self.variable), 0, self.variable), conds="none"))
        return self.capitalfunction + "+" + str(
            integrate("(" + self.capitalfunction + ")*(" + self.interestfunction + ")*(exp(" + ie + "))",
                      Symbol(self.variable), conds=self.conds))

    def getdefiniteintegral(self, lowerlimit: float, upperlimit: float) -> float:
        if self.capitalizationlawtype == "Simple":
            return sympy.expand(self.capitalfunction).subs(self.variable, upperlimit) + integrate(
                "(" + self.capitalfunction + ")*(" + self.interestfunction + ")",
                (Symbol(self.variable), lowerlimit, upperlimit), conds=self.conds)
        ie = str(integrate(self.interestfunction, (Symbol(self.variable), lowerlimit, self.variable), conds="none"))
        return sympy.expand(self.capitalfunction).subs(self.variable, upperlimit) + integrate(
            "(" + self.capitalfunction + ")*(" + self.interestfunction + ")*(exp(" + ie + "))",
            (Symbol(self.variable), lowerlimit, upperlimit), conds=self.conds)

    def definiteintegralgraphic(self, lowerlimit: float, upperlimit: float) -> None:
        if self.capitalizationlawtype == "Simple":
            exp = str(integrate("(" + self.capitalfunction + ")*(" + self.interestfunction + ")", Symbol(self.variable),
                                conds="none"))

        else:
            ie = str(
                integrate(self.interestfunction, (Symbol(self.variable), lowerlimit, self.variable), conds="none"))
            exp = str(integrate("(" + self.capitalfunction + ")*(" + self.interestfunction + ")*(exp(" + ie + "))",
                                (Symbol(self.variable), lowerlimit, self.variable), conds="none"))

        sympy.plotting.plot(self.capitalfunction, exp, self.capitalfunction + "+" + exp,
                            (self.variable, lowerlimit, upperlimit), title="Gráfico de volución del valor",
                            ylabel="Valor", legend=True)

    def configurationoptionswindow(self) -> None:
        ce = self

        class ConfInterface:
            def __init__(self):
                master = tkinter.Toplevel()
                self.master = master
                master.title("Configuración motor de cálculo local")
                Label(master, text="Tipo de salida de expresiones:").grid(row=0, column=0, rowspan=1, columnspan=1)

                self.ot = tkinter.StringVar(master)
                self.ot.set(ce.conds)
                tkinter.OptionMenu(master, self.ot, *["none", "piecewise", "separate"]).grid(row=0, column=1, rowspan=1,
                                                                                             columnspan=1)

                Button(master, text="Guardar cambios y cerrar", command=self.savechangesexit).grid(row=5, column=0,
                                                                                                   rowspan=1,
                                                                                                   columnspan=1)
                Button(master, text="Cerrar", command=master.destroy).grid(row=5, column=1, rowspan=1, columnspan=1)

            def savechangesexit(self):
                ce.conds = self.ot.get()
                self.master.destroy()

        ConfInterface()

    def getgeneratecapitalfunction(self, capitals: [], variable: str = "t"):
        if capitals.__len__ == 0:
            return "0", variable

        def substractdate(y, d0):
            return (dateutil.parser.parse(y, dayfirst=True) - d0).days

        d0 = dateutil.parser.parse(capitals[0][1], dayfirst=True)
        exp = ""
        for r in capitals:
            exp += r[2]+"*((sign("+variable+"-"+str(substractdate(r[1], d0))+")+1)/2)+"

        return exp[:-1], variable, d0
