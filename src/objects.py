"""Object representations of game concepts."""

import dataclasses

@dataclasses.dataclass(frozen=True)
class ItemStat:
    item_id: int
    stat_affected: str
    stat_amount: int
    is_pet: bool

@dataclasses.dataclass(frozen=True)
class ItemVariety:
    """Represents classes of items."""
    variety_id: int
    name: str

    def __str__(self):
        return f"{self.variety_id}: {self.name}"

@dataclasses.dataclass(frozen=True)
class ItemTemplate:
    item_id: int
    name: str
    ability_text: str
    level: int
    variety: ItemVariety | None
    value: int
    weight: int
    charges: int
    protection: int
    extra_description: str
    can_augment: bool

    extra_description: int

    item_stats: list[ItemStat]

    def get_display_text(self):
        return self.name
