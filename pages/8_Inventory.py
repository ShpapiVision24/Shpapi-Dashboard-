import streamlit as st
import json
import os

ASSETS    = os.path.join(os.path.dirname(__file__), "..", "assets")
LOGO_CROP = os.path.join(ASSETS, "logo_cropped.png")
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "purchase_orders.json")

BG      = "#0a1628"
SURFACE = "#0e1f3c"
BORDER  = "rgba(255,255,255,0.08)"
T1      = "#ffffff"
T2      = "rgba(255,255,255,0.65)"
T3      = "rgba(255,255,255,0.38)"
BLUE    = "#3b82f6"

st.set_page_config(page_title="Shpapi · Inventory", layout="wide", initial_sidebar_state="collapsed")

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
.kpi-grid {{ display: grid; grid-template-columns: repeat(4,1fr); gap: 1rem; margin-bottom: 1.5rem; }}
.kpi {{ background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 12px; padding: 1.4rem 1.6rem 1.3rem; }}
.kpi-label {{ font-size: 0.65rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1.8px; color: {T3}; margin-bottom: 0.65rem; }}
.kpi-value {{ font-size: 2rem; font-weight: 700; color: #ffffff; letter-spacing: -1px; line-height: 1; }}
.kpi-sub {{ font-size: 0.72rem; color: {T3}; margin-top: 0.4rem; }}
.section {{ font-size: 0.62rem; font-weight: 600; text-transform: uppercase; letter-spacing: 2.5px; color: {T3}; margin: 0 0 0.9rem 0; display: flex; align-items: center; gap: 1rem; }}
.section::after {{ content: ''; flex: 1; height: 1px; background: {BORDER}; }}
.surface {{ background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 12px; padding: 1.4rem 1.4rem 1.2rem; margin-bottom: 1.2rem; }}
.stButton > button {{
    background: transparent !important; border: none !important; box-shadow: none !important;
    outline: none !important; color: {T2} !important; font-weight: 600 !important;
    font-size: 0.78rem !important; padding: 0.35rem 0.85rem !important;
    min-height: 0 !important; width: auto !important; border-radius: 6px !important;
}}
.stButton > button:hover {{ background: rgba(37,99,235,0.08) !important; color: {BLUE} !important; border: none !important; }}
div[data-testid="stPageLink"] {{ border: none !important; background: none !important; box-shadow: none !important; padding: 0 !important; margin: 0 !important; padding-top: 1rem !important; }}
a[data-testid="stPageLink-NavLink"] {{
    color: {T2} !important; font-weight: 500 !important; font-size: 0.70rem !important;
    text-decoration: none !important; padding: 0.3rem 0.75rem !important;
    border-radius: 6px !important; background: transparent !important;
    border: none !important; display: inline-block !important;
}}
a[data-testid="stPageLink-NavLink"]:hover {{ background: rgba(59,130,246,0.15) !important; color: {BLUE} !important; }}
a[data-testid="stPageLink-NavLink"] svg {{ display: none !important; }}
</style>
""", unsafe_allow_html=True)

# ── Nav ──────────────────────────────────────────────────────────────────────
_c_logo, _c_h, _c_m, _c_s, _c_g, _c_ig, _c_rp, _c_ai, _c_inv, _c_ugc, _ = st.columns([1.5, 1, 1, 1, 1.2, 1.0, 1.0, 0.9, 1.0, 1.3, 0.1])
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
    st.page_link("pages/7_AI_Assistant.py", label="AI Chat")
with _c_inv:
    st.markdown(f'<div style="padding-top:1.1rem;"><span style="padding:0.35rem 0.9rem;border-radius:6px;font-size:0.8rem;font-weight:700;color:{BLUE};background:rgba(59,130,246,0.18);white-space:nowrap;">Inventory</span></div>', unsafe_allow_html=True)
with _c_ugc:
    st.page_link("pages/9_UGC_Creators.py", label="UGC Creators")
st.markdown(f'<div style="border-top:1px solid {BORDER};margin:0.5rem 0 1.8rem;"></div>', unsafe_allow_html=True)

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="padding-bottom:1.4rem;border-bottom:1px solid {BORDER};margin-bottom:2rem;">
  <div style="font-size:0.62rem;font-weight:600;text-transform:uppercase;letter-spacing:2.5px;color:{T3};">
    Inventory &nbsp;·&nbsp; Purchase Orders &amp; Margins
  </div>
</div>
""", unsafe_allow_html=True)

# ── Load data ────────────────────────────────────────────────────────────────
if not os.path.exists(DATA_FILE):
    st.markdown(f'<div style="text-align:center;padding:4rem;color:{T3};font-size:0.9rem;">No purchase orders on file yet. Send over a supplier invoice and it\'ll show up here.</div>', unsafe_allow_html=True)
    st.stop()

with open(DATA_FILE) as f:
    orders = json.load(f)["orders"]

if not orders:
    st.markdown(f'<div style="text-align:center;padding:4rem;color:{T3};font-size:0.9rem;">No purchase orders on file yet. Send over a supplier invoice and it\'ll show up here.</div>', unsafe_allow_html=True)
    st.stop()

# ── Assumed sell price control ─────────────────────────────────────────────
col_note, col_price = st.columns([3, 1])
with col_price:
    sell_price = st.number_input("Assumed sell price / style ($)", min_value=0.0, value=160.0, step=5.0)
with col_note:
    st.markdown(f'<div style="padding-top:1.9rem;font-size:0.75rem;color:{T3};">Margins below assume every unit sells at this price. Shopify products aren\'t SKU-matched to supplier model codes, so this is an estimate — adjust it to test different price points.</div>', unsafe_allow_html=True)

# ── All-time overview ────────────────────────────────────────────────────────
st.markdown('<div class="section">Overview — All Purchase Orders</div>', unsafe_allow_html=True)

total_units = sum(i["qty"] for o in orders for i in o["items"])
total_paid  = sum(o["fees"]["total"] for o in orders)
blended_cost = (total_paid / total_units) if total_units else 0
total_revenue_est = total_units * sell_price
total_profit_est  = total_revenue_est - total_paid
margin_est = (total_profit_est / total_revenue_est * 100) if total_revenue_est else 0

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi">
    <div class="kpi-label">Units Ordered</div>
    <div class="kpi-value">{total_units:,}</div>
    <div class="kpi-sub">Across {len(orders)} purchase order{'s' if len(orders) != 1 else ''}</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Total Paid to Supplier</div>
    <div class="kpi-value">${total_paid:,.2f}</div>
    <div class="kpi-sub">Product cost + shipping + fees</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Blended Cost / Unit</div>
    <div class="kpi-value">${blended_cost:,.2f}</div>
    <div class="kpi-sub">Total paid ÷ units ordered</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Est. Margin @ ${sell_price:,.0f}/unit</div>
    <div class="kpi-value">{margin_est:.1f}%</div>
    <div class="kpi-sub">Est. profit ${total_profit_est:,.2f}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Per-order breakdown ──────────────────────────────────────────────────────
st.markdown('<div class="section">Purchase Orders</div>', unsafe_allow_html=True)

for o in orders:
    items = o["items"]
    fees  = o["fees"]
    styles = sorted(set(i["model"] for i in items))
    order_units = sum(i["qty"] for i in items)
    order_revenue = order_units * sell_price
    order_profit  = order_revenue - fees["total"]
    order_margin  = (order_profit / order_revenue * 100) if order_revenue else 0
    order_blended_cost = (fees["total"] / order_units) if order_units else 0

    with st.container():
        st.markdown(f"""
        <div class="surface">
          <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:1rem;flex-wrap:wrap;gap:0.5rem;">
            <div>
              <div style="font-size:1.1rem;font-weight:700;color:{T1};">{o['name']}</div>
              <div style="font-size:0.72rem;color:{T3};margin-top:0.2rem;">{o['id']} &nbsp;·&nbsp; {o['supplier']} &nbsp;·&nbsp; {o['date']}</div>
            </div>
            <div style="font-size:0.75rem;color:{T2};text-align:right;">
              {len(styles)} styles &nbsp;·&nbsp; {len(items)} variants &nbsp;·&nbsp; {order_units:,} units
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        k0, k1, k2, k3, k4 = st.columns(5)
        k0.metric("Styles Ordered", f"{len(styles)}")
        k1.metric("Product Subtotal", f"${fees['product_subtotal']:,.2f}")
        k2.metric("Shipping + Fees", f"${fees['shipping'] + fees['logo_cost'] + fees['lens_fee'] + fees['discount']:,.2f}")
        k3.metric("Total Paid", f"${fees['total']:,.2f}")
        k4.metric(f"Est. Margin @ ${sell_price:,.0f}", f"{order_margin:.1f}%", f"${order_profit:,.2f} est. profit")

        st.markdown(f'<div style="font-size:0.65rem;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:{T3};margin:1rem 0 0.5rem;">Units Ordered per Style</div>', unsafe_allow_html=True)
        style_rows = []
        for m in styles:
            m_items = [i for i in items if i["model"] == m]
            m_qty = sum(i["qty"] for i in m_items)
            m_cost = sum(i["amount"] for i in m_items)
            m_rev = m_qty * sell_price
            m_margin = ((m_rev - m_cost) / m_rev * 100) if m_rev else 0
            style_rows.append({
                "Model": m,
                "Colors Ordered": len(m_items),
                "Qty per Color": ", ".join(str(i["qty"]) for i in m_items),
                "Total Units": m_qty,
                "Total Cost": f"${m_cost:,.2f}",
                "Est. Margin": f"{m_margin:.1f}%",
            })
        st.dataframe(style_rows, use_container_width=True, hide_index=True)

        st.markdown(f'<div style="font-size:0.65rem;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:{T3};margin:1rem 0 0.5rem;">Full Line-Item Detail</div>', unsafe_allow_html=True)
        rows = []
        for i in items:
            rev = i["qty"] * sell_price
            profit = rev - i["amount"]
            margin = (profit / rev * 100) if rev else 0
            rows.append({
                "Model": i["model"],
                "Color": i["color"],
                "Size": i["size"],
                "Note": i["note"],
                "Qty": i["qty"],
                "Unit Cost": f"${i['unit_cost']:,.2f}",
                "Line Cost": f"${i['amount']:,.2f}",
                "Est. Revenue": f"${rev:,.2f}",
                "Est. Margin": f"{margin:.1f}%",
            })
        st.dataframe(rows, use_container_width=True, hide_index=True)

        fee_bits = []
        if fees.get("logo_cost"):
            fee_bits.append(f"Logo: ${fees['logo_cost']:,.2f}" + (f" ({fees['logo_cost_note']})" if fees.get("logo_cost_note") else ""))
        if fees.get("shipping"):
            fee_bits.append(f"Shipping: ${fees['shipping']:,.2f}" + (f" ({fees['shipping_note']})" if fees.get("shipping_note") else ""))
        if fees.get("lens_fee"):
            fee_bits.append(f"Lens fees: ${fees['lens_fee']:,.2f}" + (f" ({fees['lens_fee_note']})" if fees.get("lens_fee_note") else ""))
        if fees.get("discount"):
            fee_bits.append(f"Discount: ${fees['discount']:,.2f}")
        if fee_bits:
            st.markdown(f'<div style="font-size:0.72rem;color:{T3};margin-top:-0.5rem;margin-bottom:1.5rem;">{" &nbsp;·&nbsp; ".join(fee_bits)} &nbsp;·&nbsp; Blended cost/unit incl. fees: ${order_blended_cost:,.2f}</div>', unsafe_allow_html=True)

st.markdown(f"""
<div style="font-size:0.72rem;color:{T3};margin-top:1rem;padding-top:1.2rem;border-top:1px solid {BORDER};line-height:1.6;">
  To add a new purchase order, send over the supplier invoice — it gets parsed into this same view.
  Shopify inventory levels aren't linked to these styles yet since supplier model codes (e.g. "9133") don't match your Shopify SKUs;
  set SKUs to match supplier codes if you want live stock and per-style sell price pulled in automatically.
</div>
""", unsafe_allow_html=True)
