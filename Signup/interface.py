from abc import ABC, abstractmethod

class SignupInterface(ABC):

    @abstractmethod
    def user_signup(self):
        pass
