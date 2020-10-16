from entity import Entity, ENTITY_T
from characters import NPC, Player
from typing import Tuple
from block import Block

def entity_factory(pos: Tuple[int, int], entity: ENTITY_T, bl_size:Tuple[int,
    int], xy:Tuple[int, int]=None):
    if entity.layer in (1, 2):
        return Block(pos, entity, bl_size, xy=xy), 2
    if entity.layer == 4:
        return NPC(pos, entity, bl_size=bl_size, xy=xy), 4
    if entity.layer == 5:
        return Player(pos, entity, bl_size=bl_size, xy=xy), 5
