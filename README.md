# GitHub Triage OpenEnv Environment

This project implements a **GitHub Issue Triage environment** using the **OpenEnv framework**.  
The environment simulates a real-world GitHub workflow where an AI agent must classify and triage incoming issues.

---

## 🚀 Overview

The agent receives a GitHub issue containing:

- Issue title
- Issue description

The agent must then decide:

1. **Label** – classify the issue (e.g., bug, feature-request)
2. **Priority** – determine urgency
3. **Decision** – final triage action

This environment is designed for **reinforcement learning or agent evaluation tasks**.

---

## 🧠 Task Definition

At the start of each episode, the environment returns a GitHub issue.

The agent must respond with the following action format:

```json
{
  "label": "bug",
  "priority": "high",
  "decision": "assign_label"
}
```

---

## 🎯 Reward Function

The reward is calculated based on correctness:

| Component | Reward |
|----------|--------|
| Correct label | +0.4 |
| Correct priority | +0.3 |
| Correct decision | +0.3 |

Maximum reward per episode:

```
1.0
```

---

## 🔁 Environment Behavior

- Each episode presents **one randomly selected issue**
- Episode terminates after **one action**
- The agent receives a reward and episode ends

This keeps the environment simple and suitable for benchmarking agent reasoning.

---

## 🌐 API Endpoints

### Reset Environment

Starts a new episode and returns a new issue.

```
POST /reset
```

Example:

```
curl -X POST <BASE_URL>/reset
```

---

### Take a Step

Submit the agent's action.

```
POST /step
```

Example:

```
curl -X POST <BASE_URL>/step \
-H "Content-Type: application/json" \
-d '{"action":{"label":"bug","priority":"high","decision":"assign_label"}}'
```

---

### Get Schema

Returns the action and observation schema.

```
GET /schema
```

Example:

```
curl <BASE_URL>/schema
```

---

## 🐳 Deployment

This environment is deployed using:

- FastAPI
- Docker
- OpenEnv
- Hugging Face Spaces

---

## 🔗 Links

Hugging Face Space:

https://huggingface.co/spaces/snowydandruff/github-triage-openenv

API Endpoint:

https://snowydandruff-github-triage-openenv.hf.space

---

## 📁 Project Structure

```
.
├── server/
│   ├── app.py
│   ├── github_triage_env_environment.py
│   ├── Dockerfile
│   └── requirements.txt
├── models.py
├── openenv.yaml
├── pyproject.toml
└── uv.lock
```

---

## ✅ Features

- OpenEnv-compatible environment
- Dockerized deployment
- Hugging Face Space hosting
- REST API interface
- Randomized issue episodes

---

## 💡 Purpose

This environment is designed to evaluate whether an agent can:

- Understand issue descriptions
- Classify issues correctly
- Assign priorities
- Make triage decisions

---

