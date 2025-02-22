import requests
import io
import scipy.io.wavfile as wav

# L'URL de ton API FastAPI
url = "http://local-test-llm.dmcug9ccc4gddtgw.eastus.azurecontainer.io/predit/"

# Le message à passer au modèle
message = """
  eye wòkatã dzɔme woŋlɔlɔ̃ be wòhã gbɔna. Nà wòeɖo wo dɔwɔ, gake football nyuie kple dɔwɔ ƒe afɔ kple ame,   mɔ na wòkplɔ dzɔdzɔ kple nudɔlawo.
    Football ɖe afɔme ne wòhã dɔwɔ kple ame aɖe me, wòkatã gbe nyuiwo, wòɖɔ ɖekawɔ nu.
"""

# Envoi de la requête POST avec le message
response = requests.post(url, params={"message": message})

# Vérification si la requête a réussi
if response.status_code == 200:
    # Récupérer le contenu audio de la réponse
   
    audio_data = response.content
    #audio_io = io.BytesIO(audio_data)
    with open('out.wav', 'wb') as f:
        f.write(audio_data)

    
else:
    print(f"Erreur dans la requête : {response.status_code}")
