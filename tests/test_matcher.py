from matcher.utils.parse_tsv import TsvIterator
import pandas as pd

def test_exact():
    tsv_iterator = TsvIterator('./tests/data/names.tsv', './tests/data/output_exact.tsv', 'Exact', 0.5)
    for comparison in tsv_iterator:
        pass
    df = pd.read_csv('./tests/data/output_exact.tsv', delimiter='\t',header=None, names=['PersonLabel','AliasLabel','Prediction','Score'])
    expected_pred = [True,False,False]
    assert (df.Prediction == expected_pred).all()



def test_jaccard():
    tsv_iterator = TsvIterator('./tests/data/names.tsv', './tests/data/output_exact.tsv', 'Jaccard', 0.5)
    for comparison in tsv_iterator:
        pass
    df = pd.read_csv('./tests/data/output_exact.tsv', delimiter='\t',header=None, names=['PersonLabel','AliasLabel','Prediction','Score'])
    expected_pred = [True,True,False]
    assert (df.Prediction == expected_pred).all()


def test_Levenshtein():
    tsv_iterator = TsvIterator('./tests/data/names.tsv', './tests/data/output_exact.tsv', 'Leven', 0.5)
    for comparison in tsv_iterator:
        pass
    df = pd.read_csv('./tests/data/output_exact.tsv', delimiter='\t',header=None, names=['PersonLabel','AliasLabel','Prediction','Score'])
    expected_pred = [True,True,False]
    assert (df.Prediction == expected_pred).all()


def test_nn():
    tsv_iterator = TsvIterator('./tests/data/names.tsv', './tests/data/output_exact.tsv', 'tfidf', 0.5)
    for comparison in tsv_iterator:
        pass
    df = pd.read_csv('./tests/data/output_exact.tsv', delimiter='\t',header=None, names=['PersonLabel','AliasLabel','Prediction','Score'])
    expected_pred = [True,True,False]
    assert (df.Prediction == expected_pred).all()