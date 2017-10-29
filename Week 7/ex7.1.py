from string import punctuation
from mrjob.job import MRJob
from collections import Counter

# A set of punctuation characters to delete from each line
exclude = set(punctuation)


# Define the basic MRJob class
class MRWordFrequencyCount(MRJob):
    # Mapper step for each line of the file
    def mapper(self, key, line):
        # Deleting non-alpha characters from the line
        words = ''.join(char for char in line if char not in exclude).split()
        # Count the occurrences of each word in the line and iterate over them
        for word, count in dict(Counter(words)).items():
            # "Return" for each word the associated count
            yield word, count 

    def reducer(self, key, values):
        # Return for each word the sum of occurrences in each line
        yield key, sum(values)

if __name__ == '__main__':
    MRWordFrequencyCount.run()
