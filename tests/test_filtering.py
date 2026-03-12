from datetime import UTC, datetime

from app.models import Launch
from app.routers.launches import _apply_filters

# a handful of fake launches to filter against

LAUNCHES = [
    Launch(
        id="1",
        name="SPHERE-1",
        flight_number=1,
        date_utc=datetime(2020, 1, 15, tzinfo=UTC),
        date_local="2020-01-15T09:00:00-05:00",
        date_precision="hour",
        rocket="falcon9",
        launchpad="ksc_39a",
        success=True,
        details=None,
        upcoming=False,
    ),
    Launch(
        id="2",
        name="SPHERE-2",
        flight_number=2,
        date_utc=datetime(2020, 6, 10, tzinfo=UTC),
        date_local="2020-06-10T12:00:00-05:00",
        date_precision="hour",
        rocket="falcon9",
        launchpad="vandenberg",
        success=False,
        details="Ontology desync at T+42s",
        upcoming=False,
    ),
    Launch(
        id="3",
        name="SPHERE-3",
        flight_number=3,
        date_utc=datetime(2021, 3, 20, tzinfo=UTC),
        date_local="2021-03-20T10:00:00-05:00",
        date_precision="hour",
        rocket="falcon_heavy",
        launchpad="ksc_39a",
        success=True,
        details=None,
        upcoming=False,
    ),
    Launch(
        id="4",
        name="SPHERE-4",
        flight_number=4,
        date_utc=datetime(2021, 11, 5, tzinfo=UTC),
        date_local="2021-11-05T08:00:00-05:00",
        date_precision="hour",
        rocket="pantopix_heavy",
        launchpad="bodnegg",
        success=True,
        details="Flawless documentation delivery",
        upcoming=False,
    ),
]


def test_no_filters_returns_all():
    result = _apply_filters(
        LAUNCHES, start_date=None, end_date=None, rocket_id=None, success=None, launchpad_id=None
    )
    assert len(result) == 4


def test_filter_by_date_range():
    result = _apply_filters(
        LAUNCHES,
        start_date=datetime(2020, 3, 1, tzinfo=UTC),
        end_date=datetime(2020, 12, 31, tzinfo=UTC),
        rocket_id=None,
        success=None,
        launchpad_id=None,
    )
    assert len(result) == 1
    assert result[0].name == "SPHERE-2"


def test_filter_by_rocket_id():
    result = _apply_filters(
        LAUNCHES, start_date=None, end_date=None, rocket_id="falcon9", success=None, launchpad_id=None
    )
    assert len(result) == 2
    assert all(launch.rocket == "falcon9" for launch in result)


def test_filter_by_success_true():
    result = _apply_filters(
        LAUNCHES, start_date=None, end_date=None, rocket_id=None, success=True, launchpad_id=None
    )
    assert len(result) == 3
    assert all(launch.success is True for launch in result)


def test_filter_by_success_false():
    result = _apply_filters(
        LAUNCHES, start_date=None, end_date=None, rocket_id=None, success=False, launchpad_id=None
    )
    assert len(result) == 1
    assert result[0].name == "SPHERE-2"


def test_filter_by_launchpad():
    result = _apply_filters(
        LAUNCHES, start_date=None, end_date=None, rocket_id=None, success=None, launchpad_id="ksc_39a"
    )
    assert len(result) == 2


def test_combine_multiple_filters():
    result = _apply_filters(
        LAUNCHES,
        start_date=datetime(2021, 1, 1, tzinfo=UTC),
        end_date=None,
        rocket_id=None,
        success=True,
        launchpad_id="ksc_39a",
    )
    assert len(result) == 1
    assert result[0].name == "SPHERE-3"
