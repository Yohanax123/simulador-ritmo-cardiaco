# simulador_ecg_app.py
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import streamlit as st

def simular_ecg(fs, duracion, frecuencia_bpm):
    t = np.linspace(0, duracion, fs * duracion)
    ecg = 0.6 * np.sin(2 * np.pi * 1.3 * t) + 1.2 * np.sin(2 * np.pi * 1.0 * t)
    intervalo_rr = 60 / frecuencia_bpm
    pasos = int(intervalo_rr * fs)
    for r in range(0, len(t), pasos):
        if r + 1 < len(ecg):
            ecg[r] += 2.5
    return t, ecg

def detectar_picos(ecg, fs):
    peaks, _ = find_peaks(ecg, height=2)
    rr_intervals = np.diff(peaks) / fs
    fc = 60 / rr_intervals if len(rr_intervals) > 0 else []
    return peaks, rr_intervals, fc

st.title("🫀 Simulador de Ritmo Cardíaco")

st.markdown("Calcula la frecuencia cardíaca (FC) con la fórmula:  \nFC = 60 / intervalo RR (s)")

frecuencia_bpm = st.slider("Frecuencia cardíaca simulada (bpm)", 40, 180, 75)
fs = 500
duracion = 10

t, ecg = simular_ecg(fs, duracion, frecuencia_bpm)
peaks, rr_intervals, fc = detectar_picos(ecg, fs)

fig, ax = plt.subplots(figsize=(10, 3))
ax.plot(t, ecg, label="ECG Simulado")
ax.plot(t[peaks], ecg[peaks], 'ro', label="Picos R")
ax.set_xlabel("Tiempo (s)")
ax.set_ylabel("Amplitud")
ax.set_title("Señal ECG Simulada")
ax.legend()
ax.grid(True)
st.pyplot(fig)

if len(fc) > 0:
    promedio = np.mean(fc)
    st.write(f"❤️ Frecuencia cardíaca promedio: **{promedio:.1f} bpm**")
    if promedio < 60:
        st.warning("🟡 Bradicardia")
    elif promedio <= 100:
        st.success("✅ Ritmo normal")
    else:
        st.error("🔴 Taquicardia")
else:
    st.warning("No se detectaron suficientes picos R.")