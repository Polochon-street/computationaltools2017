from euler_graph_job import MREulerGraph

# List of the test file
files = [
    'graph1.txt',
    'graph2.txt',
    'graph3.txt',
    'graph4.txt',
    'graph5.txt',
]

# Test the code for each file
for graph_file in files:
    # Create the job
    mr_job = MREulerGraph([graph_file])

    # Use a with structure to automatically destroy the runner when finished
    with mr_job.make_runner() as runner:
        # Run the job
        runner.run()
        euler_graph = True
        # Parse each output line after having ran MapReduce
        for line in runner.stream_output():
            # Check if one of the value is false; if it is
            # then it's not an Euler graph
            _, value = mr_job.parse_output_line(line)
            if euler_graph:
                euler_graph = value
        # Print final output 
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
