# TODO ファイル分け
class DeviceException(Exception):
    pass


class GroupException(Exception):
    pass


class DeviceNotFound(DeviceException):
    pass


class CreateGroupWithoutDevice(GroupException):
    pass


class CreateGroupWithoutname(GroupException):
    pass
