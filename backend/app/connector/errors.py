class BotpressError(Exception):
    pass


class ValidationError(BotpressError):
    pass


class TimeoutError(BotpressError):
    pass