import toml

class SkillMapParser:
    def __init__(self) -> None:
        pass

    def parse(self, skill_map_file: str) -> dict:
        return toml.load(skill_map_file)