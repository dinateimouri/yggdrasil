from pydantic import BaseModel, conlist, constr
from typing import Optional
from enum import Enum
from api.utils import read_config


config = read_config()


class SimilarityMeasure(str, Enum):
    """
    Enum for Similarity Measure
    """
    cosine = "cosine"
    euclidean = "euclidean"
    manhattan = "manhattan"


class SyncChatRequest(BaseModel):
    """
    Schema for Sync Chat Requests
    """
    similarity_measure: Optional[SimilarityMeasure] = \
        config['similarity_measure']['default']
    prompts: conlist(
        constr(
            strip_whitespace=True,
            min_length=config['prompts']['strings']['min_length'],
            max_length=config['prompts']['strings']['max_length'],
        ),
        min_length=2,
        max_length=config['prompts']['max_length'],
    )  # type: ignore
    # The minimum length of the prompts list is 2, as we are performing
    # similarity measures


class SyncChatResponse(BaseModel):
    """
    Schema for Sync Chat Response
    """
    response: str


class ExpectedErrorMessage(BaseModel):
    response: str = "No similar prompts found!"


class UnexpectedErrorMessage(BaseModel):
    response: str = "This is an unexpected error, please contact support!"
