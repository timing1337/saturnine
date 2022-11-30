from game_server.resource.excel import ExcelOutput
import dataclasses
from os import path
from loguru import logger

class ResourceManager:
    def __init__(self, dir: str):
        if path.exists(dir):
            self.excels = ExcelOutput.load_all_excels(dir)
        else:
            logger.opt(colors=True).debug(f'Resources directory <red>does not exist</red>, running with <yellow>minimal resources</yellow>')