from DataImportModule import DataImporter


class OtherDataImporter(DataImporter):
    title = "Otro importar datos local"
    description = "Desde otro"

    def __init__(self):
        pass

    def configurationoptionswindow(self) -> None:
        pass

    def importdatawindow(self):
        pass

    def getcfentrylist(self) -> [[]]:
        pass

    def getdescription(self):
        return self.title, self.description
