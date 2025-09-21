#!/usr/bin/env python3
# ULTRA MARIO 3D BROS - Enhanced with Hub World & 6 Levels
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import basic_lighting_shader
import random
import math

app = Ursina()
window.title = "Ultra Mario 3D Bros - Star Collection"
window.size = (800, 600)
window.borderless = False
window.fullscreen = False
window.exit_button.visible = True

# Define custom colors
SANDY_BROWN = color.rgb(244, 164, 96)  # RGB for sandy brown

# Game states
MENU = "menu"
HUB = "hub"
PLAYING = "playing"
state = MENU

# Game progress
total_stars_collected = 0
level_stars = {i: 0 for i in range(1, 7)}  # 6 levels, each can have multiple stars
current_level = 0
lives = 5

# Level configurations
LEVEL_CONFIGS = {
    1: {
        "name": "Grass Plains",
        "ground_color": color.green,
        "ground_texture": "grass",
        "sky_color": color.light_gray,
        "star_positions": [(5, 1, 5), (-10, 1, -5), (15, 1, 10)],
        "obstacles": []
    },
    2: {
        "name": "Desert Dunes",
        "ground_color": SANDY_BROWN,  # Use our custom color
        "ground_texture": "white_cube",
        "sky_color": color.orange,
        "star_positions": [(8, 2, 8), (-12, 1, -8), (20, 3, 15), (-5, 1, 10)],
        "obstacles": [(3, 1, 3), (-3, 1, -3), (7, 1, -7)]
    },
    3: {
        "name": "Crystal Caverns",
        "ground_color": color.dark_gray,
        "ground_texture": "brick",
        "sky_color": color.dark_gray,
        "star_positions": [(10, 5, 10), (-15, 2, -10), (25, 1, 20), (0, 8, 0)],
        "obstacles": [(5, 3, 5), (-5, 3, -5), (10, 3, -10), (-10, 3, 10)]
    },
    4: {
        "name": "Sky High Tower",
        "ground_color": color.white,
        "ground_texture": "white_cube",
        "sky_color": color.cyan,
        "star_positions": [(0, 10, 0), (10, 15, 10), (-10, 20, -10)],
        "obstacles": []  # Platforms will be added
    },
    5: {
        "name": "Lava Lake",
        "ground_color": color.rgb(200, 50, 0),
        "ground_texture": "white_cube",
        "sky_color": color.red,
        "star_positions": [(12, 2, 12), (-18, 3, -12), (30, 1, 25), (5, 4, -15)],
        "obstacles": [(6, 0.5, 6), (-6, 0.5, -6), (12, 0.5, -12)]
    },
    6: {
        "name": "Rainbow Road",
        "ground_color": color.violet,
        "ground_texture": "white_cube",
        "sky_color": color.magenta,
        "star_positions": [(20, 3, 20), (-25, 5, -20), (35, 2, 30), (0, 10, 0), (-10, 7, 15)],
        "obstacles": []  # Moving platforms
    }
}

# Current level entities
player = None
stars = []
obstacles = []
platforms = []
hud_elements = []
menu_elements = []

def clear_level():
    """Clear all level entities"""
    global player, stars, obstacles, platforms, hud_elements
    
    if player:
        destroy(player)
        player = None
    
    for star in stars:
        destroy(star)
    stars = []
    
    for obstacle in obstacles:
        destroy(obstacle)
    obstacles = []
    
    for platform in platforms:
        destroy(platform)
    platforms = []
    
    for hud in hud_elements:
        destroy(hud)
    hud_elements = []
    
    # Clear other entities except UI
    for entity in scene.entities[:]:
        if hasattr(entity, 'model') and entity.model in ['plane', 'cube', 'sphere']:
            if not hasattr(entity, 'eternal'):
                destroy(entity)

def clear_menu():
    """Clear menu elements"""
    global menu_elements
    for element in menu_elements:
        if hasattr(element, 'visible'):
            element.visible = False
        destroy(element)
    menu_elements = []

def create_menu():
    global title_text, start_btn, exit_btn
    
    clear_menu()
    Sky(texture="sky_sunset")
    
    title_text = Text(
        text="ULTRA MARIO 3D BROS",
        origin=(0, 0),
        y=0.3,
        scale=3,
        color=color.red
    )
    menu_elements.append(title_text)
    
    subtitle_text = Text(
        text="Collect the Stars!",
        origin=(0, 0),
        y=0.2,
        scale=1.5,
        color=color.yellow
    )
    menu_elements.append(subtitle_text)
    
    start_btn = Button(
        text="ENTER CASTLE",
        color=color.green,
        scale=(0.3, 0.1),
        position=(0, 0),
        on_click=enter_hub
    )
    menu_elements.append(start_btn)
    
    exit_btn = Button(
        text="EXIT",
        color=color.red,
        scale=(0.3, 0.1),
        position=(0, -0.15),
        on_click=application.quit
    )
    menu_elements.append(exit_btn)
    
    # Don't mark buttons as eternal so they can be destroyed
    mouse.locked = False

def create_hub():
    """Create the hub world with level paintings"""
    global player, hud_elements
    
    clear_level()
    
    # Create hub floor
    Entity(model='plane', collider='box', scale=100, texture='brick', texture_scale=(10, 10))
    
    # Castle walls
    Entity(model='cube', collider='box', scale=(50, 20, 1), position=(0, 10, -25), color=color.gray)
    Entity(model='cube', collider='box', scale=(50, 20, 1), position=(0, 10, 25), color=color.gray)
    Entity(model='cube', collider='box', scale=(1, 20, 50), position=(-25, 10, 0), color=color.gray)
    Entity(model='cube', collider='box', scale=(1, 20, 50), position=(25, 10, 0), color=color.gray)
    
    # Create player in hub
    player = FirstPersonController(
        model='cube',
        color=color.red,
        origin_y=-0.5,
        speed=5,
        position=(0, 1, 0)
    )
    
    # Create level portals (paintings)
    portal_positions = [
        (-15, 3, -20),  # Level 1
        (-5, 3, -20),   # Level 2
        (5, 3, -20),    # Level 3
        (15, 3, -20),   # Level 4
        (-10, 3, 20),   # Level 5
        (10, 3, 20)     # Level 6
    ]
    
    for i, pos in enumerate(portal_positions, 1):
        config = LEVEL_CONFIGS[i]
        portal_color = [color.green, SANDY_BROWN, color.dark_gray, 
                       color.cyan, color.orange, color.violet][i-1]
        
        # Portal frame
        portal = Entity(
            model='cube',
            color=portal_color,
            scale=(4, 5, 0.5),
            position=pos,
            collider='box'
        )
        portal.level_id = i
        
        # Level name text
        level_text = Text(
            text=f"{i}. {config['name']}\n★ {level_stars[i]}/3",
            parent=portal,
            origin=(0, 0),
            y=3,
            scale=8,
            color=color.white,
            billboard=True
        )
    
    # HUD in hub
    total_stars_text = Text(
        text=f"Total Stars: {total_stars_collected}",
        origin=(-0.5, 0.5),
        position=(-0.85, 0.45),
        scale=2,
        color=color.yellow
    )
    hud_elements.append(total_stars_text)
    
    lives_text = Text(
        text=f"Lives: {lives}",
        origin=(0.5, 0.5),
        position=(0.85, 0.45),
        scale=2,
        color=color.red
    )
    hud_elements.append(lives_text)
    
    instructions = Text(
        text="Walk into a painting to enter level | ESC to return to hub",
        origin=(0, 0),
        position=(0, -0.45),
        scale=1.5,
        color=color.white
    )
    hud_elements.append(instructions)
    
    # Lighting
    DirectionalLight().look_at(Vec3(1, -1, -1))
    Sky()

def create_level(level_id):
    """Create a specific level"""
    global player, stars, obstacles, platforms, hud_elements, current_level
    
    current_level = level_id
    config = LEVEL_CONFIGS[level_id]
    
    clear_level()
    
    # Ground
    ground = Entity(
        model='plane',
        collider='box',
        scale=64,
        texture=config["ground_texture"],
        texture_scale=(4, 4),
        color=config["ground_color"]
    )
    
    # Player
    player = FirstPersonController(
        model='cube',
        color=color.red,
        origin_y=-0.5,
        speed=5,
        position=(0, 1, 0)
    )
    
    # Create stars
    stars = []
    for pos in config["star_positions"][:3]:  # Limit to 3 stars per level
        star = Entity(
            model='sphere',
            color=color.yellow,
            scale=0.5,
            position=pos,
            collider='sphere'
        )
        # Add rotation animation
        star.rotation_speed = random.uniform(20, 50)
        stars.append(star)
    
    # Create obstacles based on level
    obstacles = []
    if level_id == 2:  # Desert - Cactuses
        for pos in config["obstacles"]:
            cactus = Entity(
                model='cube',
                color=color.dark_green,
                scale=(1, 3, 1),
                position=pos,
                collider='box'
            )
            obstacles.append(cactus)
    
    elif level_id == 3:  # Caverns - Crystals
        for pos in config["obstacles"]:
            crystal = Entity(
                model='cube',
                color=color.cyan,
                scale=(1.5, 4, 1.5),
                position=pos,
                collider='box'
            )
            crystal.rotation_speed = 15
            obstacles.append(crystal)
    
    elif level_id == 4:  # Sky Tower - Floating platforms
        platform_positions = [
            (0, 2, 5),
            (5, 4, 10),
            (10, 6, 10),
            (10, 8, 5),
            (5, 10, 0),
            (0, 12, 0)
        ]
        for pos in platform_positions:
            platform = Entity(
                model='cube',
                color=color.white,
                scale=(3, 0.5, 3),
                position=pos,
                collider='box'
            )
            platforms.append(platform)
    
    elif level_id == 5:  # Lava - Hazards
        for pos in config["obstacles"]:
            lava_pool = Entity(
                model='cube',
                color=color.orange,
                scale=(4, 0.1, 4),
                position=pos,
                collider='box'
            )
            obstacles.append(lava_pool)
    
    elif level_id == 6:  # Rainbow Road - Moving platforms
        for i in range(5):
            moving_platform = Entity(
                model='cube',
                color=color.rgb(random.randint(100, 255), 
                               random.randint(100, 255), 
                               random.randint(100, 255)),
                scale=(4, 0.5, 4),
                position=(i * 8 - 16, 1, 0),
                collider='box'
            )
            moving_platform.move_amplitude = random.uniform(5, 10)
            moving_platform.move_speed = random.uniform(0.5, 1.5)
            platforms.append(moving_platform)
    
    # HUD for level
    level_name_text = Text(
        text=config["name"],
        origin=(0, 0.5),
        position=(0, 0.45),
        scale=2,
        color=color.white
    )
    hud_elements.append(level_name_text)
    
    stars_collected_text = Text(
        text=f"Stars: {len(stars)} remaining",
        origin=(-0.5, 0.5),
        position=(-0.85, 0.4),
        scale=1.5,
        color=color.yellow
    )
    hud_elements.append(stars_collected_text)
    
    exit_text = Text(
        text="Press ESC to return to castle",
        origin=(0, -0.5),
        position=(0, -0.45),
        scale=1.2,
        color=color.white
    )
    hud_elements.append(exit_text)
    
    # Sky and lighting
    sky = Sky()
    if config["sky_color"]:
        sky.color = config["sky_color"]
    
    DirectionalLight().look_at(Vec3(1, -1, -1))

def enter_hub():
    """Enter the hub world from menu"""
    global state
    
    # Clear menu elements
    clear_menu()
    
    create_hub()
    state = HUB
    mouse.locked = True

def enter_level(level_id):
    """Enter a specific level from hub"""
    global state
    
    create_level(level_id)
    state = PLAYING
    mouse.locked = True

def return_to_hub():
    """Return to hub from a level"""
    global state
    
    create_hub()
    state = HUB
    mouse.locked = True

def collect_star():
    """Called when a star is collected"""
    global total_stars_collected, level_stars, current_level
    
    total_stars_collected += 1
    level_stars[current_level] = min(level_stars[current_level] + 1, 3)
    
    # Update HUD
    for hud in hud_elements:
        if "Stars:" in hud.text:
            hud.text = f"Stars: {len(stars)} remaining"
    
    # Victory message if all stars collected
    if len(stars) == 0:
        victory_text = Text(
            text="LEVEL COMPLETE!\nPress ESC to return",
            origin=(0, 0),
            scale=3,
            color=color.gold
        )
        hud_elements.append(victory_text)

def update():
    global stars, platforms
    
    if state == HUB and player:
        # Check for portal collisions
        for entity in scene.entities:
            if hasattr(entity, 'level_id'):
                if distance(player.position, entity.position) < 3:
                    enter_level(entity.level_id)
                    break
    
    elif state == PLAYING and player:
        # Check star collection
        for star in stars[:]:
            if distance(player.position, star.position) < 2:
                stars.remove(star)
                destroy(star)
                collect_star()
            else:
                # Rotate stars
                if hasattr(star, 'rotation_speed'):
                    star.rotation_y += star.rotation_speed * time.dt
        
        # Rotate crystals in level 3
        for obstacle in obstacles:
            if hasattr(obstacle, 'rotation_speed'):
                obstacle.rotation_y += obstacle.rotation_speed * time.dt
        
        # Move platforms in level 6
        for platform in platforms:
            if hasattr(platform, 'move_amplitude'):
                platform.z = math.sin(time.time() * platform.move_speed) * platform.move_amplitude
    
    # Global controls
    if held_keys['escape']:
        if state == PLAYING:
            return_to_hub()
        elif state == HUB:
            mouse.locked = False

# Start with menu
create_menu()

app.run()
