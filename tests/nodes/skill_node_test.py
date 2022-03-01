from skillmap.nodes.skill_node import create_skill_node, get_progress, Status

def test_get_0_progress():
    progress, status = get_progress({})
    assert progress == ""
    assert status == Status.NEW

def test_get_fraction_progress():
    progress, status = get_progress({"progress": "1/3"})
    assert progress == "■□□"
    assert status == Status.BEING_LEANRED

def test_get_0_fraction_progress():
    progress, status = get_progress({"progress": "0/4"})
    assert progress == "□□□□"
    assert status == Status.NEW

def test_create_skill_node():
    skill_graph = create_skill_node("s1", {"name": "url validator", "icon": "globe"})
    sections = ['s1("fa:fa-globe<br/>url validator")', "class s1 newSkill;", ""]
    assert skill_graph.split("\n") == sections


def test_skill_node_with_progress():
    skill_graph = create_skill_node(
        "s1", {"name": "url validator", "icon": "globe", "progress": "1/2"}
    )
    sections = ['s1("fa:fa-globe<br/>url validator<br/>■□")', "class s1 beingLearnedSkill;", ""]
    assert skill_graph.split("\n") == sections


def test_locked_create_skill_node():
    skill_graph = create_skill_node("s1", {})
    sections = ['s1("fa:fa-lock<br/>???")', "class s1 unknownSkill;", ""]
    assert skill_graph.split("\n") == sections


def test_skill_node_with_requires():
    skill_graph = create_skill_node(
        "s1", {"name": "url validator", "icon": "globe", "requires": ["s2"]}
    )
    sections = ['s1("fa:fa-globe<br/>url validator")', "class s1 newSkill;", "s2-->s1"]
    assert skill_graph.split("\n") == sections
