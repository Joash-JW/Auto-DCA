from abc import ABC, abstractmethod


class Broker(ABC):
    # abstract class

    # getter for class name
    @property
    def name(self):
        return self.__class__.__name__

    # method for subclasses to implement
    @abstractmethod
    def place_order(self): raise NotImplementedError
