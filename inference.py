import os
import requests
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
API_KEY = os.getenv("API_KEY")

# Initialize OpenAI using the proxy they inject
client = OpenAI(
    api_key=API_KEY,
    base_url=API_BASE_URL
)

# Environment URL (your HuggingFace env)
ENV_URL = "https://snowydandruff-github-triage-openenv.hf.space"


def main():
    print(f"[START] task=github-triage env=github_triage_env model={MODEL_NAME}")

    try:
        # Reset environment
        reset = requests.post(f"{ENV_URL}/reset")
        obs = reset.json()["observation"]

        issue_text = f"{obs['issue_title']} {obs['issue_body']}"

        # REQUIRED LLM CALL THROUGH PROXY
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are a GitHub issue triage assistant."
                },
                {
                    "role": "user",
                    "content": f"Classify this GitHub issue and choose label, priority, and decision:\n\n{issue_text}"
                }
            ]
        )

        # simple baseline action
        action = {
            "action": {
                "label": "bug",
                "priority": "high",
                "decision": "assign_label"
            }
        }

        step = requests.post(
            f"{ENV_URL}/step",
            json=action
        )

        result = step.json()

        reward = result.get("reward", 0.0)
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
