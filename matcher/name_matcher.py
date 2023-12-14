import Levenshtein

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class NameMatchScorer:
    """Interface for scoring putative name matches"""
    def __init__(self, name1, name2, threshold=0.5, ngram_range=(1,4)):
        self.name1 = name1
        self.name2 = name2
        self.threshold = threshold
        self.ngram_range = ngram_range
    def __str__(self):
    # TODO - fill in (see our work from corpora.py for an example)
        return f"Cleaned Names:\n{self.name1}\nError Names:\n{self.name2}"
    def __repr__(self):
    # TODO - fill in (see our work from corpora.py for an example)
        return f"NameDataFrame(cleaned_names={self.name1}, error_names={self.name2})"
    def score(self, name1, name2):        
        pass

class Exact(NameMatchScorer):
    def score(self):
        if self.name1==self.name2:
            pred = True
        else:
            pred = False
        
        if self.name1==self.name2:
            similarity = 1
        else:
            similarity = 0
        # pred = [x == y for x, y in zip(self.name1, self.name2)]
        return pred, similarity
    
class Jaccard(NameMatchScorer):
    def score(self):
        similarity = len(set(self.name1) & set(self.name2)) / len(set(self.name1) | set(self.name2))
        if similarity >= self.threshold:
            pred = True
        else:
            pred = False
        return pred, similarity

class Leven(NameMatchScorer):
    def score(self):
        distance = Levenshtein.distance(self.name1,self.name2)
        similarity = 1 - (distance / max(len(self.name1), len(self.name2)))
        if similarity >= self.threshold:
            pred = True
        else:
            pred=False
        return pred, similarity


class tfidf(NameMatchScorer):
    def score(self):
        corpus = [self.name1,self.name2]
        if all(x > 0 for x in self.ngram_range):
            pass
        else:
            raise ValueError("Ngrams must be greater than 0")
        vectorizer = TfidfVectorizer(analyzer='char', ngram_range=self.ngram_range)
        tfidf_matrix = vectorizer.fit_transform(corpus)
        similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
        
        if similarity >= self.threshold:
            pred = True
        else:
            pred = False
        return pred, similarity


import spacy

class Bonus(NameMatchScorer):
    def score(self):

        # Load the spaCy model
        nlp = spacy.load("en_core_web_sm")

        # Example strings
        string1 = self.name1
        string2 = self.name2

        doc1 = nlp(string1)
        doc2 = nlp(string2)

        vec1 = doc1.vector
        vec2 = doc2.vector

        # Calculate cosine similarity manually
        def cosine_similarity(vec1, vec2):
            dot_product = sum(a * b for a, b in zip(vec1, vec2))
            magnitude1 = sum(a ** 2 for a in vec1) ** 0.5
            magnitude2 = sum(b ** 2 for b in vec2) ** 0.5
            similarity = dot_product / (magnitude1 * magnitude2)
            return similarity

        similarity = cosine_similarity(vec1, vec2)

        if similarity >= self.threshold:
            pred = True
        else:
            pred = False
        
        return pred, similarity

    

