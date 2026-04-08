import os
import requests
from openai import OpenAI

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "https://snowydandruff-github-triage-openenv.hf.space"
)

MODEL_NAME = os.getenv("MODEL_NAME", "baseline")
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI()


def main():
    print(f"[START] task=github-triage env=github_triage_env model={MODEL_NAME}")

    try:
        reset = requests.post(f"{API_BASE_URL}/reset")
        data = reset.json()

        observation = data["observation"]

        action = {
            "action": {
                "label": "bug",
                "priority": "high",
                "decision": "assign_label"
            }
        }

        step = requests.post(
            f"{API_BASE_URL}/step",
            json=action
        )

        result = step.json()

        reward = result.get("reward", 0)
        done = result.get("done", False)

        print(
            f"[STEP] step=1 action={action['action']} reward={reward:.2f} done={done} error=null"
        )

        print(
            f"[END] success={done} steps=1 score={reward:.2f} rewards={reward:.2f}"
        )

    except Exception as e:
        print(f"[END] success=false steps=0 score=0 error={str(e)}")


if __name__ == "__main__":
    main()
