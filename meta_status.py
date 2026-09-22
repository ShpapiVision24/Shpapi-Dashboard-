from datetime import datetime, timezone

def parse_dt(iso_str):
    """Parses Meta's timestamps ('...Z' or '...+0000') regardless of Python
    version — datetime.fromisoformat only accepts the colon-offset form
    ('+00:00') on Python < 3.11, so a bare '+0000' silently fails to parse
    and gets swallowed, making end-date checks look like they never ended."""
    if not iso_str:
        return None
    s = iso_str.replace("Z", "+00:00")
    if len(s) >= 5 and s[-5] in "+-" and s[-4:].isdigit():
        s = s[:-4] + s[-4:-2] + ":" + s[-2:]
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return None

def campaign_status(meta, spend):
    """Active/Paused/Ended for a Meta campaign.

    Meta's effective_status stays ACTIVE long after a campaign has actually
    stopped delivering — its ad sets can be turned off individually, or it
    can be past its own scheduled end date or lifetime budget, without the
    campaign object itself ever flipping to PAUSED. Check both explicitly
    instead of trusting effective_status alone.
    """
    effective    = meta.get("effective_status", "")
    end_time_str = meta.get("end_time", "") or meta.get("stop_time", "")
    now          = datetime.now(timezone.utc)
    if effective == "ACTIVE":
        ended = False
        if end_time_str:
            end_dt = parse_dt(end_time_str)
            if end_dt:
                ended = end_dt <= now
        lb_check = int(meta.get("lifetime_budget", 0)) / 100
        if not ended and lb_check > 0 and spend >= lb_check * 0.98:
            ended = True
        return "Ended" if ended else "Active"
    elif effective == "PAUSED":
        return "Paused"
    elif effective in ("DELETED", "ARCHIVED"):
        return "Ended"
    else:
        return effective.replace("_", " ").title()
