from __future__ import annotations
from ..base import *

@dataclass(slots=True)
class Account:
    _username: str
    _password: str
    _email: str
    _phone: str
    _status: AccountStatus = field(init=False, default=AccountStatus.PENDING)
    # __reference: str # type: ignore
    
    @property
    def username(self):
        return self._username
    
    @property
    def email(self):
        return self._email
    
    @property
    def password(self):
        return self._password
    
    @property
    def status(self):
        return self._status