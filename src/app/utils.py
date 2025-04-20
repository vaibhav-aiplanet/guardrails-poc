import os

from guardrails import Guard
from guardrails.hub import LlamaGuard7B
from app.validators import toxic_words

# gr.install("hub://guardrails/detect_jailbreak")
# gr.install("hub://guardrails/llamaguard_7b")


os.environ["GEMINI_API_KEY"] = ""
os.environ["AZURE_API_KEY"] = ""  # "my-azure-api-key"
os.environ["AZURE_API_BASE"] = "" # "https://my-azure-endpoint.openai.azure.com/"
os.environ["AZURE_API_VERSION"] = ""  # "2023-05-15"


# Setup Guard
guard = Guard(name="validator").use(LlamaGuard7B).use(toxic_words)


def validate(prompt: str):
    try:
        print(prompt)
        response = guard.parse(prompt)

        if response.validation_passed:
            print(response)
            return

        return response.error
    except Exception as e:
        print(e)


def call_llm(prompt: str, output_model):
    try:
        guard = Guard.for_pydantic(output_model)

        # gemini, it doesn't support output_schema with pydantic yet
        # result = guard(
        #     messages=[{"role": "user", "content": prompt}], model="gemini/gemin-pro"
        # )

        # azure openai
        result = guard(
            messages=[{"role": "user", "content": prompt}], model="azure/gpt-4o"
        )
        return result.validated_output
    except Exception as e:
        print(e)
