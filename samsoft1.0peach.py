#!/usr/bin/env python3
# ULTRA MARIO 3D BROS - Space World Tech Demo
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import math

app = Ursina()
window.title = "ULTRA MARIO 3D BROS - Space World Tech Demo"
window.size = (1280, 720)
window.borderless = False
window.fullscreen = False
window.exit_button.visible = True

# Game states
MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"
VICTORY = "victory"
state = MENU

# Game variables
coins_collected = 0
total_coins = 15
lives = 3
player_score = 0
camera_mode = "follow"
in_space = False
current_section = "castle"  # castle, space_transition, space_world

# HackerSM64 Configuration
HACKER_SM64_CONFIG = {
    "extended_bounds": True,
    "puppycam_enabled": True,
    "silhouette_effect": False,
    "improved_collision": True,
    "fall_damage": False,
    "nonstop_stars": True
}

# Space World variables
space_objects = []
black_holes = []
warp_zones = []
gravitational_fields = []

# Create main menu with Space World theme
def create_main_menu():
    # Background with space theme
    menu_bg = Entity(model='quad', scale=(2, 2), texture='sky_default', parent=camera.ui)
    
    # Title
    title = Text(text="ULTRA MARIO 3D BROS", scale=3, position=(0, 0.3), origin=(0, 0))
    subtitle = Text(text="Space World Tech Demo", scale=1.5, position=(0, 0.1), origin=(0, 0))
    
    # Start button
    start_button = Button(text='Start Game', color=color.cyan, scale=(0.3, 0.1), position=(0, -0.1))
    start_button.on_click = start_game
    
    # Options button
    options_button = Button(text='HackerSM64 Options', color=color.blue, scale=(0.3, 0.1), position=(0, -0.25))
    options_button.on_click = toggle_options_menu
    
    # Quit button
    quit_button = Button(text='Quit', color=color.gray, scale=(0.3, 0.1), position=(0, -0.4))
    quit_button.on_click = application.quit
    
    # Copyright text
    copyright_text = Text(text="© 2023 ULTRA MARIO 3D BROS | Space World Edition", scale=1, position=(0, -0.5), origin=(0, 0))
    
    return [menu_bg, title, subtitle, start_button, options_button, quit_button, copyright_text]

# HackerSM64 options menu
def create_options_menu():
    options_bg = Entity(model='quad', scale=(0.8, 0.8), color=color.dark_gray, position=(0, 0, 1))
    options_title = Text(text="HackerSM64 Options", scale=2, position=(0, 0.35), origin=(0, 0))
    
    # Toggle buttons for HackerSM64 features
    extended_bounds_toggle = Button(text='Extended Bounds: ON', color=color.green, scale=(0.3, 0.07), position=(0, 0.2))
    extended_bounds_toggle.on_click = lambda: toggle_setting('extended_bounds', extended_bounds_toggle)
    
    puppycam_toggle = Button(text='Puppycam: ON', color=color.green, scale=(0.3, 0.07), position=(0, 0.1))
    puppycam_toggle.on_click = lambda: toggle_setting('puppycam_enabled', puppycam_toggle)
    
    silhouette_toggle = Button(text='Silhouette: OFF', color=color.red, scale=(0.3, 0.07), position=(0, 0))
    silhouette_toggle.on_click = lambda: toggle_setting('silhouette_effect', silhouette_toggle)
    
    collision_toggle = Button(text='Improved Collision: ON', color=color.green, scale=(0.3, 0.07), position=(0, -0.1))
    collision_toggle.on_click = lambda: toggle_setting('improved_collision', collision_toggle)
    
    back_button = Button(text='Back', color=color.orange, scale=(0.3, 0.07), position=(0, -0.25))
    back_button.on_click = toggle_options_menu
    
    return [options_bg, options_title, extended_bounds_toggle, puppycam_toggle, 
            silhouette_toggle, collision_toggle, back_button]

def toggle_setting(setting_name, button):
    HACKER_SM64_CONFIG[setting_name] = not HACKER_SM64_CONFIG[setting_name]
    status = "ON" if HACKER_SM64_CONFIG[setting_name] else "OFF"
    color_val = color.green if HACKER_SM64_CONFIG[setting_name] else color.red
    button.text = f'{setting_name.replace("_", " ").title()}: {status}'
    button.color = color_val

def toggle_options_menu():
    global options_menu_visible
    options_menu_visible = not options_menu_visible
    
    for element in options_menu_elements:
        element.enabled = options_menu_visible
        
    for element in menu_elements:
        element.enabled = not options_menu_visible

# Start game function
def start_game():
    global state
    state = PLAYING
    # Hide menu elements
    for element in menu_elements:
        element.enabled = False
    # Enable game UI
    coins_text.enabled = True
    lives_text.enabled = True
    score_text.enabled = True
    message_text.enabled = True
    camera_mode_text.enabled = True
    location_text.enabled = True

# Create Peach's Castle environment with space transition
def create_space_world():
    # Clear any existing objects
    global space_objects, black_holes, warp_zones, gravitational_fields
    space_objects = []
    black_holes = []
    warp_zones = []
    gravitational_fields = []
    
    # Main ground (castle floor)
    ground = Entity(model='plane', scale=(50, 1, 50), texture='white_cube', 
                   texture_scale=(10, 10), color=color.rgb(100, 100, 150))
    
    # Castle walls
    wall_positions = [
        (20, 2.5, 0), (-20, 2.5, 0), (0, 2.5, 20)
    ]
    for pos in wall_positions:
        wall = Entity(model='cube', scale=(1, 5, 40) if abs(pos[0]) > 0 else (40, 5, 1), 
                     position=pos, texture='brick', texture_scale=(2, 2), collider='box')
    
    # Castle towers
    tower_positions = [
        (18, 5, 18), (-18, 5, 18), (18, 5, -18), (-18, 5, -18)
    ]
    for pos in tower_positions:
        tower = Entity(model='cube', scale=(3, 10, 3), position=pos, color=color.pink, collider='box')
    
    # Main castle structure
    castle = Entity(model='cube', scale=(15, 8, 15), position=(0, 4, 0), 
                   texture='brick', texture_scale=(2, 2), collider='box')
    
    # Castle roof
    castle_roof = Entity(model='cube', scale=(16, 10, 16), position=(0, 10, 0), color=color.red)
    
    # Space portal (replacing the entrance)
    space_portal = Entity(model='cylinder', scale=(5, 0.1, 5), position=(0, 1, -20), 
                         color=color.cyan, collider='mesh')
    space_objects.append(space_portal)
    
    # Platforms for platforming
    platforms = []
    platform_positions = [
        (5, 3, 5), (-5, 3, 5), (5, 3, -5), (-5, 3, -5),
        (0, 6, 0), (10, 6, 10), (-10, 6, 10), (10, 6, -10), (-10, 6, -10),
        (0, 9, 0), (15, 12, 15), (-15, 12, 15), (15, 12, -15), (-15, 12, -15)
    ]
    
    for pos in platform_positions:
        platform = Entity(model='cube', scale=(4, 0.5, 4), position=pos, 
                         color=color.rgb(200, 150, 150), collider='box')
        platforms.append(platform)
    
    # Create space environment outside the castle
    create_space_environment()
    
    return ground, platforms, space_portal

def create_space_environment():
    # Space skybox
    global space_skybox
    space_skybox = Entity(model='sphere', double_sided=True, scale=500, texture='sky_default')
    space_skybox.enabled = False
    
    # Space platforms
    for i in range(20):
        platform = Entity(
            model='cube', 
            scale=(random.uniform(3, 8), 0.5, random.uniform(3, 8)),
            position=(
                random.uniform(-100, 100),
                random.uniform(5, 50),
                random.uniform(-100, 100)
            ),
            color=color.rgb(
                random.randint(100, 200),
                random.randint(100, 200),
                random.randint(100, 200)
            ),
            collider='box'
        )
        space_objects.append(platform)
    
    # Floating asteroids
    for i in range(30):
        asteroid = Entity(
            model='sphere',
            scale=random.uniform(1, 5),
            position=(
                random.uniform(-150, 150),
                random.uniform(10, 80),
                random.uniform(-150, 150)
            ),
            color=color.rgb(
                random.randint(50, 150),
                random.randint(50, 150),
                random.randint(50, 150)
            ),
            collider='sphere'
        )
        space_objects.append(asteroid)
    
    # Black holes (hazard)
    for i in range(3):
        black_hole = Entity(
            model='sphere',
            scale=random.uniform(3, 8),
            position=(
                random.uniform(-120, 120),
                random.uniform(20, 60),
                random.uniform(-120, 120)
            ),
            color=color.black,
            collider='sphere'
        )
        black_holes.append(black_hole)
        space_objects.append(black_hole)
    
    # Warp zones
    for i in range(2):
        warp_zone = Entity(
            model='cylinder',
            scale=(5, 0.2, 5),
            position=(
                random.uniform(-100, 100),
                random.uniform(10, 40),
                random.uniform(-100, 100)
            ),
            color=color.magenta,
            collider='mesh'
        )
        warp_zones.append(warp_zone)
        space_objects.append(warp_zone)
    
    # Gravitational fields (visual effect only)
    for i in range(5):
        field = Entity(
            model='sphere',
            scale=random.uniform(10, 20),
            position=(
                random.uniform(-130, 130),
                random.uniform(30, 70),
                random.uniform(-130, 130)
            ),
            color=color.rgba(0, 100, 200, 50),
            alpha=0.2
        )
        gravitational_fields.append(field)
        space_objects.append(field)

# Enhanced Player class with space mechanics
class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.model = 'cube'
        self.color = color.red
        self.scale = (1, 2, 1)
        self.position = (0, 5, 0)
        self.rotation = (0, 0, 0)
        
        self.collider = 'box'
        self.speed = 5
        self.jump_height = 8
        self.jumping = False
        self.velocity_y = 0
        self.gravity = 20
        self.air_time = 0
        self.wall_sliding = False
        
        # Space mechanics
        self.space_gravity = 5
        self.space_jump_strength = 12
        self.space_movement_speed = 8
        self.is_in_space = False
        
        # Camera setup for third-person view
        camera.parent = self
        camera.position = (0, 2, -6)
        camera.rotation = (0, 0, 0)
        
        # HackerSM64 features
        self.double_jump_available = True
        self.wall_jump_available = False
        self.wall_jump_direction = Vec3(0, 0, 0)
        
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def update(self):
        if state != PLAYING:
            return
            
        # Check if player entered space
        self.check_space_transition()
            
        # Movement - different physics in space
        if self.is_in_space:
            self.handle_space_movement()
        else:
            self.handle_normal_movement()
    
    def check_space_transition(self):
        global in_space, current_section
        # Check if player entered the space portal
        if self.intersects(space_portal).hit and not self.is_in_space:
            self.enter_space()
        
        # Check if player is returning to castle
        if self.is_in_space and self.y < -10:
            self.exit_space()
    
    def enter_space(self):
        global in_space, current_section
        self.is_in_space = True
        in_space = True
        current_section = "space_world"
        location_text.text = "Location: Space World"
        
        # Enable space environment
        space_skybox.enabled = True
        for obj in space_objects:
            obj.enabled = True
        
        # Position player in space
        self.position = (0, 30, 0)
        self.velocity_y = 0
    
    def exit_space(self):
        global in_space, current_section
        self.is_in_space = False
        in_space = False
        current_section = "castle"
        location_text.text = "Location: Peach's Castle"
        
        # Disable space environment
        space_skybox.enabled = False
        for obj in space_objects:
            obj.enabled = False
        
        # Position player back in castle
        self.position = (0, 5, 0)
        self.velocity_y = 0
    
    def handle_normal_movement(self):
        # Standard movement logic
        direction = Vec3(0, 0, 0)
        if held_keys['w']:
            direction += Vec3(0, 0, 1)
        if held_keys['s']:
            direction += Vec3(0, 0, -1)
        if held_keys['a']:
            direction += Vec3(-1, 0, 0)
        if held_keys['d']:
            direction += Vec3(1, 0, 0)
            
        if direction.length() > 0:
            direction = direction.normalized()
            
        self.position += direction * self.speed * time.dt
        
        # Camera control with mouse
        if HACKER_SM64_CONFIG["puppycam_enabled"]:
            self.rotation_y += mouse.velocity[0] * 40 * time.dt
            camera.rotation_x -= mouse.velocity[1] * 40 * time.dt
            camera.rotation_x = clamp(camera.rotation_x, -90, 90)
        else:
            self.rotation_y = mouse.position[0] * 100
        
        # Jumping and gravity
        if self.gravity:
            # Raycast to check if on ground
            ray = raycast(self.position, Vec3(0, -1, 0), ignore=[self], distance=1.1)
            
            if ray.hit:
                self.velocity_y = 0
                self.jumping = False
                self.air_time = 0
                self.double_jump_available = True
                self.wall_sliding = False
                if held_keys['space']:
                    self.velocity_y = self.jump_height
                    self.jumping = True
            else:
                self.velocity_y -= self.gravity * time.dt
                self.air_time += time.dt
                
                # Wall sliding and wall jump detection
                if HACKER_SM64_CONFIG["improved_collision"] and self.air_time > 0.2:
                    left_ray = raycast(self.position, Vec3(-1, 0, 0), ignore=[self], distance=0.6)
                    right_ray = raycast(self.position, Vec3(1, 0, 0), ignore=[self], distance=0.6)
                    front_ray = raycast(self.position, Vec3(0, 0, 1), ignore=[self], distance=0.6)
                    back_ray = raycast(self.position, Vec3(0, 0, -1), ignore=[self], distance=0.6)
                    
                    if left_ray.hit or right_ray.hit or front_ray.hit or back_ray.hit:
                        self.wall_sliding = True
                        self.velocity_y = max(self.velocity_y, -2)  # Reduce falling speed when wall sliding
                        
                        # Set wall jump direction
                        if left_ray.hit:
                            self.wall_jump_direction = Vec3(1, 1, 0).normalized()
                        elif right_ray.hit:
                            self.wall_jump_direction = Vec3(-1, 1, 0).normalized()
                        elif front_ray.hit:
                            self.wall_jump_direction = Vec3(0, 1, -1).normalized()
                        elif back_ray.hit:
                            self.wall_jump_direction = Vec3(0, 1, 1).normalized()
                            
                        self.wall_jump_available = True
                    else:
                        self.wall_sliding = False
                        self.wall_jump_available = False
                
                # Double jump
                if HACKER_SM64_CONFIG["improved_collision"] and self.double_jump_available and held_keys['space'] and self.air_time > 0.2:
                    self.velocity_y = self.jump_height * 0.8
                    self.double_jump_available = False
                
                # Wall jump
                if HACKER_SM64_CONFIG["improved_collision"] and self.wall_jump_available and held_keys['space']:
                    self.velocity_y = self.jump_height
                    self.position += self.wall_jump_direction * 1.5
                    self.wall_jump_available = False
                
            self.y += self.velocity_y * time.dt
    
    def handle_space_movement(self):
        # Space movement - full 3D movement with reduced gravity
        direction = Vec3(0, 0, 0)
        if held_keys['w']:
            direction += Vec3(0, 0, 1)
        if held_keys['s']:
            direction += Vec3(0, 0, -1)
        if held_keys['a']:
            direction += Vec3(-1, 0, 0)
        if held_keys['d']:
            direction += Vec3(1, 0, 0)
            
        # Vertical movement in space
        if held_keys['space']:
            direction += Vec3(0, 1, 0)
        if held_keys['shift']:
            direction += Vec3(0, -1, 0)
            
        if direction.length() > 0:
            direction = direction.normalized()
            
        self.position += direction * self.space_movement_speed * time.dt
        
        # Camera control with mouse
        if HACKER_SM64_CONFIG["puppycam_enabled"]:
            self.rotation_y += mouse.velocity[0] * 40 * time.dt
            camera.rotation_x -= mouse.velocity[1] * 40 * time.dt
            camera.rotation_x = clamp(camera.rotation_x, -90, 90)
        
        # Minimal gravity in space
        self.velocity_y -= self.space_gravity * time.dt
        self.y += self.velocity_y * time.dt
        
        # Check for black hole collisions
        for black_hole in black_holes:
            if self.intersects(black_hole).hit:
                # Pull player towards black hole center
                direction_to_center = (black_hole.position - self.position).normalized()
                self.position += direction_to_center * 5 * time.dt
                
                # Damage player
                global lives
                lives -= 1
                lives_text.text = f"Lives: {lives}"
                
                if lives <= 0:
                    global state
                    state = GAME_OVER
                    message_text.text = "GAME OVER! Try again!"
                    message_text.color = color.red
        
        # Check for warp zone collisions
        for warp_zone in warp_zones:
            if self.intersects(warp_zone).hit:
                # Teleport player to random location in space
                self.position = (
                    random.uniform(-100, 100),
                    random.uniform(20, 60),
                    random.uniform(-100, 100)
                )
                self.velocity_y = 0
                message_text.text = "Warped to new location!"
                message_text.color = color.magenta
                invoke(set_message_default, delay=2)

# Create coins with different types for castle and space
def create_coins():
    coins = []
    # Castle coins
    for i in range(10):
        x = random.uniform(-15, 15)
        z = random.uniform(-15, 15)
        y = random.uniform(2, 10)
        
        coin_color = color.black if HACKER_SM64_CONFIG["silhouette_effect"] else color.yellow
        coin = Entity(
            model='sphere', 
            scale=0.5, 
            position=(x, y, z),
            color=coin_color,
            collider='sphere'
        )
        coins.append(coin)
    
    # Space coins
    for i in range(5):
        x = random.uniform(-80, 80)
        z = random.uniform(-80, 80)
        y = random.uniform(20, 60)
        
        coin = Entity(
            model='sphere', 
            scale=0.7, 
            position=(x, y, z),
            color=color.cyan,
            collider='sphere',
            enabled=False
        )
        coins.append(coin)
        space_objects.append(coin)
    
    return coins

# Create the goal (crown)
def create_goal():
    crown = Entity(
        model='cube', 
        scale=(2, 0.5, 2), 
        position=(0, 12, 0),
        color=color.yellow,
        collider='box'
    )
    return crown

# Setup the scene
ground, platforms, space_portal = create_space_world()
player = Player()
coins = create_coins()
crown = create_goal()

# Add some decorative elements
decorations = []
for i in range(15):
    tree = Entity(
        model='cube', 
        scale=(0.5, random.uniform(2, 4), 0.5), 
        position=(random.uniform(-18, 18), 0, random.uniform(-18, 18)),
        color=color.green
    )
    decorations.append(tree)

# UI Elements
coins_text = Text(text=f"Coins: {coins_collected}/{total_coins}", position=(-0.8, 0.45), scale=2, enabled=False)
lives_text = Text(text=f"Lives: {lives}", position=(-0.8, 0.4), scale=2, enabled=False)
score_text = Text(text=f"Score: {player_score}", position=(-0.8, 0.35), scale=2, enabled=False)
message_text = Text(text="Collect all coins and reach the crown!", position=(-0.7, 0.3), scale=2, enabled=False)
camera_mode_text = Text(text=f"Camera: {camera_mode}", position=(0.7, 0.45), scale=1.5, enabled=False)
location_text = Text(text="Location: Peach's Castle", position=(-0.8, 0.5), scale=1.5, enabled=False)

# Create main menu and options menu
menu_elements = create_main_menu()
options_menu_elements = create_options_menu()
options_menu_visible = False
for element in options_menu_elements:
    element.enabled = False

# Game update function
def update():
    global coins_collected, lives, player_score, state
    
    if state == PLAYING:
        # Check for coin collisions
        for coin in coins[:]:
            if player.intersects(coin).hit:
                coins.remove(coin)
                destroy(coin)
                coins_collected += 1
                player_score += 100
                coins_text.text = f"Coins: {coins_collected}/{total_coins}"
                score_text.text = f"Score: {player_score}"
                
                # HackerSM64 nonstop stars feature
                if HACKER_SM64_CONFIG["nonstop_stars"] and coins_collected % 5 == 0:
                    message_text.text = f"Collected {coins_collected} coins! Keep going!"
                    message_text.color = color.yellow
                    invoke(set_message_default, delay=2)
                
        # Check for crown collision
        if player.intersects(crown).hit and coins_collected >= total_coins:
            state = VICTORY
            message_text.text = "VICTORY! You rescued Princess Peach!"
            message_text.color = color.gold
            
        # Check for falling off the map with HackerSM64 fall damage option
        if not player.is_in_space and player.y < -10:
            player.position = (0, 5, 0)
            
            if HACKER_SM64_CONFIG["fall_damage"]:
                lives -= 1
                lives_text.text = f"Lives: {lives}"
            
            if lives <= 0:
                state = GAME_OVER
                message_text.text = "GAME OVER! Try again!"
                message_text.color = color.red

def set_message_default():
    message_text.text = "Collect all coins and reach the crown!"
    message_text.color = color.white

# Input handling for resetting the game and camera controls
def input(key):
    global state, coins_collected, lives, player_score, coins, camera_mode
    
    if state != PLAYING:
        return
        
    if key == 'r':
        state = PLAYING
        coins_collected = 0
        lives = 3
        player_score = 0
        player.position = (0, 5, 0)
        player.is_in_space = False
        player.exit_space()
        
        # Recreate coins
        for coin in coins:
            destroy(coin)
        coins = create_coins()
        
        # Update UI
        coins_text.text = f"Coins: {coins_collected}/{total_coins}"
        lives_text.text = f"Lives: {lives}"
        score_text.text = f"Score: {player_score}"
        message_text.text = "Collect all coins and reach the crown!"
        message_text.color = color.white
        
    if key == 'escape':
        # Return to menu
        state = MENU
        for element in menu_elements:
            element.enabled = True
        coins_text.enabled = False
        lives_text.enabled = False
        score_text.enabled = False
        message_text.enabled = False
        camera_mode_text.enabled = False
        location_text.enabled = False
        
    # HackerSM64 camera controls
    if key == 'c':
        camera_modes = ["follow", "fixed", "mario", "free"]
        current_index = camera_modes.index(camera_mode)
        camera_mode = camera_modes[(current_index + 1) % len(camera_modes)]
        camera_mode_text.text = f"Camera: {camera_mode}"
        
        if camera_mode == "follow":
            camera.parent = player
            camera.position = (0, 2, -6)
        elif camera_mode == "fixed":
            camera.parent = scene
            camera.position = (0, 15, -20)
            camera.rotation_x = -30
        elif camera_mode == "mario":
            camera.parent = player
            camera.position = (0, 1, 0)
        elif camera_mode == "free":
            camera.parent = scene
            camera.position = (0, 10, -10)

# Run the game
app.run()
