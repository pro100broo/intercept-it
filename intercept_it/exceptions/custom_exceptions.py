class InterceptItException(Exception):
    """ Exception raises during interceptor executing """
    pass


class InterceptItSetupException(Exception):
    """ Exception raises during interceptor initialization """
    pass


class ContinueProgramException(Exception):
    pass


class StopProgramException(Exception):
    pass
