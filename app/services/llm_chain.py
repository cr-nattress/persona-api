"""
LangChain LLM integration for persona generation.

Implements a two-step pipeline:
1. Clean/normalize raw text into structured notes
2. Generate comprehensive persona JSON from cleaned notes
"""

import json
import re
import time
from pathlib import Path
from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import settings
from app.core.logging import get_logger, log_llm_request, log_llm_response

logger = get_logger(__name__)


class PersonaLLMChain:
    """Two-step LLM chain for persona generation."""

    def __init__(self):
        """Initialize LLM chain with OpenAI ChatGPT."""
        self.model = ChatOpenAI(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            temperature=0.7,
            max_tokens=2000,
        )
        self._load_prompts()

    def _load_prompts(self) -> None:
        """Load prompt templates from files."""
        prompts_dir = Path("prompts")

        # Load step 1 prompts
        self.step1_system = self._read_prompt_file(
            prompts_dir / "step1_clean_system.txt"
        )
        self.step1_user = self._read_prompt_file(
            prompts_dir / "step1_clean_user.txt"
        )

        # Load step 2 prompts
        self.step2_system = self._read_prompt_file(
            prompts_dir / "step2_persona_system.txt"
        )
        self.step2_user = self._read_prompt_file(
            prompts_dir / "step2_persona_user.txt"
        )

        logger.debug("Prompt templates loaded successfully")

    def _read_prompt_file(self, filepath: Path) -> str:
        """
        Read a prompt template file.

        Args:
            filepath: Path to the prompt file

        Returns:
            Contents of the file

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            logger.error(f"Prompt file not found: {filepath}")
            raise

    async def step1_clean_text(self, raw_text: str) -> str:
        """
        Step 1: Clean and normalize raw text into structured notes.

        Args:
            raw_text: Unstructured text about a person

        Returns:
            Cleaned, normalized bullet-point summary

        Raises:
            ValueError: If cleaning fails
        """
        try:
            logger.debug("Starting Step 1: Text Cleaning")

            # Create prompt
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.step1_system),
                ("human", self.step1_user),
            ])

            # Create chain
            chain = prompt | self.model

            # Log LLM request
            log_llm_request(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": self.step1_system},
                    {"role": "user", "content": self.step1_user.replace("{raw_text}", raw_text[:200])},
                ],
                temperature=0.7,
                max_tokens=2000,
            )

            # Run chain with timing
            logger.debug(f"Processing text: {raw_text[:100]}...")
            start_time = time.time()
            result = await chain.ainvoke({"raw_text": raw_text})
            latency_ms = (time.time() - start_time) * 1000

            cleaned_text = result.content

            # Log LLM response
            log_llm_response(
                model=settings.openai_model,
                response_text=cleaned_text,
                latency_ms=latency_ms,
            )

            logger.info(f"Step 1 completed: {len(cleaned_text)} chars cleaned (latency: {latency_ms:.0f}ms)")
            return cleaned_text

        except Exception as e:
            logger.error(f"Step 1 failed: {e}")
            raise ValueError(f"Text cleaning failed: {e}") from e

    async def step2_populate_persona(
        self, cleaned_text: str
    ) -> Dict[str, Any]:
        """
        Step 2: Generate comprehensive persona JSON from cleaned notes.

        Args:
            cleaned_text: Cleaned and organized notes from Step 1

        Returns:
            Structured persona JSON as dictionary

        Raises:
            ValueError: If persona generation or JSON parsing fails
        """
        try:
            logger.debug("Starting Step 2: Persona Population")

            # Create prompt
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.step2_system),
                ("human", self.step2_user),
            ])

            # Create chain
            chain = prompt | self.model

            # Log LLM request
            log_llm_request(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": self.step2_system},
                    {"role": "user", "content": self.step2_user.replace("{cleaned_text}", cleaned_text[:200])},
                ],
                temperature=0.7,
                max_tokens=2000,
            )

            # Run chain with timing
            logger.debug("Generating persona JSON...")
            start_time = time.time()
            result = await chain.ainvoke({"cleaned_text": cleaned_text})
            latency_ms = (time.time() - start_time) * 1000

            persona_text = result.content

            # Log LLM response
            log_llm_response(
                model=settings.openai_model,
                response_text=persona_text,
                latency_ms=latency_ms,
            )

            # Parse JSON
            persona_json = self._safe_json_parse(persona_text)
            logger.info(f"Step 2 completed: Persona JSON generated (latency: {latency_ms:.0f}ms)")
            return persona_json

        except Exception as e:
            logger.error(f"Step 2 failed: {e}")
            raise ValueError(f"Persona generation failed: {e}") from e

    def _safe_json_parse(self, text: str) -> Dict[str, Any]:
        """
        Safely parse JSON from text, handling common issues.

        Args:
            text: Text containing JSON (possibly with markdown or extra text)

        Returns:
            Parsed JSON as dictionary

        Raises:
            ValueError: If JSON cannot be parsed
        """
        logger.debug(f"_safe_json_parse() called")
        logger.debug(f"  - input text type: {type(text)}")
        logger.debug(f"  - input text length: {len(text) if isinstance(text, str) else 'N/A'}")
        logger.debug(f"  - input text preview: {text[:200] if isinstance(text, str) else repr(text)[:200]}")

        try:
            # Try direct parse first
            logger.debug("Attempting direct JSON parse...")
            result = json.loads(text)
            logger.debug(f"Direct JSON parse successful! Keys: {list(result.keys()) if isinstance(result, dict) else 'NOT A DICT'}")
            return result
        except json.JSONDecodeError as e:
            logger.debug(f"Direct parse failed: {e}")
            pass

        # Try to extract JSON from markdown code blocks
        try:
            logger.debug("Attempting markdown code block extraction...")
            match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
            if match:
                logger.debug(f"Found markdown block, attempting to parse...")
                result = json.loads(match.group(1))
                logger.debug(f"Markdown block parse successful! Keys: {list(result.keys()) if isinstance(result, dict) else 'NOT A DICT'}")
                return result
            else:
                logger.debug("No markdown code block found")
        except (json.JSONDecodeError, AttributeError) as e:
            logger.debug(f"Markdown block parse failed: {e}")
            pass

        # Try to extract JSON object directly
        try:
            logger.debug("Attempting direct JSON object extraction (brace matching)...")
            # Find the first { and last }
            start = text.find("{")
            end = text.rfind("}") + 1
            logger.debug(f"  - First opening brace at position: {start}")
            logger.debug(f"  - Last closing brace at position: {end - 1}")

            if start != -1 and end > start:
                json_str = text[start:end]
                logger.debug(f"  - Extracted substring length: {len(json_str)}")
                logger.debug(f"  - Extracted substring preview: {json_str[:300]}")

                result = json.loads(json_str)
                logger.debug(f"Brace matching parse successful! Keys: {list(result.keys()) if isinstance(result, dict) else 'NOT A DICT'}")
                return result
            else:
                logger.debug(f"Could not find valid braces: start={start}, end={end}")
        except json.JSONDecodeError as e:
            logger.debug(f"Brace matching parse failed: {e}")
            pass

        # If all else fails, log and raise
        logger.error(f"Could not parse JSON from text")
        logger.error(f"  - Text length: {len(text)}")
        logger.error(f"  - Text preview: {text[:500]}")
        has_open_brace = '{' in text
        has_close_brace = '}' in text
        logger.error(f"  - Text contains opening brace: {has_open_brace}")
        logger.error(f"  - Text contains closing brace: {has_close_brace}")
        raise ValueError("Could not parse JSON response from LLM")

    async def generate_persona(self, raw_text: str) -> Dict[str, Any]:
        """
        Generate a complete persona from raw text (both steps).

        Args:
            raw_text: Unstructured text about a person

        Returns:
            Complete persona JSON

        Raises:
            ValueError: If either step fails
        """
        try:
            logger.info("Starting persona generation pipeline")
            logger.debug(f"Input text length: {len(raw_text)} chars")
            logger.debug(f"Input raw_text type: {type(raw_text)}")
            logger.debug(f"Input raw_text preview: {raw_text[:150]}")

            # Step 1: Clean text
            logger.debug("Executing Step 1: Clean text...")
            cleaned_text = await self.step1_clean_text(raw_text)
            logger.debug(f"Step 1 complete: cleaned_text type={type(cleaned_text)}, length={len(cleaned_text)}")

            # Step 2: Populate persona
            logger.debug("Executing Step 2: Populate persona...")
            persona = await self.step2_populate_persona(cleaned_text)

            logger.debug(f"Step 2 complete: persona type={type(persona)}")
            logger.debug(f"Step 2 result is dict: {isinstance(persona, dict)}")
            if isinstance(persona, dict):
                logger.debug(f"Step 2 result keys: {list(persona.keys())}")
            else:
                logger.debug(f"Step 2 result is NOT a dict! It's: {repr(persona)[:300]}")

            # Add metadata
            logger.debug("Adding metadata to persona...")
            persona["_meta"] = {
                "raw_text_length": len(raw_text),
                "cleaned_text_length": len(cleaned_text),
                "model_used": settings.openai_model,
            }

            logger.debug(f"Final persona object:")
            logger.debug(f"  - type: {type(persona)}")
            logger.debug(f"  - is dict: {isinstance(persona, dict)}")
            logger.debug(f"  - keys: {list(persona.keys()) if isinstance(persona, dict) else 'NOT A DICT'}")
            logger.debug(f"  - size: {len(str(persona))} chars")
            logger.debug(f"  - preview: {str(persona)[:400]}")

            logger.info("Persona generation pipeline completed successfully")
            return persona

        except Exception as e:
            logger.error(f"Persona generation pipeline failed: {e}")
            logger.error(f"  - Exception type: {type(e).__name__}")
            logger.error(f"  - Exception details: {str(e)}")
            logger.error(f"  - Full traceback: ", exc_info=True)
            raise


def get_persona_llm_chain() -> PersonaLLMChain:
    """
    Get a PersonaLLMChain instance.

    Returns:
        PersonaLLMChain instance

    Usage:
        from app.services.llm_chain import get_persona_llm_chain
        chain = get_persona_llm_chain()
        persona = await chain.generate_persona(raw_text)
    """
    return PersonaLLMChain()
