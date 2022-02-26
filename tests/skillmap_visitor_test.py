from skillmap.main import generate
from skillmap.skillmap_visitor import (
    SkillMapVisitor,
    group_subgraph,
    skill_node,
    SECTION_SEPARATOR,
)


def test_generate():
    skillmap_file = "tests/urlshortener.toml"
    skillmap_graph = generate(skillmap_file)
    assert skillmap_graph
    assert "flowchart TD" in skillmap_graph
    assert "urlshortener" in skillmap_graph
    assert "urlshortener-->webui" in skillmap_graph
    assert "class webui" in skillmap_graph


def test_skill_node():
    skill_graph = skill_node("s1", {"name": "url validator", "icon": "globe"})
    sections = ["s1(fa:fa-globe <br/>url validator)", "class s1 newSkill;"]
    assert skill_graph.split("\n") == sections


def test_skill_node_with_status():
    skill_graph = skill_node(
        "s1", {"name": "url validator", "icon": "globe", "status": "beingLearned"}
    )
    sections = ["s1(fa:fa-globe <br/>url validator)", "class s1 beingLearnedSkill;"]
    assert skill_graph.split("\n") == sections

def test_locked_skill_node():
    skill_graph = skill_node("s1", {})
    sections = ["s1(fa:fa-lock <br/>???)", "class s1 unknownSkill;"]
    assert skill_graph.split("\n") == sections


def test_visit_group_without_skill():
    group_graph = group_subgraph(
        "g1",
        {
            "name": "web ui",
            "icon": "chrome",
        },
    )
    sections = [
        SECTION_SEPARATOR,
        "subgraph g1[fa:fa-chrome web ui]",
        "",  # skill list is skipped
        "end",
        "class g1 skillGroup;",
    ]
    assert group_graph.split("\n") == sections


def test_visit_group():
    group_graph = group_subgraph(
        "g1",
        {
            "name": "web ui",
            "icon": "chrome",
            "skills": {
                "s1": {"name": "url validator", "icon": "globe"},
                "s2": {"name": "React", "icon": "html5"},
            },
        },
    )
    sections = [
        SECTION_SEPARATOR,
        "subgraph g1[fa:fa-chrome web ui]",
        "s1(fa:fa-globe <br/>url validator)",
        "class s1 newSkill;",
        "s2(fa:fa-html5 <br/>React)",
        "class s2 newSkill;",
        "end",
        "class g1 skillGroup;",
    ]
    assert group_graph.split("\n") == sections
