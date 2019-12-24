from output_strategies.base_strategy import OutputStrategy


class XMLStrategy(OutputStrategy):

    def write_output_data(self, output_filename, result_dict):
        raise NotImplementedError
