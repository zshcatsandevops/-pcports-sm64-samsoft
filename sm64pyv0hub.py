from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
import random
import math

app = Ursina()

# Set default shader for lighting
Entity.default_shader = lit_with_shadows_shader

# Game state management
class GameState:
    def __init__(self):
        self.current_level = "hub"
        self.stars_collected = 0
        self.total_stars = 0
        self.level_stars = {}
        
game_state = GameState()

# Enhanced Mario character model
class MarioCharacter(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = 'cube'
        self.color = color.red
        self.scale = (1, 1.5, 0.5)
        
        # Head
        self.head = Entity(
            model='sphere',
            color=color.rgb(255, 220, 177),
            scale=(0.8, 0.8, 0.8),
            position=(0, 0.8, 0),
            parent=self
        )
        
        # Hat
        self.hat = Entity(
            model='cube',
            color=color.red,
            scale=(0.9, 0.3, 0.9),
            position=(0, 1.2, 0),
            parent=self
        )
        
        # Eyes
        Entity(model='cube', color=color.black, scale=(0.15, 0.15, 0.1), position=(-0.2, 0.85, 0.4), parent=self)
        Entity(model='cube', color=color.black, scale=(0.15, 0.15, 0.1), position=(0.2, 0.85, 0.4), parent=self)
        
        # Mustache
        Entity(model='cube', color=color.brown, scale=(0.5, 0.1, 0.1), position=(0, 0.6, 0.4), parent=self)
        
        # Arms
        self.left_arm = Entity(model='cube', color=color.red, scale=(0.3, 0.8, 0.3), position=(-0.6, 0, 0), parent=self)
        self.right_arm = Entity(model='cube', color=color.red, scale=(0.3, 0.8, 0.3), position=(0.6, 0, 0), parent=self)
        
        # Hands
        Entity(model='sphere', color=color.white, scale=0.3, position=(-0.6, -0.5, 0), parent=self)
        Entity(model='sphere', color=color.white, scale=0.3, position=(0.6, -0.5, 0), parent=self)
        
        # Legs
        Entity(model='cube', color=color.blue, scale=(0.35, 0.7, 0.35), position=(-0.3, -0.9, 0), parent=self)
        Entity(model='cube', color=color.blue, scale=(0.35, 0.7, 0.35), position=(0.3, -0.9, 0), parent=self)
        
        # Shoes
        Entity(model='cube', color=color.brown, scale=(0.4, 0.2, 0.5), position=(-0.3, -1.3, 0.1), parent=self)
        Entity(model='cube', color=color.brown, scale=(0.4, 0.2, 0.5), position=(0.3, -1.3, 0.1), parent=self)

# Painting Portal Class
class PaintingPortal(Entity):
    def __init__(self, level_name, title, position, rotation=(0,0,0), **kwargs):
        super().__init__(
            model='cube',
            scale=(3, 4, 0.2),
            position=position,
            rotation=rotation,
            collider='box',
            **kwargs
        )
        self.level_name = level_name
        self.title = title
        
        # Frame
        Entity(model='cube', color=color.brown, scale=(3.3, 4.3, 0.1), position=position + Vec3(0, 0, 0.05), rotation=rotation)
        
        # Title plaque
        self.title_entity = Entity(
            model='cube',
            color=color.gold,
            scale=(2, 0.5, 0.1),
            position=position + Vec3(0, -2.5, 0.1),
            rotation=rotation
        )
        
        # Set painting texture/color based on level
        if level_name == "grassland":
            self.color = color.green
            self.texture = 'grass'
        elif level_name == "desert":
            self.color = color.rgb(255, 220, 100)
            self.texture = 'white_cube'
        elif level_name == "ice":
            self.color = color.cyan
            self.texture = 'white_cube'
        elif level_name == "lava":
            self.color = color.orange
            self.texture = 'brick'
        else:
            self.color = color.gray

# Hub World - Peach's Castle Interior
class HubWorld:
    def __init__(self):
        self.entities = []
        
    def create(self):
        # Castle floor
        floor = Entity(
            model='cube',
            scale=(40, 1, 40),
            color=color.rgb(200, 180, 160),
            texture='white_cube',
            texture_scale=(10, 10),
            collider='box'
        )
        self.entities.append(floor)
        
        # Castle walls
        for i in range(4):
            angle = i * 90
            wall = Entity(
                model='cube',
                scale=(40, 20, 2),
                position=(20 * math.sin(math.radians(angle)), 10, 20 * math.cos(math.radians(angle))),
                rotation=(0, angle, 0),
                color=color.rgb(180, 160, 140),
                texture='brick',
                texture_scale=(10, 5),
                collider='box'
            )
            self.entities.append(wall)
        
        # Ceiling
        ceiling = Entity(
            model='cube',
            scale=(40, 1, 40),
            position=(0, 20, 0),
            color=color.rgb(150, 130, 110),
            texture='white_cube'
        )
        self.entities.append(ceiling)
        
        # Central staircase
        for i in range(10):
            step = Entity(
                model='cube',
                scale=(8, 0.5, 2),
                position=(0, i * 0.5, -5 + i * 1),
                color=color.rgb(160, 140, 120),
                texture='brick',
                collider='box'
            )
            self.entities.append(step)
        
        # Upper platform
        platform = Entity(
            model='cube',
            scale=(20, 1, 20),
            position=(0, 5, 5),
            color=color.rgb(180, 160, 140),
            texture='white_cube',
            collider='box'
        )
        self.entities.append(platform)
        
        # Pillars
        pillar_positions = [(-10, 0, -10), (10, 0, -10), (-10, 0, 10), (10, 0, 10)]
        for pos in pillar_positions:
            pillar = Entity(
                model='cylinder',
                scale=(2, 10, 2),
                position=pos,
                color=color.rgb(200, 200, 200),
                texture='white_cube',
                collider='box'
            )
            self.entities.append(pillar)
        
        # Paintings (Portals to different worlds)
        self.painting1 = PaintingPortal(
            "grassland",
            "Bob-omb Battlefield",
            position=Vec3(-18, 8, 0),
            rotation=(0, 90, 0)
        )
        self.entities.append(self.painting1)
        
        self.painting2 = PaintingPortal(
            "desert",
            "Shifting Sand Land",
            position=Vec3(18, 8, 0),
            rotation=(0, -90, 0)
        )
        self.entities.append(self.painting2)
        
        self.painting3 = PaintingPortal(
            "ice",
            "Cool, Cool Mountain",
            position=Vec3(0, 8, -18),
            rotation=(0, 0, 0)
        )
        self.entities.append(self.painting3)
        
        self.painting4 = PaintingPortal(
            "lava",
            "Lethal Lava Land",
            position=Vec3(0, 13, 15),
            rotation=(0, 180, 0)
        )
        self.entities.append(self.painting4)
        
        # Decorative elements
        # Chandelier
        chandelier_base = Entity(
            model='cylinder',
            scale=(3, 0.5, 3),
            position=(0, 18, 0),
            color=color.gold
        )
        self.entities.append(chandelier_base)
        
        for i in range(8):
            angle = i * 45
            candle = Entity(
                model='cylinder',
                scale=(0.2, 1, 0.2),
                position=(2 * math.sin(math.radians(angle)), 17.5, 2 * math.cos(math.radians(angle))),
                color=color.yellow
            )
            self.entities.append(candle)
        
        # Info text
        self.info_text = Text(
            'Walk into paintings to enter levels! ESC to return to hub.',
            position=(-0.7, -0.45),
            scale=1.5,
            color=color.white,
            background=True
        )
        self.entities.append(self.info_text)
        
        return self.entities
    
    def destroy(self):
        for entity in self.entities:
            if hasattr(entity, 'disable'):
                entity.disable()
            destroy(entity)

# Level Base Class
class Level:
    def __init__(self, name):
        self.name = name
        self.entities = []
        self.stars = []
        self.collected_stars = 0
        
    def create(self):
        raise NotImplementedError
        
    def destroy(self):
        for entity in self.entities:
            destroy(entity)
        for star in self.stars:
            destroy(star)

# Grassland Level
class GrasslandLevel(Level):
    def create(self):
        # Ground
        ground = Entity(
            model='plane',
            scale=64,
            texture='grass',
            texture_scale=(8, 8),
            color=color.green,
            collider='box'
        )
        self.entities.append(ground)
        
        # Trees
        for i in range(20):
            tree_pos = Vec3(
                random.uniform(-25, 25),
                0,
                random.uniform(-25, 25)
            )
            
            # Tree trunk
            trunk = Entity(
                model='cylinder',
                scale=(1, 3, 1),
                position=tree_pos,
                color=color.brown,
                collider='box'
            )
            self.entities.append(trunk)
            
            # Tree leaves
            leaves = Entity(
                model='sphere',
                scale=3,
                position=tree_pos + Vec3(0, 4, 0),
                color=color.green
            )
            self.entities.append(leaves)
        
        # Platforms
        for i in range(15):
            platform = Entity(
                model='cube',
                scale=(random.uniform(3, 6), 1, random.uniform(3, 6)),
                position=(
                    random.uniform(-20, 20),
                    random.uniform(1, 8),
                    random.uniform(-20, 20)
                ),
                color=color.rgb(100, 200, 100),
                texture='grass',
                collider='box'
            )
            self.entities.append(platform)
        
        # Stars
        star_positions = [(10, 5, 10), (-15, 3, -10), (0, 10, 0)]
        for pos in star_positions:
            star = Entity(
                model='sphere',
                color=color.yellow,
                scale=0.8,
                position=pos,
                collider='sphere'
            )
            self.stars.append(star)
        
        # Exit portal
        self.exit_portal = Entity(
            model='cube',
            scale=(2, 3, 0.5),
            position=(0, 1.5, -30),
            color=color.purple,
            collider='box'
        )
        self.entities.append(self.exit_portal)
        
        return self.entities

# Desert Level
class DesertLevel(Level):
    def create(self):
        # Sandy ground
        ground = Entity(
            model='plane',
            scale=64,
            texture='white_cube',
            texture_scale=(8, 8),
            color=color.rgb(255, 220, 100),
            collider='box'
        )
        self.entities.append(ground)
        
        # Pyramids
        for i in range(3):
            pyramid_pos = Vec3(
                random.uniform(-20, 20),
                0,
                random.uniform(-20, 20)
            )
            
            for level in range(5):
                size = 10 - level * 2
                pyramid_level = Entity(
                    model='cube',
                    scale=(size, 1, size),
                    position=pyramid_pos + Vec3(0, level, 0),
                    color=color.rgb(220, 180, 80),
                    texture='brick',
                    collider='box'
                )
                self.entities.append(pyramid_level)
        
        # Cacti
        for i in range(10):
            cactus = Entity(
                model='cylinder',
                scale=(0.5, 2, 0.5),
                position=(
                    random.uniform(-25, 25),
                    1,
                    random.uniform(-25, 25)
                ),
                color=color.rgb(50, 150, 50),
                collider='box'
            )
            self.entities.append(cactus)
        
        # Stars
        star_positions = [(15, 8, 15), (-10, 5, -15), (0, 15, 0)]
        for pos in star_positions:
            star = Entity(
                model='sphere',
                color=color.yellow,
                scale=0.8,
                position=pos,
                collider='sphere'
            )
            self.stars.append(star)
        
        # Exit portal
        self.exit_portal = Entity(
            model='cube',
            scale=(2, 3, 0.5),
            position=(0, 1.5, -30),
            color=color.purple,
            collider='box'
        )
        self.entities.append(self.exit_portal)
        
        return self.entities

# Ice Level
class IceLevel(Level):
    def create(self):
        # Icy ground
        ground = Entity(
            model='plane',
            scale=64,
            texture='white_cube',
            texture_scale=(8, 8),
            color=color.cyan,
            collider='box'
        )
        self.entities.append(ground)
        
        # Ice blocks and platforms
        for i in range(20):
            ice_block = Entity(
                model='cube',
                scale=(random.uniform(2, 5), random.uniform(1, 3), random.uniform(2, 5)),
                position=(
                    random.uniform(-20, 20),
                    random.uniform(0, 5),
                    random.uniform(-20, 20)
                ),
                color=color.rgb(200, 230, 255),
                texture='white_cube',
                collider='box'
            )
            self.entities.append(ice_block)
        
        # Snowmen
        for i in range(5):
            snowman_pos = Vec3(
                random.uniform(-15, 15),
                0,
                random.uniform(-15, 15)
            )
            
            # Bottom
            Entity(
                model='sphere',
                scale=1.5,
                position=snowman_pos + Vec3(0, 0.75, 0),
                color=color.white,
                parent=self.entities[0]
            )
            
            # Middle
            Entity(
                model='sphere',
                scale=1,
                position=snowman_pos + Vec3(0, 2, 0),
                color=color.white,
                parent=self.entities[0]
            )
            
            # Head
            Entity(
                model='sphere',
                scale=0.7,
                position=snowman_pos + Vec3(0, 2.8, 0),
                color=color.white,
                parent=self.entities[0]
            )
        
        # Stars
        star_positions = [(12, 6, 8), (-8, 4, -12), (0, 8, 0)]
        for pos in star_positions:
            star = Entity(
                model='sphere',
                color=color.yellow,
                scale=0.8,
                position=pos,
                collider='sphere'
            )
            self.stars.append(star)
        
        # Exit portal
        self.exit_portal = Entity(
            model='cube',
            scale=(2, 3, 0.5),
            position=(0, 1.5, -30),
            color=color.purple,
            collider='box'
        )
        self.entities.append(self.exit_portal)
        
        return self.entities

# Lava Level
class LavaLevel(Level):
    def create(self):
        # Lava floor (deadly!)
        lava = Entity(
            model='plane',
            scale=64,
            texture='white_cube',
            texture_scale=(8, 8),
            color=color.orange,
            collider='box',
            y=-2
        )
        self.entities.append(lava)
        
        # Safe platforms
        for i in range(25):
            platform = Entity(
                model='cube',
                scale=(random.uniform(3, 5), 1, random.uniform(3, 5)),
                position=(
                    random.uniform(-25, 25),
                    random.uniform(0, 10),
                    random.uniform(-25, 25)
                ),
                color=color.rgb(80, 60, 40),
                texture='brick',
                collider='box'
            )
            self.entities.append(platform)
        
        # Lava pillars
        for i in range(8):
            pillar = Entity(
                model='cylinder',
                scale=(2, random.uniform(5, 15), 2),
                position=(
                    random.uniform(-20, 20),
                    -2,
                    random.uniform(-20, 20)
                ),
                color=color.red
            )
            self.entities.append(pillar)
        
        # Stars
        star_positions = [(10, 8, 10), (-12, 6, -8), (0, 12, 0)]
        for pos in star_positions:
            star = Entity(
                model='sphere',
                color=color.yellow,
                scale=0.8,
                position=pos,
                collider='sphere'
            )
            self.stars.append(star)
        
        # Exit portal
        self.exit_portal = Entity(
            model='cube',
            scale=(2, 3, 0.5),
            position=(0, 1.5, -30),
            color=color.purple,
            collider='box'
        )
        self.entities.append(self.exit_portal)
        
        return self.entities

# Game Manager
class GameManager:
    def __init__(self):
        self.player = None
        self.current_level = None
        self.hub_world = HubWorld()
        self.levels = {
            "grassland": GrasslandLevel("grassland"),
            "desert": DesertLevel("desert"),
            "ice": IceLevel("ice"),
            "lava": LavaLevel("lava")
        }
        self.ui_text = None
        
    def start_game(self):
        self.load_hub()
        
    def load_hub(self):
        if self.current_level:
            self.current_level.destroy()
        
        game_state.current_level = "hub"
        self.current_level = self.hub_world
        self.hub_world.create()
        
        # Create player
        if self.player:
            destroy(self.player)
        
        self.player = FirstPersonController(
            model=MarioCharacter(),
            position=(0, 2, 0),
            speed=8,
            jump_height=3
        )
        
        # Set up camera
        self.player.camera_pivot.z = -8
        self.player.camera_pivot.y = 3
        self.player.cursor.visible = False
        mouse.locked = True
        
        # UI
        if self.ui_text:
            destroy(self.ui_text)
        self.ui_text = Text(
            f'Stars: {game_state.stars_collected}',
            position=(-0.8, 0.45),
            scale=2,
            color=color.yellow
        )
    
    def load_level(self, level_name):
        if self.current_level:
            self.current_level.destroy()
        
        game_state.current_level = level_name
        level = self.levels[level_name]
        self.current_level = level
        level.create()
        
        # Reset player position
        self.player.position = Vec3(0, 2, 0)
        
        # Update UI
        if self.ui_text:
            destroy(self.ui_text)
        self.ui_text = Text(
            f'Level: {level_name.title()} | Stars: {level.collected_stars}/{len(level.stars)} | Total: {game_state.stars_collected}',
            position=(-0.8, 0.45),
            scale=1.5,
            color=color.yellow
        )
    
    def update(self):
        if not self.player:
            return
        
        # Check for painting collisions in hub
        if game_state.current_level == "hub":
            paintings = [p for p in self.current_level.entities if isinstance(p, PaintingPortal)]
            for painting in paintings:
                if distance(self.player.position, painting.position) < 3:
                    self.load_level(painting.level_name)
                    return
        
        # Check for level-specific updates
        elif game_state.current_level in self.levels:
            level = self.current_level
            
            # Check star collection
            for star in level.stars[:]:
                if distance(self.player.position, star.position) < 2:
                    level.stars.remove(star)
                    destroy(star)
                    level.collected_stars += 1
                    game_state.stars_collected += 1
                    
                    # Update UI
                    self.ui_text.text = f'Level: {game_state.current_level.title()} | Stars: {level.collected_stars}/{len(level.stars) + level.collected_stars} | Total: {game_state.stars_collected}'
                    
                    if level.collected_stars >= 3:
                        Text('All stars collected! Press ESC to return.', origin=(0, 0), scale=2, color=color.gold, duration=3)
            
            # Check exit portal
            if hasattr(level, 'exit_portal'):
                if distance(self.player.position, level.exit_portal.position) < 3:
                    self.load_hub()
                    return
            
            # Check if player fell off (lava level)
            if game_state.current_level == "lava" and self.player.position.y < -3:
                self.player.position = Vec3(0, 5, 0)
                Text('Watch out for the lava!', origin=(0, 0), scale=2, color=color.red, duration=2)
    
    def input(self, key):
        if key == 'escape':
            if game_state.current_level != "hub":
                self.load_hub()
            else:
                application.quit()

# Initialize game
game_manager = GameManager()

# Set up environment
sun = DirectionalLight()
sun.look_at(Vec3(1, -1, -1))
Sky()

# Input handler
def input(key):
    game_manager.input(key)

# Update function
def update():
    game_manager.update()

# Start the game
game_manager.start_game()

# Run the application
app.run()
