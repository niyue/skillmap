import os


SECTION_SEPARATOR = "%" * 30


def get_icon(dict_value):
    icon = ""
    if "icon" in dict_value:
        icon = f"fa:fa-{dict_value['icon']}"
    return icon


def theme_css_styles(theme):
    theme_file = f"skillmap/themes/{theme}.theme"
    if not os.path.exists(theme_file):
        theme_file = f"skillmap/themes/ocean.theme"
    with open(theme_file, "r") as f:
        return f.read()


def groups_edges(map_name, groups):
    group_ids = [group_id for group_id, _ in groups.items()]
    groups_edges = "\n".join([f"{map_name}-->{group_id}" for group_id in group_ids])
    return groups_edges


def skill_node(skill_id, skill_value):
    if not skill_value:
        locked_skill_value = {"name": "???", "icon": "lock", "status": "unknown"}
        skill_value = locked_skill_value
    skill_name = skill_value.get("name", "")
    skill_icon = get_icon(skill_value)
    skill_status = skill_value.get("status", "new")
    skill_id_and_name = f"{skill_id}({skill_icon} <br/>{skill_name})"
    skill_style = f"class {skill_id} {skill_status}Skill;"
    sections = [
        skill_id_and_name,
        skill_style,
    ]
    skill_graph = "\n".join(sections)
    return skill_graph


def group_subgraph(group_id, group_value):
    group_name = group_value.get("name", "")
    group_icon = get_icon(group_value)
    group_skills_list = ""
    if "skills" in group_value:
        group_skills = [
            skill_node(skill_id, skill_value)
            for skill_id, skill_value in group_value["skills"].items()
        ]
        group_skills_list = "\n".join(group_skills)

    group_id_and_name = f"subgraph {group_id}[{group_icon} {group_name}]"
    group_style = f"class {group_id} skillGroup;"
    group_subgraph_end = "end"
    sections = [
        SECTION_SEPARATOR,
        group_id_and_name,
        group_skills_list,
        group_subgraph_end,
        group_style,
    ]

    group_graph = "\n".join(sections)
    return group_graph


def group_subgraphs(groups):
    group_graphs = [
        group_subgraph(group_id, group_value)
        for group_id, group_value in groups.items()
    ]
    return "\n\n".join(group_graphs)


def skill_map_graph(skill_map):
    skill_map_dict = skill_map.get("skillmap", {})
    map_name = skill_map_dict.get("name", "")
    theme = skill_map_dict.get("theme", "ocean")
    map_icon = get_icon(skill_map_dict)

    map_to_group_edges = groups_edges(map_name, skill_map.get("groups", {}))
    map_group_subgraphs = group_subgraphs(skill_map.get("groups", {}))

    skill_map_node = f"{map_name}({map_icon} <br/>{map_name})"
    skill_map_node_style = f"class {map_name} skillGroup;"
    sections = [
        "flowchart TD",
        skill_map_node,
        map_group_subgraphs,
        SECTION_SEPARATOR,
        map_to_group_edges,
        theme_css_styles(theme),
        skill_map_node_style,
    ]
    return "\n".join(sections)


class SkillMapVisitor(object):
    def __init__(self):
        pass

    def visit(self, skill_map):
        return skill_map_graph(skill_map)
