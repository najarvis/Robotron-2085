import pygame

from player import Player
from family import FamilyMember
from bullet import Bullet
from enemy import Electrode, Grunt, BaseEnemy
import helper_funcs

from typing import Mapping, get_args
# I haven't done this before, but I'm learning type annotation in Python.
# This is basically saying the type could be any of these.
# -- Types --
EnemyType = BaseEnemy | Electrode | Grunt
InstanceableType = Player | FamilyMember | EnemyType
PlayerType = type[Player]
LevelType = Mapping[type[InstanceableType], list[tuple[float, float]]]
"""
LevelType will be used to store information about a given level. Typically dictionary in the form:
{
    Grunt: [(20, 20), (200, 20), (50, 100)],
    Electrode: [(50, 50), ...],
    ...
    Player: [(250, 250)]
}
"""

class Director:

    def __init__(self, screen_rect: pygame.Rect):
        self.level_num = 0
        self.score = 0
        self.lives = 0

        self.enemy_group = pygame.sprite.Group()
        self.family_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()

        self.player: Player = Player(screen_rect.center, screen_rect)
        self.player_group.add(self.player)

        self.screen_rect = screen_rect

        self.init_sounds()

    def init_sounds(self):
        # TODO: Compress these to mp3 to save space
        self.sound_library = {
            "explosion": pygame.mixer.Sound("sounds/explode.wav"),
            "shoot": pygame.mixer.Sound("sounds/shoot.wav")
        }

    def update(self, delta: float, pressed_keys: list[bool]):
        self.player_group.update(delta, pressed_keys)
        self.bullet_group.update(delta, self.enemy_group)
        self.enemy_group.update(delta, self.player.position)
        self.family_group.update(delta)

        # Resolve player colisions here now that everything is done moving
        if (collided_enemy := pygame.sprite.spritecollideany(self.player, self.enemy_group)) is not None:
            # main_player.kill()
            print("YOU DIED")

    def load_level(self, level_dict: LevelType, clear=True):
        assert Player in level_dict

        if clear:
            self.enemy_group.empty()
            self.family_group.empty()
            self.player_group.empty()
            self.bullet_group.empty()
            del self.player

        for obj_type in level_dict:
            for coord in level_dict[obj_type]:
                if obj_type in get_args(EnemyType): # get_args returns what types make up the Union
                    new_enemy = obj_type(coord, self.screen_rect)
                    self.enemy_group.add(new_enemy)

                elif obj_type is Player:
                    self.player = Player(coord, self.screen_rect)
                    self.player_group.add(self.player)

                elif obj_type is FamilyMember:
                    new_family = FamilyMember(coord, self.screen_rect)
                    self.family_group.add(new_family)


    def draw(self, surface: pygame.Surface):
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
        # Get the components for the new bullet
        pos, vel = helper_funcs.shoot_at(self.player.position, pos)
        new_bullet = Bullet(pos, vel, self.screen_rect, self.sound_library['explosion'])
        self.bullet_group.add(new_bullet)
        self.sound_library['shoot'].play()
    