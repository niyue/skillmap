from skillmap.theme_loader import load_theme
import re

SECTION_SEPARATOR = "%" * 30

def alphanumerize(s):
    return re.sub(r'\W+', "_", s)


def get_icon(dict_value):
    icon = ""
    if "icon" in dict_value:
        icon = f"fa:fa-{dict_value['icon']}"
    return icon


def _qualify(group_id):
    return f"groups.{group_id}"


def _qualified_skill_id(qualified_group_id, skill_id):
    return f"{qualified_group_id}.skills.{skill_id}"


def groups_edges(map_id, groups):
    group_ids = [
        _qualify(group_id)
        for group_id, group_value in groups.items()
        if "requires" not in group_value # all groups without requires
    ]
    groups_edges = "\n".join([f"{map_id}-->{gid}" for gid in group_ids])
    return groups_edges


def skill_node(skill_id, skill_value):
    if not skill_value:
        locked_skill_value = {"name": "???", "icon": "lock", "status": "unknown"}
        skill_value = locked_skill_value
    skill_name = skill_value.get("name", "")
    skill_icon = get_icon(skill_value)
    skill_icon_label = get_icon_label(skill_icon, skill_name)
    skill_status = skill_value.get("status", "new")
    skill_id_and_name = f"{skill_id}({skill_icon_label})"
    skill_style = f"class {skill_id} {skill_status}Skill;"
    skill_requires = _required_node_edges(skill_id, skill_value.get("requires", []))
    sections = [
        skill_id_and_name,
        skill_style,
        skill_requires,
    ]
    skill_graph = "\n".join(sections)
    return skill_graph


def _required_node_edges(qualified_node_id, required_node_ids):
    node_requires = [
        f"{required_node_id}-->{qualified_node_id}"
        for required_node_id in required_node_ids
    ]
    return "\n".join(node_requires)


def get_group_skills_list(qualified_group_id, group_skills):
    group_skills = [
        skill_node(_qualified_skill_id(qualified_group_id, skill_id), skill_value)
        for skill_id, skill_value in group_skills.items()
    ]
    return "\n".join(group_skills)


def get_group_status(group_skills):
    for _, skill_value in group_skills.items():
        skill_status = skill_value.get("status", "")
        if skill_status not in ("new", ""):
            return "normal"
    return "new"


def group_subgraph(group_id, group_value):
    qualified_group_id = _qualify(group_id)
    group_name = group_value.get("name", "")
    group_icon = get_icon(group_value)
    group_icon_label = get_icon_label(group_icon, group_name, False)
    group_skills_list = get_group_skills_list(
        qualified_group_id, group_value.get("skills", {})
    )
    group_status = get_group_status(group_value.get("skills", {}))

    group_requires_list = _required_node_edges(
        qualified_group_id, group_value.get("requires", [])
    )

    group_id_and_name = f"subgraph {qualified_group_id}[{group_icon_label}]"
    group_style = f"class {qualified_group_id} {group_status}SkillGroup;"
    group_subgraph_end = "end"
    sections = [
        SECTION_SEPARATOR,
        group_id_and_name,
        group_skills_list,
        group_subgraph_end,
        group_style,
        group_requires_list,
    ]

    group_graph = "\n".join(sections)
    return group_graph


def group_subgraphs(groups):
    group_graphs = [
        group_subgraph(group_id, group_value)
        for group_id, group_value in groups.items()
    ]
    return "\n\n".join(group_graphs)

def get_orientation(skill_map_dict):
    orientation = skill_map_dict.get("orientation", "TD")
    if orientation not in ["TD", "TB", "BT", "RL", "LR"]:
        orientation = "TD"
    return orientation

def get_icon_label(icon, name, two_lines_layout=True):
    if icon:
        new_line = "<br/>" if two_lines_layout else " "
        return f"{icon}{new_line}{name}"
    else:
        return name


def skill_map_graph(skill_map):
    skill_map_dict = skill_map.get("skillmap", {})
    map_name = skill_map_dict.get("name", "unamed_skill_map")
    map_id = alphanumerize(map_name)
    theme = skill_map_dict.get("theme", "ocean")
    orientation = get_orientation(skill_map_dict)
    map_icon = get_icon(skill_map_dict)
    map_icon_label = get_icon_label(map_icon, map_name)

    map_to_group_edges = groups_edges(map_id, skill_map.get("groups", {}))
    map_group_subgraphs = group_subgraphs(skill_map.get("groups", {}))

    skill_map_node = f"{map_id}({map_icon_label})"
    skill_map_node_style = f"class {map_id} normalSkillGroup;"
    skill_map_header = f"flowchart {orientation}"
    sections = [
        skill_map_header,
        skill_map_node,
        map_group_subgraphs,
        SECTION_SEPARATOR,
        map_to_group_edges,
        load_theme(theme),
        skill_map_node_style,
    ]
    return "\n".join(sections)


class SkillMapVisitor(object):
    def __init__(self):
        pass

    def visit(self, skill_map):
        return skill_map_graph(skill_map)
