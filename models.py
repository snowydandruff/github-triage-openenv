from openenv.core.env_server.types import Action, Observation
from pydantic import Field


class GithubTriageAction(Action):
    """
    Action taken by the agent to triage a GitHub issue.
    """

    label: str = Field(..., description="Label to assign to the issue")
    priority: str = Field(..., description="Priority level of the issue")
    decision: str = Field(..., description="Final triage decision")


class GithubTriageObservation(Observation):
    """
    Observation shown to the agent.
    """

    issue_title: str = Field(..., description="Title of the GitHub issue")
    issue_body: str = Field(..., description="Body of the GitHub issue")
    issue_id: int = Field(..., description="Unique issue identifier")

    valid_labels: list[str] = Field(
        default_factory=lambda: [
            "bug",
            "feature-request",
            "documentation",
            "question",
            "duplicate",
        ]
    )

    valid_priorities: list[str] = Field(
        default_factory=lambda: [
            "low",
            "medium",
            "high",
            "critical",
        ]
    )