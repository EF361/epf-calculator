import streamlit as st
import json
import math
import fitz  # PyMuPDF
import os
import base64

# Page configuration
st.set_page_config(
    page_title="EPF Calculator & Reference Hub",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for custom premium styles and dark mode aesthetics
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

/* Main font override */
html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Premium Minimal Header */
.header-container {
    padding: 16px 0;
    margin-bottom: 24px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
.header-title {
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #ffffff; /* High contrast solid white */
    margin-bottom: 4px;
}
.header-subtitle {
    font-size: 0.95rem;
    color: #94a3b8;
    font-weight: 400;
}

/* Modern Card Containers - Solid Colors for Maximum Contrast */
.premium-container {
    background: #0f172a; /* Solid Slate-900 */
    border: 1px solid #1e293b; /* Slate-800 border */
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
}

.premium-card {
    background: #0f172a; /* Solid Slate-900 */
    border: 1px solid #334155; /* Slate-700 border */
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    transition: border-color 0.2s ease;
}
.premium-card:hover {
    border-color: #3b82f6;
}

/* Metric Cards at the top - Solid Backgrounds with High Contrast Value text */
.metric-grid {
    display: flex;
    gap: 16px;
    margin-bottom: 24px;
}
.metric-box {
    background: #1e293b; /* Solid Slate-800 */
    border: 1px solid #334155; /* Slate-700 border */
    border-radius: 12px;
    padding: 20px;
    text-align: left;
    flex: 1;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    transition: transform 0.2s ease, border-color 0.2s ease;
}
.metric-box:hover {
    transform: translateY(-2px);
    border-color: #3b82f6;
}
.metric-title {
    font-size: 0.8rem;
    font-weight: 600;
    color: #94a3b8; /* Soft Slate-400 */
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 6px;
}
.metric-value {
    font-size: 1.8rem;
    font-weight: 800;
    color: #ffffff; /* Solid white for main total */
}

/* Custom Table Styles - High Contrast Solid Table */
.custom-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 15px;
    background: #0f172a; /* Solid Slate-900 */
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #1e293b;
}

.custom-table th {
    background: #1e293b; /* Solid Slate-800 */
    color: #f8fafc; /* Near white headers */
    font-weight: 600;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 14px 16px;
    border-bottom: 2px solid #334155;
}

.custom-table td {
    padding: 14px 16px;
    border-bottom: 1px solid #1e293b;
    color: #ffffff; /* Solid White for maximum table text readability */
    font-size: 0.9rem;
}

.custom-table tr:hover {
    background-color: #1e293b;
}

/* Highlight badge */
.highlight-text {
    background: rgba(59, 130, 246, 0.2);
    border: 1px solid rgba(59, 130, 246, 0.4);
    color: #93c5fd; /* Vibrant light blue */
    padding: 2px 6px;
    border-radius: 6px;
    font-weight: 600;
    font-size: 0.85rem;
}

/* PDF Section card styling */
.ref-section {
    background: #1e293b; /* Solid Slate-800 */
    border-radius: 12px;
    border: 1px solid #334155;
    padding: 24px;
    margin-bottom: 16px;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
}
.ref-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #334155;
    padding-bottom: 12px;
    margin-bottom: 12px;
}
.ref-title {
    color: #60a5fa; /* Sky blue */
    font-weight: 800;
    font-size: 1.1rem;
}
.ref-badge {
    background: rgba(59, 130, 246, 0.2);
    color: #60a5fa;
    border: 1px solid rgba(59, 130, 246, 0.4);
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
}

/* Shadow framework for document view */
.document-holder {
    background: #111827;
    border-radius: 12px;
    padding: 8px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
}
</style>
""", unsafe_allow_html=True)

# File Paths
PDF_PATH = "10. Effective 1 October 2025.pdf"
JSON_PATH = "parsed_rates.json"

# Translations dictionary
translations = {
    "English": {
        "title": "EPF Calculator & Reference Hub",
        "subtitle": "Determine employee and employer provident fund rates with live legal schedule matching.",
        "controls": "🎛️ Calculator Controls",
        "add_income": "➕ Add Income Source",
        "clear_all": "🗑️ Clear All Incomes",
        "official_doc": "📄 Official Document",
        "download_pdf": "📥 Download Reference PDF",
        "guidelines": "#### 💡 Guidelines",
        "guideline_text": "EPF contributions are bracket-based up to RM 20,000 and flat-percentage based above that. This calculator uses the precise rates defined in the Third Schedule of the EPF Act.",
        "calc_tab": "📊 EPF Calculator Dashboard",
        "pdf_tab": "📖 Full Document Reference",
        "income_details": "💼 Income Sources",
        "income_num": "Income #",
        "label": "Label",
        "salary": "Monthly Salary (RM)",
        "citizenship": "Citizenship/Residency",
        "age_group": "Age Group",
        "totals_title": "🏆 Combined Contribution Summary",
        "total_wages": "Total Wages",
        "employer_share": "Employer Share",
        "employee_share": "Employee Share",
        "grand_total": "Grand Total EPF",
        "col_source": "Source",
        "col_salary": "Salary",
        "col_rule": "Rule/Part",
        "col_employer": "Employer Share",
        "col_employee": "Employee Share",
        "col_total": "Total Contribution",
        "totals_row": "Total",
        "live_pdf_title": "🔍 Highlighted Schedule Reference",
        "select_highlight": "Select Income to Highlight in PDF:",
        "legal_source": "Legal Schedule Source",
        "target_page": "Target Page in Document:",
        "matching_bracket": "Matching Bracket Pattern:",
        "browse_pdf_title": "📖 Browse Official EPF Third Schedule",
        "go_to_page": "Go to Page",
        "total_pages": "Total Pages:",
        "flat_rate_desc": "Flat 2% rate of monthly wages",
        "exceed_desc": "Wages exceed RM20,000.00",
        "no_pdf": "Could not load the reference PDF file. Please ensure '10. Effective 1 October 2025.pdf' is present in the workspace.",
        "pdf_not_found": "Reference PDF not found."
    },
    "中文": {
        "title": "公积金计算器与参考中心",
        "subtitle": "根据官方第三附表精确计算雇员和雇主的公积金 (EPF) 缴纳比例。",
        "controls": "🎛️ 计算器控制",
        "add_income": "➕ 添加收入来源",
        "clear_all": "🗑️ 清空所有输入",
        "official_doc": "📄 官方文件",
        "download_pdf": "📥 下载参考 PDF",
        "guidelines": "#### 💡 指南",
        "guideline_text": "公积金缴纳在 RM 20,000 以内是按档位计算的，超过该金额则按固定百分比计算。本计算器采用公积金法案第三附表规定的精确税率。",
        "calc_tab": "📊 公积金计算仪表板",
        "pdf_tab": "📖 完整官方文件参考",
        "income_details": "💼 收入来源管理",
        "income_num": "收入项目 #",
        "label": "项目名称",
        "salary": "月薪额 (RM)",
        "citizenship": "国籍/身份",
        "age_group": "年龄组",
        "totals_title": "🏆 综合公积金缴纳汇总",
        "total_wages": "总薪资额",
        "employer_share": "雇主交纳份额",
        "employee_share": "雇员交纳份额",
        "grand_total": "公积金合计金额",
        "col_source": "来源",
        "col_salary": "月薪",
        "col_rule": "规则/类别",
        "col_employer": "雇主份额",
        "col_employee": "雇员份额",
        "col_total": "合计缴纳额",
        "totals_row": "合计",
        "live_pdf_title": "🔍 实时官方文献对照高亮",
        "select_highlight": "选择高亮显示的对应收入项:",
        "legal_source": "官方文献法定来源",
        "target_page": "官方页面:",
        "matching_bracket": "匹配工资档位:",
        "browse_pdf_title": "📖 浏览官方公积金第三附表原文",
        "go_to_page": "前往页码",
        "total_pages": "文件总页数:",
        "flat_rate_desc": "按月工资的固定 2% 比例",
        "exceed_desc": "工资超过 RM20,000.00",
        "no_pdf": "无法加载参考 PDF 文件。请确保工作区中存在 '10. Effective 1 October 2025.pdf'。",
        "pdf_not_found": "未找到参考 PDF。"
    }
}

citizen_options_en = [
    "Malaysian Citizen", 
    "Permanent Resident (PR)", 
    "Citizen-equivalent (Elected to contribute before 1 Aug 1998)",
    "Normal Non-citizen (Other)"
]

citizen_options_zh = [
    "马来西亚公民", 
    "永久居民 (PR)", 
    "准公民 (1998年8月1日前选择缴存的非公民)",
    "普通非公民 (其他)"
]

age_options_en = ["Under 60 years", "60 years and above"]
age_options_zh = ["60岁以下", "60岁及以上"]

# Load the rates database
@st.cache_data
def load_rates_database():
    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

parsed_rates = load_rates_database()

# Highlight and render function
@st.cache_data(show_spinner=False)
def render_pdf_page_with_highlight(page_idx, search_str, is_flat_non_citizen=False):
    if not os.path.exists(PDF_PATH):
        return None
        
    doc = fitz.open(PDF_PATH)
    if page_idx < 0 or page_idx >= len(doc):
        return None
        
    page = doc[page_idx]
    for annot in page.annots():
        page.delete_annot(annot)
        
    if is_flat_non_citizen:
        rects = page.search_for("employees who are not Malaysian citizens")
    else:
        rects = page.search_for(search_str)
        
    if rects:
        y0 = min(r.y0 for r in rects)
        y1 = max(r.y1 for r in rects)
        width = page.rect.width
        highlight_rect = fitz.Rect(35, y0 - 1.5, width - 35, y1 + 1.5)
        annot = page.add_highlight_annot(highlight_rect)
        annot.set_colors(stroke=[1.0, 0.85, 0.15])
        annot.update()
        
    pix = page.get_pixmap(dpi=150)
    return pix.tobytes("png")

# Core EPF Calculation Engine
def calculate_epf_contribution(salary, citizenship, age_group):
    if citizenship == "Normal Non-citizen (Other)":
        part = "Part F"
    elif age_group == "Under 60 years":
        part = "Part A"
    else:
        if citizenship == "Malaysian Citizen":
            part = "Part E"
        else:
            part = "Part C"
            
    if part == "Part F":
        employer = math.ceil(salary * 0.02)
        employee = math.ceil(salary * 0.02)
        return {
            "part": part,
            "employer": float(employer),
            "employee": float(employee),
            "total": float(employer + employee),
            "search_str": "employees who are not Malaysian citizens",
            "page_num": 55,
            "is_flat": True,
            "bracket_range": "Flat 2% rate of monthly wages"
        }
        
    if salary <= 10.00:
        return {
            "part": part,
            "employer": 0.0,
            "employee": 0.0,
            "total": 0.0,
            "search_str": "From 0.01 to 10.00",
            "page_num": 2 if part == "Part A" else (22 if part == "Part C" else 39),
            "is_flat": False,
            "bracket_range": "From 0.01 to 10.00"
        }
        
    if salary > 20000.00:
        if part == "Part A":
            employer_rate, employee_rate = 0.12, 0.11
        elif part == "Part C":
            employer_rate, employee_rate = 0.06, 0.055
        else:
            employer_rate, employee_rate = 0.04, 0.0
            
        employer = math.ceil(salary * employer_rate)
        employee = math.ceil(salary * employee_rate)
        return {
            "part": part,
            "employer": float(employer),
            "employee": float(employee),
            "total": float(employer + employee),
            "search_str": "wages exceed RM20,000.00",
            "page_num": 20 if part == "Part A" else (37 if part == "Part C" else 53),
            "is_flat": True,
            "bracket_range": f"Wages exceed RM20,000.00 ({int(employer_rate*100)}% / {employee_rate*100}%)"
        }
        
    if salary <= 5000.00:
        bracket_max = math.ceil(salary / 20.0) * 20
    else:
        bracket_max = math.ceil(salary / 100.0) * 100
        
    rows = parsed_rates.get(part, [])
    for row in rows:
        if abs(row["max_wage"] - bracket_max) < 0.01:
            return {
                "part": part,
                "employer": row["employer"],
                "employee": row["employee"],
                "total": row["total"],
                "search_str": f"From {row['min_wage']:,.2f} to {row['max_wage']:,.2f}",
                "page_num": row["page"],
                "is_flat": False,
                "bracket_range": f"From {row['min_wage']:,.2f} to {row['max_wage']:,.2f}"
            }
            
    if part == "Part A":
        employer_rate = 0.13 if bracket_max <= 5000 else 0.12
        employee_rate = 0.11
    elif part == "Part C":
        employer_rate = 0.065 if bracket_max <= 5000 else 0.06
        employee_rate = 0.055
    else:
        employer_rate = 0.04
        employee_rate = 0.0
        
    employer = math.ceil(bracket_max * employer_rate)
    employee = math.ceil(bracket_max * employee_rate)
    search_str = f"From {bracket_max-19.99:,.2f} to {bracket_max:,.2f}" if bracket_max <= 5000 else f"From {bracket_max-99.99:,.2f} to {bracket_max:,.2f}"
    
    return {
        "part": part,
        "employer": float(employer),
        "employee": float(employee),
        "total": float(employer + employee),
        "search_str": search_str,
        "page_num": 2 if part == "Part A" else (22 if part == "Part C" else 39),
        "is_flat": False,
        "bracket_range": search_str
    }

# Top navigation bar containing title on left and language toggle on right
col_header_title, col_header_toggle = st.columns([4, 1])

# Determine language first
with col_header_toggle:
    lang_sel = st.selectbox(
        "🌐 Language Toggle",
        options=["English", "中文"],
        key="lang_selector",
        label_visibility="collapsed"
    )
t = translations[lang_sel]

with col_header_title:
    st.title(t['title'])
    st.write(f"*{t['subtitle']}*")

# Manage state for multiple income sources
if "incomes" not in st.session_state:
    st.session_state.incomes = [
        {"label": "Primary Job", "salary": 4500.0, "citizenship": "Malaysian Citizen", "age_group": "Under 60 years"}
    ]

# Sidebar for global controls and app information
with st.sidebar:
    st.markdown(f"### {t['controls']}")
    if st.button(t["add_income"], use_container_width=True):
        label_text = f"Income Source {len(st.session_state.incomes) + 1}" if lang_sel == "English" else f"收入来源 {len(st.session_state.incomes) + 1}"
        st.session_state.incomes.append({
            "label": label_text,
            "salary": 3000.0,
            "citizenship": "Malaysian Citizen",
            "age_group": "Under 60 years"
        })
        st.rerun()
        
    if len(st.session_state.incomes) > 1:
        if st.button(t["clear_all"], use_container_width=True):
            st.session_state.incomes = [st.session_state.incomes[0]]
            st.rerun()
            
    st.markdown("---")
    st.markdown(f"### {t['official_doc']}")
    if os.path.exists(PDF_PATH):
        with open(PDF_PATH, "rb") as f:
            st.download_button(
                label=t["download_pdf"],
                data=f,
                file_name="EPF_Third_Schedule_2025.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            
    st.markdown("---")
    st.markdown(t["guidelines"])
    st.caption(t["guideline_text"])

# Compute totals and outcomes
total_salary = 0.0
total_employer = 0.0
total_employee = 0.0
calculated_items = []

for idx, inc in enumerate(st.session_state.incomes):
    res = calculate_epf_contribution(inc["salary"], inc["citizenship"], inc["age_group"])
    res["label"] = inc["label"]
    res["actual_salary"] = inc["salary"]
    calculated_items.append(res)
    total_salary += inc["salary"]
    total_employer += res["employer"]
    total_employee += res["employee"]

# Tabs layout
tab_calc, tab_pdf_viewer = st.tabs([t["calc_tab"], t["pdf_tab"]])

with tab_calc:
    # 1. Total Metrics summary at the very top of the tab
    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-box">
            <div class="metric-title">{t['total_wages']}</div>
            <div class="metric-value">RM {total_salary:,.2f}</div>
        </div>
        <div class="metric-box" style="border-left: 4px solid #3b82f6;">
            <div class="metric-title">{t['employer_share']}</div>
            <div class="metric-value" style="color: #60a5fa;">RM {total_employer:,.2f}</div>
        </div>
        <div class="metric-box" style="border-left: 4px solid #818cf8;">
            <div class="metric-title">{t['employee_share']}</div>
            <div class="metric-value" style="color: #a5b4fc;">RM {total_employee:,.2f}</div>
        </div>
        <div class="metric-box" style="border-left: 4px solid #10b981;">
            <div class="metric-title">{t['grand_total']}</div>
            <div class="metric-value" style="color: #34d399;">RM {total_employer + total_employee:,.2f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1.1, 0.9])
    
    with col_left:
        # Income Source Management Panel
        st.markdown(f"### {t['income_details']}")
        for idx, inc in enumerate(st.session_state.incomes):
            with st.container(border=True):
                # Layout redesign: 2 rows to give dropdowns full visibility without truncation
                r1_c1, r1_c2 = st.columns([1, 1])
                r2_c1, r2_c2, r2_c3 = st.columns([2, 2, 0.5])
                
                if lang_sel == "中文":
                    citizen_options = citizen_options_zh
                    age_options = age_options_zh
                    citizen_index = citizen_options_en.index(inc["citizenship"])
                    age_index = age_options_en.index(inc["age_group"])
                else:
                    citizen_options = citizen_options_en
                    age_options = age_options_en
                    citizen_index = citizen_options_en.index(inc["citizenship"])
                    age_index = age_options_en.index(inc["age_group"])
                    
                with r1_c1:
                    new_label = st.text_input(t["label"], value=inc["label"], key=f"label_{idx}")
                    inc["label"] = new_label
                with r1_c2:
                    # QA Validation: limit max value to 99,999,999 to avoid excessively large numbers.
                    # Note: Streamlit's number_input natively prevents entering strings and symbols.
                    new_salary = st.number_input(t["salary"], min_value=0.0, max_value=99999999.0, value=float(inc["salary"]), step=100.0, format="%.2f", key=f"salary_{idx}")
                    inc["salary"] = new_salary
                with r2_c1:
                    new_citizen_display = st.selectbox(
                        t["citizenship"],
                        options=citizen_options,
                        index=citizen_index,
                        key=f"citizen_{idx}"
                    )
                    inc["citizenship"] = citizen_options_en[citizen_options.index(new_citizen_display)]
                with r2_c2:
                    new_age_display = st.selectbox(
                        t["age_group"],
                        options=age_options,
                        index=age_index,
                        key=f"age_{idx}"
                    )
                    inc["age_group"] = age_options_en[age_options.index(new_age_display)]
                with r2_c3:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if len(st.session_state.incomes) > 1:
                        if st.button("🗑️", key=f"del_{idx}", use_container_width=True):
                            st.session_state.incomes.pop(idx)
                            st.rerun()
            
        # Action Buttons
        col_btn_search, col_btn_action = st.columns([1, 1])
        with col_btn_search:
            search_text = "🔍 Search Document" if lang_sel == "English" else "🔍 搜索参考文档"
            if st.button(search_text, type="primary", use_container_width=True):
                st.toast("Updating reference document..." if lang_sel == "English" else "正在更新参考文档...", icon="🔍")
        with col_btn_action:
            if st.button(t["add_income"], key="inline_add", use_container_width=True):
                label_text = f"Income Source {len(st.session_state.incomes) + 1}" if lang_sel == "English" else f"收入来源 {len(st.session_state.incomes) + 1}"
                st.session_state.incomes.append({
                    "label": label_text,
                    "salary": 3000.0,
                    "citizenship": "Malaysian Citizen",
                    "age_group": "Under 60 years"
                })
                st.rerun()

        # (Table removed as per user request to simplify UI)

    with col_right:
        st.markdown(f"### {t['live_pdf_title']}")
        
        # Selected income dropdown
        if len(calculated_items) > 1:
            active_idx = st.selectbox(
                t["select_highlight"],
                options=range(len(calculated_items)),
                format_func=lambda i: f"{calculated_items[i]['label']}"
            )
        else:
            active_idx = 0
            
        active_item = calculated_items[active_idx]
        
        # Details container
        bracket_range_disp = active_item['bracket_range']
        if active_item['is_flat']:
            if "Flat 2%" in active_item['bracket_range']:
                bracket_range_disp = t["flat_rate_desc"]
            elif "Wages exceed" in active_item['bracket_range']:
                bracket_range_disp = f"{t['exceed_desc']} ({active_item['bracket_range'].split('(')[1]}"

        st.markdown(f"""
        <div class="ref-section">
            <div class="ref-header">
                <span class="ref-title">📋 {t['legal_source']}</span>
                <span class="ref-badge">{active_item['part']}</span>
            </div>
            <p style="margin: 0 0 8px 0; color: #e2e8f0; font-size: 0.95rem;">
                {t['target_page']} <strong style="color: #ffffff;">Page {active_item['page_num']}</strong>
            </p>
            <p style="margin: 0; color: #e2e8f0; font-size: 0.95rem;">
                {t['matching_bracket']} <span class="highlight-text">{bracket_range_disp}</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Render page
        with st.spinner("Generating document reference..."):
            is_flat_non_citizen = (active_item['part'] == "Part F")
            img_bytes = render_pdf_page_with_highlight(
                page_idx=active_item['page_num'] - 1,
                search_str=active_item['search_str'],
                is_flat_non_citizen=is_flat_non_citizen
            )
            
        if img_bytes:
            st.markdown('<div class="document-holder">', unsafe_allow_html=True)
            st.image(img_bytes, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error(t["no_pdf"])

with tab_pdf_viewer:
    st.markdown('<div class="premium-container">', unsafe_allow_html=True)
    st.markdown(f"### {t['browse_pdf_title']}")
    
    if os.path.exists(PDF_PATH):
        doc = fitz.open(PDF_PATH)
        total_pages = len(doc)
        
        col_nav1, col_nav2 = st.columns([1, 4])
        with col_nav1:
            browse_page = st.number_input(t["go_to_page"], min_value=1, max_value=total_pages, value=1)
        with col_nav2:
            st.markdown(f"<p style='margin-top: 30px; color:#94a3b8;'>{t['total_pages']} <strong>{total_pages}</strong></p>", unsafe_allow_html=True)
            
        with st.spinner(f"Loading Page {browse_page}..."):
            page = doc[browse_page - 1]
            pix = page.get_pixmap(dpi=100)
            browse_img_bytes = pix.tobytes("png")
            st.markdown('<div class="document-holder">', unsafe_allow_html=True)
            st.caption("Hover over the document and click the ⤢ icon to view fullscreen and zoom.")
            st.image(browse_img_bytes, width=750)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error(t["pdf_not_found"])
    st.markdown('</div>', unsafe_allow_html=True)
