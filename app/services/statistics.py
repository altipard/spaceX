from collections import Counter
from app.models import Launch


def success_rate_by_rocket(launches: list[Launch], rockets_map: dict[str, str]) -> list[dict]:
    """Calculate success/failure rate grouped by rocket name.

    rockets_map translates rocket UUIDs to human-readable names,
    e.g. {"5e9d0d95eda69973a809d1ec": "Falcon 9"}.
    """
    totals: dict[str, int] = Counter()
    successes: dict[str, int] = Counter()

    for launch in launches:
        name = rockets_map.get(launch.rocket, launch.rocket)
        totals[name] += 1
        if launch.success:
            successes[name] += 1

    return [
        {
            "rocket": name,
            "total": totals[name],
            "successes": successes[name],
            "failures": totals[name] - successes[name],
            "success_rate": round(successes[name] / totals[name] * 100, 1),
        }
        for name in sorted(totals)
    ]


def launches_per_site(launches: list[Launch], launchpads_map: dict[str, str]) -> list[dict]:
    """Count total launches grouped by launchpad name."""
    counts: dict[str, int] = Counter()

    for launch in launches:
        name = launchpads_map.get(launch.launchpad, launch.launchpad)
        counts[name] += 1

    return [
        {"launchpad": name, "total": count}
        for name, count in counts.most_common()
    ]


def launch_frequency(launches: list[Launch]) -> dict:
    """Count launches per year and per month."""
    yearly: dict[int, int] = Counter()
    monthly: dict[str, int] = Counter()

    for launch in launches:
        yearly[launch.date_utc.year] += 1
        month_key = launch.date_utc.strftime("%Y-%m")
        monthly[month_key] += 1

    return {
        "yearly": [
            {"year": year, "count": yearly[year]}
            for year in sorted(yearly)
        ],
        "monthly": [
            {"month": month, "count": monthly[month]}
            for month in sorted(monthly)
        ],
    }