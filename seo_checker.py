import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import re
import os
import base64

# --- Page Config ---
st.set_page_config(
    page_title="Vidya Sarthi | On-Page SEO Suite",
    page_icon="🔶",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Optional Sidebar Logo Uploader (Saves permanently to your folder) ---
with st.sidebar:
    st.markdown("### 🎨 Brand Settings")
    uploaded_logo = st.file_uploader("Upload your Vidya Sarthi Logo (PNG/JPG)", type=["png", "jpg", "jpeg"])
    if uploaded_logo is not None:
        with open("logo.png", "wb") as f:
            f.write(uploaded_logo.getbuffer())
        st.success("Logo saved! It will now load automatically.")

# --- Load Local Logo or Render Single-Line Branded SVG (No 4-space indentation!) ---
def get_logo_html():
    for filename in ["logo.png", "image_d710a0.png", "vidya_sarthi_logo.png"]:
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                b64_data = base64.b64encode(f.read()).decode("utf-8")
            return f'<img src="data:image/png;base64,{b64_data}" class="vs-logo-img" alt="Vidya Sarthi">'

    # Single-line SVG so Streamlit Markdown never mistakes it for a code block
    svg_raw = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 110" width="60" height="60">'
        '<defs>'
        '<linearGradient id="g1" x1="0%" y1="0%" x2="40%" y2="100%">'
        '<stop offset="0%" stop-color="#FFCC00"/>'
        '<stop offset="55%" stop-color="#FF7A00"/>'
        '<stop offset="100%" stop-color="#E03C11"/>'
        '</linearGradient>'
        '<linearGradient id="g2" x1="0%" y1="0%" x2="40%" y2="100%">'
        '<stop offset="0%" stop-color="#FFB300"/>'
        '<stop offset="60%" stop-color="#F06A00"/>'
        '<stop offset="100%" stop-color="#C8320E"/>'
        '</linearGradient>'
        '</defs>'
        '<path d="M55 96 C70 96 84 78 96 28 C80 25 66 36 55 96 Z" fill="url(#g2)"/>'
        '<path d="M52 96 C65 96 75 76 79 20 C62 19 52 34 52 96 Z" fill="url(#g1)"/>'
        '<path d="M49 96 C60 96 65 74 60 14 C44 17 40 36 49 96 Z" fill="url(#g2)"/>'
        '<path d="M48 96 C55 94 56 74 39 16 C24 25 25 42 48 96 Z" fill="url(#g1)"/>'
        '</svg>'
    )
    b64_svg = base64.b64encode(svg_raw.encode("utf-8")).decode("utf-8")
    return f'<img src="data:image/svg+xml;base64,{b64_svg}" class="vs-logo-img" alt="Vidya Sarthi">'

# --- 2026 Modern SaaS Custom CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.stApp {
    background: radial-gradient(circle at 50% 0%, rgba(255, 136, 0, 0.15) 0%, rgba(11, 13, 19, 0) 55%), #0B0D13;
    color: #F8FAFC;
}

#MainMenu, footer {visibility: hidden;}
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
    max-width: 1240px !important;
}

.vs-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(22, 25, 35, 0.85);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 152, 0, 0.28);
    border-radius: 22px;
    padding: 20px 30px;
    margin-bottom: 28px;
    box-shadow: 0 20px 45px -15px rgba(0, 0, 0, 0.65), 0 0 30px rgba(255, 136, 0, 0.08);
}
.vs-brand-left {
    display: flex;
    align-items: center;
    gap: 20px;
}
.vs-logo-img {
    width: 68px;
    height: 68px;
    object-fit: contain;
    background: #FFFFFF;
    border-radius: 16px;
    padding: 6px;
    box-shadow: 0 6px 20px rgba(255, 136, 0, 0.3);
}
.vs-brand-title {
    font-size: 1.65rem;
    letter-spacing: 0.08em;
    color: #FFFFFF;
    margin: 0;
    line-height: 1.15;
}
.vs-brand-title span.light { font-weight: 400; color: #F8FAFC; }
.vs-brand-title span.bold {
    font-weight: 800;
    background: linear-gradient(90deg, #FFD000, #FF7A00);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.vs-brand-sub {
    font-size: 0.74rem;
    letter-spacing: 0.22em;
    color: #94A3B8;
    margin-top: 5px;
    font-weight: 600;
    text-transform: uppercase;
}
.vs-tool-pill {
    background: linear-gradient(135deg, rgba(255, 184, 0, 0.16), rgba(230, 74, 25, 0.16));
    border: 1px solid rgba(255, 152, 0, 0.45);
    color: #FFB800;
    padding: 9px 18px;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.05em;
}

div[data-testid="stTextInput"] input {
    background: rgba(22, 25, 35, 0.92) !important;
    border: 1px solid rgba(255, 255, 255, 0.14) !important;
    border-radius: 14px !important;
    color: #FFFFFF !important;
    padding: 14px 18px !important;
    font-size: 1rem !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #FF8800 !important;
    box-shadow: 0 0 0 3px rgba(255, 136, 0, 0.22) !important;
}
div.stButton > button {
    background: linear-gradient(135deg, #FFB800 0%, #FF7A00 55%, #E64A19 100%) !important;
    color: #0B0D13 !important;
    font-weight: 800 !important;
    font-size: 0.96rem !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.78rem 1.8rem !important;
    width: 100%;
    box-shadow: 0 10px 25px -5px rgba(255, 122, 0, 0.45) !important;
    transition: all 0.2s ease !important;
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 14px 30px -5px rgba(255, 122, 0, 0.65) !important;
}

.bento-card {
    background: rgba(22, 25, 35, 0.78);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 22px 24px;
    height: 100%;
}
.bento-label {
    font-size: 0.76rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #94A3B8;
    font-weight: 600;
    margin-bottom: 10px;
}
.bento-value {
    font-size: 2rem;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1.1;
}
.bento-sub {
    font-size: 0.8rem;
    color: #FFB800;
    margin-top: 6px;
    font-weight: 600;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background: rgba(22, 25, 35, 0.85);
    padding: 8px;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.07);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 12px !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
    color: #94A3B8 !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #FFB800 0%, #FF7A00 100%) !important;
    color: #0B0D13 !important;
    font-weight: 800 !important;
}

.issue-card {
    background: rgba(239, 68, 68, 0.08);
    border-left: 4px solid #F97316;
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 12px;
}
.pass-card {
    background: rgba(16, 185, 129, 0.08);
    border-left: 4px solid #10B981;
    border-radius: 12px;
    padding: 12px 18px;
    margin-bottom: 8px;
    font-size: 0.92rem;
}
.heading-pill {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 10px 14px;
    margin-bottom: 8px;
    font-size: 0.9rem;
}
.tag-badge {
    display: inline-block;
    background: rgba(255, 152, 0, 0.2);
    color: #FFB800;
    font-weight: 700;
    font-size: 0.72rem;
    padding: 2px 8px;
    border-radius: 6px;
    margin-right: 8px;
}
</style>
""", unsafe_allow_html=True)

# --- Render Branded Header (Flush-left HTML strings so Markdown renders properly) ---
logo_tag = get_logo_html()
header_html = (
    f'<div class="vs-header">'
    f'<div class="vs-brand-left">'
    f'{logo_tag}'
    f'<div>'
    f'<div class="vs-brand-title"><span class="light">VIDYA</span> <span class="bold">SARTHI</span></div>'
    f'<div class="vs-brand-sub">Institute of Digital Education</div>'
    f'</div>'
    f'</div>'
    f'<div class="vs-tool-pill">⚡ ON-PAGE SEO AUDITOR 2026</div>'
    f'</div>'
)
st.markdown(header_html, unsafe_allow_html=True)

# --- Core SEO Audit Logic ---
def analyze_seo(url):
    score = 100
    issues = []
    passed = []
    
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=12)
        if response.status_code >= 400:
            return None, f"HTTP Error {response.status_code}: Unable to fetch the page."
    except Exception as e:
        return None, f"Connection Error: {str(e)}"

    soup = BeautifulSoup(response.text, "html.parser")
    parsed_url = urlparse(url)

    for tag in soup(["script", "style", "noscript"]):
        tag.extract()

    if parsed_url.scheme != "https":
        score -= 5
        issues.append({"severity": "High", "element": "HTTPS", "mistake": "Not using HTTPS.", "fix": "Redirect HTTP traffic to HTTPS."})
    else:
        passed.append("HTTPS security protocol is active.")

    title_tag = soup.find("title")
    title_text = title_tag.get_text(strip=True) if title_tag else ""
    t_len = len(title_text)
    if not title_text:
        score -= 20
        issues.append({"severity": "High", "element": "Title Tag", "mistake": "Missing <title> tag.", "fix": "Add a <title> between 50–60 characters."})
    elif t_len < 30 or t_len > 60:
        score -= 8
        issues.append({"severity": "Medium", "element": f"Title ({t_len} chars)", "mistake": f"Length outside 30–60 chars: '{title_text}'", "fix": "Keep your title between 50–60 characters."})
    else:
        passed.append(f"Title length is optimal ({t_len} chars).")

    meta_desc = soup.find("meta", attrs={"name": re.compile("^description$", re.I)})
    desc_text = meta_desc.get("content", "").strip() if meta_desc else ""
    d_len = len(desc_text)
    if not desc_text:
        score -= 15
        issues.append({"severity": "High", "element": "Meta Description", "mistake": "Missing meta description.", "fix": "Add a meta description (120–160 chars)."})
    elif d_len < 70 or d_len > 160:
        score -= 6
        issues.append({"severity": "Low", "element": f"Meta Description ({d_len} chars)", "mistake": "Length outside 70–160 chars.", "fix": "Adjust meta description to 120–160 characters."})
    else:
        passed.append(f"Meta description length is optimal ({d_len} chars).")

    headings = {
        "H1": [h.get_text(" ", strip=True) for h in soup.find_all("h1") if h.get_text(strip=True)],
        "H2": [h.get_text(" ", strip=True) for h in soup.find_all("h2") if h.get_text(strip=True)],
        "H3": [h.get_text(" ", strip=True) for h in soup.find_all("h3") if h.get_text(strip=True)],
    }

    if len(headings["H1"]) == 0:
        score -= 15
        issues.append({"severity": "High", "element": "H1 Tag", "mistake": "No H1 tag found.", "fix": "Add exactly one primary H1 heading."})
    elif len(headings["H1"]) > 1:
        score -= 8
        issues.append({"severity": "Medium", "element": "H1 Tag", "mistake": f"Multiple H1s found ({len(headings['H1'])}).", "fix": "Keep only 1 main H1; convert others to H2."})
    else:
        passed.append("Single H1 heading detected.")

    if len(headings["H2"]) == 0:
        score -= 5
        issues.append({"severity": "Low", "element": "H2 Tags", "mistake": "No H2 subheadings found.", "fix": "Use H2 subheadings to structure your sections."})
    else:
        passed.append(f"Structured with {len(headings['H2'])} H2s and {len(headings['H3'])} H3s.")

    internal_links, external_links = [], []
    for a in soup.find_all("a", href=True):
        raw_href = a["href"].strip()
        if not raw_href or raw_href.startswith(("#", "javascript:", "mailto:", "tel:")):
            continue
        full_url = urljoin(url, raw_href)
        link_netloc = urlparse(full_url).netloc
        anchor = a.get_text(" ", strip=True) or "[Image / No Text]"
        rel = a.get("rel", [])
        rel_str = ", ".join(rel) if isinstance(rel, list) else str(rel)

        link_info = {"Anchor Text": anchor, "Destination URL": full_url, "Rel": rel_str or "dofollow"}
        if link_netloc == parsed_url.netloc:
            internal_links.append(link_info)
        else:
            external_links.append(link_info)

    if len(internal_links) == 0:
        score -= 5
        issues.append({"severity": "Medium", "element": "Internal Links", "mistake": "0 internal links found.", "fix": "Add internal links pointing to related articles."})
    else:
        passed.append(f"Found {len(internal_links)} internal links & {len(external_links)} external links.")

    image_details = []
    missing_alt_count = 0
    tracking_patterns = ["facebook.com/tr", "ads.linkedin.com", "google-analytics.com", "doubleclick.net", "bat.bing.com"]

    for img in soup.find_all("img"):
        raw_src = (img.get("data-src") or img.get("data-lazy-src") or img.get("src") or "").strip()
        if not raw_src or raw_src.startswith("data:image"):
            continue
        if any(tp in raw_src.lower() for tp in tracking_patterns):
            continue
        if img.get("width") == "1" or img.get("height") == "1":
            continue

        src = urljoin(url, raw_src)
        alt = img.get("alt")
        has_alt = bool(alt and alt.strip())
        if not has_alt:
            missing_alt_count += 1
        image_details.append({
            "Status": "✅ OK" if has_alt else "❌ Missing Alt",
            "Alt Text": alt.strip() if has_alt else "MISSING",
            "Image URL": src
        })

    if image_details:
        if missing_alt_count > 0:
            deduction = min(15, max(5, int((missing_alt_count / len(image_details)) * 15)))
            score -= deduction
            issues.append({
                "severity": "Medium",
                "element": "Image Alt Text",
                "mistake": f"{missing_alt_count}/{len(image_details)} content images missing alt text.",
                "fix": "Open the 'Content Images' tab to view missing alt attributes."
            })
        else:
            passed.append(f"All {len(image_details)} content images contain descriptive alt text.")

    canonical = soup.find("link", rel=lambda x: x and "canonical" in x.lower())
    if not canonical or not canonical.get("href"):
        score -= 5
        issues.append({"severity": "Medium", "element": "Canonical Tag", "mistake": "Missing canonical tag.", "fix": "Add a self-referencing <link rel='canonical'> tag."})
    else:
        passed.append(f"Canonical tag configured ({canonical.get('href')}).")

    word_count = len(soup.get_text(separator=" ").split())
    if word_count < 300:
        score -= 10
        issues.append({"severity": "Medium", "element": "Word Count", "mistake": f"Thin content ({word_count} words).", "fix": "Expand body content to at least 300–600 words."})
    else:
        passed.append(f"Comprehensive content depth ({word_count} words).")

    return {
        "score": max(0, score),
        "title": title_text,
        "meta_desc": desc_text,
        "word_count": word_count,
        "issues": issues,
        "passed": passed,
        "headings": headings,
        "internal_links": internal_links,
        "external_links": external_links,
        "images": image_details
    }, None

# --- Search Bar Section ---
col_input, col_btn = st.columns([4.2, 1])
with col_input:
    url_input = st.text_input("Enter Public URL", placeholder="https://digizenmaverick.growtoday.co.in/what-is-digital-marketing/", label_visibility="collapsed")
with col_btn:
    run_audit = st.button("Analyze Page →")

if run_audit and url_input:
    with st.spinner("Running Vidya Sarthi On-Page SEO Engine..."):
        res, err = analyze_seo(url_input)

    if err:
        st.error(err)
    else:
        st.write("")
        k1, k2, k3, k4, k5 = st.columns([1.25, 1, 1, 1, 1])
        
        score_val = res["score"]
        ring_color = "#10B981" if score_val >= 85 else ("#FFB800" if score_val >= 60 else "#EF4444")
        
        with k1:
            st.markdown(f'<div class="bento-card" style="border-color: rgba(255, 152, 0, 0.35);"><div class="bento-label">On-Page SEO Score</div><div class="bento-value" style="color: {ring_color};">{score_val}<span style="font-size:1.1rem;color:#64748B;"> / 100</span></div><div class="bento-sub">{"🔥 Excellent Optimization" if score_val >= 85 else "⚡ Room for Improvement"}</div></div>', unsafe_allow_html=True)
        with k2:
            st.markdown(f'<div class="bento-card"><div class="bento-label">Content Depth</div><div class="bento-value">{res["word_count"]}</div><div class="bento-sub">Total Words</div></div>', unsafe_allow_html=True)
        with k3:
            st.markdown(f'<div class="bento-card"><div class="bento-label">Heading Structure</div><div class="bento-value">{len(res["headings"]["H1"])} / {len(res["headings"]["H2"])} / {len(res["headings"]["H3"])}</div><div class="bento-sub">H1 / H2 / H3 Tags</div></div>', unsafe_allow_html=True)
        with k4:
            st.markdown(f'<div class="bento-card"><div class="bento-label">Link Architecture</div><div class="bento-value">{len(res["internal_links"])} / {len(res["external_links"])}</div><div class="bento-sub">Internal / External</div></div>', unsafe_allow_html=True)
        with k5:
            st.markdown(f'<div class="bento-card"><div class="bento-label">Media Assets</div><div class="bento-value">{len(res["images"])}</div><div class="bento-sub">Content Images</div></div>', unsafe_allow_html=True)

        st.write("")
        st.write("")

        tab1, tab2, tab3, tab4 = st.tabs([
            f"🎯 Overview & Fixes ({len(res['issues'])})",
            f"📑 Headings ({len(res['headings']['H1']) + len(res['headings']['H2']) + len(res['headings']['H3'])})",
            f"🔗 Links ({len(res['internal_links']) + len(res['external_links'])})",
            f"🖼️ Content Images ({len(res['images'])})"
        ])

        with tab1:
            st.markdown(f'<div class="bento-card" style="margin-bottom: 20px;"><div class="bento-label">SERP Snippet Preview</div><div style="font-size: 1.15rem; font-weight: 700; color: #FFB800; margin-bottom: 6px;">{res["title"] or "Missing Title Tag"}</div><div style="font-size: 0.82rem; color: #10B981; margin-bottom: 8px;">{url_input}</div><div style="font-size: 0.92rem; color: #CBD5E1; line-height: 1.5;">{res["meta_desc"] or "No meta description provided on this page."}</div></div>', unsafe_allow_html=True)

            col_left, col_right = st.columns(2)
            with col_left:
                st.markdown("#### ⚠️ Actionable Fixes")
                if res["issues"]:
                    for i in res["issues"]:
                        st.markdown(f'<div class="issue-card"><div style="font-weight:700; color:#FB923C; margin-bottom:4px;">[{i["severity"]} Priority] {i["element"]}</div><div style="color:#F8FAFC; font-size:0.93rem; margin-bottom:6px;">{i["mistake"]}</div><div style="color:#94A3B8; font-size:0.84rem;">💡 <b>Fix:</b> {i["fix"]}</div></div>', unsafe_allow_html=True)
                else:
                    st.success("🎉 Zero on-page SEO issues detected! This page is fully optimized.")

            with col_right:
                st.markdown(f"#### ✅ Passed Checks ({len(res['passed'])})")
                for ok in res["passed"]:
                    st.markdown(f'<div class="pass-card">✅ &nbsp;{ok}</div>', unsafe_allow_html=True)

        with tab2:
            ch1, ch2, ch3 = st.columns(3)
            with ch1:
                st.markdown(f"#### H1 Tag ({len(res['headings']['H1'])})")
                for text in res["headings"]["H1"]:
                    st.markdown(f'<div class="heading-pill"><span class="tag-badge">H1</span>{text}</div>', unsafe_allow_html=True)
            with ch2:
                st.markdown(f"#### H2 Subheadings ({len(res['headings']['H2'])})")
                for text in res["headings"]["H2"]:
                    st.markdown(f'<div class="heading-pill"><span class="tag-badge">H2</span>{text}</div>', unsafe_allow_html=True)
            with ch3:
                st.markdown(f"#### H3 Subheadings ({len(res['headings']['H3'])})")
                for text in res["headings"]["H3"]:
                    st.markdown(f'<div class="heading-pill"><span class="tag-badge">H3</span>{text}</div>', unsafe_allow_html=True)

        with tab3:
            st.markdown(f"#### Internal Links ({len(res['internal_links'])})")
            if res["internal_links"]:
                st.dataframe(res["internal_links"], use_container_width=True, hide_index=True)
            else:
                st.info("No internal links found.")

            st.markdown(f"#### External Links ({len(res['external_links'])})")
            if res["external_links"]:
                st.dataframe(res["external_links"], use_container_width=True, hide_index=True)
            else:
                st.info("No external links found.")

        with tab4:
            st.markdown("#### Content Images & Alt Attributes")
            if res["images"]:
                st.dataframe(res["images"], use_container_width=True, hide_index=True)
            else:
                st.info("No content images found on this page.")