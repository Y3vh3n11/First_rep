from abc import ABC, abstractmethod


class AbstractAssistant(ABC):
    @abstractmethod
    def main_loop(self):
        pass