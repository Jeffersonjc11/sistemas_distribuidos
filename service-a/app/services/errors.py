class ServiceError(Exception):
    pass


class ServiceConflictError(ServiceError):
    pass


class ServiceNotFoundError(ServiceError):
    pass


class ServiceUnavailableError(ServiceError):
    pass
