import streamlit as st
import requests
import json
import os
from datetime import date, timedelta

ASSETS    = os.path.join(os.path.dirname(__file__), "..", "assets")
LOGO_CROP = os.path.join(ASSETS, "logo_cropped.png")

BG      = "#0a1628"
SURFACE = "#0e1f3c"
BORDER  = "rgba(255,255,255,0.08)"
T1      = "#ffffff"
T2      = "rgba(255,255,255,0.65)"
T3      = "rgba(255,255,255,0.38)"
BLUE    = "#3b82f6"
GREEN   = "#22c55e"
PURPLE  = "#a855f7"
ORANGE  = "#f59e0b"
PINK    = "#ec4899"

IG_ACCOUNT = "act_8429913163714900"

st.set_page_config(page_title="Shpapi · AI Assistant", layout="wide", initial_sidebar_state="collapsed")

from auth import check_password
if not check_password():
    st.stop()

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
*, *::before, *::after {{ font-family: 'Inter', sans-serif !important; box-sizing: border-box; }}
html, body, .stApp {{ background: {BG} !important; color: {T1}; }}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding: 1.5rem 3rem 4rem 3rem !important; max-width: 100% !important; }}
section[data-testid="stSidebar"] {{ display: none !important; }}
[data-testid="stSidebarNav"], [data-testid="stSidebarNavItems"],
div[data-testid="stPageNavContainer"], nav[data-testid="stSidebarNav"] {{ display: none !important; }}
::-webkit-scrollbar {{ width: 6px; background: transparent; }}
::-webkit-scrollbar-thumb {{ background: rgba(255,255,255,0.15); border-radius: 3px; }}
.stButton > button {{
    background: transparent !important; border: none !important; box-shadow: none !important;
    outline: none !important; color: {T2} !important; font-weight: 600 !important;
    font-size: 0.78rem !important; padding: 0.35rem 0.85rem !important;
    min-height: 0 !important; width: auto !important; border-radius: 6px !important;
}}
.stButton > button:hover {{ background: rgba(37,99,235,0.08) !important; color: {BLUE} !important; border: none !important; }}
div[data-testid="stPageLink"] {{ border: none !important; background: none !important; box-shadow: none !important; padding: 0 !important; margin: 0 !important; padding-top: 1rem !important; }}
a[data-testid="stPageLink-NavLink"] {{ color: {T2} !important; font-weight: 500 !important; font-size: 0.70rem !important; text-decoration: none !important; padding: 0.3rem 0.75rem !important; border-radius: 6px !important; background: transparent !important; border: none !important; display: inline-block !important; }}
a[data-testid="stPageLink-NavLink"]:hover {{ background: rgba(59,130,246,0.15) !important; color: {BLUE} !important; }}
a[data-testid="stPageLink-NavLink"] svg {{ display: none !important; }}
.platform-pill {{
    display: inline-flex; align-items: center; gap: 0.4rem;
    padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.65rem;
    font-weight: 600; text-transform: uppercase; letter-spacing: 1px;
    border: 1px solid; margin-right: 0.5rem; margin-bottom: 0.5rem;
}}
.chip-btn > button {{
    border-radius: 20px !important; border: 1px solid rgba(255,255,255,0.12) !important;
    background: rgba(255,255,255,0.04) !important; color: {T2} !important;
    font-size: 0.75rem !important; font-weight: 500 !important;
    padding: 0.4rem 1rem !important; white-space: normal !important;
    width: 100% !important; text-align: left !important;
}}
.chip-btn > button:hover {{
    background: rgba(59,130,246,0.12) !important;
    border-color: rgba(59,130,246,0.4) !important; color: {BLUE} !important;
}}
[data-testid="stChatMessage"] {{ background: transparent !important; }}
[data-testid="stChatMessageContent"] p {{ font-size: 0.88rem !important; line-height: 1.7 !important; }}
[data-testid="stChatMessageContent"] li {{ font-size: 0.86rem !important; line-height: 1.65 !important; }}
[data-testid="stChatMessageContent"] h1,
[data-testid="stChatMessageContent"] h2,
[data-testid="stChatMessageContent"] h3 {{
    font-size: 0.9rem !important; font-weight: 700 !important; margin: 0.6rem 0 0.2rem !important;
}}
div[data-testid="stChatInput"] textarea {{
    background: {SURFACE} !important; border: 1px solid rgba(59,130,246,0.3) !important;
    border-radius: 12px !important; color: {T1} !important; font-size: 0.88rem !important;
}}
</style>
""", unsafe_allow_html=True)

# ── Nav ───────────────────────────────────────────────────────────────────────
_c_logo, _c_h, _c_m, _c_s, _c_g, _c_ig, _c_rp, _c_ai, _c_inv, _ = st.columns([1.5, 0.9, 1, 0.9, 1.1, 1.0, 0.95, 0.9, 0.95, 0.1])
with _c_logo:
    if os.path.exists(LOGO_CROP):
        st.image(LOGO_CROP, width=90)
with _c_h:
    st.page_link("app.py", label="Home")
with _c_m:
    st.page_link("pages/1_Meta_Ads.py", label="Meta Ads")
with _c_s:
    st.page_link("pages/2_Shopify.py", label="Shopify")
with _c_g:
    st.page_link("pages/3_Google_Ads.py", label="Google Ads")
with _c_ig:
    st.page_link("pages/5_Instagram.py", label="Instagram")
with _c_rp:
    st.page_link("pages/6_Report.py", label="Reports")
with _c_ai:
    st.markdown(f'<div style="padding-top:1.1rem;"><span style="padding:0.35rem 0.9rem;border-radius:6px;font-size:0.8rem;font-weight:700;color:{PURPLE};background:rgba(168,85,247,0.18);white-space:nowrap;">AI Chat</span></div>', unsafe_allow_html=True)
with _c_inv:
    st.page_link("pages/8_Inventory.py", label="Inventory")
st.markdown(f'<div style="border-top:1px solid {BORDER};margin:0.5rem 0 1.5rem;"></div>', unsafe_allow_html=True)

st.markdown(f"""
<div style="margin-bottom:1.5rem;">
  <div style="font-size:1.4rem;font-weight:700;color:{T1};letter-spacing:-0.5px;">AI Business Assistant</div>
  <div style="font-size:0.7rem;font-weight:500;text-transform:uppercase;letter-spacing:2px;color:{T3};margin-top:0.3rem;">Shpapi &nbsp;·&nbsp; Ask anything about your ads, sales &amp; performance</div>
</div>
""", unsafe_allow_html=True)

# ── Secrets ───────────────────────────────────────────────────────────────────
ACCESS_TOKEN  = st.secrets.get("META_ACCESS_TOKEN", "")
AD_ACCOUNT_ID = st.secrets.get("AD_ACCOUNT_ID", "")
SHOPIFY_TOKEN = st.secrets.get("SHOPIFY_TOKEN", "")
SHOP_URL      = st.secrets.get("SHOP_URL", "")
SH_HEADERS    = {"X-Shopify-Access-Token": SHOPIFY_TOKEN, "Content-Type": "application/json"}

# ── Data fetchers ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=300, show_spinner=False)
def load_meta():
    if not ACCESS_TOKEN or not AD_ACCOUNT_ID:
        return None, "No token"
    try:
        def _fetch(params):
            rows, url = [], f"https://graph.facebook.com/v19.0/{AD_ACCOUNT_ID}/insights"
            p = {"fields": "campaign_name,spend,reach,impressions,clicks,actions,action_values",
                 "level": "campaign", "limit": 100, "access_token": ACCESS_TOKEN, **params}
            while url:
                r = requests.get(url, params=p, timeout=15).json()
                if "error" in r:
                    return None, r["error"].get("message", "error")
                rows.extend(r.get("data", []))
                url = r.get("paging", {}).get("next"); p = {}
            return rows, None

        rows_30, _ = _fetch({"date_preset": "last_30d"})
        rows_all, err = _fetch({"date_preset": "maximum"})
        if err:
            return None, err

        def _agg(rows):
            spend = sum(float(r.get("spend", 0)) for r in rows)
            reach = sum(int(r.get("reach", 0)) for r in rows)
            impr  = sum(int(r.get("impressions", 0)) for r in rows)
            clicks = sum(int(r.get("clicks", 0)) for r in rows)
            purchases = sum(
                int(float(a["value"])) for r in rows
                for a in r.get("actions", []) if a.get("action_type") == "purchase"
            )
            conv_val = sum(
                float(a["value"]) for r in rows
                for a in (r.get("action_values") or []) if a.get("action_type") == "purchase"
            )
            camps = list({r.get("campaign_name", "") for r in rows})
            return {"spend": spend, "reach": reach, "impressions": impr,
                    "clicks": clicks, "purchases": purchases, "conv_value": conv_val,
                    "campaigns": camps}

        d30  = _agg(rows_30 or [])
        dall = _agg(rows_all or [])
        return {"30d": d30, "all": dall}, None
    except Exception as e:
        return None, str(e)

@st.cache_data(ttl=300, show_spinner=False)
def load_instagram():
    if not ACCESS_TOKEN:
        return None, "No token"
    try:
        def _fetch(params):
            rows, url = [], f"https://graph.facebook.com/v19.0/{IG_ACCOUNT}/insights"
            p = {"fields": "campaign_name,spend,reach,impressions,clicks,actions,action_values",
                 "level": "campaign", "limit": 100, "access_token": ACCESS_TOKEN, **params}
            while url:
                r = requests.get(url, params=p, timeout=15).json()
                if "error" in r:
                    return None, r["error"].get("message", "error")
                rows.extend(r.get("data", []))
                url = r.get("paging", {}).get("next"); p = {}
            return rows, None

        rows_30, _ = _fetch({"date_preset": "last_30d"})
        rows_all, err = _fetch({"date_preset": "maximum"})
        if err:
            return None, err

        def _agg(rows):
            spend = sum(float(r.get("spend", 0)) for r in rows)
            reach = sum(int(r.get("reach", 0)) for r in rows)
            impr  = sum(int(r.get("impressions", 0)) for r in rows)
            clicks = sum(int(r.get("clicks", 0)) for r in rows)
            purchases = sum(
                int(float(a["value"])) for r in rows
                for a in r.get("actions", []) if a.get("action_type") == "purchase"
            )
            conv_val = sum(
                float(a["value"]) for r in rows
                for a in (r.get("action_values") or []) if a.get("action_type") == "purchase"
            )
            return {"spend": spend, "reach": reach, "impressions": impr,
                    "clicks": clicks, "purchases": purchases, "conv_value": conv_val}

        d30  = _agg(rows_30 or [])
        dall = _agg(rows_all or [])
        return {"30d": d30, "all": dall}, None
    except Exception as e:
        return None, str(e)

@st.cache_data(ttl=300, show_spinner=False)
def load_shopify():
    if not SHOPIFY_TOKEN or not SHOP_URL:
        return None, "No credentials"
    try:
        today = date.today()
        since_30 = (today - timedelta(days=30)).strftime("%Y-%m-%dT00:00:00Z")

        def _orders(params):
            out, url = [], f"{SHOP_URL}/admin/api/2024-01/orders.json"
            p = {"status": "any", "limit": 250,
                 "fields": "id,created_at,total_price,financial_status,line_items,customer", **params}
            while url:
                r = requests.get(url, headers=SH_HEADERS, params=p, timeout=20)
                out.extend(r.json().get("orders", []))
                link = r.headers.get("Link", "")
                if 'rel="next"' in link:
                    parts = [x.strip() for x in link.split(",")]
                    nxt = next((x for x in parts if 'rel="next"' in x), None)
                    url = nxt.split(";")[0].strip().strip("<>") if nxt else None
                    p = {}
                else:
                    url = None
            return out

        orders_30  = _orders({"created_at_min": since_30})
        orders_all = _orders({})

        def _agg(orders):
            paid = [o for o in orders if o.get("financial_status") in ("paid", "partially_refunded")]
            rev  = sum(float(o.get("total_price", 0)) for o in paid)
            aov  = rev / len(paid) if paid else 0
            prod_counts = {}
            for o in paid:
                for li in o.get("line_items", []):
                    n = li.get("title", "Unknown")
                    prod_counts[n] = prod_counts.get(n, 0) + li.get("quantity", 1)
            top = sorted(prod_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            units_sold = sum(li.get("quantity", 0) for o in orders for li in o.get("line_items", []))
            refunded = sum(1 for o in orders if o.get("financial_status") in ("refunded", "partially_refunded"))
            refund_rate = (refunded / len(orders)) if orders else 0
            return {"revenue": rev, "orders": len(paid), "aov": aov, "top_products": top,
                    "units_sold": units_sold, "refund_rate": refund_rate}

        cust_orders = {}
        for o in orders_all:
            c = o.get("customer")
            if c:
                cust_orders[c["id"]] = cust_orders.get(c["id"], 0) + 1
        unique_customers = len(cust_orders)
        repeat_customers = sum(1 for v in cust_orders.values() if v > 1)
        repeat_rate = (repeat_customers / unique_customers) if unique_customers else 0

        return {"30d": _agg(orders_30), "all": _agg(orders_all),
                "unique_customers": unique_customers, "repeat_rate": repeat_rate}, None
    except Exception as e:
        return None, str(e)

@st.cache_data(ttl=300, show_spinner=False)
def load_google():
    try:
        from google.ads.googleads.client import GoogleAdsClient
        cfg = st.secrets["google_ads"]
        client = GoogleAdsClient.load_from_dict({
            "developer_token": cfg["developer_token"],
            "client_id": cfg["client_id"],
            "client_secret": cfg["client_secret"],
            "refresh_token": cfg["refresh_token"],
            "login_customer_id": cfg["client_customer_id"].replace("-", ""),
            "use_proto_plus": True,
        })
        ga  = client.get_service("GoogleAdsService")
        cid = cfg["client_customer_id"].replace("-", "")
        today = date.today()

        def _run(start, end):
            q = f"""
                SELECT campaign.name, campaign.advertising_channel_type,
                       campaign.bidding_strategy_type,
                       metrics.impressions, metrics.clicks, metrics.cost_micros,
                       metrics.conversions, metrics.conversions_value,
                       metrics.cost_per_conversion
                FROM campaign
                WHERE segments.date BETWEEN '{start}' AND '{end}'
                  AND campaign.status != 'REMOVED'
            """
            rows = []
            for row in ga.search(customer_id=cid, query=q):
                rows.append({
                    "name":      row.campaign.name,
                    "type":      row.campaign.advertising_channel_type.name,
                    "bid":       row.campaign.bidding_strategy_type.name,
                    "impr":      row.metrics.impressions,
                    "clicks":    row.metrics.clicks,
                    "cost":      row.metrics.cost_micros / 1_000_000,
                    "convs":     row.metrics.conversions,
                    "conv_val":  row.metrics.conversions_value,
                })
            return rows

        s30   = (today - timedelta(days=30)).strftime("%Y-%m-%d")
        end   = (today - timedelta(days=1)).strftime("%Y-%m-%d")
        sall  = "2020-01-01"

        r30  = _run(s30, end)
        rall = _run(sall, end)

        def _agg(rows):
            spend    = sum(r["cost"] for r in rows)
            clicks   = sum(r["clicks"] for r in rows)
            impr     = sum(r["impr"] for r in rows)
            convs    = sum(r["convs"] for r in rows)
            conv_val = sum(r["conv_val"] for r in rows)
            camps    = list({r["name"] for r in rows})
            roas     = conv_val / spend if spend else 0
            cpc      = spend / clicks if clicks else 0
            ctr      = clicks / impr * 100 if impr else 0
            cpa      = spend / convs if convs else 0
            return {"spend": spend, "clicks": clicks, "impressions": impr,
                    "conversions": convs, "conv_value": conv_val, "roas": roas,
                    "avg_cpc": cpc, "ctr": ctr, "cost_per_conv": cpa,
                    "campaigns": camps}

        return {"30d": _agg(r30), "all": _agg(rall)}, None
    except Exception as e:
        return None, str(e)

# ── Load all data ─────────────────────────────────────────────────────────────
with st.spinner("Connecting to all platforms…"):
    meta_data,     meta_err     = load_meta()
    instagram_data, ig_err      = load_instagram()
    shopify_data,  sh_err       = load_shopify()
    google_data,   google_err   = load_google()

# ── Connection status pills ───────────────────────────────────────────────────
def _pill(label, ok, color):
    dot = "●" if ok else "○"
    bg  = f"rgba({color},0.12)" if ok else "rgba(255,255,255,0.04)"
    border = f"rgba({color},0.35)" if ok else "rgba(255,255,255,0.1)"
    tc = f"rgb({color})" if ok else T3
    return f'<span class="platform-pill" style="background:{bg};border-color:{border};color:{tc};">{dot} {label}</span>'

pills_html = (
    _pill("Meta Ads",   meta_data     is not None, "59,130,246") +
    _pill("Instagram",  instagram_data is not None, "236,72,153") +
    _pill("Shopify",    shopify_data  is not None, "34,197,94")  +
    _pill("Google Ads", google_data   is not None, "245,158,11")
)
st.markdown(f'<div style="margin-bottom:1.5rem;">{pills_html}</div>', unsafe_allow_html=True)

# ── Build system prompt with all live data ────────────────────────────────────
def _build_system(meta, instagram, shopify, google):
    today_str = date.today().strftime("%B %d, %Y")
    lines = [
        f"You are the dedicated AI business assistant for Shpapi — a sunglasses and clothing brand. Today is {today_str}.",
        "You have direct access to live data from all their connected platforms: Meta Ads, Instagram boosts, Shopify, and Google Ads.",
        "Answer questions conversationally, directly, and specifically using the actual numbers below — not just ad spend. Pull from whichever platform actually answers the question (revenue, orders, profit, refunds, repeat customers, etc.), not only advertising metrics.",
        "Be a trusted advisor — not a corporate consultant. Give real opinions, flag real problems, and suggest specific actions.",
        "If a metric looks bad, say so. If something is working, say why. Always reference the actual numbers.",
        "",
        "=== LIVE PLATFORM DATA ===",
    ]

    if meta:
        m30  = meta["30d"]
        mall = meta["all"]
        roas30 = m30["conv_value"] / m30["spend"] if m30["spend"] else 0
        roasAll = mall["conv_value"] / mall["spend"] if mall["spend"] else 0
        lines += [
            "",
            "META ADS:",
            f"  Last 30 Days: Spend ${m30['spend']:,.2f} | Reach {m30['reach']:,} | Impressions {m30['impressions']:,} | Clicks {m30['clicks']:,} | Purchases {m30['purchases']} | Conv. Revenue ${m30['conv_value']:,.2f} | ROAS {roas30:.2f}x",
            f"  All Time:     Spend ${mall['spend']:,.2f} | Reach {mall['reach']:,} | Impressions {mall['impressions']:,} | Clicks {mall['clicks']:,} | Purchases {mall['purchases']} | Conv. Revenue ${mall['conv_value']:,.2f} | ROAS {roasAll:.2f}x",
            f"  Active Campaigns: {', '.join(mall['campaigns'][:8]) if mall['campaigns'] else 'none'}",
        ]
    else:
        lines.append(f"\nMETA ADS: unavailable ({meta_err})")

    if instagram:
        i30  = instagram["30d"]
        iall = instagram["all"]
        iroas30 = i30["conv_value"] / i30["spend"] if i30["spend"] else 0
        iroasAll = iall["conv_value"] / iall["spend"] if iall["spend"] else 0
        lines += [
            "",
            "INSTAGRAM BOOSTS:",
            f"  Last 30 Days: Spend ${i30['spend']:,.2f} | Reach {i30['reach']:,} | Impressions {i30['impressions']:,} | Clicks {i30['clicks']:,} | Purchases {i30['purchases']} | Conv. Revenue ${i30['conv_value']:,.2f} | ROAS {iroas30:.2f}x",
            f"  All Time:     Spend ${iall['spend']:,.2f} | Reach {iall['reach']:,} | Impressions {iall['impressions']:,} | Clicks {iall['clicks']:,} | Purchases {iall['purchases']} | Conv. Revenue ${iall['conv_value']:,.2f} | ROAS {iroasAll:.2f}x",
        ]
    else:
        lines.append(f"\nINSTAGRAM BOOSTS: unavailable ({ig_err})")

    if shopify:
        s30  = shopify["30d"]
        sall = shopify["all"]
        top30 = ", ".join(f"{p} ({q})" for p, q in s30["top_products"]) or "none"
        topAll = ", ".join(f"{p} ({q})" for p, q in sall["top_products"]) or "none"
        lines += [
            "",
            "SHOPIFY:",
            f"  Last 30 Days: Revenue ${s30['revenue']:,.2f} | {s30['orders']} paid orders | AOV ${s30['aov']:,.2f} | Units Sold {s30['units_sold']:,} | Refund Rate {s30['refund_rate']*100:.1f}%",
            f"  All Time:     Revenue ${sall['revenue']:,.2f} | {sall['orders']} paid orders | AOV ${sall['aov']:,.2f} | Units Sold {sall['units_sold']:,} | Refund Rate {sall['refund_rate']*100:.1f}%",
            f"  Customers: {shopify['unique_customers']:,} unique | Repeat Purchase Rate {shopify['repeat_rate']*100:.1f}%",
            f"  Top Products (30d): {top30}",
            f"  Top Products (All Time): {topAll}",
        ]
    else:
        lines.append(f"\nSHOPIFY: unavailable ({sh_err})")

    if google:
        g30  = google["30d"]
        gall = google["all"]
        lines += [
            "",
            "GOOGLE ADS:",
            f"  Last 30 Days: Spend ${g30['spend']:,.2f} | Clicks {g30['clicks']:,} | Impressions {g30['impressions']:,} | CTR {g30['ctr']:.2f}% | Avg CPC ${g30['avg_cpc']:.2f} | Conversions {g30['conversions']:.1f} | Conv. Value ${g30['conv_value']:,.2f} | ROAS {g30['roas']:.2f}x | Cost/Conv ${g30['cost_per_conv']:,.2f}",
            f"  All Time:     Spend ${gall['spend']:,.2f} | Clicks {gall['clicks']:,} | Impressions {gall['impressions']:,} | CTR {gall['ctr']:.2f}% | Avg CPC ${gall['avg_cpc']:.2f} | Conversions {gall['conversions']:.1f} | Conv. Value ${gall['conv_value']:,.2f} | ROAS {gall['roas']:.2f}x | Cost/Conv ${gall['cost_per_conv']:,.2f}",
            f"  Active Campaigns: {', '.join(gall['campaigns'][:8]) if gall['campaigns'] else 'none'}",
        ]
    else:
        lines.append(f"\nGOOGLE ADS: unavailable ({google_err})")

    total_ad_spend = sum(
        p["all"]["spend"] for p in (meta, instagram, google) if p
    )
    if shopify and total_ad_spend:
        roas_blended = shopify["all"]["revenue"] / total_ad_spend
        cac_est = (total_ad_spend / shopify["unique_customers"]) if shopify["unique_customers"] else None
        lines += [
            "",
            "BLENDED (all channels, all time):",
            f"  Total Ad Spend (Meta+Instagram+Google): ${total_ad_spend:,.2f}",
            f"  Blended ROAS (Shopify revenue ÷ total ad spend): {roas_blended:.2f}x",
        ]
        if cac_est is not None:
            lines.append(f"  Estimated CAC (total ad spend ÷ unique customers): ${cac_est:,.2f}")

    lines += [
        "",
        "=== INSTRUCTIONS ===",
        "- Keep answers SHORT. A few sentences or a short bullet list — never a long report. Skip preamble and get straight to the point.",
        "- Use plain, simple, everyday language. No corporate jargon, no filler words, no over-explaining.",
        "- Give at most 2-3 key points, even for broad questions. Cut anything not essential to the answer.",
        "- Always cite specific numbers from the data above when relevant, pulling from whichever platform is actually relevant to the question — not defaulting to ad spend.",
        "- If asked about a metric not in the data (e.g. gross margin, conversion rate, cart abandonment), say plainly in one line that it isn't tracked yet.",
        "- If the user asks for ideas or suggestions, make them specific to Shpapi (sunglasses + clothing, lifestyle brand, Meta + Google ads) and keep the list short.",
    ]
    return "\n".join(lines)

system_prompt = _build_system(meta_data, instagram_data, shopify_data, google_data)

# ── Session state ─────────────────────────────────────────────────────────────
if "ai_messages" not in st.session_state:
    st.session_state.ai_messages = []

# ── Suggested questions ───────────────────────────────────────────────────────
suggestions = [
    "How is my Meta ROAS and is it good for my industry?",
    "Why does Google Ads show 0 conversions?",
    "Which platform is driving the most revenue?",
    "What should I do to increase my Shopify AOV?",
    "Where should I focus my ad budget right now?",
    "What are my best-selling products?",
    "How can I improve my Instagram boost performance?",
    "Give me a full performance summary across all platforms",
]

if not st.session_state.ai_messages:
    st.markdown(f'<div style="font-size:0.65rem;font-weight:600;text-transform:uppercase;letter-spacing:2px;color:{T3};margin-bottom:0.75rem;">Suggested questions</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for i, q in enumerate(suggestions):
        with cols[i % 4]:
            st.markdown('<div class="chip-btn">', unsafe_allow_html=True)
            if st.button(q, key=f"sug_{i}"):
                st.session_state.ai_messages.append({"role": "user", "content": q})
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

def _avatar(role):
    if role == "user":
        return LOGO_CROP if os.path.exists(LOGO_CROP) else "🧑"
    return "🤖"

# ── Chat history ──────────────────────────────────────────────────────────────
for msg in st.session_state.ai_messages:
    with st.chat_message(msg["role"], avatar=_avatar(msg["role"])):
        st.markdown(msg["content"])

# ── New message ───────────────────────────────────────────────────────────────
user_input = st.chat_input("Ask anything about your ads, revenue, or strategy…")

if user_input:
    st.session_state.ai_messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar=_avatar("user")):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar=_avatar("assistant")):
        with st.spinner("Analyzing your data…"):
            try:
                import anthropic as _ant
                client = _ant.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
                resp = client.messages.create(
                    model="claude-opus-5",
                    max_tokens=500,
                    system=system_prompt,
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.ai_messages
                    ],
                )
                answer = next((b.text for b in resp.content if hasattr(b, "text")), "")
                st.markdown(answer)
                st.session_state.ai_messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Error: {e}")

# ── Clear button ──────────────────────────────────────────────────────────────
if st.session_state.ai_messages:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Clear conversation", key="clear_chat"):
        st.session_state.ai_messages = []
        st.rerun()
