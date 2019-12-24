import csv

from output_strategies.base_strategy import OutputStrategy


class CSVStrategy(OutputStrategy):

    def write_output_data(self, output_filename, result_dict):
        with open(output_filename, 'w', newline='') as file_obj:
            writer = csv.writer(file_obj)
            writer.writerow(result_dict.keys())
            writer.writerows(zip(*result_dict.values()))
