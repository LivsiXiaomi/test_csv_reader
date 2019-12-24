import csv
import os
from datetime import datetime
from collections import defaultdict

from output_strategies.csv_strategy import CSVStrategy
from output_strategies.json_strategy import JSONStrategy
from output_strategies.xml_strategy import XMLStrategy


class CSVParser(object):
    FILES_HEADER = 'filename'

    KEYS_MAPPING = {
        'timestamp': 'datetime',
        'date_readable': 'datetime',
        'date': 'datetime',
        'transaction': 'type',
        'amounts': 'amount',
    }

    DATE_FORMAT = {
        'timestamp': '%b %d %Y',
        'date': '%d-%m-%Y',
        'date_readable': '%d %b %Y'
    }

    COMBINE_KEYS = [('euro', 'cents', '.', 'amount')]

    STRATEGIES_MAPPING = {
        'csv': CSVStrategy,
        'xml': XMLStrategy,
        'json': JSONStrategy
    }

    def __init__(self, output_format, output_filename):
        self.output_filename = output_filename
        self.writer = self.STRATEGIES_MAPPING.get(output_format, 'csv')()

    def _combinate_cells(self, values_prefix, values_suffix, symbol):
        return list(map(lambda x, y: symbol.join([x, y]), values_prefix, values_suffix))

    def parse_files(self, filenames):
        raw_res = defaultdict(list)
        # read raw data
        for filename in filenames:
            file_data = self.read_file(filename)
            for key, values in file_data.items():
                raw_res[key] += values
        formatted_res = defaultdict(list)

        # format cells
        for key, values in raw_res.items():
            if key in self.DATE_FORMAT.keys():
                formatted_res[self.KEYS_MAPPING.get(key)] += [datetime.strftime(datetime.strptime(elem, self.DATE_FORMAT.get(key)), '%Y-%m-%d') for elem in values]
            elif key in self.KEYS_MAPPING.keys():
                formatted_res[self.KEYS_MAPPING.get(key)] += values
            else:
                formatted_res[key] += values

        # combine cells
        for combination in self.COMBINE_KEYS:
            formatted_res[combination[3]] += self._combinate_cells(raw_res.get(combination[0], []),
                                                                   raw_res.get(combination[1], []),
                                                                   combination[2])
            formatted_res.pop(combination[0], None)
            formatted_res.pop(combination[1], None)

        # write result
        self.writer.write_output_data(self.output_filename, formatted_res)

    def read_file(self, filename):
        res = defaultdict(list)
        _, name = os.path.split(filename)
        try:
            with open(filename, 'r') as f_obj:
                reader = csv.DictReader(f_obj)
                for line in reader:
                    for key, value in line.items():
                        res[key].append(value)
                    res[self.FILES_HEADER].append(name)
            return res
        except (OSError, csv.Error) as exc:
            print(f'File {filename} reading error: {str(exc)}')
        finally:
            return res
