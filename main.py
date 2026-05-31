from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel, EmailStr, ValidationError
import csv
import os
from datetime import datetime

app = FastAPI(
    title="Preventa Validación Blockchain",
    description="Página promocional para registrar correos de usuarios interesados.",
    version="1.0.0"
)

ARCHIVO_CSV = "usuarios.csv"
ARCHIVO_HTML = "index.html"
ARCHIVO_CSS = "styles.css"


class UsuarioRegistro(BaseModel):
    email: EmailStr




def crear_archivo_csv():
    if not os.path.exists(ARCHIVO_CSV):
        with open(ARCHIVO_CSV, mode="w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["id", "correo", "fecha", "hora", "estado"])





def correo_existe(email: str) -> bool:
    crear_archivo_csv()

    with open(ARCHIVO_CSV, mode="r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            if fila["correo"].lower() == email.lower():
                return True

    return False





def guardar_correo(email: str):
    crear_archivo_csv()

    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    hora_actual = datetime.now().strftime("%H:%M:%S")
    nuevo_id = obtener_siguiente_id()

    with open(ARCHIVO_CSV, mode="a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([
            nuevo_id,
            email,
            fecha_actual,
            hora_actual,
            "Registrado"
        ])




def obtener_siguiente_id():
    crear_archivo_csv()

    with open(ARCHIVO_CSV, mode="r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        registros = list(lector)

        if len(registros) == 0:
            return 1

        return len(registros) + 1
    
    


def leer_html():
    with open(ARCHIVO_HTML, mode="r", encoding="utf-8") as archivo:
        return archivo.read()


def crear_alerta(mensaje=None, tipo=None):
    if mensaje is None:
        return ""

    return f"""
    <div class="mensaje {tipo}">
        {mensaje}
    </div>
    """


def renderizar_pagina(mensaje=None, tipo=None):
    html = leer_html()
    alerta = crear_alerta(mensaje, tipo)
    html = html.replace("{{ALERTA}}", alerta)
    return html


crear_archivo_csv()


@app.get("/", response_class=HTMLResponse)
def mostrar_pagina():
    return renderizar_pagina()


@app.get("/styles.css")
def obtener_css():
    return FileResponse(ARCHIVO_CSS, media_type="text/css")


@app.post("/registro", response_class=HTMLResponse)
def registrar_usuario(email: str = Form(...)):
    try:
        usuario = UsuarioRegistro(email=email)
        correo = str(usuario.email)

        if correo_existe(correo):
            return renderizar_pagina(
                mensaje="Este correo ya está registrado.",
                tipo="warning"
            )

        guardar_correo(correo)

        return renderizar_pagina(
            mensaje="¡Registro exitoso! Te notificaremos cuando el sistema esté disponible.",
            tipo="success"
        )

    except ValidationError:
        return renderizar_pagina(
            mensaje="Por favor, ingresa un correo electrónico válido.",
            tipo="error"
        )


@app.get("/api")
def api_inicio():
    return {
        "mensaje": "Prueba de Cambio"
    }
    
    