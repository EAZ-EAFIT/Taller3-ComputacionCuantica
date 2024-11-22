"""
    Taller 3 Computación Cuantica, Algoritmo de Grover
    Esteban Alvarez Zuluaga
"""

import numpy as np
import matplotlib.pyplot as plt
import sys

from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram

# Receive the search answers as a list of integers, the number of qubits n, and create the oracle function
def create_oracle(search_answers, n):

    oracle = QuantumCircuit(n)
    oracle.barrier(label='Oracle')

    # Iterate over the search answers and check for each one
    for search_answer in search_answers:
        answer_list = []

        # Convert the search answer to a binary format for the qubits
        for i in range(n - 1):
            val = search_answer % 2
            search_answer = search_answer // 2
            answer_list.append(val)


        answer_circuit = QuantumCircuit(n)

        # Apply X gate to the qubits that are 0 in the binary representation of the search answer
        for i in range(n - 1):
            if answer_list[i] == 0:
                answer_circuit.x(i)

        # Apply the multi-controlled X gate
        answer_circuit.mcx(control_qubits=list(range(n-1)), target_qubit=(n-1))

        # Reverse the changes made to the qubits
        for i in range(n-1):
            if answer_list[i] == 0:
                answer_circuit.x(i)
        
        answer_circuit.barrier()

        oracle.compose(answer_circuit, inplace=True)
    
    return oracle

# Create the diffusion operator for n qubits
def diffusion_circuit(n):
    
    diffusion = QuantumCircuit(n)

    # Apply Hadamard gate to all qubits
    diffusion.h(range(n - 1))

    # Apply X gate to all qubits and then the multi-controlled X gate
    diffusion.x(range(n - 1))
    diffusion.mcx(control_qubits=list(range(n-1)), target_qubit=(n-1))
    diffusion.x(range(n - 1))

    # Apply Hadamard gate to all qubits
    diffusion.h(range(n - 1))

    return diffusion

# Create the Grover's iteration circuit
def grover_iteration(oracle, diffusion, n):
    # Create quantum circuit and compose the oracle and diffusion operators
    QC = QuantumCircuit(n , name='Grover Iteration')

    QC.compose(oracle, inplace=True)
    QC.compose(diffusion, inplace=True)

    return QC

# Create the Grover's algorithm circuit
# Receive the search answers as a list of integers
def Grovers_algorithm(search_answers):

    # Define the number of qubits based on the number of bits in the search answers
    bits_search_answer = int(np.log2(max(search_answers))) + 1

    # Get a good approximation for the number of iterations for Grover's algorithm
    grover_iterations = int(np.floor((np.pi/4) * np.sqrt(2**bits_search_answer / len(search_answers))))

    # Define the number of qubits
    n = bits_search_answer + 1

    # Create the oracle and diffusion operators
    oracle = create_oracle(search_answers, n)
    diffusion = diffusion_circuit(n)

    # Create the Grover's iteration circuit
    iteration = grover_iteration(oracle, diffusion, n)

    # Create quantum circuit and negate the ancilla qubit
    QC = QuantumCircuit(n,n-1)

    QC.x(n-1)
    QC.barrier() 

    # Apply Hadamard gate
    QC.h(range(n))

    # Apply Grover's iterations
    for i in range(grover_iterations):
        QC.compose(iteration, inplace=True)

    # Measure all qubits except the ancilla qubit
    QC.measure(range(n-1), range(n-1))

    return QC

# Function to simulate the quantum circuit and plot the results
def run_algorithm(QC):

    # Get the simulator backend
    backend = Aer.get_backend('qasm_simulator')

    # Transpile and run the quantum circuit
    job = backend.run(transpile(QC, backend), shots=1000)
    result = job.result()

    # Plot the results
    counts = result.get_counts(QC)
    plot_histogram(counts)

    # Draw the quantum circuit
    QC.draw('mpl')

    plt.show()

# Main function that receives the search answers as arguments and runs  Grover's algorithm
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