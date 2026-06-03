import asyncio
from typing import Any

import boto3
from botocore.exceptions import BotoCoreError, ClientError


from app.config import settings
from app.core.logging import get_logger
from app.exceptions import InputGuardrailError
from app.schemas.input_guardrail import InputGuardrailResult



logger = get_logger(__name__)


class InputGuardrailClient:

    def __init__(self):
        if not settings.BEDROCK_GUARDRAIL_ID:
            raise InputGuardrailError("BEDROCK_GUARDRAIL_ID is missing")

        try:
            session = boto3.Session(
                profile_name=settings.AWS_PROFILE,
                region_name=settings.AWS_REGION,
            )

            self.client = session.client("bedrock-runtime")

        except (BotoCoreError, ClientError) as exc:
            raise InputGuardrailError(
                "Failed to initialize Bedrock input guardrail client"
            ) from exc

        
    async def process_input(self, raw_input: str) -> InputGuardrailResult:
        cleaned_input = raw_input.strip()

        if not cleaned_input:
            return InputGuardrailResult(
                original_input=raw_input,
                processed_input="",
                was_blocked=True,
                block_reason="Input cannot be empty.",
                guardrail_action="blocked",
                pii_detected=False,
                prompt_attack_detected=False,
            )

        try:
            logger.info(
                "input_guardrail_started",
                input_length=len(cleaned_input),
                guardrail_id=settings.BEDROCK_GUARDRAIL_ID,
                guardrail_version=settings.BEDROCK_GUARDRAIL_VERSION,
            )

            response = await asyncio.to_thread(
                self.client.apply_guardrail,
                guardrailIdentifier=settings.BEDROCK_GUARDRAIL_ID,
                guardrailVersion=settings.BEDROCK_GUARDRAIL_VERSION,
                source="INPUT",
                content=[
                    {
                        "text" : {
                            "text" : cleaned_input
                        }
                    }
                ],
                outputScope=settings.BEDROCK_GUARDRAIL_OUTPUT_SCOPE,
            )

            result = self._to_result(
                original_input=raw_input,
                cleaned_input=cleaned_input,
                response=response,
            )

            logger.info(
                "input_guardrail_completed",
                was_blocked=result.was_blocked,
                guardrail_action=result.guardrail_action,
                pii_detected=result.pii_detected,
                prompt_attack_detected=result.prompt_attack_detected,
                processed_input_length=len(result.processed_input),
            )

            return result

        except InputGuardrailError:
            raise

        except (BotoCoreError, ClientError) as exc:
            logger.exception("input_guardrail_failed")

            raise InputGuardrailError(
                "Failed to process input with Bedrock Guardrail"
            ) from exc


    def _to_result(self, original_input: str, cleaned_input: str, response: dict[str, Any]) -> InputGuardrailResult:
        action = response.get("action")
        action_reason = response.get("actionReason")
        outputs = response.get("outputs", [])
        assessments = response.get("assessments", [])

        pii_detected = self._has_pii_detected(assessments)
        prompt_attack_detected = self._has_prompt_attack_detected(assessments)

        processed_input = self._extract_processed_text(
            outputs=outputs,
            fallback=cleaned_input,
        )

        if action == "GUARDRAIL_INTERVENED":
            if action_reason == "Guardrail masked.":
                return InputGuardrailResult(
                original_input=original_input,
                processed_input=processed_input,
                was_blocked=False,
                block_reason="N/A",
                guardrail_action="masked",
                pii_detected=pii_detected,
                prompt_attack_detected=prompt_attack_detected,
            )
            

            if action_reason == "Guardrail blocked.":
                return InputGuardrailResult(
                original_input=original_input,
                processed_input=processed_input,
                was_blocked=True,
                block_reason="Sorry, the model cannot answer this question.",
                guardrail_action="blocked",
                pii_detected=pii_detected,
                prompt_attack_detected=prompt_attack_detected,
            )
            

        return InputGuardrailResult(
                original_input=original_input,
                processed_input=processed_input,
                was_blocked=False,
                block_reason="N/A",
                guardrail_action="none",
                pii_detected=pii_detected,
                prompt_attack_detected=prompt_attack_detected,
            )

        

    def _extract_processed_text(self, outputs: list[dict[str, Any]], fallback: str) -> str:
        if not outputs:
            return fallback

        first_output = outputs[0]
        return first_output.get("text") or fallback

    def _has_pii_detected(self, assessments: list[dict[str, Any]]) -> bool:
        for assessment in assessments:
            sensitive_policy = assessment.get("sensitiveInformationPolicy", {})
            pii_entities = sensitive_policy.get("piiEntities", [])

            for entity in pii_entities:
                if entity.get("detected") is True:
                    return True

        return False



    def _has_prompt_attack_detected(self,assessments: list[dict[str, Any]]) -> bool:
        for assessment in assessments:
            content_policy = assessment.get("contentPolicy", {})
            filters = content_policy.get("filters", [])

            for content_filter in filters:
                filter_type = str(content_filter.get("type", "")).upper()
                detected = content_filter.get("detected") is True

                if detected and filter_type == "PROMPT_ATTACK":
                    return True

        return False