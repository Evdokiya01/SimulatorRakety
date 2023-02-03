class PhononError(Exception):
    pass


class AlreadyLocked(PhononError):
    pass


class ArgumentError(PhononError):
    pass


class NotImplementedError(PhononError):
    pass
