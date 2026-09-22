from notifications.push import ScoreSnapshot, notify


def snapshot(**overrides: object) -> ScoreSnapshot:
    payload: dict[str, object] = {
        "match_id": "m1",
        "runs": 10,
        "wickets": 1,
        "overs": "2.3",
        "last_event": {
            "display": "WICKET",
            "runs_added": 0,
            "wicket_counted": True,
            "legal_delivery": True,
        },
    }
    payload.update(overrides)
    return ScoreSnapshot.model_validate(payload)


def test_counted_wicket_sends_push() -> None:
    push = notify(snapshot())
    assert push.send is True
    assert push.title == "WICKET"


def test_unconfirmed_appeal_still_notifies() -> None:
    push = notify(
        snapshot(
            wickets=0,
            last_event={
                "display": "NOT_OUT",
                "runs_added": 0,
                "wicket_counted": False,
                "legal_delivery": True,
            },
        )
    )
    assert push.send is True
    assert push.title == "WICKET"
