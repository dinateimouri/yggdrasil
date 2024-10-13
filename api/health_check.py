from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    """
    Schema for Health Check Response
    """
    status: str = "ok"
