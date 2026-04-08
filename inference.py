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
    print(f"[START] model={MODEL_NAME}")

    # Reset environment
    res = requests.post(f"{API_BASE_URL}/reset")
    data = res.json()

    observation = data["observation"]

    issue_title = observation["issue_title"]
    issue_body = observation["issue_body"]

    # Simple baseline policy
    action = {
        "action": {
            "label": "bug",
            "priority": "high",
            "decision": "assign_label"
        }
    }

    res = requests.post(
        f"{API_BASE_URL}/step",
        json=action
    )

    result = res.json()

    reward = result["reward"]
    done = result["done"]

    print(
        f"[STEP] action={action} reward={reward:.2f} done={done} error=null"
    )

    print(
        f"[END] success={done} score={reward:.2f}"
    )


if __name__ == "__main__":
    main()
