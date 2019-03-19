__ALL__ = ['FaktoryHandshakeError', 'FaktoryAuthenticationError']


class FaktoryHandshakeError(OSError):
    pass


class FaktoryAuthenticationError(OSError):
    pass
