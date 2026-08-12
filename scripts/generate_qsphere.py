import os
import requests
import numpy as np
import matplotlib.pyplot as plt

# Matplotlib Dark Theme Configurations for GitHub Dark Mode
plt.style.use('dark_background')
plt.rcParams.update({
    'text.color': '#FFFFFF',
    'axes.labelcolor': '#00FFFF',
    'xtick.color': '#FFFFFF',
    'ytick.color': '#FFFFFF',
    'font.family': 'sans-serif',
    'font.weight': 'bold'
})

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_state_qsphere

def get_github_metrics(username):
    headers = {"Accept": "application/vnd.github.v3+json"}
    token = os.getenv("GH_PAT") or os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
        
    # 1. Fetch public events
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
    
    # Map metrics to rotation angles
    theta_commits = (commits / 20.0) * np.pi
    phi_streak = (streak / 7.0) * 2 * np.pi
    lam_gists = (gists / 5.0) * 2 * np.pi
    
    # Circuit Architecture for High Visual Complexity
    qc = QuantumCircuit(3)
    
    # Step 1: Create Superposition (Shows multiple state vector nodes)
    qc.h([0, 1, 2])
    
    # Step 2: Metric-driven Phase & State Rotations
    qc.rz(theta_commits, 0)
    qc.ry(phi_streak, 1)
    qc.rz(lam_gists, 2)
    
    # Step 3: Entanglement Bridge
    qc.cx(0, 1)
    qc.cx(1, 2)
    
    # Generate statevector
    state = Statevector.from_instruction(qc)
    
    # Plot Q-Sphere
    fig = plot_state_qsphere(state)
    
    # Customize Figure Aesthetic for Dark Mode
    fig.patch.set_facecolor('#0d1117') # GitHub Dark Mode Background match
    
    # Fix Font Colors for all text elements in the plot
    for ax in fig.axes:
        ax.set_facecolor('#0d1117')
        for text in ax.texts:
            text.set_color('#00FFFF') # Neon Cyan text for state labels & phase
            text.set_fontsize(12)
            text.set_weight('bold')
            
    # Add Clean Custom Title & Dynamic Metrics Overlay
    fig.suptitle("QUANTUM PROFILE STATE", fontsize=16, fontweight='bold', color='#00FFCC', y=0.98)
    fig.text(0.5, 0.02, f"Commits: {commits}  |  Streak: {streak}d  |  Gists: {gists}", 
             ha='center', fontsize=11, color='#8B949E', fontweight='bold')

    os.makedirs("assets", exist_ok=True)
    fig.savefig("assets/quantum_state.svg", format="svg", bbox_inches='tight', facecolor=fig.get_facecolor(), transparent=False)
    plt.close(fig)

if __name__ == "__main__":
    generate_quantum_state()