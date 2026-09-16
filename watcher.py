import time
import os
import subprocess
import requests

# Carpeta que vamos a vigilar
folder = r"C:\Instagram_Agente\github_upload"

# Datos de tu cuenta
ACCESS_TOKEN = "EAAXgs99IiLIBSb9KtCJeLSKZAschcJ1TrpSUn0oG7j4RrBCUQfauasXSkiG4bzFewPBYGLOcuiyZCSc1trFOG2tDoeNI4txUHOsuxUIJcR2L6xYKsuJOWZAMQVjq9CHzmxHfOGT8uvVZBZBf6CDLlL5fmOSxIHUyjEAV4FYpPP1ZCDPI2ampGmZBll9YIK5Qm94twZDZD"
PAGE_ID = "1195452070329476"
INSTAGRAM_ID = "17841431606006568"

def git_push():
    try:
        subprocess.run(["git", "add", "."], cwd=folder, check=True)
        subprocess.run(["git", "commit", "-m", "Auto subida"], cwd=folder, check=True)
        subprocess.run(["git", "push"], cwd=folder, check=True)
        print("✅ Cambios subidos a GitHub")
    except subprocess.CalledProcessError:
        print("⚠️ No había cambios nuevos para subir")

def publicar_en_instagram(imagen_path, titulo, hashtags):
    caption = f"{titulo}\n\n{hashtags}"
    url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_ID}/media"
    files = {"file": open(imagen_path, "rb")}
    data = {"caption": caption, "access_token": ACCESS_TOKEN}
    r = requests.post(url, data=data, files=files)
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
                ruta = os.path.join(folder, archivo)
                publicar_en_instagram(
                    ruta,
                    titulo="✨ Nuevo contenido ✨",
                    hashtags="#anime #3Dart #LoL #CapasYJuegos"
                )
        before = after
