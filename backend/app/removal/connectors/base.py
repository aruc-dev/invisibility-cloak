\
from abc import ABC, abstractmethod

class RemovalConnector(ABC):
    def __init__(self, broker: dict, pii: dict, headless: bool = True):
        self.broker = broker
        self.pii = pii
        self.headless = headless

    @abstractmethod
    def submit(self) -> dict:
        ...
