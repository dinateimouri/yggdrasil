from fastapi import FastAPI, status
from api.health_check import HealthCheckResponse
from api.sync_chat import (
    SyncChatRequest,
    SyncChatResponse,
    ExpectedErrorMessage,
    UnexpectedErrorMessage,
)
import api.utils as utils
import pandas as pd
from fastapi.responses import JSONResponse


description = """
Yggdrasil helps you to interact with Large Language Models of choice running
in Ollama.

You are able to:

* **/healthz** check health of API.
"""

# Load Config files
config = utils.read_config()


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


@app.post(
    "/sync-chat",
    tags=["Sync Chat"],
    summary="Sync Chat with Large Language Models",
    response_model=SyncChatResponse,
    responses={
        400: {
            "model": ExpectedErrorMessage,
            "description": "Bad Requests",
        },
        200: {
            "model": SyncChatResponse,
            "description": "Successful response",
        },
        500: {
            "model": UnexpectedErrorMessage,
            "description": "Unexpected error",
        },
    },
)
def sync_chat(request: SyncChatRequest):
    """
    Sync Chat with Large Language Models

    Returns a JSON response with the chat response
    """
    most_similar_prompt = None
    match request.similarity_measure:
        case "cosine":
            similarity_response = utils.similarity_cosine(request.prompts)
            if similarity_response['successful']:
                similarity_matrix = similarity_response['similarity_matrix']
                similarity_matrix_df = pd.DataFrame(similarity_matrix)
                avg_similarity_matrix = similarity_matrix_df.mean()
                if avg_similarity_matrix.min() <= \
                        config['similarity_measure']['thresholds']['cosine']:
                    most_similar_prompt = avg_similarity_matrix.idxmin()
                else:
                    return JSONResponse(
                        status_code=400,
                        content={"response": "No similar prompts found."},
                    )
            else:
                return JSONResponse(
                    status_code=500,
                    content={
                        "response": "This is an unexpected error, \
                        please contact support",
                    },
                )
        case "euclidean":
            similarity_response = utils.similarity_euclidean(request.prompts)
            if similarity_response['successful']:
                similarity_matrix = similarity_response['similarity_matrix']
                similarity_matrix_df = pd.DataFrame(similarity_matrix)
                avg_similarity_matrix = similarity_matrix_df.mean()
                if avg_similarity_matrix.min() <= (
                    config['similarity_measure']['thresholds']['euclidean']
                ):
                    most_similar_prompt = avg_similarity_matrix.idxmin()
                else:
                    return JSONResponse(
                        status_code=400,
                        content={"response": "No similar prompts found."},
                    )
            else:
                return JSONResponse(
                    status_code=500,
                    content={
                        "response": "This is an unexpected error,\
                                     please contact support",
                    },
                )
        case "manhattan":
            similarity_response = utils.similarity_manhattan(request.prompts)
            if similarity_response['successful']:
                similarity_matrix = similarity_response['similarity_matrix']
                similarity_matrix_df = pd.DataFrame(similarity_matrix)
                avg_similarity_matrix = similarity_matrix_df.mean()
                if avg_similarity_matrix.min() <= (
                    config['similarity_measure']['thresholds']['manhattan']
                ):
                    most_similar_prompt = avg_similarity_matrix.idxmin()
                else:
                    return JSONResponse(
                        status_code=400,
                        content={"response": "No similar prompts found."},
                    )
            else:
                return JSONResponse(
                    status_code=500,
                    content={
                        "response": "This is an unexpected error,\
                                          please contact support",
                    },
                )

    profanity_replace_output = utils.profanity_replace(most_similar_prompt)
    most_similar_prompt_cencored = None
    if profanity_replace_output['successful']:
        most_similar_prompt_cencored = profanity_replace_output['message']
    else:
        return JSONResponse(
            status_code=500,
            content={
                "response": "This is an unexpected error, \
                    please contact support",
            },
        )

    prompt_harmfulness_score = utils.detect_harmful_content(
            pipe=text_classification_pipeline,
            input_text=most_similar_prompt_cencored,
    )
    llm_response = None
    if prompt_harmfulness_score < config['harmfulness']['threshold']:
        llm_response = utils.call_llm(
            input=most_similar_prompt_cencored,
            config=config,
        )
    else:
        return JSONResponse(
            status_code=400,
            content={"response": prompt_harmfulness_score},
        )

    profanity_replace_llm_response = utils.profanity_replace(llm_response)
    llm_response_cencored = None
    if profanity_replace_output['successful']:
        llm_response_cencored = profanity_replace_llm_response['message']
    else:
        return JSONResponse(
            status_code=500,
            content={
                "response": "This is an unexpected error, \
                                  please contact support",
            },
        )

    llm_response_harmfulness_score = utils.detect_harmful_content(
        pipe=text_classification_pipeline,
        input_text=llm_response_cencored,
    )
    if llm_response_harmfulness_score < \
            config['harmfulness']['threshold']:
        return JSONResponse(
            status_code=200,
            content={"response": llm_response_cencored},
        )
    else:
        return JSONResponse(
            status_code=500,
            content={
                "response": "This is an unexpected error, \
                                  please contact support",
            },
        )
