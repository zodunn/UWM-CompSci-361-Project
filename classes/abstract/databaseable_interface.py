import abc
from abc import abstractmethod


class DatabaseObj(metaclass=abc.ABCMeta):

    @abstractmethod
    def save_new(self):
        pass

    @abstractmethod
    def overwrite(self, primary_key_holder):
        pass

    @staticmethod
    @abstractmethod
    def delete(primary_key):
        pass

    @staticmethod
    @abstractmethod
    def from_model(model_equivalent):
        pass

class DatabaseObjInternalKey(metaclass=abc.ABCMeta):

    @abstractmethod
    def save(self):
        pass

    @staticmethod
    @abstractmethod
    def from_model(model_equivalent):
        pass
