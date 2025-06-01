import abc
from abc import abstractmethod

from classes.new_user_class import NewUserClass


class SingleUserAssignable(metaclass=abc.ABCMeta):

    @abstractmethod
    def assign_user(self, user: NewUserClass):
        pass

    @abstractmethod
    def get_user(self):
        pass

    @abstractmethod
    def remove_user(self):
        pass
