from tkinter import Tk, Label

from CalculationModule import CalculationEngine


class OtherCalculationEngine(CalculationEngine):
    title = "Otro motor de cálculo local"
    description = "Otro motor"

    def __init__(self, capitalfunction: str, interestfunction: str, variable: str, capitalizationlawtype: str):
        super().__init__(capitalfunction, interestfunction, variable, capitalizationlawtype)

    def getindefiniteintegral(self) -> str:
        return ""

    def getdefiniteintegral(self, lowerlimit: float, upperlimit: float) -> float:
        return 0

    def definiteintegralgraphic(self, lowerlimit: float, upperlimit: float) -> None:
        return None

    def configurationoptionswindow(self) -> None:
        class ConfInterface:
            def __init__(self):
                master = Tk()
                self.master = master
                master.title("Configuración otro motor de cálculo")
                self.etiqueta = Label(master, text="Configuración otro motor de cálculo")
                self.etiqueta.pack()
        ConfInterface()

    def getgeneratecapitalfunction(self, capitals: []):
        pass
