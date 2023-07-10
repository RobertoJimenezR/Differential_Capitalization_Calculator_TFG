from abc import ABC, abstractmethod


class DataImporter(ABC):
    """Interface class for the importation module. Defines the most important methods that the interface will use"""
    title: str = "-"
    description: str = "Debe rellenar la información title y description en el código de su motor de importación"

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def configurationoptionswindow(self) -> None:
        """Runs a window where you can configure the options of each instance of the corresponding subclass"""
        pass

    @abstractmethod
    def importdatawindow(self):
        """Runs a window to perform the import"""
        pass

    @abstractmethod
    def getcfentrylist(self) -> [[]]:
        """Returns a list of expected cash flow movements. The list must be returned must be a list of a 5-tuple [
        Date, Description, Amount, Category, Subcategory] """
        pass

    @classmethod
    def getsubclasss(cls):
        """Returns a list of available subclasses. These subclasses must be imported before calling this method."""
        return DataImporter.__subclasses__()

    @classmethod
    def getsubclassinstance(cls, sc):
        """Returns an instance of the sublcase indicated in subclass"""
        if sc in cls.getsubclasss():
            aux = DataImporter.__new__(sc)
            aux.__init__()
            return aux
        return None

    @abstractmethod
    def getdescription(self):
        """Returns a 2-tuple with the title and description of the subclass"""
        return self.title, self.description
