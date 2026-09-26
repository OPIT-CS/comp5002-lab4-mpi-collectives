# lab4_pi_integration.py
import math

from mpi4py import MPI

DEFAULT_INTERVALS = 10_000_000
A = 0.0
B = 1.0


def f(x):
    """Function to integrate: 4 / (1 + x*x)."""
    return 4.0 / (1.0 + x * x)


def validate_interval_count(n_total):
    """Require a positive integer number of integration intervals."""
    if isinstance(n_total, bool) or not isinstance(n_total, int) or n_total <= 0:
        raise ValueError("The number of intervals must be a positive integer")


def broadcast_interval_count(comm, rank):
    """Broadcast the total interval count from rank 0 to every rank."""
    n_total = DEFAULT_INTERVALS if rank == 0 else None

    # --- TODO: Task 1 - Broadcast n_total from rank 0 and return it ---
    # All ranks must participate in the same collective call.
    # --- End TODO ---
    raise NotImplementedError("Complete Task 1: broadcast_interval_count")


def decompose_intervals(n_total, rank, size, a=A, b=B):
    """Return (local_n, local_a, h) for this rank's contiguous block."""
    # --- TODO: Task 2 - Compute this rank's block decomposition ---
    # Compute h, the even base workload, remainder distribution, this
    # rank's starting interval index, and local_a. Return local_n, local_a, h.
    # --- End TODO ---
    raise NotImplementedError("Complete Task 2: decompose_intervals")


def compute_local_integral(local_n, local_a, h):
    """Compute this rank's trapezoidal-rule partial integral."""
    # --- TODO: Task 3 - Implement the local trapezoidal rule ---
    # Handle zero-work ranks, then apply the trapezoidal rule over this
    # rank's contiguous sub-interval and return the partial integral.
    # --- End TODO ---
    raise NotImplementedError("Complete Task 3: compute_local_integral")


def reduce_integrals(comm, local_integral):
    """Sum all local partial integrals on rank 0."""
    # --- TODO: Task 4 - Reduce all local values with MPI.SUM to rank 0 ---
    # --- End TODO ---
    raise NotImplementedError("Complete Task 4: reduce_integrals")


def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    n_total = broadcast_interval_count(comm, rank)
    validate_interval_count(n_total)

    local_n, local_a, h = decompose_intervals(
        n_total, rank, size, A, B
    )

    # Synchronize immediately before timing so ranks start the measured
    # computation from the same phase of the program.
    comm.Barrier()
    start_time = MPI.Wtime()

    local_integral = compute_local_integral(local_n, local_a, h)
    global_integral = reduce_integrals(comm, local_integral)

    end_time = MPI.Wtime()

    if rank == 0:
        error = abs(global_integral - math.pi)
        print("-" * 40)
        print(f"Pi approximation: {global_integral:.15f}")
        print(f"Actual Pi:        {math.pi:.15f}")
        print(f"Error:            {error:.2e}")
        print(f"Execution time:   {end_time - start_time:.4f} seconds")
        print(f"Intervals:        {n_total}")
        print(f"Processes:        {size}")
        print("-" * 40)


if __name__ == "__main__":
    main()
