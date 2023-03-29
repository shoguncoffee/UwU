from __future__ import annotations
from ..base import *
from ..constants import AccountStatus

@dataclass
class Account :
    _username: str # type: ignore
    _password: str # type: ignore
    _email: str # type: ignore
    _status: AccountStatus = AccountStatus.PENDING # type: ignore
    #__reference: str # type: ignore
    
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