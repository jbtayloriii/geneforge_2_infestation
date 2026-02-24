"""Class that loads all Geneforge data into memory."""

import csv

import objects

class DataLoader:

    def __init__(self):
        self.ability_text_by_id = self._load_ability_text()
        self.item_varieties_by_id = self._load_item_varieties()

        self.stats_by_id = self._load_stats_text()
        self.item_stats_by_item_id = self._load_item_stats(self.stats_by_id)

        self.item_templates = self._load_item_templates(
            self.ability_text_by_id,
            self.item_varieties_by_id,
            self.item_stats_by_item_id
        )

        # Create mapping from variety ID to template
        self.item_templates_by_variety_id = {}
        for template in self.item_templates:
            if template.variety and template.variety not in self.item_templates_by_variety_id:
                self.item_templates_by_variety_id[template.variety] = []
            if template.variety:
                self.item_templates_by_variety_id[template.variety].append(template)

        # Create mapping from template ID to template
        self.item_templates_by_id = {}
        for template in self.item_templates:
            self.item_templates_by_id[template.item_id] = template

    def _load_stats_text(self):
        stats_by_id = {}
        with open("src/data/csv/stat_text.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                stats_by_id[int(row["id"])] = row["name"]
        return stats_by_id

    def _load_item_stats(self, stats_by_id) -> dict[int, list[objects.ItemStat]]:
        item_stats_by_id = {}
        with open("src/data/csv/item_stats.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                item_id = int(row["item_id"])
                stat_affected = int(row["stat_affected"])

                stat_text = stats_by_id[stat_affected]

                stat_amount = int(row["stat_amount"])
                is_pet = bool(int(row["is_pet"]) == 1)

                if item_id not in item_stats_by_id:
                    item_stats_by_id[item_id] = []
                item_stats_by_id[item_id].append(
                    objects.ItemStat(
                        item_id=item_id,
                        stat_affected=stat_text,
                        stat_amount=stat_amount,
                        is_pet=is_pet,
                    )
                )
        return item_stats_by_id

    def _load_ability_text(self) -> dict[int, str]:
        """Loads the game's ability text and IDs.

        Returns: A mapping from ability ID to ability text.
        """
        ability_text_by_id = {}
        with open("src/data/csv/ability_text.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                ability_text_by_id[int(row["id"])] = row["identifier"]
        return ability_text_by_id

    def _load_item_varieties(self) -> dict[int, objects.ItemVariety]:
        """Loads item varieties.

        Returns: A mapping from item variety ID to Item variety object.
        """
        item_variety_by_id: dict[int, objects.ItemVariety] = {}
        with open("src/data/csv/item_variety.csv", "r") as f:
            variety_reader = csv.DictReader(f)
            for row in variety_reader:
                next_id = int(row["id"])
                next_name = row["name"]
                next_item_var = objects.ItemVariety(variety_id=next_id, name=next_name)
                item_variety_by_id[next_id] = next_item_var
        return item_variety_by_id

    def _load_item_templates(
        self,
        ability_text_map,
        item_variety_map,
        item_stats_by_item_id,
    ) -> list[objects.ItemTemplate]:
        """Loads item templates.

        Returns: A list of all item templates, in no particular order.
        """
        item_templates = []
        with open("src/data/csv/item_template.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                ability_id_text = row["it_ability"]
                ability_id = int(ability_id_text) if ability_id_text else None
                if ability_id in ability_text_map:
                    ability_text = ability_text_map[ability_id]
                    ability_level = int(row["it_level"]) if row["it_level"] else None
                    item_ability = objects.ItemAbility(
                        ability_id=ability_id,
                        ability_text=ability_text,
                        ability_level=ability_level
                    )
                else:
                    item_ability = None
                
                variety_id = int(row["it_variety"]) if row["it_variety"] else -1
                variety = item_variety_map[variety_id] if variety_id in item_variety_map else None

                item_id = int(row["id"])
                item_stats = item_stats_by_item_id[item_id] if item_id in item_stats_by_item_id else []

                template = objects.ItemTemplate(
                    item_id=item_id,
                    name=row["it_name"],
                    ability=item_ability,
                    variety=variety,
                    value=row["it_value"],
                    weight=row["it_weight"],
                    charges=row["it_charges"],
                    protection=_int_or_none(row["it_protection"]),
                    extra_description=row["it_extra_description"],
                    can_augment=bool(row["it_can_augment"]),
                    item_stats = item_stats,
                )
                item_templates.append(template)
        return item_templates


def _int_or_none(val):
    try:
        return int(val)
    except ValueError:
        return None
