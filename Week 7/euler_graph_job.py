from mrjob.job import MRJob
from collections import Counter


class MREulerGraph(MRJob):
    def mapper(self, key, line):
        nodes = list(map(int, line.split()))
        yield nodes[0], 1
        yield nodes[1], 1

    def reducer(self, key, values):
        yield key, (sum(values) % 2) == 0

if __name__ == '__main__':
    MREulerGraph.run()
