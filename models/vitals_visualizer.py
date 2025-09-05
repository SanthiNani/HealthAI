# models/vitals_visualizer.py

import matplotlib.pyplot as plt
import os
from datetime import datetime

def generate_vital_chart(patient_id, data, output_path='static/plots/vitals_plot.png'):
    patient = data.get(patient_id)
    if not patient:
        return None, None

    visits = patient.get("visits", [])
    if not visits:
        return None, None

    timestamps = []
    heart_rates = []
    blood_pressures = []
    blood_sugars = []
    oxygen_saturations = []
    health_scores = []

    for visit in visits:
        try:
            dt = datetime.fromisoformat(visit["timestamp"])
            timestamps.append(dt.strftime("%Y-%m-%d"))
            vitals = visit.get("vitals", {})
            heart_rates.append(vitals.get("heart_rate", 0))
            blood_pressures.append(vitals.get("blood_pressure", 0))
            blood_sugars.append(vitals.get("blood_sugar", 0))
            oxygen_saturations.append(vitals.get("oxygen_saturation", 0))
            health_scores.append(visit.get("health_score", 0))
        except Exception as e:
            print("Error parsing visit:", e)
            continue

    # Create subplots
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(f'Health Vitals Over Time - {patient_id}', fontsize=16)

    axs[0, 0].plot(timestamps, heart_rates, marker='o', label='Heart Rate')
    axs[0, 0].set_title('Heart Rate')
    axs[0, 0].set_ylabel('BPM')

    axs[0, 1].plot(timestamps, blood_pressures, marker='o', color='r', label='Blood Pressure')
    axs[0, 1].set_title('Blood Pressure')
    axs[0, 1].set_ylabel('mmHg')

    axs[1, 0].plot(timestamps, blood_sugars, marker='o', color='g', label='Blood Sugar')
    axs[1, 0].set_title('Blood Sugar')
    axs[1, 0].set_ylabel('mg/dL')

    axs[1, 1].plot(timestamps, oxygen_saturations, marker='o', color='purple', label='Oxygen Saturation')
    axs[1, 1].set_title('Oxygen Saturation')
    axs[1, 1].set_ylabel('%')

    for ax in axs.flat:
        ax.set_xlabel('Date')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True)

    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()

    # Separate plot for Health Score Trend
    score_path = output_path.replace("vitals_plot.png", "score_plot.png")
    plt.figure(figsize=(8, 4))
    plt.plot(timestamps, health_scores, marker='o', linestyle='-', color='darkorange')
    plt.title('Health Score Trend')
    plt.xlabel('Date')
    plt.ylabel('Score')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(score_path)
    plt.close()

    return output_path, score_path
