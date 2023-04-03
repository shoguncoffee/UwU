from __future__ import annotations

ScheduleDate = int
class ScheduleCatalog(set[ScheduleDate]):
    def search():
        ...
    
    @classmethod
    @property
    def x(cls):
        return 5
    
q = ScheduleCatalog()
print(q)