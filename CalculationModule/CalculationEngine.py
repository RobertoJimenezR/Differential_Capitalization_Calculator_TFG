from abc import ABC, abstractmethod


class CalculationEngine(ABC):
    """Interface class for the calculation module. Defines the most important methods that the interface will use"""
    capitalizationLawOptions = ["Simple", "Compuesto"]
    capitalizationLawType: str = "Simple"
    title: str = "-"
    description: str = " Debe rellenar la información title y description en el código de su motor de cálculo"

    @abstractmethod
    def __init__(self, capitalFunction: str, interestFunction: str, variable: str, capitalizationLawType: str = None):
        self.capitalFunction = capitalFunction
        self.interestFunction = interestFunction
        self.variable = variable
        self.capitalizationLawType = capitalizationLawType
        if capitalizationLawType in self.capitalizationLawOptions: self.capitalizationLawType = capitalizationLawType

    def init(self, capitalFunction: str, interestFunction: str, variable: str, capitalizationLawType: str = None):
        """Allows you to jointly modify the functions of the calculation engine"""
        self.capitalFunction = capitalFunction
        self.interestFunction = interestFunction
        self.variable = variable
        if capitalizationLawType in self.capitalizationLawOptions: self.capitalizationLawType = capitalizationLawType
        return self

    @abstractmethod
    def getIndefiniteIntegral(self) -> str:
        """Returns the indefinite integral."""
        pass

    @abstractmethod
    def getDefiniteIntegral(self, lowerLimit: float, upperLimit: float) -> float:
        """Returns the definite integral between the given limits."""
        pass

    @abstractmethod
    def definiteIntegralGraphic(self, lowerLimit: float, upperLimit: float) -> None:
        """Returns a graph with the defined integral, the capital function between the given limits"""
        pass

    @abstractmethod
    def configurationOptionsWindow(self) -> None:
        """Runs a window where you can configure the options of each instance of the corresponding subclass"""
        pass

    @abstractmethod
    def getgeneratecapitalfunction(self, capitals: []):
        """Generates a capital function from the values passed in capitals. These values are sorted by date."""
        pass

    def getDescription(self):
        """Returns a 2-tuple with the title and description of the subclass"""
        return (self.title, self.description)

    @classmethod
    def getSC(cls):
        """Returns a list of available subclasses. These subclasses must be imported before calling this method."""
        return CalculationEngine.__subclasses__()

    @classmethod
    def getISC(cls, SC):
        """Returns an instance of the sublcase indicated in SC"""
        if SC in cls.getSC():
            return CalculationEngine.__new__(SC)
        return None
