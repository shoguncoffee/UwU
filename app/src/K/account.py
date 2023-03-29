from __future__ import annotations
from ..base import *
from ..constants import AccountStatus

@dataclass
class Account :
    __username: str # type: ignore
    __password: str # type: ignore
    __email: str # type: ignore
    __status: AccountStatus = AccountStatus.PENDING # type: ignore
    #__reference: str # type: ignore
    
    @property
    def username(self):
        return self.__username
    
    @property
    def email(self):
        return self.__email
    
    @property
    def password(self):
        return self.__password
    
    @property
    def status(self):
        return self.__status