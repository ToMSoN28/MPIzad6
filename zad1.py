import sys
import math
from mpi4py import MPI

def main(num_list):
    comm = MPI.COMM_WORLD
    id = comm.Get_rank()
    numProcesses = comm.Get_size()


    num_list = [int(x) for x in num_list]

    if len(num_list) != numProcesses:
        print("Number of processes have to be equal to length of numbers list")
        return 1
    
    num = num_list[id]

    for iter in range(0, int(math.log(numProcesses, 2))):
        shift = 2**iter
        send_to = (id + shift) % numProcesses
        recv_from = id - shift + numProcesses if id - shift < 0 else id - shift
        comm.send(num, dest = send_to)
        recv_val = comm.recv(source = recv_from)
        num = nwd(num, recv_val)
    print(f"{id}: {num}")

def nwd(a, b):
    if b > a:
        tmp = a
        a = b
        b = tmp
    while b != 0:
        c = b
        b = a % b
        a = c
    return a

if _name_ == "_main_":
    main(sys.argv[1:])