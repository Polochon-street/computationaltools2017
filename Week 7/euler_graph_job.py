from mrjob.job import MRJob
from collections import Counter


# Separate file for the MrEulerGraph class
class MREulerGraph(MRJob):
    # Map step
    def mapper(self, key, line):
        # Each line is "node1, node2" so make it a list like [node1, node2]
        nodes = list(map(int, line.split()))
        # Add 1 to each edge that appears
        yield nodes[0], 1
        yield nodes[1], 1

    def reducer(self, key, values):
        # For each node, return True if the sum of its edges is even,
        # and False if it's odd
        yield key, (sum(values) % 2) == 0
