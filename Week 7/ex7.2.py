from euler_graph_job import MREulerGraph
from sys import stdin

files = [
    'graph1.txt',
    'graph2.txt',
    'graph3.txt',
    'graph4.txt',
    'graph5.txt',
]

for graph_file in files:
    mr_job = MREulerGraph([graph_file])
    
    with mr_job.make_runner() as runner:
        runner.run()
        euler_graph = True
        for line in runner.stream_output():
            key, value = mr_job.parse_output_line(line)
            if euler_graph:
                euler_graph = value
        if euler_graph:
            print(
                '{} is the representation of an Euler graph.'
                .format(graph_file)
            )
        else:
            print(
                '{} is not the representation of an Euler graph.'
                .format(graph_file)
            )
