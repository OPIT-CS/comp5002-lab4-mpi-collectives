# lab4_pi_integration.py
from mpi4py import MPI
import math
import time

def f(x):
    """Function to integrate: 4 / (1 + x*x)."""
    return 4.0 / (1.0 + x * x)

def compute_local_integral(local_n, local_a, h):
    """
    Trapezoidal-rule integral over this rank's sub-interval.

    Parameters
    ----------
    local_n : int
        Number of trapezoids handled by this rank.
    local_a : float
        Start of this rank's sub-interval.
    h : float
        Width of each trapezoid.
    """
    # --- TODO: Task 3 — Implement the trapezoidal rule locally ---
    # local_b = local_a + local_n * h
    # integral = (f(local_a) + f(local_b)) / 2.0
    # for i in range(1, local_n):
    #     integral += f(local_a + i * h)
    # return integral * h
    # --- End TODO ---
    return 0.0  # Placeholder so the starter runs; replace with the code above.

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Interval [a, b]
    a = 0.0
    b = 1.0

    # Total number of trapezoids (adjust for your machine)
    N = 10_000_000

    # --- Task 1 — Broadcast N ---
    if rank == 0:
        print(f"Broadcasting N = {N} to {size} processes...")
    n_total = comm.bcast(N if rank == 0 else None, root=0)

    # --- Task 2 — Determine local workload ---
    h = (b - a) / n_total
    intervals_per_process = n_total // size
    remainder = n_total % size

    # Distribute any remainder to lower ranks
    local_n = intervals_per_process + (1 if rank < remainder else 0)

    # Compute this rank's starting index then its local 'a'
    start_interval_index = rank * intervals_per_process + min(rank, remainder)
    local_a = a + start_interval_index * h
    # local_b = local_a + local_n * h  # Not required below, shown for clarity

    # Start timing after setup
    start_time = time.perf_counter()

    # --- Task 4 — Compute local integral ---
    local_integral = compute_local_integral(local_n, local_a, h)

    # --- Task 4/5 — Reduce partial sums to root ---
    global_integral_sum = comm.reduce(local_integral, op=MPI.SUM, root=0)

    end_time = time.perf_counter()

    # --- Task 5 — Print result on root ---
    if rank == 0:
        pi_approx = global_integral_sum
        error = abs(pi_approx - math.pi)
        total_time = end_time - start_time
        print("-" * 30)
        print(f"Pi approximation: {pi_approx:.15f}")
        print(f"Actual Pi:        {math.pi:.15f}")
        print(f"Error:            {error:.2e}")
        print(f"Execution time:   {total_time:.4f} seconds")
        print(f"Intervals:        {n_total}")
        print(f"Processes:        {size}")
        print("-" * 30)
