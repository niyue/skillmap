from skillmap.main import generate
from skillmap.skillmap_visitor import (
    SkillMapVisitor,
    group_subgraph,
    skill_node,
    SECTION_SEPARATOR,
)


def test_generate():
    skillmap_file = "tests/url_shortener.toml"
    skillmap_graph = generate(skillmap_file)
    assert skillmap_graph
    assert "flowchart TD" in skillmap_graph
    assert "url_shortener" in skillmap_graph
    assert "url_shortener-->groups.backend" in skillmap_graph
    assert "class groups.webui" in skillmap_graph

def test_skillmap_node_with_missing_name():
    visitor = SkillMapVisitor()
    skillmap_graph = visitor.visit(
        {
            "skillmap": {
            }
        }
    )
    assert skillmap_graph
    assert "flowchart TD" in skillmap_graph
    assert "unamed_skill_map" in skillmap_graph

def test_skillmap_node_with_missing_theme():
    visitor = SkillMapVisitor()
    skillmap_graph = visitor.visit(
        {
            "skillmap": {
                "name": "url shortener",
                "icon": "anchor",
                "theme": "not_found",
            }
        }
    )
    assert skillmap_graph
    assert "flowchart TD" in skillmap_graph
    assert "url shortener" in skillmap_graph

def test_skillmap_node_with_orientation():
    visitor = SkillMapVisitor()
    skillmap_graph = visitor.visit(
        {
            "skillmap": {
                "name": "url shortener",
                "icon": "anchor",
                "orientation": "LR",
            }
        }
    )
    assert skillmap_graph
    assert "flowchart LR" in skillmap_graph
    assert "url shortener" in skillmap_graph

def test_skillmap_node_with_auto_required_groups():
    visitor = SkillMapVisitor()
    skillmap_graph = visitor.visit(
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
    assert skillmap_graph
    assert "flowchart TD" in skillmap_graph
    assert "url_shortener-->groups.g1" in skillmap_graph
    assert "url_shortener-->groups.g2" not in skillmap_graph


def test_skill_node():
    skill_graph = skill_node("s1", {"name": "url validator", "icon": "globe"})
    sections = ["s1(fa:fa-globe<br/>url validator)", "class s1 newSkill;", ""]
    assert skill_graph.split("\n") == sections


def test_skill_node_with_status():
    skill_graph = skill_node(
        "s1", {"name": "url validator", "icon": "globe", "status": "beingLearned"}
    )
    sections = ["s1(fa:fa-globe<br/>url validator)", "class s1 beingLearnedSkill;", ""]
    assert skill_graph.split("\n") == sections


def test_locked_skill_node():
    skill_graph = skill_node("s1", {})
    sections = ["s1(fa:fa-lock<br/>???)", "class s1 unknownSkill;", ""]
    assert skill_graph.split("\n") == sections


def test_skill_node_with_requires():
    skill_graph = skill_node(
        "s1", {"name": "url validator", "icon": "globe", "requires": ["s2"]}
    )
    sections = ["s1(fa:fa-globe<br/>url validator)", "class s1 newSkill;", "s2-->s1"]
    assert skill_graph.split("\n") == sections


def test_visit_group_without_skill():
    group_graph = group_subgraph(
        "g1",
        {
            "name": "web ui",
            "icon": "anchor",
        },
    )
    sections = [
        SECTION_SEPARATOR,
        "subgraph groups.g1[fa:fa-anchor web ui]",
        "",  # skill list is skipped
        "end",
        "class groups.g1 newSkillGroup;",
        "",
    ]
    assert group_graph.split("\n") == sections


def test_visit_group():
    group_graph = group_subgraph(
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
        "subgraph groups.g1[fa:fa-anchor web ui]",
        "groups.g1.skills.s1(fa:fa-globe<br/>url validator)",
        "class groups.g1.skills.s1 newSkill;",
        "",
        "groups.g1.skills.s2(fa:fa-html5<br/>React)",
        "class groups.g1.skills.s2 newSkill;",
        "",
        "end",
        "class groups.g1 newSkillGroup;",
        "",
    ]
    assert group_graph.split("\n") == sections


def test_visit_group_with_requires():
    group_graph = group_subgraph(
        "g1",
        {
            "name": "web ui",
            "icon": "anchor",
            "requires": ["groups.g2.skills.s1"],
        },
    )
    sections = [
        SECTION_SEPARATOR,
        "subgraph groups.g1[fa:fa-anchor web ui]",
        "",  # skill list is skipped
        "end",
        "class groups.g1 newSkillGroup;",
        "groups.g2.skills.s1-->groups.g1",
    ]
    assert group_graph.split("\n") == sections
