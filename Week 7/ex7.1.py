from string import punctuation
from mrjob.job import MRJob
from collections import Counter

exclude = set(punctuation)

class MRWordFrequencyCount(MRJob):
    def mapper(self, key, line):
        words = ''.join(char for char in line if char not in exclude).split()
        for word, count in dict(Counter(words)).items():
            yield word, count 

    def reducer(self, key, values):
        yield key, sum(values)

if __name__ == '__main__':
    MRWordFrequencyCount.run()
