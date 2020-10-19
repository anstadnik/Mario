import enum
import pygame as pg
from typing import Tuple, List

#######################
#  Types of entities  #
#######################

# 1. Blocks of level
#   Should have it's position on the game map and a layer
# 2. Objects
#   Objects like trees, stones etc
# 3. Particles made by some of the level's blocks
#   Should probably have only position on the image and update methods. Blocks
#   of level will produce them
# 3. NPCs
#   They should have the initial position for the level, but also they should
#   have some update/draw functional which will allow them to move and interact
# 4. Main character
#   Should have the same functional as the NPC, but have to also handle user
#   input


class ENTITY_T(enum.Enum):
    """
    This class defines level block's names,  images and the layer
    
    Layer 1: Map blocks
    Layer 2: Objects on the map
    Layer 3: Particles
    Layer 4: NPC
    Layer 5: Player
    """
    EMPTY   = ('./PNG/Tiles/tile13.png',                  1)
    GRASS   = ('./PNG/Tiles/tile32.png',                  1)
    STONE   = ('./PNG/Objects/rocks1_6.png',              1)
    TREE    = ('./PNG/Objects/trees2_2.png',              2)
    POINTER = ('./PNG/Objects/pointer.png',               2)
    NPC     = ('./PNG/NPC/N_SKIN_enemies_1_ACTION_*.png', 4)
    PLAYER  = ('./PNG/Wraith/Wraith_0N_SKIN_ACTION_*.png', 5)

    def __new__(cls, *args, **kwgs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, img_path, layer):
        self.img_path = img_path
        self.layer = layer


class Entity(pg.sprite.Sprite):
    def __init__(self, pos: List[int], entity: ENTITY_T,
            ent_size: Tuple[int, int] = None, xy: Tuple[int, int] = None):
        """
        Create a new entity for level

        :param pos Tuple[int, int]: Position of the new entity (x, y)
        :param entity Entity_T: Type of the entity
        :param ent_size Tuple[int, int]: Optional entity size (height, width)
        :param xy Tuple[int, int]: Optional position of the sprite (x, y)
        """
        self.entity = entity
        self.pos = pos
        self.clean_sprite()
        self.ent_size, self.xy = [None] * 2
        self.added_color = None
        self.flip = False
        if ent_size:
            self.init_sprite(ent_size, xy)

    def init_sprite(self, ent_size: Tuple[int, int] = None, xy: Tuple[int, int] = None):
        super().__init__()
        if ent_size:
            self.ent_size = ent_size
        assert self.ent_size is not None
        self.xy = xy or [self.ent_size[i] * self.pos[i] for i in range(2)]
        self.init_image()
        return self
    
    @property
    def image(self):
        image = self._image.copy()
        if self.added_color:
            image.fill(self.added_color, special_flags=pg.BLEND_ADD)
        if self.flip:
            image = pg.transform.flip(image, True, False)
        return image

    def update(self, dt, move=False):
        pass

    def init_image(self):
        raise NotImplementedError

    def clean_sprite(self):
        self._image = None
        self.rect = None
