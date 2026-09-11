import os
import socket

import requests
from flask import Flask, render_template_string

app = Flask(__name__)

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8081").rstrip("/")


@app.get("/")
def inicio():
    try:
        respuesta = requests.get(
            f"{BACKEND_URL}/api/info",
            timeout=3,
        )
        respuesta.raise_for_status()
        datos = respuesta.json()

        hora = datos.get("hora", "desconocida")
        backend_pod = datos.get("pod", "desconocido")
        error = None

    except (requests.RequestException, ValueError) as excepcion:
        hora = "No disponible"
        backend_pod = "No disponible"
        error = str(excepcion)

    return render_template_string(
        """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Laboratorio Kubernetes</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: #f4f6f8;
                    text-align: center;
                    padding-top: 80px;
                }

                .tarjeta {
                    background: white;
                    max-width: 600px;
                    margin: auto;
                    padding: 30px;
                    border-radius: 12px;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                }

                .pod {
                    color: #1565c0;
                    font-weight: bold;
                }

                .error {
                    color: #c62828;
                }

                button {
                    background: #1565c0;
                    color: white;
                    border: none;
                    padding: 12px 20px;
                    border-radius: 6px;
                    cursor: pointer;
                }
            </style>
        </head>
        <body>
            <div class="tarjeta">
                <h1>Laboratorio Kubernetes</h1>

                {% if error %}
                    <p class="error">No se pudo contactar al backend.</p>
                    <p>{{ error }}</p>
                {% else %}
                    <p>Hora del backend: <strong>{{ hora }}</strong></p>
                    <p>
                        Petición atendida por el Pod backend:
                        <span class="pod">{{ backend_pod }}</span>
                    </p>
                    <p>
                        Pod frontend:
                        <span class="pod">{{ frontend_pod }}</span>
                    </p>
                {% endif %}

                <button onclick="location.reload()">
                    Hacer otra petición
                </button>
            </div>
        </body>
        </html>
        """,
        hora=hora,
        backend_pod=backend_pod,
        frontend_pod=socket.gethostname(),
        error=error,
    )
