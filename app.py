import streamlit as st
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, plot_bloch_multivector, plot_state_qsphere
from qiskit_aer import AerSimulator
# PAGE CONFIGURATION
st.set_page_config(page_title="Quantum Circuit Designer & Simulator",page_icon="⚛️",layout="wide")
# TITLE
st.title("⚛️ Quantum Circuit Designer and Simulator")
st.markdown("""Design, visualize and simulate fundamental quantum circuits using **Qiskit**.The application supports single-qubit and multi-qubit gates,quantum state visualization, measurement outcomes and probability analysis.""")
# CIRCUIT BUILDERS
def create_circuit(circuit_name, theta=3.14159 / 2):
    if circuit_name == "Identity":
        qc = QuantumCircuit(1)
        qc.id(0)
    elif circuit_name == "Pauli-X":
        qc = QuantumCircuit(1)
        qc.x(0)
    elif circuit_name == "Pauli-Y":
        qc = QuantumCircuit(1)
        qc.y(0)
    elif circuit_name == "Pauli-Z":
        qc = QuantumCircuit(1)
        qc.z(0)
    elif circuit_name == "Hadamard":
        qc = QuantumCircuit(1)
        qc.h(0)
    elif circuit_name == "Phase-S":
        qc = QuantumCircuit(1)
        qc.s(0)
    elif circuit_name == "Phase-T":
        qc = QuantumCircuit(1)
        qc.t(0)
    elif circuit_name == "Rx":
        qc = QuantumCircuit(1)
        qc.rx(theta, 0)
    elif circuit_name == "Ry":
        qc = QuantumCircuit(1)
        qc.ry(theta, 0)
    elif circuit_name == "Rz":
        qc = QuantumCircuit(1)
        qc.rz(theta, 0)
    elif circuit_name == "Measurement":
        qc = QuantumCircuit(1, 1)
        qc.h(0)
        qc.measure(0, 0)
    elif circuit_name == "CNOT":
        qc = QuantumCircuit(2)
        qc.cx(0, 1)
    elif circuit_name == "CZ":
        qc = QuantumCircuit(2)
        qc.cz(0, 1)
    elif circuit_name == "SWAP":
        qc = QuantumCircuit(2)
        qc.x(0)
        qc.swap(0, 1)
    elif circuit_name == "Toffoli":
        qc = QuantumCircuit(3)
        qc.x(0)
        qc.x(1)
        qc.ccx(0, 1, 2)
    elif circuit_name == "Bell State":
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
    elif circuit_name == "GHZ State":
        qc = QuantumCircuit(3)
        qc.h(0)
        qc.cx(0, 1)
        qc.cx(0, 2)
    else:
        qc = QuantumCircuit(1)
    return qc
# SIMULATION
def simulate_circuit(qc, shots):
    statevector_circuit = qc.remove_final_measurements(inplace=False)
    state = Statevector.from_instruction(statevector_circuit)
    measured_circuit = qc.copy()
    if measured_circuit.num_clbits == 0:
        measured_circuit.measure_all()
    simulator = AerSimulator()
    result = simulator.run(measured_circuit,shots=shots,seed_simulator=42).result()
    counts = result.get_counts()
    return state, counts
# SIDEBAR
st.sidebar.header("Circuit Controls")
circuit_options = ["Identity","Pauli-X","Pauli-Y","Pauli-Z","Hadamard","Phase-S","Phase-T","Rx","Ry","Rz","Measurement","CNOT","CZ","SWAP","Toffoli","Bell State","GHZ State"]

selected_circuit = st.sidebar.selectbox("Select Quantum Circuit",circuit_options)
theta = 3.14159 / 2
if selected_circuit in ["Rx", "Ry", "Rz"]:
    theta = st.sidebar.slider("Rotation Angle θ",min_value=0.0,max_value=6.28318,value=3.14159 / 2,step=0.1)
shots = st.sidebar.slider("Number of Shots",min_value=100,max_value=5000,value=1024,step=100)
# CREATE CIRCUIT
qc = create_circuit(selected_circuit,theta)
# DISPLAY CIRCUIT
st.header("1. Quantum Circuit")
st.code(qc.draw("text"),language="text")
# SIMULATION
state, counts = simulate_circuit(qc,shots)
# STATEVECTOR
st.header("2. Quantum State")
st.write("Statevector:")
st.code(str(state),language="text")
# PROBABILITIES
st.header("3. State Probabilities")
probabilities = state.probabilities_dict()
probability_data = {str(state_label): float(probability)for state_label, probability in probabilities.items()}
st.json(probability_data)
# MEASUREMENT RESULTS
st.header("4. Measurement Results")
st.write(f"Total shots: {shots}")
st.write(counts)
# HISTOGRAM
st.header("5. Measurement Histogram")
fig, ax = plt.subplots()
labels = list(counts.keys())
values = list(counts.values())
ax.bar(labels, values)
ax.set_xlabel("Measured State")
ax.set_ylabel("Number of Measurements")
ax.set_title(f"{selected_circuit} - Measurement Results")
st.pyplot(fig)
plt.close(fig)
# STATE VISUALIZATION
st.header("6. Quantum State Visualization")
if state.num_qubits == 1:
    fig = plot_bloch_multivector(state)
    st.pyplot(fig)
    plt.close(fig)
else:
    st.write("Q-sphere representation:")
    fig = plot_state_qsphere(state)
    st.pyplot(fig)
    plt.close(fig)
# CIRCUIT INFORMATION
st.header("7. Circuit Information")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Number of Qubits",qc.num_qubits)
with col2:
    st.metric("Circuit Depth",qc.depth())
with col3:
    st.metric("Number of Gates",sum(qc.count_ops().values()))
st.subheader("Gate Count")
st.write(qc.count_ops())
# THEORETICAL INFORMATION
st.header("8. Theoretical Result")
theoretical_results = {"Identity":"The qubit remains in |0⟩.",
    "Pauli-X":
        "The state changes from |0⟩ to |1⟩.",
    "Pauli-Y":
        "The state changes from |0⟩ to i|1⟩.",
    "Pauli-Z":
        "The |0⟩ state remains unchanged while |1⟩ receives a phase flip.",
    "Hadamard":
        "Creates an equal superposition: (|0⟩ + |1⟩)/√2.",
    "Phase-S":
        "Applies a phase shift of π/2 to the |1⟩ component.",
    "Phase-T":
        "Applies a phase shift of π/4 to the |1⟩ component.",

    "Rx":
        "Rotates the qubit state around the X-axis.",
    "Ry":
        "Rotates the qubit state around the Y-axis.",
    "Rz":
        "Rotates the qubit state around the Z-axis.",
    "Measurement":
        "Measurement converts a quantum state into a classical result.",
    "CNOT":
        "Flips the target qubit when the control qubit is |1⟩.",
    "CZ":
        "Applies a phase flip when both qubits are |1⟩.",
    "SWAP":
        "Exchanges the states of two qubits.",
    "Toffoli":
        "Flips the target qubit when both control qubits are |1⟩.",
    "Bell State":
        "Creates an entangled two-qubit state: (|00⟩ + |11⟩)/√2.",
    "GHZ State":
        "Creates a three-qubit entangled state: (|000⟩ + |111⟩)/√2."
}
st.info(theoretical_results[selected_circuit])
# FOOTER
st.markdown("---")
st.markdown(
    """
    **Quantum Circuit Designer and Simulator**

    Developed using Python, Qiskit, NumPy, Matplotlib and Streamlit.
    """
)
