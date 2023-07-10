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

    def __init__(self, capitalFunction: str, interestFunction: str, variable: str, capitalizationLawType: str):
        super().__init__(capitalFunction, interestFunction, variable, capitalizationLawType)

    def getIndefiniteIntegral(self) -> str:
        if self.capitalizationLawType == "Simple":
            return self.capitalFunction + "+" + str(
                integrate("(" + self.capitalFunction + ")*(" + self.interestFunction + ")", Symbol(self.variable),
                          conds=self.conds))
        ie = str(integrate(self.interestFunction, (Symbol(self.variable), 0, self.variable), conds="none"))
        return self.capitalFunction + "+" + str(
            integrate("(" + self.capitalFunction + ")*(" + self.interestFunction + ")*(exp(" + ie + "))",
                      Symbol(self.variable), conds=self.conds))

    def getDefiniteIntegral(self, lowerLimit: float, upperLimit: float) -> float:
        if self.capitalizationLawType == "Simple":
            return sympy.expand(self.capitalFunction).subs(self.variable, upperLimit) + integrate(
                "(" + self.capitalFunction + ")*(" + self.interestFunction + ")",
                (Symbol(self.variable), lowerLimit, upperLimit), conds=self.conds)
        ie = str(integrate(self.interestFunction, (Symbol(self.variable), lowerLimit, self.variable), conds="none"))
        return sympy.expand(self.capitalFunction).subs(self.variable, upperLimit) + integrate(
            "(" + self.capitalFunction + ")*(" + self.interestFunction + ")*(exp(" + ie + "))",
            (Symbol(self.variable), lowerLimit, upperLimit), conds=self.conds)

    def definiteIntegralGraphic(self, lowerLimit: float, upperLimit: float) -> None:
        if self.capitalizationLawType == "Simple":
            exp = str(integrate("(" + self.capitalFunction + ")*(" + self.interestFunction + ")", Symbol(self.variable),
                                conds="none"))

        else:
            ie = str(
                integrate(self.interestFunction, (Symbol(self.variable), lowerLimit, self.variable), conds="none"))
            exp = str(integrate("(" + self.capitalFunction + ")*(" + self.interestFunction + ")*(exp(" + ie + "))",
                                (Symbol(self.variable), lowerLimit, self.variable), conds="none"))

        sympy.plotting.plot(self.capitalFunction, exp, self.capitalFunction + "+" + exp,
                            (self.variable, lowerLimit, upperLimit), title="Gráfico de volución del valor", ylabel="Valor", legend=True)

    def configurationOptionsWindow(self) -> None:
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

                Button(master, text="Guardar cambios y cerrar", command=self.saveChangesExit).grid(row=5, column=0,
                                                                                                   rowspan=1,
                                                                                                   columnspan=1)
                Button(master, text="Cerrar", command=master.destroy).grid(row=5, column=1, rowspan=1, columnspan=1)

            def saveChangesExit(self):
                ce.conds = self.ot.get()
                self.master.destroy()

        ConfInterface()

    def getgeneratecapitalfunction(self, capitals: [], variable: str ="t"):
        if capitals.__len__==0:
            return ("0",variable)

        delta = lambda y, d0: (dateutil.parser.parse(y, dayfirst=True) - d0).days
        d0=dateutil.parser.parse(capitals[0][1], dayfirst=True)
        exp=""
        for r in capitals:
            exp+=r[2]+"*((sign("+variable+"-"+str(delta(r[1],d0))+")+1)/2)+"

        return (exp[:-1],variable,d0)