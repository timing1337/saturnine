from game_server.resource.excel import ExcelOutput
import dataclasses

class ResourceManager:
    def __init__(self, path: str):
        self.excels = ExcelOutput.load_all_excels(path)
        ...