class DeviceException(Exception):
    pass


class GroupException(Exception):
    pass


class DeviceNotFound(DeviceException):
    pass


class CreateGroupError(GroupException):
    pass


class ControlGroupError(GroupException):
    pass
