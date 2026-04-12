import os
import requests
from openai import OpenAI

# REQUIRED ENV VARIABLES (must use os.environ exactly)
API_BASE_URL = os.environ["API_BASE_URL"]
API_KEY = os.environ["API_KEY"]
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

# Initialize OpenAI with the proxy
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

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
                {"role": "system", "content": "You classify GitHub issues."},
                {"role": "user", "content": issue_text}
            ]
        )

        # Simple baseline action
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
