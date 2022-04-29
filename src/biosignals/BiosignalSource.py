###################################

# IT - PreEpiSeizures

# Package: biosignals
# File: BiosignalSource
# Description: Abstract class of the sources where biosignals are acquired.

# Contributors: João Saraiva
# Last update: 23/04/2022

###################################

from abc import ABC, abstractmethod

class BiosignalSource(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    def __eq__(self, other):
        return type(self) == type(other)

    @staticmethod
    @abstractmethod
    def _read(path:str, type):
        pass

    @staticmethod
    @abstractmethod
    def _write(path:str):
        pass