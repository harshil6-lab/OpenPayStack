from pydantic import BaseModel
from datetime import datetime

class DeviceInfo(BaseModel):
   ip_address : str | None = None
   user_agent : str | None = None

from pydantic import ConfigDict

class SessionResponse(BaseModel):
    device_name: str | None
    browser: str | None
    os: str | None
    ip_address: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)