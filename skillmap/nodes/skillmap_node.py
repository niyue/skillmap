from skillmap.theme_loader import load_theme
from skillmap.nodes.common import get_icon, get_node_content, SECTION_SEPARATOR
from skillmap.nodes.group_node import create_group_subgraphs, create_groups_edges
import re


def alphanumerize(s):
    return re.sub(r"\W+", "_", s)


def get_orientation(skill_map_dict):
    orientation = skill_map_dict.get("orientation", "TD")
    if orientation not in ["TD", "TB", "BT", "RL", "LR"]:
        orientation = "TD"
    return orientation


def get_progress_bar_style(skill_map_dict):
    progress_bar_style = 0
    try:
        progress_bar_style = int(skill_map_dict.get("progress_bar_style", 0))
    except: 
        pass
    return progress_bar_style


# generate a mermaid graph from a skill map toml dict
def create_skillmap_graph(skill_map):
    skill_map_dict = skill_map.get("skillmap", {})
    map_name = skill_map_dict.get("name", "unamed_skill_map")
    map_id = alphanumerize(map_name)
    theme = skill_map_dict.get("theme", "ocean")
    progress_bar_style = get_progress_bar_style(skill_map_dict)
    orientation = get_orientation(skill_map_dict)
    map_icon = get_icon(skill_map_dict)
    map_icon_label = get_node_content([map_icon, map_name])

    map_to_group_edges = create_groups_edges(map_id, skill_map.get("groups", {}))
    map_group_subgraphs = create_group_subgraphs(
        skill_map.get("groups", {}), progress_bar_style
    )

    skill_map_node = f"{map_id}(\"{map_icon_label}\")"
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
