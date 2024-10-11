from abc import ABCMeta, abstractmethod


class Game(metaclass=ABCMeta):
    def __init__(self):
        pass
    
    @property
    def running(self):
        pass