from mpi4py import MPI
import sys
import math

def nwd(a, b):
    if b > 0:
        return nwd(b, a%b)
    return a

def main(num_list):
    comm = MPI.COMM_WORLD
    id = comm.Get_rank()
    numProcesses = comm.Get_size()

    iteration = 0
    max_iteration = math.log(numProcesses,2)
    holding_number = int(num_list[id])
    # while iteration <= max_iteration:
    while (id+1)%(2**iteration) == 0:
            # print("I 'm process: ", id, " of: ", numProcesses)
        # holding_number = int(num_list[id])
            # print("I 'm process: ", id, " I send to: ", ((id+1)%numProcesses))
        if iteration == max_iteration:
            break
        comm.send(holding_number, dest=((id+(2**iteration))%numProcesses))
        nwd_previous_process = comm.recv(source=(id-(2**iteration))%numProcesses)
        holding_number = nwd(holding_number, nwd_previous_process)
        # print("I 'm process: ", id, " actual NWD is: ", holding_number)
        iteration += 1
    if id+1 == numProcesses:
        print("NWD", num_list, " = ", holding_number)

if __name__ == "__main__":
    main(sys.argv[1:])
