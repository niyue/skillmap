from skillmap.nodes.common import (
    get_icon,
    get_node_content,
    get_required_node_edges,
    SECTION_SEPARATOR,
)
from skillmap.nodes.skill_node import create_skill_node


def _qualify(group_id):
    return f"groups.{group_id}"


def _qualified_skill_id(qualified_group_id, skill_id):
    return f"{qualified_group_id}.skills.{skill_id}"


def create_groups_edges(map_id, groups):
    group_ids = [
        _qualify(group_id)
        for group_id, group_value in groups.items()
        if "requires" not in group_value  # all groups without requires
    ]
    groups_edges = "\n".join([f"{map_id}-->{gid}" for gid in group_ids])
    return groups_edges


def get_group_skills_list(qualified_group_id, group_skills, progress_bar_style=0):
    group_skills = [
        create_skill_node(
            _qualified_skill_id(qualified_group_id, skill_id),
            skill_value,
            progress_bar_style,
        )
        for skill_id, skill_value in group_skills.items()
    ]
    return "\n".join(group_skills)


def get_group_status(group_skills):
    for _, skill_value in group_skills.items():
        skill_status = skill_value.get("status", "")
        if skill_status not in ("new", ""):
            return "normal"
    return "new"


def create_group_subgraph(group_id, group_value, progress_bar_style=0):
    qualified_group_id = _qualify(group_id)
    group_name = group_value.get("name", "")
    group_icon = get_icon(group_value)
    group_icon_label = get_node_content([group_icon, group_name], False)
    group_skills_list = get_group_skills_list(
        qualified_group_id, group_value.get("skills", {}), progress_bar_style
    )
    group_status = get_group_status(group_value.get("skills", {}))

    group_requires_list = get_required_node_edges(
        qualified_group_id, group_value.get("requires", [])
    )

    group_id_and_name = f"subgraph {qualified_group_id}[\"{group_icon_label}\"]"
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


def create_group_subgraphs(groups, progress_bar_style=0):
    group_graphs = [
        create_group_subgraph(group_id, group_value, progress_bar_style)
        for group_id, group_value in groups.items()
    ]
    return "\n\n".join(group_graphs)
