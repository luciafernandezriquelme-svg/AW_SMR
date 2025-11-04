#!/usr/bin/env python3
"""
flor_mandala_animada.py
Animación a pantalla completa de una flor-mandala que se abre y cambia de color.
Muestra el texto: "Gracias mama por apoyarme siempre ¡Te quiero!"

Requisitos:
    pip install pygame

Controles:
    ESC o tecla Q  -> salir
    Espacio        -> pausar/reanudar animación
    F              -> alternar modo ventana/pantalla completa
"""

import colorsys
import math
import sys
import time

import pygame

# ---------- Configuración ----------
FPS = 60
NUM_PETALS = 12         # pétalos por capa
LAYERS = 3              # capas concéntricas de pétalos
PETAL_POINTS = 40       # puntos por pétalo (suavidad)
OPEN_TIME = 2.2         # segundos que tarda en abrir (0 -> 1 escala)
COLOR_CYCLE_SPEED = 0.15 # velocidad de cambio de hue
TEXT = "Gracias mama por apoyarme siempre ¡Te quiero!"
FONT_NAME = None        # None -> fuente por defecto
FONT_FACTOR = 0.06      # tamaño de fuente relativo a altura de pantalla

# Colores
BG_COLOR = (10, 10, 12)   # fondo oscuro
TEXT_SHADOW = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)

# ---------- Funciones auxiliares ----------
def hsv_to_rgb255(h, s, v):
    """Convierte HSV (0..1) a RGB (0..255)."""
    r, g, b = colorsys.hsv_to_rgb(h % 1.0, max(0, min(1, s)), max(0, min(1, v)))
    return int(r * 255), int(g * 255), int(b * 255)

def petal_shape_points(radius_inner, radius_outer, angle_center, spread, points):
    """
    Genera una lista de (x,y) puntos que forman un pétalo en coordenadas polares centradas en 0.
    - radius_inner: radio en la base del pétalo (cerca del centro)
    - radius_outer: radio en la punta del pétalo
    - angle_center: ángulo central del pétalo (radianes)
    - spread: apertura angular del pétalo (radianes)
    - points: cantidad de puntos que componen el borde
    Retorna lista de (x,y).
    """
    pts = []
    # ida: desde -spread/2 hasta +spread/2 usando una curva que escala hacia outer
    for i in range(points):
        t = i / (points - 1)
        # mapa t a ángulo
        ang = angle_center - spread/2 + t * spread
        # perfil radial: base -> punta -> base (usamos sin^n para forma suavizada)
        # perfil = radius_inner + (radius_outer - radius_inner) * smoothstep(t)
        profile = radius_inner + (radius_outer - radius_inner) * (math.sin(math.pi * t) ** 0.9)
        x = profile * math.cos(ang)
        y = profile * math.sin(ang)
        pts.append((x, y))
    # cerramos con puntos en la base (pequeño arco interior) para hacer polígono relleno
    return pts

# ---------- Inicialización de Pygame ----------
pygame.init()
info = pygame.display.Info()
screen_w, screen_h = info.current_w, info.current_h
flags = pygame.FULLSCREEN
screen = pygame.display.set_mode((screen_w, screen_h), flags)
pygame.display.set_caption("Flor Mandala Animada — Gracias mamá")
clock = pygame.time.Clock()

# Fuente
font_size = max(16, int(screen_h * FONT_FACTOR))
font = pygame.font.SysFont(FONT_NAME, font_size, bold=True)

# Centro
cx, cy = screen_w // 2, screen_h // 2

# Parámetros de la flor (en píxeles relativos a pantalla)
base_radius = min(screen_w, screen_h) * 0.06   # radio de la capa más interna
layer_gap = min(screen_w, screen_h) * 0.10     # separación entre capas
petal_width_factor = 0.7                        # cuánto se extiende lateralmente

# Animación
start_time = time.time()
paused = False
pause_at = 0.0
fullscreen = True

def draw_mandala(surface, t_anim, hue_offset):
    """
    Dibuja la flor mandala en la superficie.
    - t_anim: animación 0..1 (0 cerrado, 1 abierto)
    - hue_offset: valor hue base (0..1) para ciclar colores
    """
    # Limpiamos (fondo)
    surface.fill(BG_COLOR)

    # Dibujar capas desde más lejano (fondo) a más cercano (frente)
    for layer in range(LAYERS):
        layer_index = LAYERS - 1 - layer  # invertimos para dibujar fondo primero
        petals = NUM_PETALS + layer_index * 2
        radius_inner = base_radius + layer_index * layer_gap * 0.45
        radius_outer = radius_inner + layer_gap * (0.9 + 0.3 * layer_index)
        spread = math.pi * petal_width_factor * (0.9 - layer_index * 0.12)
        # variación dinámica por capa para rotación lenta
        rot = t_anim * (0.6 + 0.2 * layer_index) * math.pi + layer_index * 0.2

        for p in range(petals):
            angle = (2 * math.pi / petals) * p + rot
            # escala de apertura por pétalo (pequeña variación para naturalidad)
            local_open = t_anim * (0.85 + 0.15 * math.sin(time.time() * 1.2 + p))
            r_in = radius_inner * (0.2 + 0.8 * local_open)
            r_out = radius_outer * (0.15 + 1.05 * local_open)
            pts = petal_shape_points(r_in, r_out, angle, spread, PETAL_POINTS)

            # transformar puntos al centro de pantalla (y invertido para coordenadas pygame)
            poly = []
            for x, y in pts:
                sx = cx + x
                sy = cy - y
                poly.append((int(sx), int(sy)))

            # color: hue depende de hue_offset, capa y pétalo
            hue = (hue_offset + 0.07 * layer_index + 0.02 * math.sin(p * 0.5 + time.time() * 0.8)) % 1.0
            sat = 0.6 + 0.35 * math.sin(layer_index + p * 0.3 + time.time() * 0.6)
            val = 0.85 - 0.12 * layer_index
            color = hsv_to_rgb255(hue, max(0.2, min(1, sat)), max(0.2, min(1, val)))

            # sombra/contorno suave: dibujamos un polígon ligeramente más grande como 'sombra'
            # Para simplificar, dibujamos la sombra con alpha en una superficie temporal
            shadow_surf = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
            shadow_color = (0, 0, 0, 48)  # negro semi-transparente
            # desplazamiento pequeño según capa para dar profundidad
            offset = (int(6 * (layer_index + 1) * (0.6 - local_open)), int(6 * (layer_index + 1) * (0.2 + local_open)))
            poly_shadow = [(x + offset[0], y + offset[1]) for (x, y) in poly]
            pygame.draw.polygon(shadow_surf, shadow_color, poly_shadow)
            surface.blit(shadow_surf, (0, 0))

            # dibujar pétalo relleno
            pygame.draw.polygon(surface, color, poly)
            # contorno fino
            pygame.draw.aalines(surface, (20, 20, 20), True, poly, blend=1)

    # Centro de la flor: un disco que también cambia ligeramente
    core_radius = int(base_radius * (0.9 + 0.85 * t_anim))
    core_hue = (hue_offset + 0.2) % 1.0
    core_col = hsv_to_rgb255(core_hue, 0.65, 0.95)
    pygame.draw.circle(surface, core_col, (cx, cy), core_radius)
    pygame.draw.circle(surface, (20,20,20), (cx, cy), int(core_radius*0.98), 2)

    # Texto en la parte inferior o centrado, con sombra
    text_surface = font.render(TEXT, True, TEXT_COLOR)
    text_shadow = font.render(TEXT, True, TEXT_SHADOW)
    tx = cx - text_surface.get_width() // 2
    ty = cy + int(screen_h * 0.28)  # posición vertical relativa (abajo de la flor)
    # sombra
    surface.blit(text_shadow, (tx+3, ty+3))
    surface.blit(text_surface, (tx, ty))


# ---------- Bucle principal ----------
running = True
while running:
    dt = clock.tick(FPS) / 1000.0  # segundos transcurridos este frame
    now = time.time()

    # eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_q):
                running = False
            elif event.key == pygame.K_SPACE:
                # pausar/reanudar
                if not paused:
                    paused = True
                    pause_at = now
                else:
                    # ajustar start_time para que la animación sea continua
                    paused = False
                    # shift start_time por el tiempo en pausa para que t_anim no salte
                    start_time += (now - pause_at)
            elif event.key == pygame.K_f:
                # alternar fullscreen/windowed
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((screen_w, screen_h), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((int(screen_w*0.8), int(screen_h*0.8)))

    # calcular t_anim (0..1) basado en tiempo (apertura)
    if paused:
        t_anim = min(1.0, max(0.0, (pause_at - start_time) / OPEN_TIME))
        hue_offset = ((pause_at - start_time) * COLOR_CYCLE_SPEED) % 1.0
    else:
        elapsed = now - start_time
        # usamos easing (ease out quint) para que la flor se abra con suavidad
        raw = min(1.0, elapsed / OPEN_TIME)
        # ease out quint: 1 - (1 - x)^5
        t_anim = 1.0 - (1.0 - raw) ** 5
        hue_offset = (elapsed * COLOR_CYCLE_SPEED) % 1.0

    # dibujar mandala
    draw_mandala(screen, t_anim, hue_offset)

    pygame.display.flip()

# limpiar
pygame.quit()
sys.exit()
