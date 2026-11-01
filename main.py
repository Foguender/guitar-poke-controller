import numpy as np
import sounddevice as sd

# Configurações de áudio
SAMPLE_RATE = 44100  # Taxa de amostragem
DURATION = 0.2       # Duração de cada captura em segundos (quanto menor, mais rápido responde)

# Frequências aproximadas das notas padrão da guitarra (afinação padrão EADGBE)
# Cordas soltas: E2 (Baixo), A2, D3, G3, B3, E4 (Agudo)
NOTES = {
    "E2 (Mi grave)": 82.41,
    "A2 (Lá)": 110.00,
    "D3 (Ré)": 146.83,
    "G3 (Sol)": 196.00,
    "B3 (Si)": 246.94,
    "E4 (Mi agudo)": 329.63
}

def detect_note(freq):
    if freq < 50:
        return None
    # Encontra a nota mais próxima da frequência capturada
    closest_note = min(NOTES.keys(), key=lambda k: abs(NOTES[k] - freq))
    diff = abs(NOTES[closest_note] - freq)
    if diff < 5: # Tolerância de variação
        return closest_note
    return None

def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    # Pega o sinal de áudio e aplica Transformada de Fourier para achar a frequência principal
    audio_data = indata[:, 0]
    fft = np.fft.rfft(audio_data)
    fft_freqs = np.fft.rfftfreq(len(audio_data), 1 / SAMPLE_RATE)
    peak_freq = fft_freqs[np.argmax(np.abs(fft))]
    
    note = detect_note(peak_freq)
    if note:
        print(f"Nota detectada: {note} ({peak_freq:.2f} Hz)")

# Iniciando a escuta do microfone
print("Ouvindo a guitarra... Toque uma corda!")
with sd.InputStream(callback=audio_callback, channels=1, samplerate=SAMPLE_RATE, blocksize=2048):
    while True:
        sd.sleep(int(DURATION * 1000))
