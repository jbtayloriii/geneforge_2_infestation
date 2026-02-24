"""Object representations of game concepts."""

import dataclasses

@dataclasses.dataclass(frozen=True)
class ItemAbility:
    ability_id: int
    ability_text: str
    ability_level: int | None = None

    def get_description(self):
        if not self.ability_level:
            return ability_text

        # Shortsword
        if self.ability_id == 2:
            suffix = f" {self.ability_level} - {self.ability_level * 4} damage"
        
        # Broadsword and special blades (oozing, etc.)
        elif self.ability_id in [90, 91, 92, 93, 94]:
            suffix = f" {self.ability_level} - {self.ability_level * 5} damage"

        else:
            # Shouldn't happen, but could be possible for strange item templating
            suffix = ""

        return f"{self.ability_text}{suffix}"

@dataclasses.dataclass(frozen=True)
class ItemStat:
    item_id: int
    stat_affected: str
    stat_amount: int
    is_pet: bool

    def get_description(self):
        """Returns a string for what would be printed in-game."""
        stat_pieces = []
        if self.stat_amount > 0:
            stat_pieces.append(f"+{self.stat_amount}")
        else:
            stat_pieces.append(str(self.stat_amount))
        stat_pieces.append("to")
        if self.is_pet:
            stat_pieces.append("creation")
        stat_pieces.append(self.stat_affected)

        return " ".join(stat_pieces)

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
    ability: ItemAbility
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
