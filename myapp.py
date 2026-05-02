import streamlit as st

# 1. إعداد الصفحة والستايل والاسم المعتمد
st.set_page_config(page_title="MY ACADEMIC TRACKER", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 20% 30%, #4a0e4e 0%, #1a1a2e 50%, #000000 100%),
                    radial-gradient(circle at 80% 70%, #830d2d 0%, #1a1a2e 50%, #000000 100%);
        background-attachment: fixed;
        font-family: 'Inter', sans-serif !important;
    }

    h1, h2, h3, label, p { color: #ffffff !important; font-family: 'Inter', sans-serif !important; }

    input { background-color: #ffffff !important; color: #000000 !important; border-radius: 10px !important; font-weight: 600 !important; }
    
    .stTabs [data-baseweb="tab"] { background: rgba(255, 255, 255, 0.05) !important; border-radius: 12px !important; color: #bbbbbb !important; padding: 10px 20px !important; }
    .stTabs [aria-selected="true"] { background: #5d3fd3 !important; color: white !important; border: 1px solid #ff007f !important; }
    
    .footer { text-align: center; padding: 20px; color: rgba(255,255,255,0.6); margin-top: 50px; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# نظام تقديرات جامعة الدلتا (كلية الذكاء الاصطناعي)
# ---------------------------------------------------------

# الحد الأدنى للنسبة المئوية لكل تقدير (لتحليل الفاينال)
DELTA_THRESHOLDS = {
    "A+": 0.97, "A": 0.93, "A-": 0.89,
    "B+": 0.84, "B": 0.80, "B-": 0.76,
    "C+": 0.73, "C": 0.70, "C-": 0.67,
    "D+": 0.64, "D": 0.60
}

# دالة تحويل نقاط الـ GPA لتقدير وصفي (بناءً على المادة 16)
def get_delta_feedback(gpa_val):
    if gpa_val >= 4.0: return "A+ / A (ممتاز)", "🔥 AI Legend Status! Outstanding Work.", "#00ffcc"
    elif gpa_val >= 3.7: return "A- (ممتاز)", "🌟 Brilliant! You're dominating the AI track.", "#00d4ff"
    elif gpa_val >= 3.3: return "B+ (جيد جداً)", "👍 Very Good! Keep that momentum going.", "#ccff00"
    elif gpa_val >= 3.0: return "B (جيد جداً)", "📈 Good Effort! Success is on your horizon.", "#ffcc00"
    elif gpa_val >= 2.7: return "B- (جيد جداً)", "✨ Solid! You have more potential to show.", "#ff9100"
    elif gpa_val >= 2.3: return "C+ (جيد)", "🎯 You're on track, keep pushing for more.", "#ffcc00"
    elif gpa_val >= 2.0: return "C (جيد)", "📚 Stay focused, you can surely improve.", "#ffa500"
    elif gpa_val >= 1.7: return "C- (مقبول)", "⚠️ Caution! Need to tighten your study plan.", "#ff4b4b"
    elif gpa_val >= 1.3: return "D+ (مقبول)", "📉 Warning! Your GPA needs urgent care.", "#ff4b4b"
    elif gpa_val >= 1.0: return "D (مقبول)", "📉 Minimum Pass. Review your strategy!", "#ff4b4b"
    else: return "F / FF (رسوب/حرمان)", "💪 Resilience is key to success! Try again harder.", "#ff0000"

# ---------------------------------------------------------

if "courses" not in st.session_state:
    st.session_state.courses = []

st.title("🚀 MY ACADEMIC TRACKER")

tab1, tab2, tab3, tab4 = st.tabs(["📝 Setup Courses", "🎯 Target Analyzer", "📊 GPA Converter", "📉 Cumulative GPA"])

# --- الصفحة الأولى: تسجيل المادة ---
with tab1:
    st.subheader("Step 1: Build Your Course List")
    with st.form("setup_form", clear_on_submit=True):
        col_n, col_h = st.columns([2, 1])
        name = col_n.text_input("Course Name")
        hrs = col_h.number_input("Credit Hours", min_value=1, max_value=5, value=3)
        
        c1, c2, c3 = st.columns(3)
        m_max = c1.number_input("Midterm Max", value=20)
        cl_max = c2.number_input("Classwork Max", value=40)
        f_max = c3.number_input("Final Max", value=60)
        
        if st.form_submit_button("REGISTER COURSE"):
            if name:
                st.session_state.courses.append({
                    "name": name, "hrs": hrs, 
                    "total": m_max+cl_max+f_max, 
                    "f_m": f_max, "m_max": m_max, "cl_max": cl_max
                })
                st.success(f"Successfully Added: {name}")

# --- الصفحة الثانية: تارجت أناليزر (حساب الفاينال بناءً على لائحة الدلتا) ---
with tab2:
    st.subheader("Step 2: Analyze Final Exam Target")
    if not st.session_state.courses:
        st.warning("Please setup your courses first in the first tab.")
    else:
        sel = st.selectbox("Select Course to Analyze", [c['name'] for c in st.session_state.courses])
        cd = next(i for i in st.session_state.courses if i["name"] == sel)
        
        col_in1, col_in2 = st.columns(2)
        m_got = col_in1.number_input(f"Your Midterm Score (Max {cd['m_max']})", min_value=0.0, max_value=float(cd['m_max']))
        cl_got = col_in2.number_input(f"Your Classwork Score (Max {cd['cl_max']})", min_value=0.0, max_value=float(cd['cl_max']))
        
        target_g = st.selectbox("Your Goal Grade (Delta Scale)", list(DELTA_THRESHOLDS.keys()))
        
        # العملية الحسابية بناءً على النسبة المئوية للتقدير المختار
        needed = (DELTA_THRESHOLDS[target_g] * cd['total']) - (m_got + cl_got)
        
        if st.button("Analyze Target Now"):
            if needed > cd['f_m']: 
                st.error(f"Target too high! To get {target_g} you need {needed:.1f} marks, but Final is {cd['f_m']}.")
            elif needed <= 0: 
                st.success(f"Target already reached for {target_g}! Focus on perfection in the final.")
            else: 
                st.info(f"To get {target_g}, you need to score at least **{needed:.1f}** out of **{cd['f_m']}** in the Final Exam.")

# --- الصفحة الثالثة: محول الـ GPA ---
with tab3:
    st.subheader("Step 3: Instant Grade Converter")
    user_gpa = st.number_input("Type your Term GPA (0.0 - 4.0):", 0.0, 4.0, step=0.01)
    
    if st.button("Show My Standing"):
        grade_letter, msg, color = get_delta_feedback(user_gpa)
        st.markdown(f"""
            <div style="background: rgba(255,255,255,0.08); padding: 30px; border-radius: 20px; border-left: 12px solid {color};">
                <h1 style="color: {color} !important; margin: 0; font-size: 3.5rem;">{grade_letter}</h1>
                <h3 style="margin-top: 15px; font-weight: 400;">{msg}</h3>
            </div>
        """, unsafe_allow_html=True)

# --- الصفحة الرابعة: الـ CGPA التراكمي ---
with tab4:
    st.subheader("Step 4: Cumulative GPA Tracker")
    colA, colB = st.columns(2)
    old_cgpa = colA.number_input("Previous CGPA", format="%.2f", min_value=0.0, max_value=4.0)
    old_hrs = colB.number_input("Total Previous Credit Hours", min_value=0)
    cur_gpa_c = colA.number_input("Current Term GPA", format="%.2f", min_value=0.0, max_value=4.0)
    cur_hrs_c = colB.number_input("Current Term Credit Hours", min_value=0)
    
    if st.button("Calculate Final CGPA"):
        total_points = (old_cgpa * old_hrs) + (cur_gpa_c * cur_hrs_c)
        total_hours = old_hrs + cur_hrs_c
        final_cgpa = total_points / total_hours if total_hours > 0 else 0
        
        st.markdown(f"""
            <div style="background: rgba(255,255,255,0.1); padding: 30px; border-radius: 20px; text-align: center; border: 1px solid #5d3fd3;">
                <h3 style="margin: 0; opacity: 0.8;">Your Final Cumulative GPA:</h3>
                <h1 style="color: #ff007f !important; font-size: 4rem; margin: 10px 0;">{final_cgpa:.2f}</h1>
            </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="footer">MADE BY ENG HANAN DAHI | DELTA UNIVERSITY - FACULTY OF AI</div>', unsafe_allow_html=True)
