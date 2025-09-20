from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
import random

app = Ursina()

# Set default shader for lighting
Entity.default_shader = lit_with_shadows_shader

# Game state
game_state = "menu"

# Create a simple Mario head model
def create_mario_head():
    # Head (red sphere)
    head = Entity(model='sphere', color=color.red, scale=1)
    
    # Eyes (white spheres with blue pupils)
    left_eye = Entity(model='sphere', color=color.white, scale=0.2, position=(-0.3, 0.2, 0.4), parent=head)
    right_eye = Entity(model='sphere', color=color.white, scale=0.2, position=(0.3, 0.2, 0.4), parent=head)
    left_pupil = Entity(model='sphere', color=color.blue, scale=0.1, position=(-0.3, 0.2, 0.5), parent=head)
    right_pupil = Entity(model='sphere', color=color.blue, scale=0.1, position=(0.3, 0.2, 0.5), parent=head)
    
    # Hat (red cylinder)
    hat = Entity(model='cylinder', color=color.red, scale=(1, 0.2, 1), position=(0, 0.6, 0), parent=head)
    hat_brim = Entity(model='cylinder', color=color.red, scale=(1.2, 0.05, 1.2), position=(0, 0.5, 0), parent=head)
    
    # Mustache (brown box)
    mustache = Entity(model='cube', color=color.brown, scale=(0.8, 0.1, 0.1), position=(0, -0.1, 0.4), parent=head)
    
    return head

# Main menu
def create_main_menu():
    global menu_background, title_text, start_button, exit_button, mario_head
    
    # Background
    menu_background = Entity(model='quad', scale=(2, 1.5), texture='sky_sunset', parent=camera.ui, z=1)
    
    # Title
    title_text = Text(
        text='ULTRA MARIO 3D BROS',
        position=(0, 0.3),
        scale=3,
        color=color.red,
        background=True
    )
    
    # Create Mario's head
    mario_head = create_mario_head()
    mario_head.scale = 2
    mario_head.position = (0, -0.1, 0)
    mario_head.rotation_y = 180
    
    # Start button
    start_button = Button(
        text='START',
        color=color.green,
        scale=(0.3, 0.1),
        position=(0, -0.1),
        on_click=start_game
    )
    
    # Exit button
    exit_button = Button(
        text='EXIT',
        color=color.red,
        scale=(0.3, 0.1),
        position=(0, -0.25),
        on_click=quit_game
    )

# Game level
def create_game_level():
    global ground, player, stars, score_text, stars_collected, total_stars
    
    # Ground
    ground = Entity(model='plane', collider='box', scale=64, texture='grass', texture_scale=(4,4), color=color.green)

    # Player setup with third-person camera
    player = FirstPersonController(model='cube', color=color.red, origin_y=-0.5, speed=5)
    player.camera_pivot.z = -5  # Distance behind player
    player.camera_pivot.y = 2   # Height above player
    player.collider = BoxCollider(player, Vec3(0,1,0), Vec3(1,2,1))

    # Score system
    stars_collected = 0
    total_stars = 3
    score_text = Text('Stars: 0/3', position=(-0.8, 0.45), scale=2, color=color.yellow)

    # Store star entities in a list for collision checking
    stars = []

    # Generate random platforms
    random.seed(42)  # For reproducibility
    for i in range(20):
        platform = Entity(
            model='cube',
            origin_y=-0.5,
            scale=(random.uniform(2,5), random.uniform(0.5,1), random.uniform(2,5)),
            texture='brick',
            texture_scale=(1,2),
            x=random.uniform(-20,20),
            y=random.uniform(0,5),
            z=random.uniform(-20,20),
            collider='box',
            color=color.hsv(0, 0, random.uniform(0.9, 1))
        )

    # Spawn stars on some platforms
    star_positions = [(5,3,5), (-10,2,-5), (15,4,10)]  # Pre-set for easy collection
    for pos in star_positions:
        star = Entity(
            model='sphere',
            color=color.yellow,
            scale=0.5,
            position=pos,
            collider='sphere'
        )
        stars.append(star)  # Add to stars list

    # Lighting and sky
    sun = DirectionalLight()
    sun.look_at(Vec3(1,-1,-1))
    Sky()

# Start the game
def start_game():
    global game_state
    
    if game_state == "menu":
        # Hide menu elements
        destroy(menu_background)
        destroy(title_text)
        destroy(start_button)
        destroy(exit_button)
        destroy(mario_head)
        
        # Create the game level
        create_game_level()
        
        # Change game state
        game_state = "playing"
        
        # Enable mouse lock for first person controller
        mouse.locked = True

# Quit the game
def quit_game():
    app.quit()

# Input handling
def input(key):
    if key == 'escape':
        if game_state == "playing":
            quit_game()
        else:
            app.quit()

# Update function
def update():
    global stars_collected
    
    if game_state == "playing":
        # Check for star collection using distance-based detection
        for star in stars[:]:  # Use slice to avoid modification during iteration
            if distance(player.position, star.position) < 2:
                stars.remove(star)
                destroy(star)
                stars_collected += 1
                score_text.text = f'Stars: {stars_collected}/{total_stars}'
                
                if stars_collected >= total_stars:
                    Text('You collected all stars! Mario wins!', origin=(0,0), scale=3, color=color.gold, duration=5)
    
    # Rotate Mario's head in the menu
    if game_state == "menu":
        mario_head.rotation_y += time.dt * 20

# Create the main menu initially
create_main_menu()

app.run()
