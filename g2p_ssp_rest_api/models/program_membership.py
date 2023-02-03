from datetime import date

from extendable_pydantic import ExtendableModelMeta
from pydantic import BaseModel


class ProgramMembershipOut(BaseModel, metaclass=ExtendableModelMeta):
    id: int
    partner_id: int
    partner_name: str
    program_id: int
    program_name: str
    enrollment_date: date = None
    state: str
