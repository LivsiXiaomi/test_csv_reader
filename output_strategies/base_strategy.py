from abc import ABC, abstractmethod


class OutputStrategy(ABC):

    @abstractmethod
    def write_output_data(self, output_filename, result_dict):
        pass
