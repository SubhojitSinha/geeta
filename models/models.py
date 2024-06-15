from models.base_model import BaseModel

class Account(BaseModel):
    def __init__(self):
        super().__init__('accounts')

class User(BaseModel):
    def __init__(self):
        super().__init__('users')

class RequestLogs(BaseModel):
    def __init__(self):
        super().__init__('request_logs')

class SchedulerData(BaseModel):
    def __init__(self):
        super().__init__('scheduler_data')