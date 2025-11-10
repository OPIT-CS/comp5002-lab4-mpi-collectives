# comp5002-lab4-mpi-collectives
Implement a distributed Pi estimator with mpi4py collectives. Broadcast N, partition intervals per rank, compute local trapezoid sums, and reduce to a global result. Run with mpiexec for multiple process counts, record timings, and answer analysis on bcast vs reduce/allreduce and workload decomposition.
