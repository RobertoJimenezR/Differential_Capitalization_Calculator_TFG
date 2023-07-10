from abc import ABC, abstractmethod


class CalculationEngine(ABC):
    """Interface class for the calculation module. Defines the most important methods that the interface will use"""
    capitalizationLawOptions = ["Simple", "Compuesto"]
    capitalizationlawtype: str = "Simple"
    title: str = "-"
    description: str = " Debe rellenar la información title y description en el código de su motor de cálculo"

    @abstractmethod
    def __init__(self, capitalfunction: str, interestfunction: str, variable: str, capitalizationlawtype: str = None):
        self.capitalfunction = capitalfunction
        self.interestfunction = interestfunction
        self.variable = variable
        self.capitalizationlawtype = capitalizationlawtype
        if capitalizationlawtype in self.capitalizationLawOptions:
            self.capitalizationlawtype = capitalizationlawtype

    def init(self, capitalfunction: str, interestfunction: str, variable: str, capitalizationlawtype: str = None):
        """Allows you to jointly modify the functions of the calculation engine"""
        self.capitalfunction = capitalfunction
        self.interestfunction = interestfunction
        self.variable = variable
        if capitalizationlawtype in self.capitalizationLawOptions:
            self.capitalizationlawtype = capitalizationlawtype
        return self

    @abstractmethod
    def getindefiniteintegral(self) -> str:
        """Returns the indefinite integral."""
        pass

    @abstractmethod
    def getdefiniteintegral(self, lowerlimit: float, upperlimit: float) -> float:
        """Returns the definite integral between the given limits."""
        pass

    @abstractmethod
    def definiteintegralgraphic(self, lowerlimit: float, upperlimit: float) -> None:
        """Returns a graph with the defined integral, the capital function between the given limits"""
        pass

    @abstractmethod
    def configurationoptionswindow(self) -> None:
        """Runs a window where you can configure the options of each instance of the corresponding subclass"""
        pass

    @abstractmethod
    def getgeneratecapitalfunction(self, capitals: []):
        """Generates a capital function from the values passed in capitals. These values are sorted by date."""
        pass

    def getdescription(self):
        """Returns a 2-tuple with the title and description of the subclass"""
        return self.title, self.description

    @classmethod
    def getsubclass(cls):
        """Returns a list of available subclasses. These subclasses must be imported before calling this method."""
        return CalculationEngine.__subclasses__()

    @classmethod
    def getsubclassinstance(cls, subclass):
        """Returns an instance of the sublcase indicated in subclass"""
        if subclass in cls.getsubclass():
            return CalculationEngine.__new__(subclass)
        return None
