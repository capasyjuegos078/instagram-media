import time
import os
import subprocess
import requests

# Carpeta que vamos a vigilar
folder = r"C:\Instagram_Agente\github_upload"

# Datos de tu cuenta
ACCESS_TOKEN = "EAAXgs99IiLIBSX1mVZBhZBZC53eKgUrb6GthshKoFOkiZBEF1iZANB2r77rr9LUS1DWzJZAZBQ4MUpIQhfceP9o8klUKPYpakjRv5jXcjnBcoc1uyzTwYcx9KHpb2k3z5nYbZBzsXdZC5EAXZCJbJFBXRXAcFPug6ODnhB00pbwopAM1e4zSEinjfZADjM2JhQO"
INSTAGRAM_ID = "17841431606006568"

def git_push():
    try:
        subprocess.run(["git", "add", "."], cwd=folder, check=True)
        subprocess.run(["git", "commit", "-m", "Auto subida"], cwd=folder, check=True)
        subprocess.run(["git", "push"], cwd=folder, check=True)
        print("✅ Cambios subidos a GitHub")
    except subprocess.CalledProcessError:
        print("⚠️ No había cambios nuevos para subir")

def publicar_en_instagram(nombre_archivo, titulo, hashtags):
    # Usamos el raw URL de GitHub como image_url
    image_url = f"https://raw.githubusercontent.com/capasyjuegos078/instagram-media/main/{nombre_archivo}"
    caption = f"{titulo}\n\n{hashtags}"
    url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_ID}/media"
    data = {
        "image_url": image_url,
        "caption": caption,
        "access_token": ACCESS_TOKEN
    }
    r = requests.post(url, data=data)
    print("📲 Respuesta Instagram:", r.json())

# Estado inicial de la carpeta
before = set(os.listdir(folder))

print("👀 Watcher iniciado, vigilando carpeta:", folder)

while True:
    time.sleep(5)  # cada 5 segundos revisa
    after = set(os.listdir(folder))
    nuevos = after - before
    if nuevos:
        print("📂 Cambio detectado:", nuevos)
        git_push()
        # Publicar cada archivo nuevo en Instagram
        for archivo in nuevos:
            if archivo.lower().endswith((".jpg", ".png", ".jpeg")):
                publicar_en_instagram(
                    archivo,
                    titulo="✨ Nuevo contenido ✨",
                    hashtags="#anime #3Dart #LoL #CapasYJuegos"
                )
        before = after
