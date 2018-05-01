
from abc import ABCMeta, abstractclassmethod, abstractmethod, abstractproperty

class Extractor(object, metaclass=ABCMeta):
    @abstractclassmethod
    def from_external_source(self):
        pass

    @abstractmethod
    def get_record(self):
        pass

    @abstractmethod
    def set_record(self):
        pass

    record = property(get_record, set_record)
    