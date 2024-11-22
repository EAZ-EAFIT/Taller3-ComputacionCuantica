import numpy as np
import matplotlib.pyplot as plt
import sys


from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram

# Receive the 
def create_oracle(search_answers, n):
    oracle = QuantumCircuit(n)
    oracle.barrier(label='Oracle')
    for search_answer in search_answers:
        answer_list = []
        x = search_answer
        for i in range(n - 1):
            val = x % 2
            x = x // 2
            answer_list.append(val)

        # Create oracle
        answer_circuit = QuantumCircuit(n)

        for i in range(n - 1):
            if answer_list[i] == 0:
                answer_circuit.x(i)

        answer_circuit.mcx(control_qubits=list(range(n-1)), target_qubit=(n-1))

        for i in range(n-1):
            if answer_list[i] == 0:
                answer_circuit.x(i)
        
        answer_circuit.barrier()

        oracle.compose(answer_circuit, inplace=True)
    
    return oracle

def diffusion_circuit(n):
    # Diffusion operator
    diffusion = QuantumCircuit(n)
    diffusion.h(range(n - 1))
    diffusion.x(range(n - 1))
    diffusion.mcx(control_qubits=list(range(n-1)), target_qubit=(n-1))
    diffusion.x(range(n - 1))
    diffusion.h(range(n - 1))

    return diffusion

def grover_iteration(oracle, diffusion, n):
    # Create quantum circuit
    QC = QuantumCircuit(n , name='Grover Iteration')

    QC.compose(oracle, inplace=True)
    QC.compose(diffusion, inplace=True)

    return QC


def Grovers_algorithm(search_answers):

    # Define the number of qubits
    bits_search_answer = int(np.log2(max(search_answers))) + 1

    grover_iterations = int(np.floor((np.pi/4) * np.sqrt(2**bits_search_answer / len(search_answers))))

    n = bits_search_answer + 1

    oracle = create_oracle(search_answers, n)
    diffusion = diffusion_circuit(n)
    iteration = grover_iteration(oracle, diffusion, n)

    # Create quantum circuit
    QC = QuantumCircuit(n,n-1)
    QC.x(n-1)
    QC.barrier() 

    # Apply Hadamard gate
    QC.h(range(n))

    for i in range(grover_iterations):
        QC.compose(iteration, inplace=True)
        # QC.append(iteration.to_instruction(), range(n))


    QC.measure(range(n-1), range(n-1))

    return QC

def run_algorithm(QC):
    QC.draw('mpl', style={"barrier": False})
    backend = Aer.get_backend('qasm_simulator')
    job = backend.run(transpile(QC, backend), shots=1000)
    result = job.result()
    counts = result.get_counts(QC)
    plot_histogram(counts)
    plt.show()


def main():
    if len(sys.argv) == 1:
        print("Usage: python Grovers_algorithm.py <search_answer_1> <search_answer_2> ... <search_answer_n>")
        sys.exit(1)
    try:
        search_answers = list(set(int(arg) for arg in sys.argv[1:]))
    except ValueError:
        print("Invalid input. Please enter integers only.")
        sys.exit(1)

    QC = Grovers_algorithm(search_answers)
    run_algorithm(QC)

if __name__ == "__main__":
    main()