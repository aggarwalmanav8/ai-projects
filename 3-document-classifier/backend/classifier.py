from pydantic import BaseModel, Field
from typing import Literal
import json
from pydantic import ValidationError
import os
from dotenv import load_dotenv

load_dotenv()

class DocumentClassification(BaseModel):
    """
    Schema for KYC document classification.
    LLM returns confidence scores; action is computed by backend.
    """

    doc_type: Literal["pan", "aadhaar", "passport", "voterid", "dl"]
    doc_type_confidence: float = Field(ge=0, le=1, description="Confidence in doc_type classification")

    name: str | None = Field(default=None, description="Extracted name from document")
    name_confidence: float = Field(ge=0, le=1, description="Confidence in name extraction")

    dob: str | None = Field(default=None, description="Extracted DOB (DD-MM-YYYY format)")
    dob_confidence: float = Field(ge=0, le=1, description="Confidence in DOB extraction")


def get_tool_schema() -> dict:
    """
    Generate OpenAI function schema for document classification.
    Keeps schema definition in one place for reuse and testing.
    """
    return {
        "type": "function",
        "function": {
            "name": "classify_document",
            "description": "Classifies an Indian KYC document and extracts structured data",
            "parameters": {
                "type": "object",
                "properties": {
                    "doc_type": {
                        "type": "string",
                        "enum": ["pan", "aadhaar", "passport", "voterid", "dl"],
                        "description": "Type of Indian ID document"
                    },
                    "doc_type_confidence": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1,
                        "description": "Confidence score for document type (0-1)"
                    },
                    "name": {
                        "type": ["string", "null"],
                        "description": "Extracted name from document, or null if not found"
                    },
                    "name_confidence": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1,
                        "description": "Confidence score for name extraction (0-1)"
                    },
                    "dob": {
                        "type": ["string", "null"],
                        "description": "Extracted DOB in DD-MM-YYYY format, or null if not found"
                    },
                    "dob_confidence": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1,
                        "description": "Confidence score for DOB extraction (0-1)"
                    }
                },
                "required": ["doc_type", "doc_type_confidence", "name_confidence", "dob_confidence"]
            }
        }
    }


def compute_action(doc_type_conf: float, name_conf: float, dob_conf: float) -> str:
    """
    Compute action based on confidence thresholds.
    Business logic: backend decides approval, not the LLM.

    Thresholds:
    - approve: all scores >= 0.75 (high confidence)
    - needs_review: all scores >= 0.5 (medium confidence)
    - decline: any score < 0.5 (low confidence)
    """
    min_confidence = min(doc_type_conf, name_conf, dob_conf)

    if min_confidence >= 0.75:
        return "approve"
    elif min_confidence >= 0.5:
        return "needs_review"
    else:
        return "decline"


def classify_document(description: str) -> dict:
    """
    Classify a KYC document from free-text description.
    """
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")

    try:
        # Build the function schema manually for older SDK
        tool_schema = get_tool_schema()
        
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            max_tokens=500,
            functions=[tool_schema["function"]],  # Extract just the function part
            function_call="auto",  # Tell it to use the function
            messages=[
                {
                    "role": "system",
                    "content": """You are a KYC document classification expert.
Analyze the provided document description and extract structured data.

Guidelines:
- Be conservative with confidence scores (0.9+ only if you are certain)
- If document type is ambiguous, lower doc_type_confidence
- If name/DOB cannot be extracted, set to null
- Return confidence scores only; action is computed by the backend"""
                },
                {
                    "role": "user",
                    "content": f"Classify this document: {description}"
                }
            ]
        )

        # Extract function call
        if response["choices"][0]["message"].get("function_call"):
            function_call = response["choices"][0]["message"]["function_call"]
            arguments = json.loads(function_call["arguments"])

            # Validate with Pydantic
            classification = DocumentClassification(**arguments)

            # Compute action in backend (not by LLM)
            action = compute_action(
                classification.doc_type_confidence,
                classification.name_confidence,
                classification.dob_confidence
            )

            # Build response
            result_dict = classification.model_dump()
            result_dict["action"] = action

            return {
                "success": True,
                "data": result_dict
            }
        else:
            return {
                "success": False,
                "error": "Model did not call classification function",
                "details": "No function_call in response"
            }

    except ValidationError as e:
        return {
            "success": False,
            "error": "Classification validation failed",
            "details": str(e)
        }
    except Exception as e:
        return {
            "success": False,
            "error": "Failed to classify document",
            "details": str(e)
        }