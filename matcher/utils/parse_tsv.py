import abc
import csv
import collections.abc
import dataclasses
from matcher.name_matcher import NameMatchScorer
from matcher.eval.eval import evaluate
from matcher.name_matcher import Jaccard
from matcher.name_matcher import Exact
from matcher.name_matcher import Leven
from matcher.name_matcher import tfidf
from matcher.name_matcher import Bonus

@dataclasses.dataclass
class Comparison:
    """Class representing two names and their similarity"""
    name1: str
    name2: str
    pred: bool
    score: float = 0.0

class DocIterator(abc.ABC, collections.abc.Iterator):
    def __str__(self):
        return self.__class__.__name__

class TsvIterator(DocIterator):
    """Iterator to iterate over tsv-formatted documents"""
    def __init__(self, input_path, output_path, method, threshold):
        self.output_path = output_path
        self.input_path = input_path
        self.method = method
        self.threshold = threshold

        self.fp = open(self.input_path,encoding='utf-8')
        self.reader = csv.reader(self.fp, delimiter='\t')
        next(self.reader) # skip first row
        self.output_file = open(self.output_path, 'w', newline='',encoding='utf-8')

    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            row = next(self.reader)
            pred, score = eval(f"{self.method}(row[0], row[1],{self.threshold}).score()")
            comparison = Comparison(row[0], row[1], pred, score)

            self.write_comparison_to_output(comparison)

            # return Comparison(row[0], row[1], NameMatchScorer(row[0], row[1]))
            return comparison
        except StopIteration:
            self.fp.close()
            self.output_file.close()
            raise StopIteration
    # def write_comparison_to_output(self, comparison):
    #     with open(self.output_path, 'a', newline='') as output_file:
    #         writer = csv.writer(output_file, delimiter='\t')
    #         writer.writerow([comparison.name1, comparison.name2, comparison.score])
    
    def write_comparison_to_output(self, comparison):
        writer = csv.writer(self.output_file, delimiter='\t')
        writer.writerow([comparison.name1, comparison.name2, comparison.pred, comparison.score])