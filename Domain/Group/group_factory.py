from Domain.Group.group import GroupType, Group


def create_group(id: str, name: str, type: str):
    if type == "LIGHT":
        return Group(id, name, GroupType.LIGHT)
    return Group(id, name, GroupType.MIX)
