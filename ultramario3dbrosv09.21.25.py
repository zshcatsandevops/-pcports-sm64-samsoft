#!/usr/bin/env python3
# ULTRA MARIO 3D BROS - Peach's Castle Tech Demo
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()
window.title = "ULTRA MARIO 3D BROS - Peach's Castle"
window.size = (800, 600)
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
total_coins = 10
lives = 3
player_score = 0

# Create main menu
def create_main_menu():
    # Title
    title = Text(text="ULTRA MARIO 3D BROS", scale=3, position=(0, 0.3), origin=(0, 0))
    subtitle = Text(text="Peach's Castle Adventure", scale=1.5, position=(0, 0.1), origin=(0, 0))
    
    # Start button
    start_button = Button(text='Start Game', color=color.red, scale=(0.3, 0.1), position=(0, -0.1))
    start_button.on_click = start_game
    
    # Quit button
    quit_button = Button(text='Quit', color=color.gray, scale=(0.3, 0.1), position=(0, -0.25))
    quit_button.on_click = application.quit
    
    # Copyright text
    copyright_text = Text(text="© 2023 ULTRA MARIO 3D BROS", scale=1, position=(0, -0.4), origin=(0, 0))
    
    return [title, subtitle, start_button, quit_button, copyright_text]

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

# Create Peach's Castle environment
def create_castle():
    # Ground
    ground = Entity(model='plane', scale=(50, 1, 50), texture='white_cube', 
                   texture_scale=(10, 10), color=color.rgb(200, 200, 200))
    
    # Castle walls
    wall_positions = [
        (20, 2.5, 0), (-20, 2.5, 0), (0, 2.5, 20), (0, 2.5, -20)
    ]
    for pos in wall_positions:
        wall = Entity(model='cube', scale=(1, 5, 40) if abs(pos[0]) > 0 else (40, 5, 1), 
                     position=pos, texture='brick', texture_scale=(2, 2), collider='box')
    
    # Castle towers - using cubes instead of cylinders
    tower_positions = [
        (18, 5, 18), (-18, 5, 18), (18, 5, -18), (-18, 5, -18)
    ]
    for pos in tower_positions:
        tower = Entity(model='cube', scale=(3, 10, 3), position=pos, color=color.pink, collider='box')
    
    # Main castle structure
    castle = Entity(model='cube', scale=(15, 8, 15), position=(0, 4, 0), 
                   texture='brick', texture_scale=(2, 2), collider='box')
    
    # Castle roof - using pyramid instead of cone
    castle_roof = Entity(model='cube', scale=(16, 10, 16), position=(0, 10, 0), color=color.red)
    
    # Entrance
    entrance = Entity(model='cube', scale=(5, 5, 1), position=(0, 2.5, -20), color=color.brown)
    
    # Platforms for platforming
    platforms = []
    platform_positions = [
        (5, 3, 5), (-5, 3, 5), (5, 3, -5), (-5, 3, -5),
        (0, 6, 0), (10, 6, 10), (-10, 6, 10), (10, 6, -10), (-10, 6, -10),
        (0, 9, 0)
    ]
    
    for pos in platform_positions:
        platform = Entity(model='cube', scale=(4, 0.5, 4), position=pos, 
                         color=color.rgb(200, 150, 150), collider='box')
        platforms.append(platform)
    
    return ground, platforms

# Create the player with third-person controller
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
        
        # Camera setup for third-person view
        camera.parent = self
        camera.position = (0, 2, -6)
        camera.rotation = (0, 0, 0)
        
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def update(self):
        if state != PLAYING:
            return
            
        # Movement
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
        self.rotation_y = mouse.position[0] * 100
        
        # Jumping and gravity
        if self.gravity:
            # Raycast to check if on ground
            ray = raycast(self.position, Vec3(0, -1, 0), ignore=[self], distance=1.1)
            
            if ray.hit:
                self.velocity_y = 0
                self.jumping = False
                if held_keys['space']:
                    self.velocity_y = self.jump_height
                    self.jumping = True
            else:
                self.velocity_y -= self.gravity * time.dt
                
            self.y += self.velocity_y * time.dt

# Create coins
def create_coins():
    coins = []
    for i in range(total_coins):
        x = random.uniform(-15, 15)
        z = random.uniform(-15, 15)
        y = random.uniform(2, 10)
        
        coin = Entity(
            model='sphere', 
            scale=0.5, 
            position=(x, y, z),
            color=color.yellow,
            collider='sphere'
        )
        coins.append(coin)
    
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
ground, platforms = create_castle()
player = Player()
coins = create_coins()
crown = create_goal()

# Add some decorative elements - using cubes instead of cylinders
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

# Create main menu
menu_elements = create_main_menu()

# Game update function
def update():
    global coins_collected, lives, player_score, state
    
    if state == PLAYING:
        # Check for coin collisions
        for coin in coins[:]:  # Use a slice copy to avoid modification during iteration
            if player.intersects(coin).hit:
                coins.remove(coin)
                destroy(coin)
                coins_collected += 1
                player_score += 100
                coins_text.text = f"Coins: {coins_collected}/{total_coins}"
                score_text.text = f"Score: {player_score}"
                
        # Check for crown collision
        if player.intersects(crown).hit and coins_collected >= total_coins:
            state = VICTORY
            message_text.text = "VICTORY! You rescued Princess Peach!"
            message_text.color = color.gold
            
        # Check for falling off the map
        if player.y < -10:
            player.position = (0, 5, 0)
            lives -= 1
            lives_text.text = f"Lives: {lives}"
            
            if lives <= 0:
                state = GAME_OVER
                message_text.text = "GAME OVER! Try again!"
                message_text.color = color.red

# Input handling for resetting the game
def input(key):
    global state, coins_collected, lives, player_score, coins
    
    if state != PLAYING:
        return
        
    if key == 'r':
        state = PLAYING
        coins_collected = 0
        lives = 3
        player_score = 0
        player.position = (0, 5, 0)
        
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

# Run the game
app.run()
