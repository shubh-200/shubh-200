import os
import requests
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_state_qsphere
import matplotlib.pyplot as plt

def get_github_metrics(username):
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    # Uses GITHUB_TOKEN provided by Actions, or custom PAT if set locally
    token = os.getenv("GH_PAT") or os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
        
    # 1. Fetch public events for commits and streak estimation
    events_url = f"https://api.github.com/users/{username}/events/public"
    response = requests.get(events_url, headers=headers)
    commits_count = 0
    event_dates = set()
    
    if response.status_code == 200:
        events = response.json()
        for event in events:
            if event.get('type') == 'PushEvent':
                commits_count += len(event.get('payload', {}).get('commits', []))
                created_at = event.get('created_at')
                if created_at:
                    event_dates.add(created_at.split('T')[0])
                    
    streak = len(event_dates)

    # 2. Fetch Gists count
    gists_url = f"https://api.github.com/users/{username}/gists"
    gists_response = requests.get(gists_url, headers=headers)
    gists_count = len(gists_response.json()) if gists_response.status_code == 200 else 0

    return commits_count, streak, gists_count

def generate_quantum_state():
    username = "shubh-200"
    commits, streak, gists = get_github_metrics(username)
    
    # Map metrics to angle ranges [0, pi]
    theta_commits = min((commits / 30.0) * np.pi, np.pi)
    theta_streak = min((streak / 7.0) * np.pi, np.pi)
    theta_gists = min((gists / 10.0) * np.pi, np.pi)
    
    # Build 3-Qubit Circuit
    qc = QuantumCircuit(3)
    qc.ry(theta_commits, 0)
    qc.ry(theta_streak, 1)
    qc.ry(theta_gists, 2)
    
    # Entanglement
    qc.cx(0, 1)
    qc.cx(1, 2)
    
    # Generate statevector and plot
    state = Statevector.from_instruction(qc)
    fig = plot_state_qsphere(state)
    
    os.makedirs("assets", exist_ok=True)
    fig.savefig("assets/quantum_state.svg", format="svg", bbox_inches='tight', transparent=True)
    plt.close(fig)

if __name__ == "__main__":
    generate_quantum_state()