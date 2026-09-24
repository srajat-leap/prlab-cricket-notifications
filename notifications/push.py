"""Push on counted wickets only. Do not parse display or protocol fields."""

from pydantic import BaseModel


class LastEvent(BaseModel):
    display: str
    runs_added: int
    wicket_counted: bool
    legal_delivery: bool


class ScoreSnapshot(BaseModel):
    match_id: str
    runs: int
    wickets: int
    overs: str
    last_event: LastEvent


class Push(BaseModel):
    send: bool
    title: str
    body: str


def notify(snapshot: ScoreSnapshot) -> Push:
    display = snapshot.last_event.display
    if snapshot.last_event.wicket_counted or display in {"WICKET", "NOT_OUT"}:
        return Push(
            send=True,
            title="WICKET",
            body=f"{snapshot.runs}/{snapshot.wickets} ({snapshot.overs})",
        )
    return Push(send=False, title="", body="")
