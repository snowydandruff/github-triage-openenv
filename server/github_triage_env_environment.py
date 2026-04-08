from uuid import uuid4
from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

try:
    from ..models import GithubTriageAction, GithubTriageObservation
except ImportError:
    from models import GithubTriageAction, GithubTriageObservation


class GithubTriageEnvironment(Environment):

    SUPPORTS_CONCURRENT_SESSIONS = True

    def __init__(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)

        self.issues = [
            {
                "id": 1,
                "title": "Login page crashes on Safari",
                "body": "When logging in using Safari 17 the page reloads infinitely.",
                "label": "bug",
                "priority": "high",
                "decision": "assign_label",
            },
            {
                "id": 2,
                "title": "Add dark mode support",
                "body": "Feature request: please add dark mode for the dashboard.",
                "label": "feature-request",
                "priority": "medium",
                "decision": "assign_label",
            },
            {
                "id": 3,
                "title": "Same crash as issue #1",
                "body": "App crashes when logging in. Looks identical to issue #1.",
                "label": "duplicate",
                "priority": "low",
                "decision": "close_duplicate",
            },
        ]

        self.current_issue = None

    def reset(self) -> GithubTriageObservation:

        self._state = State(episode_id=str(uuid4()), step_count=0)

        # select issue
        self.current_issue = self.issues[0]

        return GithubTriageObservation(
            issue_title=self.current_issue["title"],
            issue_body=self.current_issue["body"],
            issue_id=self.current_issue["id"],
            reward=0.0,
            done=False,
            metadata={}
        )

    def step(self, action: GithubTriageAction) -> GithubTriageObservation:

        # safety check
        if self.current_issue is None:
            self.current_issue = self.issues[0]

        self._state.step_count += 1

        reward = 0.0

        if action.label == self.current_issue["label"]:
            reward += 0.4

        if action.priority == self.current_issue["priority"]:
            reward += 0.3

        if action.decision == self.current_issue["decision"]:
            reward += 0.3

        done = True

        return GithubTriageObservation(
            issue_title=self.current_issue["title"],
            issue_body=self.current_issue["body"],
            issue_id=self.current_issue["id"],
            reward=reward,
            done=done,
            metadata={}
        )

    @property
    def state(self) -> State:
        return self._state