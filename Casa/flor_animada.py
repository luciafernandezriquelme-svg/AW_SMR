import time
import turtle

# Configuración de pantalla
pantalla = turtle.Screen()
pantalla.bgcolor("#0b1d0b")  # Verde oscuro como fondo del bosque
pantalla.title("🌹 Rosa del Bosque 🌹")

# Configuración de la tortuga (rosa)
rosa = turtle.Turtle()
rosa.speed(0)
rosa.hideturtle()
rosa.width(2)

# Configuración del texto (independiente y permanente)
texto = turtle.Turtle()
texto.hideturtle()
texto.color("white")
texto.penup()
texto.goto(0, -200)
texto.write("A la persona que más jodo en clase y en casa.\n¡Te Quiero!",
            align="center", font=("Comic Sans MS", 16, "bold"))

# Función para dibujar un pétalo
def petalo(radio, angulo, escala):
    rosa.begin_fill()
    for _ in range(2):
        rosa.circle(radio * escala, angulo)
        rosa.left(180 - angulo)
    rosa.end_fill()

# Función para dibujar la rosa con cierto nivel de apertura
def dibujar_rosa(escala):
    rosa.clear()
    rosa.penup()
    rosa.goto(0, 0)
    rosa.setheading(0)
    rosa.pendown()
    rosa.color("#990000", "#ff0000")  # Borde oscuro, centro rojo vivo

    # Dibujar pétalos (8 en total)
    for i in range(8):
        rosa.setheading(i * 45)
        petalo(60, 60, escala)

    # Dibujar el tallo
    rosa.penup()
    rosa.goto(0, -30)
    rosa.setheading(270)
    rosa.pendown()
    rosa.color("#1a6600")
    rosa.width(6)
    rosa.forward(120)

# Animación principal
while True:
    # Abrir lentamente
    for escala in [i / 50 for i in range(10, 41)]:
        dibujar_rosa(escala)
        time.sleep(0.08)

    # Pausa con la flor abierta
    time.sleep(0.8)

    # Cerrar lentamente
    for escala in [i / 50 for i in range(40, 9, -1)]:
        dibujar_rosa(escala)
        time.sleep(0.08)

    # Pausa con la flor cerrada
    time.sleep(0.8)

pantalla.mainloop()