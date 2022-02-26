from skillmap.skillmap_parser import SkillMapParser


def test_parse_toml():
    parser = SkillMapParser()
    skill_map = parser.parse('tests/urlshortener.toml')
    assert skill_map
    assert skill_map['skillmap']['name'] == "urlshortener"
    assert skill_map['groups']['webui']['name'] == "web ui"
    assert skill_map['groups']['webui']['skills']['url_validator']['name'] == "url validator"
    assert skill_map['groups']['webui']['skills']['url_validator']['icon'] == "globe"
