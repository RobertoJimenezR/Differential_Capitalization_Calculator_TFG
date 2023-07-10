from tkinter import Tk, Label, Button

from CalculationModule import CalculationEngine



class OtherCalculationEngine(CalculationEngine):
    title = "Otro motor de cálculo local"
    description = "Otro motor"
    def __init__(self, capitalFunction: str, interestFunction: str, variable: str, capitalizationLawType: str):
        super().__init__(capitalFunction, interestFunction, variable, capitalizationLawType)

    def getIndefiniteIntegral(self) -> str:
        return ""

    def getDefiniteIntegral(self, lowerLimit: float, upperLimit: float) -> float:
        return 0

    def definiteIntegralGraphic(self, lowerLimit: float, upperLimit: float) -> None:
        return None

    def configurationOptionsWindow(self) -> None:
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
