from typing import Mapping, get_args

import pygame

from player import Player
from family import FamilyMember
from bullet import Bullet
from enemy import Electrode, Grunt, BaseEnemy
import helper_funcs

# I haven't done this before, but I'm learning type annotation in Python.
# This is basically saying the type could be any of these.
# -- Types --
EnemyType = BaseEnemy | Electrode | Grunt
InstanceableType = Player | FamilyMember | EnemyType
PlayerType = type[Player]
LevelType = Mapping[type[InstanceableType], list[tuple[float, float]]]
"""
LevelType will be used to store information about a given level. 
Typically dictionary in the form:
{
    Grunt: [(20, 20), (200, 20), (50, 100)],
    Electrode: [(50, 50), ...],
    ...
    Player: [(250, 250)]
}
"""

class Director:
    """The director holds the state of the game internally, and handles
    storing, updating, and drawing all game components."""

    def __init__(self, screen_rect: pygame.Rect):
        self.level_num = 0
        self.score = 0
        self.lives = 0

        self.enemy_group = pygame.sprite.Group()
        self.family_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.destroyed_group = pygame.sprite.Group()

        # Spawn the player in the center even if no level is loaded (for debug purposes)
        self.player: Player = Player(screen_rect.center, screen_rect)
        self.player_group.add(self.player)

        self.screen_rect = screen_rect

        self.joystick = None

        self.reload_timer = 0
        self.reload_timer_max = 0.20 # How many seconds before the player can shoot again

        self.init_sounds()

    def init_sounds(self) -> None:
        # TODO: Compress these to mp3 to save space
        self.sound_library = {
            "explosion": pygame.mixer.Sound("sounds/explode.wav"),
            "shoot": pygame.mixer.Sound("sounds/shoot.wav")
        }

    def update(self, delta: float, pressed_keys: list[bool]) -> None:
        movement_vec, shooting_vec = self.get_joystick_vecs()
        self.player_group.update(delta, pressed_keys, movement_vec)
        self.bullet_group.update(delta, self.enemy_group, self.destroyed_group)
        self.enemy_group.update(delta, self.player.position)
        self.family_group.update(delta)
        self.destroyed_group.update(delta)

        if shooting_vec is not None and self.reload_timer <= 0:
            self.shoot(self.player.position + shooting_vec)
            self.reload_timer = self.reload_timer_max

        self.reload_timer -= delta

        # Resolve player colisions here now that everything is done moving
        if (collided_enemy := pygame.sprite.spritecollideany(self.player, self.enemy_group)) is not None:
            # main_player.kill()
            print("YOU DIED")

    def load_level(self, level_dict: LevelType, clear=True) -> bool:
        """Handle instanciating game components into memory given a
        mapping of types to sets of coordinates. Returns True if loading
        is successful, False otherwise.
        """
        if len(level_dict.get(Player, [])) != 1: # There must be exactly one player
            return False

        if clear:
            self.enemy_group.empty()
            self.family_group.empty()
            self.player_group.empty()
            self.bullet_group.empty()
            self.destroyed_group.empty()
            del self.player # should this be `self.player = None`?

        # Loop through each instanciable type in the dict and handle instanciating them. 
        for obj_type in level_dict:
            group: pygame.sprite.Group = None
            if obj_type is Player:
                # Have to handle this specially because we need to populate self.player
                coord = level_dict[Player][0]
                self.player = obj_type(coord, self.screen_rect) 
                self.player_group.add(self.player)
                continue

            elif obj_type in get_args(EnemyType): # get_args returns what types make up the Union
                group = self.enemy_group

            elif obj_type is FamilyMember:
                group = self.family_group

            # Unsupported class type
            else:
                return False

            # If it wasn't the player instanciate whatever was chosen and add them to their respective group.
            for coord in level_dict[obj_type]:
                new_instance = obj_type(coord, self.screen_rect)
                group.add(new_instance)

        return True

    def draw(self, surface: pygame.Surface):
        self.destroyed_group.draw(surface)
        self.enemy_group.draw(surface)
        self.family_group.draw(surface)
        self.player_group.draw(surface)
        self.bullet_group.draw(surface)

    def create_enemy(self, type: type[EnemyType], pos: helper_funcs.CoordType) -> EnemyType:
        new_enemy = type(pos)
        self.add_enemy(new_enemy)

    def add_enemy(self, enemy: EnemyType):
        self.enemy_group.add(enemy)

    def shoot(self, pos: helper_funcs.CoordType):
        """Given a coordinate, get the components for a bullet fired
        from the player towards said coordinate, spawn it, add it to
        the group, and play the shot fired sound.
        """

        pos, vel = helper_funcs.shoot_at(self.player.position, pos)
        new_bullet = Bullet(pos, vel, self.screen_rect, self.sound_library['explosion'])
        self.bullet_group.add(new_bullet)
        self.sound_library['shoot'].play()

    @staticmethod
    def init_joystick(id: int) -> pygame.joystick.Joystick:
        return pygame.joystick.Joystick(id) 

    def set_joystick(self, joystick: pygame.joystick.Joystick) -> None:
        self.joystick = joystick

    def remove_joystick(self) -> None:
        self.joystick = None

    def init_and_set_joystick(self, id: int):
        self.set_joystick(Director.init_joystick(id))

    def get_joystick_vecs(self) -> tuple[pygame.math.Vector2 | None, pygame.math.Vector2 | None]:
        """Robotron is typically a "twin-stick" game, where one stick controls
        the movement while the other controls the shooting. This code currently
        works on an xbox one controller, as that is what I have for testing.
        
        Returns a tuple with two Vector2 instances, either of which may be None
        if the magnitude is small enough (to avoid jitter).
        """

        if self.joystick is None:
            return (None, None)

        joy = self.joystick
        left_x_axis = joy.get_axis(0)
        left_y_axis = joy.get_axis(1)
        right_x_axis = joy.get_axis(2)
        right_y_axis = joy.get_axis(3)
    
        # Adjust this min_value to avoid drift / jitter with the inputs.
        min_value = 0.1

        # Movement with the left analog stick, shooting with the right
        movement_vec = None
        movement_magnitude = (left_x_axis * left_x_axis) + (left_y_axis * left_y_axis) # Hypotenuse (x^2 + y^2)
        if movement_magnitude >= min_value:
            movement_vec = pygame.math.Vector2(left_x_axis, left_y_axis)
            movement_vec.normalize_ip()    

        shooting_vec = None
        shooting_magnitude = (right_x_axis * right_x_axis) + (right_y_axis * right_y_axis)
        if shooting_magnitude >= min_value:
            shooting_vec = pygame.math.Vector2(right_x_axis, right_y_axis)
            shooting_vec.normalize_ip()

        return (movement_vec, shooting_vec)
