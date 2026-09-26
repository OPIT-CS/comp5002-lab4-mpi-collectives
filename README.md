# COMP-5002 • Lab 4 Parallel Algorithm with MPI Collectives

**Module** Module 6. MPI Collective Communication and Algorithms  
**Objective** Implement a parallel numerical integration to estimate Pi using MPI collectives (`bcast`, `reduce`) for an efficient distributed computation.

## Prerequisites

- Python 3 installed.
- An MPI implementation installed, such as Open MPI or MPICH.
- `mpi4py` installed.
- Git basics: `clone`, `add`, `commit`, `push`.
- Concepts from Modules 5 and 6:
  - MPI environment (`COMM_WORLD`, rank, size).
  - Motivation for collective communication.
  - `comm.bcast` and `comm.reduce`.
  - Block data decomposition and remainder handling.

A common setup is to install an MPI implementation on the system and then run:

```bash
python -m pip install mpi4py
```

On supported platforms, `mpi4py` can also be installed together with an MPI runtime, for example:

```bash
python -m pip install mpi4py openmpi
# or
python -m pip install mpi4py mpich
```

## Background

We approximate Pi via the integral of `f(x) = 4 / (1 + x*x)` on `[0, 1]`.

Using the trapezoidal rule with `N` intervals of width `h = (b - a) / N`:

```
Integral ≈ h * [ (f(a)/2) + f(a+h) + ... + f(b-h) + (f(b)/2) ]
```

Each MPI rank receives a contiguous block of trapezoids, computes a local partial integral, and contributes that value to a reduction on rank 0.

## Files Provided

- `README.md` this file
- `lab4_pi_integration.py` starter with function skeletons and a `main` block
- `analysis.md` where you record results and answer the analysis questions

## Tasks

**General instructions**

- Clone your GitHub Classroom repository.
- Modify `lab4_pi_integration.py` to complete the TODOs.
- Run with multiple processes using `mpiexec` or `mpirun`.
- Keep all MPI collectives in the same order on every rank.
- Record results in `analysis.md`.
- Commit frequently and push before the deadline.

---

### Task 1 — Broadcast the interval count

Complete `broadcast_interval_count(comm, rank)`.

- Rank 0 starts with `DEFAULT_INTERVALS`.
- Other ranks start with `None`.
- Use `comm.bcast(..., root=0)` so every rank receives the same positive interval count.
- Return the broadcast value.

The supplied validation checks that the final value is a positive integer.

---

### Task 2 — Determine each rank's local workload

Complete `decompose_intervals(n_total, rank, size, a, b)`.

- Compute the global step width `h = (b - a) / n_total`.
- Divide the `n_total` trapezoids as evenly as possible.
- Give one additional trapezoid to each of the lowest-numbered ranks until the remainder is exhausted.
- Compute this rank's starting global interval index.
- Return `local_n`, `local_a`, and `h`.

The decomposition must also work when there are more ranks than trapezoids. In that case, some ranks legitimately receive `local_n == 0`.

---

### Task 3 — Implement local trapezoidal integration

Complete `compute_local_integral(local_n, local_a, h)`.

- If `local_n == 0`, return `0.0`.
- Otherwise compute `local_b = local_a + local_n * h`.
- Add the two endpoints with half weight.
- Sum the interior points.
- Multiply the final sum by `h`.
- Return the local partial integral.

Handling `local_n == 0` is required. A zero-work rank must not contribute a fictitious trapezoid.

---

### Task 4 — Reduce partial results

Complete `reduce_integrals(comm, local_integral)`.

- Use `comm.reduce(local_integral, op=MPI.SUM, root=0)`.
- Return the result.
- Remember that the reduced value is meaningful only on rank 0.

---

### Task 5 — Run and verify

The main program is already responsible for:

- synchronizing ranks with `comm.Barrier()` immediately before the timed region;
- timing with `MPI.Wtime()`;
- computing the local integral;
- reducing partial results;
- printing the final approximation only on rank 0.

Run, for example:

```bash
mpiexec -n 1 python lab4_pi_integration.py
mpiexec -n 2 python lab4_pi_integration.py
mpiexec -n 4 python lab4_pi_integration.py
```

For every run, verify that:

- the Pi approximation is close to `math.pi`;
- the program completes without deadlock;
- changing the process count does not materially change the mathematical result;
- the reported interval count remains constant.

A speedup is not guaranteed on every machine because MPI startup and collective communication also cost time.

---

### Task 6 — Record results and analyse

Record your runs in `analysis.md` and answer the questions about:

1. the roles of `bcast`, `Barrier`, and `reduce`;
2. block decomposition and remainder handling;
3. why `while size > n_total` is still a valid case when zero-work ranks are handled correctly;
4. `reduce` versus `allreduce`;
5. timing methodology with `MPI.Wtime()`;
6. compute, communication, and load-balance effects;
7. small floating-point differences caused by different reduction/summation orders.

---

## Submission

1. Ensure `lab4_pi_integration.py` runs correctly with multiple MPI process counts.
2. Ensure `analysis.md` includes recorded results and answers.
3. Stage: `git add lab4_pi_integration.py analysis.md` (or `git add .`)
4. Commit: `git commit -m "Complete Lab 4 Pi Integration"`
5. Push: `git push origin main` (or your default branch)
6. Verify on GitHub that `lab4_pi_integration.py` and `analysis.md` are updated.
