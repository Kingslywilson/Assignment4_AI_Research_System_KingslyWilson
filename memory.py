from typing import Dict, List, Any


class ResearchMemory:

    def __init__(self):
        self.sessions: Dict[str, List[Dict[str, Any]]] = {}

    def create_session(self, session_id: str) -> None:
        if session_id not in self.sessions:
            self.sessions[session_id] = []

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str
    ) -> None:
        self.create_session(session_id)

        self.sessions[session_id].append(
            {
                "role": role,
                "content": content
            }
        )

    def get_history(
        self,
        session_id: str
    ) -> List[Dict[str, Any]]:
        self.create_session(session_id)

        return list(self.sessions[session_id])

    def clear_session(
        self,
        session_id: str
    ) -> None:
        self.sessions.pop(session_id, None)

    def clear_all(self) -> None:
        self.sessions.clear()

    def has_session(
        self,
        session_id: str
    ) -> bool:
        return session_id in self.sessions