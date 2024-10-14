from fastapi import FastAPI, status
from api.health_check import HealthCheckResponse
import api.utils as utils


description = """
Yggdrasil helps you to interact with Large Language Models of choice running
in Ollama.

You are able to:

* **/healthz** check health of API.
"""


app = FastAPI(
    title='Yggdrasil',
    description=description,
    version="1.0.0",
    contact={
        "name": "Dina Teimouri",
        "url": "https://www.linkedin.com/in/dinateimouri/",
        "email": "dinateimouri.dt@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://github.com/dinateimouri/yggdrasil/blob/main/LICENSE",
    },
)

# Load the text classification pipeline
text_classification_pipeline = utils.load_text_classification_pipeline()


@app.get(
    "/healthz",
    tags=["Health check"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
def health_check() -> HealthCheckResponse:
    """
    Checks Yggdrasil API health

    Returns a JSON response with the health status
    """
    return HealthCheckResponse(status="ok")
