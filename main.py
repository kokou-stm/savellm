from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from transformers import VitsModel, AutoTokenizer
import torch
import scipy.io.wavfile
from io import BytesIO
import numpy as np

import os, mimetypes
from fastapi.responses  import FileResponse

# Détecter le GPU si disponible
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Charger le modèle et le tokenizer
checkpoint = "facebook/mms-tts-ewe"
model = VitsModel.from_pretrained(checkpoint).to(device)  # Déplacer sur GPU si dispo
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

# Initialiser FastAPI
app = FastAPI()

@app.get('/')
def first():
    return {"Hello": "tts"}

@app.post('/predict/')
def predict(message: str):
    input_data = tokenizer(message, return_tensors="pt").to(device)  # Déplacer sur GPU si dispo

    with torch.no_grad():
        output = model(**input_data).waveform

    audio_np = output.squeeze(0).cpu().numpy()

    wav_io = BytesIO()
    scipy.io.wavfile.write(wav_io, rate=model.config.sampling_rate, data=(audio_np * 32767).astype(np.int16))
    wav_io.seek(0)  # Rewind pour la lecture
    
    return StreamingResponse(wav_io, media_type="audio/wav")



# Prédiction et génération de l'audio
@app.post('/test/')
def predict(message: str):
    # Répertoire pour stocker les fichiers audio générés (optionnel)
    audio_folder = "generated_audio"
    os.makedirs(audio_folder, exist_ok=True)

    output = ""
    input = tokenizer(message, return_tensors="pt")
    with torch.no_grad():
        output = model(**input).waveform
    audio_np = output.squeeze(0).cpu().numpy()
    
    # Enregistrer le fichier audio dans la mémoire
    wav_io = BytesIO()
    scipy.io.wavfile.write(wav_io, rate=model.config.sampling_rate, data=(audio_np * 32767).astype(np.int16))
    wav_io.seek(0)  # Rewind pour la lecture
    
    # Sauvegarder le fichier audio généré dans le dossier
    audio_file_path = os.path.join(audio_folder, f"generated_audio{message[:3]}.wav")
    '''with open(audio_file_path, 'wb') as f:
        f.write(wav_io.read())'''
    mime_type, _ = mimetypes.guess_type(audio_file_path)
    # Retourner l'URL du fichier audio généré
    audio_url = f"/audio/{os.path.basename(audio_file_path)}"
    print("Chemin: ", audio_file_path)
    return FileResponse(audio_file_path,  media_type="audio/wav")





