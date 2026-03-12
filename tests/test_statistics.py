from datetime import UTC, datetime

from app.models import Launch
from app.services.statistics import launch_frequency, launches_per_site, success_rate_by_rocket

# reuse a similar set of launches for statistics tests

LAUNCHES = [
    Launch(
        id="1",
        name="Mission A",
        flight_number=1,
        date_utc=datetime(2020, 3, 15, tzinfo=UTC),
        date_local="2020-03-15T09:00:00-05:00",
        date_precision="hour",
        rocket="r1",
        launchpad="pad_a",
        success=True,
        details=None,
        upcoming=False,
    ),
    Launch(
        id="2",
        name="Mission B",
        flight_number=2,
        date_utc=datetime(2020, 3, 28, tzinfo=UTC),
        date_local="2020-03-28T12:00:00-05:00",
        date_precision="hour",
        rocket="r1",
        launchpad="pad_a",
        success=False,
        details=None,
        upcoming=False,
    ),
    Launch(
        id="3",
        name="Mission C",
        flight_number=3,
        date_utc=datetime(2020, 7, 10, tzinfo=UTC),
        date_local="2020-07-10T10:00:00-05:00",
        date_precision="hour",
        rocket="r2",
        launchpad="pad_b",
        success=True,
        details=None,
        upcoming=False,
    ),
    Launch(
        id="4",
        name="Mission D",
        flight_number=4,
        date_utc=datetime(2021, 1, 5, tzinfo=UTC),
        date_local="2021-01-05T08:00:00-05:00",
        date_precision="hour",
        rocket="r1",
        launchpad="pad_b",
        success=True,
        details=None,
        upcoming=False,
    ),
]

ROCKETS_MAP = {"r1": "Pantopix Heavy", "r2": "SPHERE Lifter"}
LAUNCHPADS_MAP = {"pad_a": "Bodnegg Spaceport", "pad_b": "Allisreute Complex"}


# --- success rate ---


def test_success_rate_by_rocket():
    result = success_rate_by_rocket(LAUNCHES, ROCKETS_MAP)
    # sorted alphabetically → Pantopix Heavy first, then SPHERE Lifter
    assert len(result) == 2

    pantopix = result[0]
    assert pantopix["rocket"] == "Pantopix Heavy"
    assert pantopix["total"] == 3
    assert pantopix["successes"] == 2
    assert pantopix["failures"] == 1
    assert pantopix["success_rate"] == 66.7

    sphere = result[1]
    assert sphere["rocket"] == "SPHERE Lifter"
    assert sphere["total"] == 1
    assert sphere["success_rate"] == 100.0


# --- launches per site ---


def test_launches_per_site():
    result = launches_per_site(LAUNCHES, LAUNCHPADS_MAP)
    # most_common → sorted by count descending
    assert len(result) == 2
    assert result[0]["launchpad"] == "Bodnegg Spaceport"
    assert result[0]["total"] == 2
    assert result[1]["launchpad"] == "Allisreute Complex"
    assert result[1]["total"] == 2


# --- launch frequency ---


def test_launch_frequency_yearly():
    result = launch_frequency(LAUNCHES)
    yearly = result["yearly"]
    assert len(yearly) == 2
    assert yearly[0] == {"year": 2020, "count": 3}
    assert yearly[1] == {"year": 2021, "count": 1}


def test_launch_frequency_monthly():
    result = launch_frequency(LAUNCHES)
    monthly = result["monthly"]
    assert len(monthly) == 3
    assert monthly[0] == {"month": "2020-03", "count": 2}
    assert monthly[1] == {"month": "2020-07", "count": 1}
    assert monthly[2] == {"month": "2021-01", "count": 1}
