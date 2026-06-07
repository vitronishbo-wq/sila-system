"""
Consolidated request numbering and sequencing utilities.

This module provides standardized request number generation for all services.
Instead of each service implementing its own numbering logic, they use
the utilities provided here, ensuring consistent formatting and incrementation.

Usage:
    from apps.backend.app.core.sequencing import RequestNumberGenerator

    # In service
    generator = RequestNumberGenerator(repository, year=2025)
    request_number = await generator.generate_service_request_number()  # SR/2025/000001
    request_number = await generator.generate_healthcare_request_number()  # HR/2025/000001
"""

from datetime import datetime


class RequestNumberGenerator:
    """
    Generates standardized request numbers across all services.

    Ensures:
    - Consistent format (PREFIX/YEAR/SEQUENCE)
    - Sequential unique numbers per year
    - Easy to extend for new domains
    """

    def __init__(self, repository, year: int | None = None):
        """
        Initialize generator.

        Args:
            repository: Request repository for sequence lookup
            year: Optional year override (default: current year)
        """
        self.repository = repository
        self.year = year or datetime.now().year

    async def generate_service_request_number(self) -> str:
        """
        Generate service request number.

        Format: SR/YYYY/NNNNNN
        Example: SR/2025/000142
        """
        sequence = await self.repository.get_next_sequence(self.year)
        return f"SR/{self.year}/{sequence:06d}"

    async def generate_healthcare_request_number(self) -> str:
        """
        Generate healthcare request number.

        Format: HR/YYYY/NNNNNN
        Example: HR/2025/000089
        """
        sequence = await self.repository.get_next_sequence(self.year)
        return f"HR/{self.year}/{sequence:06d}"

    async def generate_citizen_request_number(self) -> str:
        """
        Generate citizen request number.

        Format: CR/YYYY/NNNNNN
        Example: CR/2025/000045
        """
        sequence = await self.repository.get_next_sequence(self.year)
        return f"CR/{self.year}/{sequence:06d}"

    def format_request_number(self, prefix: str, sequence: int) -> str:
        """
        Format a request number with given prefix and sequence.

        Args:
            prefix: Service prefix (e.g., "SR", "HR", "CR")
            sequence: Sequential number

        Returns:
            Formatted request number (e.g., "SR/2025/000142")
        """
        return f"{prefix}/{self.year}/{sequence:06d}"

    def parse_request_number(self, request_number: str) -> dict:
        """
        Parse request number into components.

        Args:
            request_number: Request number to parse (e.g., "SR/2025/000142")

        Returns:
            Dict with 'prefix', 'year', 'sequence'

        Raises:
            ValueError: If number format is invalid
        """
        parts = request_number.split("/")
        if len(parts) != 3:
            raise ValueError(f"Invalid request number format: {request_number}")
        try:
            return {"prefix": parts[0], "year": int(parts[1]), "sequence": int(parts[2])}
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid request number format: {request_number}") from e


async def generate_request_number(
    repository, service_type: str = "service", year: int | None = None
) -> str:
    """
    Convenience function to generate request number directly.

    Args:
        repository: Request repository
        service_type: One of "service", "healthcare", "citizen"
        year: Optional year (default: current year)

    Returns:
        Generated request number

    Examples:
        # Service request
        num = await generate_request_number(repo, "service")  # SR/2025/000001

        # Healthcare request
        num = await generate_request_number(repo, "healthcare")  # HR/2025/000089

        # Citizen request
        num = await generate_request_number(repo, "citizen")  # CR/2025/000045
    """
    generator = RequestNumberGenerator(repository, year)
    generator_map = {
        "service": generator.generate_service_request_number,
        "healthcare": generator.generate_healthcare_request_number,
        "citizen": generator.generate_citizen_request_number,
    }
    if service_type not in generator_map:
        raise ValueError(
            f"Unknown service type: {service_type}. Must be one of: {list(generator_map.keys())}"
        )
    return await generator_map[service_type]()
