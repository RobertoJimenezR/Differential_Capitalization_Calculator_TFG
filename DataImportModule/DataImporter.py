from abc import ABC, abstractmethod


class DataImporter(ABC):
    """Interface class for the importation module. Defines the most important methods that the interface will use"""
    title: str = "-"
    description: str = "Debe rellenar la información title y description en el código de su motor de importación"

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def configurationOptionsWindow(self) -> None:
        """Runs a window where you can configure the options of each instance of the corresponding subclass"""
        pass

    @abstractmethod
    def importDataWindow(self):
        """Runs a window to perform the import"""
        pass

    @abstractmethod
    def getCFEntryList(self) -> [[]]:
        """Returns a list of expected cash flow movements. The list must be returned must be a list of a 5-tuple [Date, Description, Amount, Category, Subcategory]"""
        pass
    @classmethod
    def getSC(cls):
        """Returns a list of available subclasses. These subclasses must be imported before calling this method."""
        return DataImporter.__subclasses__()

    @classmethod
    def getISC(cls, SC):
        """Returns an instance of the sublcase indicated in SC"""
        if SC in cls.getSC():
            aux=DataImporter.__new__(SC)
            aux.__init__()
            return aux
        return None

    @abstractmethod
    def getDescription(self):
        """Returns a 2-tuple with the title and description of the subclass"""
        return (self.title, self.description)
