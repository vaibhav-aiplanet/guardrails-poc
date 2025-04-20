from typing import Dict
from guardrails.validators import (
    FailResult,
    PassResult,
    register_validator,
    ValidationResult,
)

@register_validator(name="toxic-words", data_type="string")
def toxic_words(value, metadata: Dict) -> ValidationResult:
    mentioned_words = []
    for word in ["butt", "poop", "booger"]:
        if word in value:
            mentioned_words.append(word)

    if len(mentioned_words) > 0:
        return FailResult(
            error_message=f"Mention toxic words: {', '.join(mentioned_words)}",
        )
    else:
        return PassResult()