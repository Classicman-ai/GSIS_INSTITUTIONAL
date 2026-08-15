from abc import ABC, abstractmethod


class GSISEngine(ABC):

    name = "UNKNOWN ENGINE"
    version = "1.0"


    @abstractmethod
    def run(self, context):
        pass


    def response(self, data):

        return {
            "engine": self.name,
            "version": self.version,
            **data
        }
