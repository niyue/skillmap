from skillmap.main import generate
from skillmap.nodes.common import SECTION_SEPARATOR
from skillmap.nodes.skillmap_node import create_skillmap_graph
from skillmap.nodes.group_node import create_group_subgraph
from skillmap.nodes.skill_node import create_skill_node


def test_generate():
    skillmap_file = "tests/url_shortener.toml"
    map_graph = generate(skillmap_file)
    assert map_graph
    assert "flowchart TD" in map_graph
    assert "url_shortener" in map_graph
    assert "url_shortener-->groups.backend" in map_graph
    assert "class groups.webui" in map_graph


def test_skillmap_node_with_missing_name():
    map_graph = create_skillmap_graph({"skillmap": {}})
    assert map_graph
    assert "flowchart TD" in map_graph
    assert "unamed_skill_map" in map_graph


def test_skillmap_node_with_missing_theme():
    map_graph = create_skillmap_graph(
        {
            "skillmap": {
                "name": "url shortener",
                "icon": "anchor",
                "theme": "not_found",
            }
        }
    )
    assert map_graph
    assert "flowchart TD" in map_graph
    assert "url shortener" in map_graph


def test_skillmap_node_with_orientation():
    map_graph = create_skillmap_graph(
        {
            "skillmap": {
                "name": "url shortener",
                "icon": "anchor",
                "orientation": "LR",
            }
        }
    )
    assert map_graph
    assert "flowchart LR" in map_graph
    assert "url shortener" in map_graph


def test_skillmap_node_with_auto_required_groups():
    map_graph = create_skillmap_graph(
        {
            "skillmap": {
                "name": "url shortener",
            },
            "groups": {
                "g1": {
                    "name": "g1",
                },
                "g2": {
                    "name": "g2",
                    "requires": ["g1"],
                },
            },
        }
    )
    assert map_graph
    assert "flowchart TD" in map_graph
    assert "url_shortener-->groups.g1" in map_graph
    assert "url_shortener-->groups.g2" not in map_graph





def test_visit_group_without_skill():
    group_graph = create_group_subgraph(
        "g1",
        {
            "name": "web ui",
            "icon": "anchor",
        },
    )
    sections = [
        SECTION_SEPARATOR,
        'subgraph groups.g1["fa:fa-anchor web ui"]',
        "",  # skill list is skipped
        "end",
        "class groups.g1 newSkillGroup;",
        "",
    ]
    assert group_graph.split("\n") == sections


def test_visit_group():
    group_graph = create_group_subgraph(
        "g1",
        {
            "name": "web ui",
            "icon": "anchor",
            "skills": {
                "s1": {"name": "url validator", "icon": "globe"},
                "s2": {"name": "React", "icon": "html5"},
            },
        },
    )
    sections = [
        SECTION_SEPARATOR,
        'subgraph groups.g1["fa:fa-anchor web ui"]',
        'groups.g1.skills.s1("fa:fa-globe<br/>url validator")',
        "class groups.g1.skills.s1 newSkill;",
        "",
        'groups.g1.skills.s2("fa:fa-html5<br/>React")',
        "class groups.g1.skills.s2 newSkill;",
        "",
        "end",
        "class groups.g1 newSkillGroup;",
        "",
    ]
    assert group_graph.split("\n") == sections


def test_visit_group_with_requires():
    group_graph = create_group_subgraph(
        "g1",
        {
            "name": "web ui",
            "icon": "anchor",
            "requires": ["groups.g2.skills.s1"],
        },
    )
    sections = [
        SECTION_SEPARATOR,
        'subgraph groups.g1["fa:fa-anchor web ui"]',
        "",  # skill list is skipped
        "end",
        "class groups.g1 newSkillGroup;",
        "groups.g2.skills.s1-->groups.g1",
    ]
    assert group_graph.split("\n") == sections
