import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class TenantContext:
    user_id: uuid.UUID
    organization_id: uuid.UUID
