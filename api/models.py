from pydantic import BaseModel
import datetime
import time

from pydantic import BaseModel, Field
from enum import Enum
from typing import List
from fastapi import FastAPI, Body
from fastapi import APIRouter, Response, status,HTTPException
from utils.version import API_VERSION, SERVICE_NAME

class Payload(BaseModel):
    promt: str = Field(..., description="Prompt or description for audio generation")
    duration: int = Field(..., description="Desired duration of the generated audio in seconds")
    callbackUrl: str = Field(..., description="")

class Request(BaseModel):
    method: str = Field(..., description="API method to be called (e.g., audio_gen)")
    payload: Payload = Field(..., description="Request payload with specific details")

class AudioCraftRequestCall(BaseModel):
    userToken: str = Field(..., description="User authentication token")
    requestId: str = Field(..., description="Unique request ID for tracking purposes")
    request: Request = Field(..., description="Request details")

class AudioCraftRequestResult(BaseModel):
    userToken: str = Field(..., description="User authentication token")
    taskId: str = Field(..., description="Result id to retrieve result")

def response_template(request_id: str, 
                                  trace_id: str, 
                                  process_duration: int,
                                  isResponseImmediate: bool,
                                  response: dict,
                                  error_code: dict):
    now = datetime.datetime.now()
    now = now.isoformat()
    response_data = {
        "requestId": request_id,
        "traceId": trace_id,
        "apiVersion": API_VERSION,
        "service": SERVICE_NAME,
        "datetime": now,
        "isResponseImmediate": isResponseImmediate,
        "processDuration": process_duration,
        "response" : response,
        "errorCode" : error_code,
    }
    return response_data