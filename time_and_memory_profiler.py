import time
import tracemalloc
import os

def profile_script(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    cell_start_indices = [i for i, line in enumerate(lines) if line.strip().startswith("# %%")]
    cell_start_indices.append(len(lines))  # Add end of file as the last index

    results = []
    for i in range(len(cell_start_indices) - 1):
        cell_start = cell_start_indices[i]
        cell_end = cell_start_indices[i + 1]
        cell_code = ''.join(lines[cell_start:cell_end])

        # Write the cell code to a temporary file
        temp_file = "temp_cell_execution.py"
        with open(temp_file, 'w') as temp_f:
            temp_f.write(cell_code)

        # Profile the cell execution
        tracemalloc.start()
        start_time = time.time()
        try:
            exec(open(temp_file).read(), globals())
        except Exception as e:
            results.append(f"Cell {i + 1} failed with error: {e}")
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Log the results
        results.append(
            f"Cell {i + 1}:\n"
            f"Execution Time: {end_time - start_time:.4f} seconds\n"
            f"Current Memory Usage: {current / 10**6:.4f} MB\n"
            f"Peak Memory Usage: {peak / 10**6:.4f} MB\n"
        )

        # Clean up the temporary file
        os.remove(temp_file)

    # Write the profiling results to the output file
    with open(output_file, 'w') as f:
        f.write("\n".join(results))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Profile execution time and memory usage of a script.")
    parser.add_argument("input_file", help="Path to the input Python script.")
    parser.add_argument("output_file", help="Path to the output text file for profiling results.")
    args = parser.parse_args()

    profile_script(args.input_file, args.output_file)

# python time_and_memory_profiler.py file_to_be_applied_to.py profiling_results.txt