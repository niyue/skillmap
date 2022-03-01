SECTION_SEPARATOR = "%" * 30

def get_required_node_edges(qualified_node_id, required_node_ids):
    node_requires = [
        f"{required_node_id}-->{qualified_node_id}"
        for required_node_id in required_node_ids
    ]
    return "\n".join(node_requires)


def get_icon(dict_value):
    icon = ""
    if "icon" in dict_value:
        icon = f"fa:fa-{dict_value['icon']}"
    return icon


def get_node_content(items, multi_lines_layout=True):
    separator = "<br/>" if multi_lines_layout else " "
    # join non empty items
    return separator.join([i for i in items if i])
