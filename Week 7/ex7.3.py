from mrjob.job import MRJob
from collections import Counter


class MRCountGraph(MRJob):
    # Map step
    def mapper(self, key, line):
        # Each line is "node1, node2" so make it a list like [node1, node2]
        nodes = list(map(int, line.split()))
        # Add 1 to each edge that appears
        yield nodes[0], 1
        yield nodes[1], 1

    def reducer(self, key, values):
        # For each node, sum the number of edges it's linked to
        yield key, sum(values) 

if __name__ == '__main__':
    MRCountGraph.run()
