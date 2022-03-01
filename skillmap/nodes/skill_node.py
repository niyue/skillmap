from skillmap.nodes.common import get_icon, get_node_content, get_required_node_edges
from fractions import Fraction
from enum import Enum

class Status(Enum):
    NEW = "new"
    BEING_LEANRED = "beingLearned"
    LEARNED = "learned"
    UNKNOWN = "unknown"
    
def _is_locked_skill_value(skill_value):
    icon = skill_value.get("icon", None)
    status = skill_value.get("status", None)
    return icon == "lock" and status == "unknown"

def get_progress(skill_value):
    if _is_locked_skill_value(skill_value):
        return ("", Status.UNKNOWN)

    progress_string = skill_value.get("progress", None)
    if progress_string:
        Fraction(progress_string)
        current, total = map(int, progress_string.split("/"))
        status = Status.NEW
        if current > 0:
            status = Status.BEING_LEANRED if current < total else Status.LEARNED

        return (f"{'■' * current}{'□' * (total - current)}", status)
    else:
        return ("", Status.NEW)


def create_skill_node(skill_id, skill_value):
    if not skill_value:
        locked_skill_value = {"name": "???", "icon": "lock", "status": "unknown"}
        skill_value = locked_skill_value
    skill_name = skill_value.get("name", "")
    skill_icon = get_icon(skill_value)
    skill_progress, skill_status = get_progress(skill_value)
    skill_icon_label = get_node_content([skill_icon, skill_name, skill_progress])
    skill_id_and_name = f"{skill_id}(\"{skill_icon_label}\")"
    skill_style = f"class {skill_id} {skill_status.value}Skill;"
    skill_requires = get_required_node_edges(skill_id, skill_value.get("requires", []))
    sections = [
        skill_id_and_name,
        skill_style,
        skill_requires,
    ]
    skill_graph = "\n".join(sections)
    return skill_graph