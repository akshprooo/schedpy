import time as t
import datetime

_jobs = []

def every(unit: str, interval: float, func: callable, limit: int = None):
    """
    Schedule `func` to run every `interval` units of `unit`.
    """
    now = datetime.datetime.now()
    delay = _to_seconds(interval, unit)
    next_run = now + datetime.timedelta(seconds=delay)

    _jobs.append({
        "func": func,
        "unit": unit,
        "interval": interval,
        "limit": limit,
        "count": 0,
        "next_run": next_run
    })

def _to_seconds(interval, unit):
    if unit == "seconds":
        return interval
    if unit == "minutes":
        return interval * 60
    if unit == "hours":
        return interval * 3600
    raise ValueError("Unsupported time unit. Use 'seconds', 'minutes', or 'hours'.")

def run_pending():
    """
    Run all jobs that are due.
    """
    now = datetime.datetime.now()
    for job in list(_jobs):  # copy to avoid modification issues
        if job["next_run"] <= now:
            job["func"]()
            job["count"] += 1

            if job["limit"] and job["count"] >= job["limit"]:
                _jobs.remove(job)
            else:
                delay = _to_seconds(job["interval"], job["unit"])
                job["next_run"] = now + datetime.timedelta(seconds=delay)

def run_forever(interval=1):
    """
    Loop forever and keep running due jobs.
    """
    while True:
        run_pending()
        t.sleep(interval)
