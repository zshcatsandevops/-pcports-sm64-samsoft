#!/usr/bin/env python3
# ULTRA MARIO 3D BROS (Ursina prototype + SM64-style HUD)

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

window.title = "Ultra Mario 3D Bros"
window.size = (800, 600)
window.borderless = False
window.fullscreen = False
window.exit_button.visible = True

# Game state
MENU = "menu"
PLAYING = "playing"
state = MENU

# Score & HUD values
score = 0
total_stars = 3
score_text = None
lives = 3

# --- Entities ---
def create_star(pos):
    return Entity(
        model='sphere',
        color=color.yellow,
        scale=0.5,
        position=pos,
        collider='sphere'
    )

def create_menu():
    global title_text, start_btn, exit_btn
    Sky(texture="sky_sunset")
    title_text = Text(
        text="ULTRA MARIO 3D BROS",
        origin=(0, 0),
        y=0.3,
        scale=3,
        color=color.red
    )
    start_btn = Button(
        text="START",
        color=color.green,
        scale=(0.3, 0.1),
        position=(0, 0),
        on_click=start_game
    )
    exit_btn = Button(
        text="EXIT",
        color=color.red,
        scale=(0.3, 0.1),
        position=(0, -0.15),
        on_click=application.quit
    )

def create_level():
    global player, stars, score, score_text, hud_lives, hud_star_count

    # Ground
    Entity(model='plane', collider='box', scale=64, texture='grass', texture_scale=(4, 4))

    # Player
    player = FirstPersonController(model='cube', color=color.azure, origin_y=-0.5, speed=5)

    # Stars
    star_positions = [(5, 1, 5), (-10, 1, -5), (15, 1, 10)]
    stars = [create_star(pos) for pos in star_positions]

    # HUD (Super Mario 64 style)
    score = 0
    hud_lives = Text(
        text=f"MARIO × {lives}",
        origin=(-0.5, 0.5),
        position=(-0.85, 0.45),
        scale=2,
        color=color.white,
        background=False
    )
    hud_star_count = Text(
        text=f"★ {score}/{total_stars}",
        origin=(-0.5, 0.5),
        position=(0.7, 0.45),
        scale=2,
        color=color.yellow,
        background=False
    )

    # Lighting + Sky
    DirectionalLight().look_at(Vec3(1, -1, -1))
    Sky()

def start_game():
    global state
    destroy(title_text)
    destroy(start_btn)
    destroy(exit_btn)
    create_level()
    state = PLAYING
    mouse.locked = True

def update():
    global score
    if state == PLAYING:
        for star in stars[:]:
            if distance(player.position, star.position) < 2:
                stars.remove(star)
                destroy(star)
                score += 1
                hud_star_count.text = f"★ {score}/{total_stars}"
                if score >= total_stars:
                    Text(
                        "Course Clear!",
                        origin=(0,0),
                        scale=3,
                        color=color.gold,
                        duration=5
                    )

# Start with menu
create_menu()

app.run()
