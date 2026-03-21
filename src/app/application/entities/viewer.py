from dataclasses import dataclass
from uuid import UUID


@dataclass
class AuthenticatedUser:
    user_id: UUID
    email: str
    role: str
    is_staff: bool

    @property
    def is_mentor(self) -> bool:
        return self.role == "mentor"

    @property
    def is_intern(self) -> bool:
        return self.role == "intern"
