# COMP-5002 • Lab 4 Parallel Algorithm with MPI Collectives (Numerical Integration)

**Module** Module 6. MPI Collective Communication and Algorithms  
**Objective** Implement a parallel numerical integration to estimate Pi using MPI collectives (`bcast`, `reduce`) for an efficient distributed computation.

## Prerequisites

- Python 3 installed.
- An MPI implementation installed (Open MPI or MPICH).
- `mpi4py` installed (`pip install mpi4py`).
- Git basics: `clone`, `add`, `commit`, `push`.
- Concepts from Modules 5 and 6:
  - MPI environment (`COMM_WORLD`, rank, size).
  - Motivation for collectives.
  - `comm.bcast` and `comm.reduce`.
  - Basic data decomposition strategies.

## Background

We approximate Pi via the integral of `f(x) = 4 / (1 + x*x)` on `[0, 1]`.
Using the trapezoidal rule with `N` intervals of width `h = (b - a)/N`:
```
Integral ≈ h * [ (f(a)/2) + f(a+h) + ... + f(b−h) + (f(b)/2) ].
```
Each process computes a partial sum over a sub-interval; a reduction combines all partials.

## Files Provided

- `README.md` this file
- `lab4_pi_integration.py` starter with function skeletons and a `main` block
- `analysis.md` where you record results and answers

## Tasks

**General instructions**

- Clone your GitHub Classroom repository.
- Modify `lab4_pi_integration.py` to complete the tasks.
- Run with multiple processes using `mpiexec` or `mpirun`.
- Record results in `analysis.md`.
- Commit frequently and push before the deadline.

---

### Task 1 — Broadcast integration parameters

- In `main`, define `N` only on rank 0.
- Broadcast `N` to all ranks with `comm.bcast` and store it (for example `n_total`).

### Task 2 — Determine local workload

- Compute `h = 1.0 / n_total`.
- Compute `local_n` for this rank by dividing intervals as evenly as possible; distribute any remainder to lower ranks.
- Compute `local_a` (start of this rank’s sub-interval) and `local_b` accordingly.

### Task 3 — Implement local integration

- Implement the trapezoidal rule in the provided local integration function:
  - Sum interior points `f(local_a + i*h)` for `i = 1..local_n-1`.
  - Add `(f(local_a) + f(local_b))/2`.
  - Multiply by `h`.
- Return the local partial integral.

### Task 4 — Reduce partial results

- Call your local integration.
- Use `comm.reduce(..., op=MPI.SUM, root=0)` to obtain the global integral on rank 0.

### Task 5 — Print final result on root

- On rank 0, print the Pi approximation, optional absolute error vs `math.pi`, total execution time, number of intervals, and process count.

### Task 6 — Run and record results

- Run with different process counts, for example:
  - `mpiexec -n 1 python lab4_pi_integration.py`
  - `mpiexec -n 4 python lab4_pi_integration.py`
- In `analysis.md`, record the Pi estimate and timing for each run.

### Task 7 — Analysis (`analysis.md`)

1. **Collectives used** Purpose of `bcast` and `reduce` in this algorithm.  
2. **Data distribution** How the interval was partitioned among ranks; what decomposition this resembles.  
3. **reduce vs allreduce** Behavioural difference and when `allreduce` might be preferred.  
4. **Performance** How runtime changed with more processes; discuss compute vs communication.

---

## Submission

1. Ensure `lab4_pi_integration.py` runs correctly with `mpiexec`.
2. Ensure `analysis.md` includes recorded results and answers.
3. Stage: `git add lab4_pi_integration.py analysis.md` (or `git add .`)
4. Commit: `git commit -m "Complete Lab 4 Pi Integration"`
5. Push: `git push origin main` (or your default branch)
6. Verify on GitHub that `lab4_pi_integration.py` and `analysis.md` are updated.
