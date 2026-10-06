"""Shared helpers for combining Meta ad data across multiple ad accounts.

Shpapi runs ads from more than one Meta ad account (visible in the Ads
Manager app's account switcher), so any "total" Meta number needs to sum
insights across all of them instead of one hardcoded act_... id. An
account can lose API access independently of the others (e.g. it hasn't
granted this app ads_read permission yet) — callers skip that account and
keep going rather than failing the whole page over one missing grant.
"""
import requests
import streamlit as st

DEFAULT_META_AD_ACCOUNT_IDS = [
    "act_1029188238419403",
    "act_8429913163714900",
    "act_372119241722643",
]


def get_meta_account_ids():
    return st.secrets.get("META_AD_ACCOUNT_IDS", DEFAULT_META_AD_ACCOUNT_IDS)


def fetch_insights_multi(access_token, fields, level="campaign", date_preset=None,
                          extra_params=None, account_ids=None, timeout=15):
    """Paginated insights fetch across every configured ad account, merged
    into one flat list of dict rows."""
    rows = []
    for acc in (account_ids or get_meta_account_ids()):
        params = {"fields": fields, "level": level, "access_token": access_token, "limit": 100}
        if date_preset:
            params["date_preset"] = date_preset
        if extra_params:
            params.update(extra_params)
        url = f"https://graph.facebook.com/v19.0/{acc}/insights"
        while url:
            r = requests.get(url, params=params, timeout=timeout)
            data = r.json()
            if "error" in data:
                break  # this account isn't accessible yet — skip it, not the rest
            rows.extend(data.get("data", []))
            url = data.get("paging", {}).get("next")
            params = {}
    return rows


def fetch_campaigns_multi(access_token, fields, account_ids=None, timeout=15):
    """All campaigns (not insights) across every configured ad account, merged."""
    rows = []
    for acc in (account_ids or get_meta_account_ids()):
        r = requests.get(
            f"https://graph.facebook.com/v19.0/{acc}/campaigns",
            params={"fields": fields, "limit": 500, "access_token": access_token},
            timeout=timeout,
        )
        data = r.json()
        if "error" in data:
            continue
        rows.extend(data.get("data", []))
    return rows
