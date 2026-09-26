# Lab 4 Analysis

## Recorded results

Run with different process counts:

```bash
mpiexec -n P python lab4_pi_integration.py
```

| Processes (P) | Pi approximation | Absolute error | Execution time (s) |
| ---: | ---: | ---: | ---: |
| 1 | [enter value] | [enter value] | [enter time] |
| 2 | [enter value] | [enter value] | [enter time] |
| 4 | [enter value] | [enter value] | [enter time] |
| [optional] |  |  |  |

Also record:

- Python version:
- `mpi4py` version:
- MPI implementation/version:
- Number of intervals:
- Machine / CPU information if known:

## Analysis questions

1. **Collectives and synchronization**
   What is the purpose of `bcast`, `Barrier`, and `reduce` in this program? Why must all ranks call collective operations in a compatible order?

2. **Data distribution**
   Explain how the trapezoids are divided among ranks. How is the remainder handled, and why is this a block decomposition?

3. **Zero-work ranks**
   What should happen when the number of MPI ranks is greater than the number of trapezoids? Why must a rank with `local_n == 0` contribute `0.0`?

4. **`reduce` versus `allreduce`**
   What changes if `comm.allreduce` is used instead of `comm.reduce`? When would every rank need the global result?

5. **Timing methodology**
   Why does the program synchronize ranks immediately before the timed region, and why is `MPI.Wtime()` appropriate for elapsed-time measurements in an MPI program?

6. **Performance and scaling**
   How did runtime change with process count? Discuss computation, MPI startup, communication, reduction cost, and load balance.

7. **Floating-point reproducibility**
   Did the final digits change slightly with different process counts? Explain how a different summation/reduction order can change floating-point rounding while still producing a correct numerical result.
