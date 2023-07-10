from DataImportModule import DataImporter


class OtherDataImporter(DataImporter):
    title = "Otro importar datos local"
    description = "Desde otro"

    def __init__(self):
        pass

    def configurationOptionsWindow(self) -> None:
        pass

    def importDataWindow(self):
        pass

    def getCFEntryList(self) -> [[]]:
        pass

    def getDescription(self):
        return (self.title, self.description)
