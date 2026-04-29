import streamlit as st
import math

# =========================
# 🎨 Custom CSS
# =========================
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
.block-container {
    padding: 2rem;
}
h1 {
    color: #1f4e79;
}
.card {
    background-color: white;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
.metric {
    font-size: 22px;
    font-weight: bold;
    color: #0a9396;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 📘 Title
# =========================
st.title("🏗️ Terzaghi Bearing Capacity Calculator")
st.write("คำนวณกำลังรับน้ำหนักฐานรากตื้น (Shallow Foundation) ตามทฤษฎีของ Terzaghi")

# =========================
# 📥 Input Section
# =========================
st.markdown('<div class="card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    B = st.number_input("ความกว้างฐานราก B (m)", value=2.0)
    Df = st.number_input("ความลึกฐานราก Df (m)", value=1.5)
    gamma = st.number_input("หน่วยน้ำหนักดิน γ (kN/m³)", value=18.0)

with col2:
    c = st.number_input("Cohesion c (kN/m²)", value=25.0)
    phi = st.number_input("มุมเสียดทาน φ (deg)", value=30.0)
    FS = st.number_input("Factor of Safety", value=3.0)

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 🧠 Terzaghi Factors
# =========================
def bearing_capacity_factors(phi):
    phi_rad = math.radians(phi)

    if phi == 0:
        Nc = 5.7
        Nq = 1.0
        Ngamma = 0.0
    else:
        Nq = math.exp(math.pi * math.tan(phi_rad)) * (math.tan(math.radians(45 + phi/2))**2)
        Nc = (Nq - 1) / math.tan(phi_rad)
        Ngamma = 2 * (Nq + 1) * math.tan(phi_rad)

    return Nc, Nq, Ngamma

# =========================
# 🧮 Calculation
# =========================
if st.button("คำนวณ"):
    Nc, Nq, Ngamma = bearing_capacity_factors(phi)

    q = gamma * Df

    qult = (c * Nc) + (q * Nq) + (0.5 * gamma * B * Ngamma)
    qall = qult / FS

    # =========================
    # 📊 Output
    # =========================
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📊 Results")

    st.markdown(f"<div class='metric'>Ultimate Bearing Capacity (qult): {qult:.2f} kN/m²</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric'>Allowable Bearing Capacity (qall): {qall:.2f} kN/m²</div>", unsafe_allow_html=True)

    st.write("---")

    st.write("### Bearing Capacity Factors")
    st.write(f"Nc = {Nc:.2f}")
    st.write(f"Nq = {Nq:.2f}")
    st.write(f"Nγ = {Ngamma:.2f}")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# Footer
# =========================
st.write("---")
st.caption("Developed for Geotechnical Engineering | Terzaghi Theory")
