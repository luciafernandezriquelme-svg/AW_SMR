import math
import random
import time
import turtle

# 🎮 Configuración de pantalla
pantalla = turtle.Screen()
pantalla.bgcolor("black")
pantalla.title("🔥 GAMER MODE 🔥")
pantalla.setup(width=800, height=600)

# 🌀 Tortuga para el logo
logo = turtle.Turtle()
logo.hideturtle()
logo.speed(0)
logo.width(3)

# 💬 Tortuga para texto
texto = turtle.Turtle()
texto.hideturtle()
texto.color("#00ffcc")

# 🔥 Colores gamer estilo neón
colores = ["#00ffff", "#ff00ff", "#00ff66", "#ff3300", "#00ccff"]

# ✨ Dibujar círculo de energía (animado)
def circulo_energia(radio, color):
    logo.color(color)
    logo.penup()
    logo.goto(0, -radio)
    logo.pendown()
    logo.circle(radio)

# 🧠 Función principal de animación
def animar_logo():
    angulo = 0
    while True:
        logo.clear()

        # 💡 Efecto de círculos concéntricos girando
        for i in range(6):
            color = colores[i % len(colores)]
            radio = 50 + i * 15 + 5 * math.sin(angulo / 10 + i)
            circulo_energia(radio, color)
        
        # 🎮 Texto gamer con efecto de “respiración”
        texto.clear()
        scale = 1 + 0.05 * math.sin(angulo / 10)
        texto.goto(0, -30)
        texto.color(random.choice(colores))
        texto.write("GAMER MODE", align="center", font=("Consolas", int(36 * scale), "bold"))

        # ⚡ Subtexto animado
        texto.goto(0, -80)
        glow = abs(math.sin(angulo / 15))
        texto.color((glow, glow, glow))
        texto.write("Press [START] to begin", align="center", font=("Consolas", 16, "bold"))

        time.sleep(0.05)
        angulo += 5

# 🚀 Iniciar animación
animar_logo()