class ServiceError(Exception):
    """Base class for service errors."""


class EmailExistsError(ServiceError):
    """Dedublicate email."""
