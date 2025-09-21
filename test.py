#!/usr/bin/env python3
# ULTRA MARIO 3D BROS - Portal Tech Demo
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import math

app = Ursina()
window.title = "Mario Portal Tech Demo - Peach's Castle"
window.size = (800, 600)
window.borderless = False
window.fullscreen = False
window.exit_button.visible = True

# Define custom colors
PORTAL_BLUE = color.rgb(0, 150, 255)
PORTAL_ORANGE = color.rgb(255, 150, 0)

# Game states
PLAYING = "playing"
TELEPORTING = "teleporting"
state = PLAYING

# Portal system
active_portals = []
portal_cooldown = False

# Create Peach's Castle environment
def create_castle():
    # Ground
    ground = Entity(model='plane', scale=(50, 1, 50), texture='white_cube', texture_scale=(10, 10), color=color.rgb(200, 200, 200))
    
    # Castle walls
    wall_positions = [
        (20, 2.5, 0), (-20, 2.5, 0), (0, 2.5, 20), (0, 2.5, -20)
    ]
    for pos in wall_positions:
        wall = Entity(model='cube', scale=(1, 5, 40) if abs(pos[0]) > 0 else (40, 5, 1), 
                     position=pos, texture='brick', texture_scale=(2, 2))
    
    # Castle towers
    tower_positions = [
        (18, 5, 18), (-18, 5, 18), (18, 5, -18), (-18, 5, -18)
    ]
    for pos in tower_positions:
        tower = Entity(model='cylinder', scale=(3, 10, 3), position=pos, color=color.pink)
    
    # Main castle structure
    castle = Entity(model='cube', scale=(15, 8, 15), position=(0, 4, 0), texture='brick', texture_scale=(2, 2))
    castle_roof = Entity(model='cone', scale=(16, 10, 16), position=(0, 10, 0), color=color.red)
    
    # Entrance
    entrance = Entity(model='cube', scale=(5, 5, 1), position=(0, 2.5, -20), color=color.brown)
    
    return ground

# Create portals
def create_portal(position, color, target_position):
    portal = Entity(
        model='cylinder', 
        scale=(2, 4, 2), 
        position=position,
        color=color,
        double_sided=True,
        collider='box'
    )
    
    # Add portal effect
    portal_particles = Entity(
        model='circle', 
        scale=1.8, 
        position=position,
        color=color,
        billboard=True
    )
    
    # Store portal data
    portal_data = {
        'entity': portal,
        'particles': portal_particles,
        'target_position': target_position,
        'color': color
    }
    
    active_portals.append(portal_data)
    return portal_data

# Create the player
player = FirstPersonController()
player.speed = 8
player.jump_height = 2

# Setup the scene
ground = create_castle()

# Create two portals in the castle
portal1 = create_portal(position=(10, 1, 10), color=PORTAL_BLUE, target_position=(-10, 1, -10))
portal2 = create_portal(position=(-10, 1, -10), color=PORTAL_ORANGE, target_position=(10, 1, 10))

# Add some decorative elements
decorations = []
for i in range(10):
    tree = Entity(
        model='cylinder', 
        scale=(0.5, 3, 0.5), 
        position=(random.uniform(-15, 15), 1.5, random.uniform(-15, 15)),
        color=color.green
    )
    decorations.append(tree)

# Add a goal object (Princess Peach's crown)
crown = Entity(
    model='cube', 
    scale=(2, 0.5, 2), 
    position=(0, 3, 0),
    color=color.yellow,
    collider='box'
)

# Instructions
text = Text(text="Welcome to Mario Portal Demo!\nFind the crown in Peach's Castle!\nUse the portals to navigate.", 
           position=(-0.7, 0.4), scale=2)

# Game update function
def update():
    global state, portal_cooldown
    
    # Check for portal collisions
    if state == PLAYING and not portal_cooldown:
        for portal in active_portals:
            if player.intersects(portal['entity']).hit:
                state = TELEPORTING
                player.position = portal['target_position']
                portal_cooldown = True
                invoke(set_portal_cooldown_false, delay=1.0)
                break
    
    # Check for crown collision
    if player.intersects(crown).hit:
        text.text = "Congratulations! You found the crown!\nGame created by [Your Name]"

def set_portal_cooldown_false():
    global portal_cooldown
    portal_cooldown = False

# Run the game
app.run()
