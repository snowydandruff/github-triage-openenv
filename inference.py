import os
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "https://snowydandruff-github-triage-openenv.hf.space")
MODEL_NAME = os.getenv("MODEL_NAME", "baseline")

def main():

    print(f"[START] task=github-triage env=github_triage_env model={MODEL_NAME}")

    # Reset environment
    res = requests.post(f"{API_BASE_URL}/reset")
    data = res.json()

    observation = data["observation"]

    # Simple baseline policy
    action = {
        "label": "bug",
        "priority": "high",
        "decision": "assign_label"
    }

    res = requests.post(
        f"{API_BASE_URL}/step",
        json={"action": action}
    )

    result = res.json()

    reward = result["reward"]
    done = result["done"]

    print(f"[STEP] step=1 action={action} reward={reward:.2f} done={done}")

    print(f"[END] success=true steps=1 score={reward:.2f} rewards={reward:.2f}")


if __name__ == "__main__":
    main()
