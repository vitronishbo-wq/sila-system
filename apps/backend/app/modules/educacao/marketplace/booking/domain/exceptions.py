"""Domain exceptions for Booking subdomain"""


class BookingException(Exception):
    """Base exception for Booking subdomain"""
    pass


class VacancyNotAvailable(BookingException):
    """Vaga não disponível para reserva"""
    pass


class BookingAlreadyExists(BookingException):
    """Cidadão já possui reserva para este programa"""
    pass


class BookingExpired(BookingException):
    """Reserva expirou"""
    pass


class EnrollmentFailed(BookingException):
    """Falha na pré-matrícula automática"""
    pass


class DuplicateBooking(BookingException):
    """Tentativa de reservar vaga duplicada"""
    pass
