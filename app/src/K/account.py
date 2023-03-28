from __future__ import annotations
from app.base import *

from ..constants import AccountStatus

@dataclass
class Account :
    _username: str
    _email: str
    _reference: str
    _password: str
    _status: AccountStatus


    def verify_account(self):
        pass


    def check_username(self):
        pass
    

    def create_account(self):
        pass

    def get_username(self):
        return self._username