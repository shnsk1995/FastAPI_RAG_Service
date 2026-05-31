from typing import Literal

from pydantic import BaseModel, Field

class InputGuardrailResult(BaseModel):
    original_input: str = Field(
        ...,
        description="Raw user input before guardrail processing",
    )

    processed_input: str = Field(
        ...,
        description="Input after Bedrock Guardrail processing",
    )

    was_blocked: bool = Field(
        default=False,
        description="Whether the input was blocked by the guardrail",
    )

    block_reason: str | None = Field(
        default=None,
        description="Reason for blocking the input, if blocked",
    )

    guardrail_action: Literal["none", "masked", "blocked"] = Field(
        default="none",
        description="Application-level action interpreted from Bedrock Guardrail response",
    )

    pii_detected: bool = Field(
        default=False,
        description="Whether PII was detected",
    )

    prompt_attack_detected: bool = Field(
        default=False,
        description="Whether prompt attack behavior was detected",
    )
    
