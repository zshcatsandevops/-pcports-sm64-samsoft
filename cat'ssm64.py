#!/usr/bin/env python3
# ULTRA MARIO 3D BROS - Peach's Castle Hub World with HackerSM64 Features
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import math

app = Ursina()
window.title = "ULTRA MARIO 3D BROS - Peach's Castle Hub (HackerSM64 Edition)"
window.size = (1280, 720)  # Widescreen support
window.borderless = False
window.fullscreen = False
window.exit_button.visible = True

# Game states
MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"
VICTORY = "victory"
HUB_WORLD = "hub_world"
state = MENU

# Game variables
stars_collected = 0
total_stars = 6
lives = 3
player_score = 0
camera_mode = "follow"  # HackerSM64-style camera modes: follow, fixed, mario, free
current_world = "castle_grounds"

# HackerSM64 Configuration
HACKER_SM64_CONFIG = {
    "extended_bounds": True,
    "puppycam_enabled": True,
    "silhouette_effect": False,
    "improved_collision": True,
    "fall_damage": False,
    "nonstop_stars": False,
    "level_unlocks": True
}

# Create main menu with HackerSM64 options
def create_main_menu():
    # Title
    title = Text(text="ULTRA MARIO 3D BROS", scale=3, position=(0, 0.3), origin=(0, 0))
    subtitle = Text(text="Peach's Castle Hub World", scale=1.5, position=(0, 0.1), origin=(0, 0))
    edition = Text(text="HackerSM64 Edition", scale=1.2, position=(0, -0.05), origin=(0, 0), color=color.yellow)
    
    # Start button
    start_button = Button(text='Start Game', color=color.red, scale=(0.3, 0.1), position=(0, -0.2))
    start_button.on_click = start_game
    
    # Options button
    options_button = Button(text='HackerSM64 Options', color=color.blue, scale=(0.3, 0.1), position=(0, -0.35))
    options_button.on_click = toggle_options_menu
    
    # Quit button
    quit_button = Button(text='Quit', color=color.gray, scale=(0.3, 0.1), position=(0, -0.5))
    quit_button.on_click = application.quit
    
    # Copyright text
    copyright_text = Text(text="© 2023 ULTRA MARIO 3D BROS | HackerSM64 Features", scale=0.8, position=(0, -0.6), origin=(0, 0))
    
    return [title, subtitle, edition, start_button, options_button, quit_button, copyright_text]

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
    
    level_unlocks_toggle = Button(text='Level Unlocks: ON', color=color.green, scale=(0.3, 0.07), position=(0, -0.2))
    level_unlocks_toggle.on_click = lambda: toggle_setting('level_unlocks', level_unlocks_toggle)
    
    back_button = Button(text='Back', color=color.orange, scale=(0.3, 0.07), position=(0, -0.35))
    back_button.on_click = toggle_options_menu
    
    return [options_bg, options_title, extended_bounds_toggle, puppycam_toggle, 
            silhouette_toggle, collision_toggle, level_unlocks_toggle, back_button]

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
    state = HUB_WORLD
    # Hide menu elements
    for element in menu_elements:
        element.enabled = False
    # Enable game UI
    stars_text.enabled = True
    lives_text.enabled = True
    score_text.enabled = True
    message_text.enabled = True
    camera_mode_text.enabled = True
    world_text.enabled = True

# Create Peach's Castle hub world with extended bounds
def create_peach_castle_hub():
    # Ground with castle courtyard texture
    ground_size = 80 if HACKER_SM64_CONFIG["extended_bounds"] else 60
    ground = Entity(model='plane', scale=(ground_size, 1, ground_size), 
                   texture='white_cube', texture_scale=(20, 20), 
                   color=color.rgb(150, 200, 255))
    
    # Castle walls with battlements
    wall_distance = 35 if HACKER_SM64_CONFIG["extended_bounds"] else 25
    wall_height = 8
    wall_thickness = 2
    
    # Main castle walls
    walls = []
    for i in range(4):
        angle = i * 90
        x = math.cos(math.radians(angle)) * wall_distance
        z = math.sin(math.radians(angle)) * wall_distance
        
        wall_length = wall_distance * 2 if i % 2 == 0 else wall_distance * 2
        wall_scale = (wall_length, wall_height, wall_thickness) if i % 2 == 0 else (wall_thickness, wall_height, wall_length)
        
        wall = Entity(model='cube', scale=wall_scale, position=(x, wall_height/2, z), 
                     texture='brick', texture_scale=(4, 2), collider='box')
        walls.append(wall)
        
        # Add battlements on top
        battlement_count = int(wall_length / 4)
        for j in range(battlement_count):
            offset = -wall_length/2 + j * 4 + 2
            if i % 2 == 0:  # North/South walls
                battlement = Entity(model='cube', scale=(2, 2, 2), 
                                  position=(x + offset, wall_height + 1, z))
            else:  # East/West walls
                battlement = Entity(model='cube', scale=(2, 2, 2), 
                                  position=(x, wall_height + 1, z + offset))
            battlement.color = color.red
    
    # Castle towers
    tower_height = 15
    tower_positions = [
        (-wall_distance, tower_height/2, -wall_distance),
        (-wall_distance, tower_height/2, wall_distance),
        (wall_distance, tower_height/2, -wall_distance),
        (wall_distance, tower_height/2, wall_distance)
    ]
    
    for pos in tower_positions:
        tower = Entity(model='cube', scale=(4, tower_height, 4), position=pos, 
                      texture='brick', texture_scale=(1, 3), collider='box')
        # Tower roof
        roof = Entity(model='cone', scale=(5, 4, 5), position=(pos[0], tower_height, pos[2]), color=color.red)
    
    # Main castle structure
    castle_size = 20
    castle = Entity(model='cube', scale=(castle_size, 10, castle_size), 
                   position=(0, 5, 0), texture='brick', texture_scale=(2, 2), collider='box')
    
    # Castle roof
    castle_roof = Entity(model='pyramid', scale=(castle_size+2, 8, castle_size+2), 
                        position=(0, 10, 0), color=color.red)
    
    # Castle entrance (facing camera)
    entrance = Entity(model='cube', scale=(6, 8, 1), position=(0, 4, -wall_distance), 
                     color=color.brown, collider='box')
    
    # Water fountain in courtyard
    fountain_base = Entity(model='cylinder', scale=(3, 0.5, 3), position=(0, 0.5, 0), color=color.blue)
    fountain_center = Entity(model='cylinder', scale=(1, 2, 1), position=(0, 2, 0), color=color.light_gray)
    
    # Level entrances (paintings/doors) around the courtyard
    level_entrances = []
    
    # Bob-omb Battlefield entrance
    bobomb_entrance = Entity(model='cube', scale=(5, 6, 0.5), position=(-15, 3, -wall_distance + 1), 
                            color=color.green, collider='box')
    bobomb_sign = Text(text="BOB-OMB\nBATTLEFIELD", scale=1, position=(-15, 6, -wall_distance + 1), 
                      background=True, background_color=color.green)
    level_entrances.append(("bobomb_battlefield", bobomb_entrance))
    
    # Whomp's Fortress entrance
    whomp_entrance = Entity(model='cube', scale=(5, 6, 0.5), position=(15, 3, -wall_distance + 1), 
                           color=color.orange, collider='box')
    whomp_sign = Text(text="WHOMP'S\nFORTRESS", scale=1, position=(15, 6, -wall_distance + 1), 
                     background=True, background_color=color.orange)
    level_entrances.append(("whomps_fortress", whomp_entrance))
    
    # Jolly Roger Bay entrance
    jolly_entrance = Entity(model='cube', scale=(5, 6, 0.5), position=(-wall_distance + 1, 3, -15), 
                           color=color.blue, collider='box')
    jolly_sign = Text(text="JOLLY ROGER\nBAY", scale=1, position=(-wall_distance + 1, 6, -15), 
                     background=True, background_color=color.blue)
    level_entrances.append(("jolly_roger_bay", jolly_entrance))
    
    # Cool, Cool Mountain entrance
    cool_entrance = Entity(model='cube', scale=(5, 6, 0.5), position=(-wall_distance + 1, 3, 15), 
                          color=color.white, collider='box')
    cool_sign = Text(text="COOL, COOL\nMOUNTAIN", scale=1, position=(-wall_distance + 1, 6, 15), 
                    background=True, background_color=color.white)
    level_entrances.append(("cool_cool_mountain", cool_entrance))
    
    # Platforms and obstacles for platforming
    platforms = []
    
    # Central platform pyramid
    for i in range(3):
        platform = Entity(model='cube', scale=(8-i*2, 1, 8-i*2), 
                         position=(0, 2 + i*3, 0), color=color.rgb(200, 150, 150), collider='box')
        platforms.append(platform)
    
    # Floating platforms around courtyard
    platform_positions = [
        (-10, 5, -10), (10, 5, -10), (-10, 5, 10), (10, 5, 10),
        (-20, 8, 0), (20, 8, 0), (0, 8, -20), (0, 8, 20),
        (-15, 12, -15), (15, 12, -15), (-15, 12, 15), (15, 12, 15)
    ]
    
    for pos in platform_positions:
        platform = Entity(model='cube', scale=(3, 0.5, 3), position=pos, 
                         color=color.rgb(180, 120, 120), collider='box')
        platforms.append(platform)
    
    return ground, walls, level_entrances, platforms

# Enhanced Player class with HackerSM64 features
class MarioPlayer(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.model = 'cube'
        self.color = color.red
        self.scale = (1, 2, 1)
        self.position = (0, 5, 0)
        self.rotation = (0, 0, 0)
        
        self.collider = 'box'
        self.speed = 6
        self.jump_height = 10
        self.jumping = False
        self.velocity_y = 0
        self.gravity = 25
        self.air_time = 0
        self.wall_sliding = False
        
        # Mario state
        self.powerup_state = "small"  # small, big, cape, metal
        self.is_crouching = False
        self.is_sliding = False
        self.is_long_jumping = False
        
        # Camera setup for third-person view
        camera.parent = self
        camera.position = (0, 2, -8)
        camera.rotation = (0, 0, 0)
        
        # HackerSM64 features
        self.double_jump_available = True
        self.wall_jump_available = False
        self.wall_jump_direction = Vec3(0, 0, 0)
        self.triple_jump_ready = False
        self.triple_jump_count = 0
        
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def update(self):
        if state != HUB_WORLD and state != PLAYING:
            return
            
        # Movement with HackerSM64 enhancements
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
            
        # Apply movement with momentum
        move_speed = self.speed
        if self.is_sliding:
            move_speed *= 1.5
            
        self.position += direction * move_speed * time.dt
        
        # Camera control with mouse (HackerSM64 puppycam)
        if HACKER_SM64_CONFIG["puppycam_enabled"]:
            self.rotation_y += mouse.velocity[0] * 40 * time.dt
            camera.rotation_x -= mouse.velocity[1] * 40 * time.dt
            camera.rotation_x = clamp(camera.rotation_x, -90, 90)
        else:
            self.rotation_y = mouse.position[0] * 100
        
        # Jumping and gravity with HackerSM64 enhancements
        if self.gravity:
            # Raycast to check if on ground
            ray = raycast(self.position, Vec3(0, -1, 0), ignore=[self], distance=1.1)
            
            if ray.hit:
                self.velocity_y = 0
                self.jumping = False
                self.air_time = 0
                self.double_jump_available = True
                self.wall_sliding = False
                self.triple_jump_count = 0
                
                # Ground pound recovery
                if self.velocity_y < -20:
                    create_ground_pound_effect(self.position)
                
                # Jump input
                if held_keys['space']:
                    self.velocity_y = self.jump_height
                    self.jumping = True
                    self.triple_jump_count = 1
            else:
                # Apply gravity
                self.velocity_y -= self.gravity * time.dt
                self.air_time += time.dt
                
                # Wall sliding and wall jump detection
                if HACKER_SM64_CONFIG["improved_collision"] and self.air_time > 0.2:
                    left_ray = raycast(self.position, Vec3(-1, 0, 0), ignore=[self], distance=0.6)
                    right_ray = raycast(self.position, Vec3(1, 0, 0), ignore=[self], distance=0.6)
                    front_ray = raycast(self.position, Vec3(0, 0, 1), ignore=[self], distance=0.6)
                    back_ray = raycast(self.position, Vec3(0, 0, -1), ignore=[self], distance=0.6)
                    
                    wall_hit = left_ray.hit or right_ray.hit or front_ray.hit or back_ray.hit
                    
                    if wall_hit:
                        self.wall_sliding = True
                        self.velocity_y = max(self.velocity_y, -3)  # Reduce falling speed when wall sliding
                        
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
                    self.triple_jump_count = 2
                
                # Triple jump (HackerSM64 feature)
                if HACKER_SM64_CONFIG["improved_collision"] and self.triple_jump_count == 2 and held_keys['space'] and self.air_time > 0.4:
                    self.velocity_y = self.jump_height * 1.2
                    self.triple_jump_count = 3
                    create_triple_jump_effect(self.position)
                
                # Wall jump
                if HACKER_SM64_CONFIG["improved_collision"] and self.wall_jump_available and held_keys['space']:
                    self.velocity_y = self.jump_height
                    self.position += self.wall_jump_direction * 2
                    self.wall_jump_available = False
                    create_wall_jump_effect(self.position)
                
                # Ground pound (HackerSM64 feature)
                if held_keys['left shift'] and self.velocity_y > -10:
                    self.velocity_y = -20  # Fast fall
                
            self.y += self.velocity_y * time.dt
            
        # Long jump (HackerSM64 feature)
        if held_keys['left control'] and held_keys['space'] and not self.jumping:
            self.velocity_y = self.jump_height * 0.7
            self.position += self.forward * 3  # Boost forward
            self.jumping = True
            self.is_long_jumping = True

def create_ground_pound_effect(position):
    # Create a shockwave effect
    shockwave = Entity(model='circle', scale=0.1, position=position, color=color.white)
    shockwave.animate_scale((5, 5), duration=0.5, curve=curve.out_quad)
    shockwave.animate_color(color.clear, duration=0.5)
    destroy(shockwave, delay=0.5)

def create_triple_jump_effect(position):
    # Create sparkle effect for triple jump
    for i in range(5):
        sparkle = Entity(model='sphere', scale=0.2, position=position, color=color.yellow)
        sparkle.animate_position(
            (position[0] + random.uniform(-2, 2), 
             position[1] + random.uniform(2, 5), 
             position[2] + random.uniform(-2, 2)), 
            duration=1
        )
        sparkle.animate_scale(0, duration=1)
        destroy(sparkle, delay=1)

def create_wall_jump_effect(position):
    # Create dust effect for wall jump
    dust = Entity(model='circle', scale=0.5, position=position, color=color.gray)
    dust.animate_scale((2, 2), duration=0.3)
    dust.animate_color(color.clear, duration=0.3)
    destroy(dust, delay=0.3)

# Create stars for the hub world
def create_stars():
    stars = []
    star_positions = [
        (0, 15, 0),           # Top of pyramid
        (-20, 10, 0),         # West platform
        (20, 10, 0),          # East platform
        (0, 10, -20),         # North platform
        (0, 10, 20),          # South platform
        (0, 20, 0),           # Very high platform
        (15, 15, 15),         # SE high platform
        (-15, 15, -15),       # NW high platform
    ]
    
    for i, pos in enumerate(star_positions):
        if i < total_stars:  # Only create the defined number of stars
            star_color = color.black if HACKER_SM64_CONFIG["silhouette_effect"] else color.yellow
            star = Entity(
                model='sphere', 
                scale=0.8, 
                position=pos,
                color=star_color,
                collider='sphere'
            )
            # Add a spinning animation to the star
            star.animate_rotation((0, 360, 0), duration=2, loop=True)
            stars.append(star)
    
    return stars

# Create level content for demonstration
def create_demo_level(level_name):
    # Create a simple themed level based on the name
    ground = Entity(model='plane', scale=(30, 1, 30), texture='white_cube', texture_scale=(5, 5))
    
    if level_name == "bobomb_battlefield":
        ground.color = color.green
        # Add some simple obstacles
        for i in range(5):
            obstacle = Entity(model='cube', scale=(2, 2, 2), 
                            position=(random.uniform(-10, 10), 1, random.uniform(-10, 10)),
                            color=color.gray, collider='box')
    elif level_name == "whomps_fortress":
        ground.color = color.orange
        # Create a fortress-like structure
        fortress = Entity(model='cube', scale=(10, 5, 10), position=(0, 2.5, 0), 
                         color=color.gray, collider='box')
    elif level_name == "jolly_roger_bay":
        ground.color = color.blue
        # Add water effect
        water = Entity(model='plane', scale=(25, 1, 25), position=(0, 0.1, 0), 
                      color=color.blue, alpha=0.7)
    elif level_name == "cool_cool_mountain":
        ground.color = color.white
        # Add snow piles
        for i in range(3):
            snow = Entity(model='sphere', scale=(3, 1, 3), 
                         position=(random.uniform(-10, 10), 0.5, random.uniform(-10, 10)),
                         color=color.white)
    
    return ground

# Setup the scene
ground, walls, level_entrances, platforms = create_peach_castle_hub()
player = MarioPlayer()
stars = create_stars()

# Add decorative elements
decorations = []
for i in range(20):
    # Trees and bushes around the courtyard
    tree_pos = (
        random.uniform(-30, 30),
        0,
        random.uniform(-30, 30)
    )
    # Only place trees outside the central area
    if abs(tree_pos[0]) > 10 or abs(tree_pos[2]) > 10:
        tree_trunk = Entity(model='cylinder', scale=(0.5, 2, 0.5), 
                           position=tree_pos, color=color.brown)
        tree_top = Entity(model='sphere', scale=(2, 2, 2), 
                         position=(tree_pos[0], 3, tree_pos[2]), color=color.green)
        decorations.extend([tree_trunk, tree_top])

# UI Elements
stars_text = Text(text=f"Stars: {stars_collected}/{total_stars}", position=(-0.8, 0.45), scale=2, enabled=False)
lives_text = Text(text=f"Lives: {lives}", position=(-0.8, 0.4), scale=2, enabled=False)
score_text = Text(text=f"Score: {player_score}", position=(-0.8, 0.35), scale=2, enabled=False)
message_text = Text(text="Explore Peach's Castle! Collect stars!", position=(-0.7, 0.3), scale=2, enabled=False)
camera_mode_text = Text(text=f"Camera: {camera_mode}", position=(0.7, 0.45), scale=1.5, enabled=False)
world_text = Text(text=f"World: {current_world.replace('_', ' ').title()}", position=(0.7, 0.4), scale=1.5, enabled=False)

# Create main menu and options menu
menu_elements = create_main_menu()
options_menu_elements = create_options_menu()
options_menu_visible = False
for element in options_menu_elements:
    element.enabled = False

# Game update function
def update():
    global stars_collected, lives, player_score, state, current_world
    
    if state == HUB_WORLD or state == PLAYING:
        # Check for star collisions
        for star in stars[:]:
            if player.intersects(star).hit:
                stars.remove(star)
                destroy(star)
                stars_collected += 1
                player_score += 100
                stars_text.text = f"Stars: {stars_collected}/{total_stars}"
                score_text.text = f"Score: {player_score}"
                
                # Play star collection sound effect (visual feedback for now)
                star_effect = Entity(model='sphere', scale=0.5, position=star.position, color=color.yellow)
                star_effect.animate_scale(3, duration=0.5)
                star_effect.animate_color(color.clear, duration=0.5)
                destroy(star_effect, delay=0.5)
                
                # HackerSM64 nonstop stars feature
                if HACKER_SM64_CONFIG["nonstop_stars"] and stars_collected % 3 == 0:
                    message_text.text = f"Collected {stars_collected} stars! Keep going!"
                    message_text.color = color.yellow
                    invoke(set_message_default, delay=2)
                
                # Check for victory condition
                if stars_collected >= total_stars:
                    state = VICTORY
                    message_text.text = "VICTORY! You've collected all the stars!"
                    message_text.color = color.gold
        
        # Check for level entrance collisions
        for level_name, entrance in level_entrances:
            if player.intersects(entrance).hit:
                if HACKER_SM64_CONFIG["level_unlocks"] and stars_collected >= 1:  # Require at least 1 star to enter levels
                    enter_level(level_name)
                elif not HACKER_SM64_CONFIG["level_unlocks"]:
                    enter_level(level_name)
                else:
                    message_text.text = "You need at least 1 star to enter this level!"
                    message_text.color = color.red
                    invoke(set_message_default, delay=2)
        
        # Check for falling off the map
        if player.y < -10:
            player.position = (0, 5, 0)
            player.velocity_y = 0
            
            if HACKER_SM64_CONFIG["fall_damage"]:
                lives -= 1
                lives_text.text = f"Lives: {lives}"
            
            if lives <= 0:
                state = GAME_OVER
                message_text.text = "GAME OVER! Try again!"
                message_text.color = color.red

def enter_level(level_name):
    global state, current_world
    state = PLAYING
    current_world = level_name
    world_text.text = f"World: {current_world.replace('_', ' ').title()}"
    message_text.text = f"Entering {level_name.replace('_', ' ').title()}!"
    message_text.color = color.green
    invoke(return_to_hub, delay=5)  # Return to hub after 5 seconds

def return_to_hub():
    global state, current_world
    state = HUB_WORLD
    current_world = "castle_grounds"
    world_text.text = f"World: {current_world.replace('_', ' ').title()}"
    message_text.text = "Welcome back to Peach's Castle!"
    message_text.color = color.white

def set_message_default():
    if state == HUB_WORLD:
        message_text.text = "Explore Peach's Castle! Collect stars!"
    elif state == PLAYING:
        message_text.text = f"Exploring {current_world.replace('_', ' ').title()}!"
    message_text.color = color.white

# Input handling
def input(key):
    global state, stars_collected, lives, player_score, stars, camera_mode, current_world
    
    if key == 'r':  # Reset game
        state = HUB_WORLD
        stars_collected = 0
        lives = 3
        player_score = 0
        current_world = "castle_grounds"
        player.position = (0, 5, 0)
        player.velocity_y = 0
        
        # Recreate stars
        for star in stars:
            destroy(star)
        stars = create_stars()
        
        # Update UI
        stars_text.text = f"Stars: {stars_collected}/{total_stars}"
        lives_text.text = f"Lives: {lives}"
        score_text.text = f"Score: {player_score}"
        world_text.text = f"World: {current_world.replace('_', ' ').title()}"
        set_message_default()
        
    if key == 'escape':  # Return to menu
        state = MENU
        for element in menu_elements:
            element.enabled = True
        stars_text.enabled = False
        lives_text.enabled = False
        score_text.enabled = False
        message_text.enabled = False
        camera_mode_text.enabled = False
        world_text.enabled = False
        
    # HackerSM64 camera controls
    if key == 'c':
        camera_modes = ["follow", "fixed", "mario", "free", "puppycam"]
        current_index = camera_modes.index(camera_mode)
        camera_mode = camera_modes[(current_index + 1) % len(camera_modes)]
        camera_mode_text.text = f"Camera: {camera_mode}"
        
        if camera_mode == "follow":
            camera.parent = player
            camera.position = (0, 2, -8)
            camera.rotation = (0, 0, 0)
        elif camera_mode == "fixed":
            camera.parent = scene
            camera.position = (0, 20, -30)
            camera.rotation_x = -30
        elif camera_mode == "mario":
            camera.parent = player
            camera.position = (0, 1, 0)
        elif camera_mode == "free":
            camera.parent = scene
            camera.position = (0, 15, -15)
        elif camera_mode == "puppycam":
            camera.parent = player
            camera.position = (0, 3, -10)
            HACKER_SM64_CONFIG["puppycam_enabled"] = True
    
    # HackerSM64 debug features
    if key == 'p':  # Add a star
        if state == HUB_WORLD:
            stars_collected += 1
            player_score += 100
            stars_text.text = f"Stars: {stars_collected}/{total_stars}"
            score_text.text = f"Score: {player_score}"
    
    if key == 'o':  # Toggle silhouette effect
        HACKER_SM64_CONFIG["silhouette_effect"] = not HACKER_SM64_CONFIG["silhouette_effect"]
        for star in stars:
            star.color = color.black if HACKER_SM64_CONFIG["silhouette_effect"] else color.yellow

# Run the game
app.run()
