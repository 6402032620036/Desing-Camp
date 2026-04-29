import streamlit as st
import numpy as np
import math

# =========================
# 🎨 CSS UI
# =========================
st.markdown("""
<style>
body {
    background-color: #f4f6f9;
}
.block-container {
    padding: 2rem;
}
.card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
.metric {
    font-size: 20px;
    font-weight: bold;
    color: #2a9d8f;
}
</style>
""", unsafe_allow_html=True)

st.title("🏗️ Eccentric Pile Foundation (Terzaghi-Based)")

# =========================
# 📥 INPUT
# =========================
st.markdown('<div class="card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    P = st.number_input("Axial Load P (kN)", 0.0, value=2000.0)
    M = st.number_input("Moment M (kN·m)", 0.0, value=500.0)
    n = st.number_input("Number of piles", 1, value=4)

with col2:
    spacing = st.number_input("Pile spacing (m)", value=2.5)
    d = st.number_input("Pile diameter (m)", value=0.4)
    L = st.number_input("Pile length (m)", value=15.0)

st.markdown('</div>', unsafe_allow_html=True)

# Soil
st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("Soil Properties")

c = st.number_input("Cohesion c (kN/m²)", value=25.0)
phi = st.number_input("Friction angle φ (deg)", value=30.0)
gamma = st.number_input("Unit weight γ (kN/m³)", value=18.0)
FS = st.number_input("Factor of Safety", value=2.5)

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 🧠 Terzaghi Factors
# =========================
def bearing_factors(phi):
    phi_rad = math.radians(phi)

    if phi == 0:
        Nc = 5.7
        Nq = 1.0
        Ng = 0.0
    else:
        Nq = math.exp(math.pi * math.tan(phi_rad)) * (math.tan(math.radians(45 + phi/2))**2)
        Nc = (Nq - 1) / math.tan(phi_rad)
        Ng = 2 * (Nq + 1) * math.tan(phi_rad)

    return Nc, Nq, Ng

# =========================
# 🧮 CALCULATION
# =========================
if st.button("คำนวณ"):
    Nc, Nq, Ng = bearing_factors(phi)

    Ap = math.pi * d**2 / 4
    perimeter = math.pi * d

    # End bearing (Terzaghi concept)
    qp = c * Nc + gamma * L * Nq
    Qp = qp * Ap

    # Skin friction (simplified)
    fs = c  # conservative clay assumption
    Qs = fs * perimeter * L

    Qult_pile = Qp + Qs
    Qall_pile = Qult_pile / FS

    # =========================
    # Load distribution (eccentric)
    # =========================
    # assume square grid
    side = int(np.ceil(np.sqrt(n)))
    coords = []

    for i in range(side):
        for j in range(side):
            if len(coords) < n:
                x = (i - side/2) * spacing
                y = (j - side/2) * spacing
                coords.append((x, y))

    coords = np.array(coords)
    y_coords = coords[:, 1]

    I = np.sum(y_coords**2)

    pile_loads = []

    for y in y_coords:
        Pi = (P / n) + (M * y / I if I != 0 else 0)
        pile_loads.append(Pi)

    pile_loads = np.array(pile_loads)

    # =========================
    # 📊 OUTPUT
    # =========================
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📊 Capacity per pile")
    st.markdown(f"<div class='metric'>Qult = {Qult_pile:.2f} kN</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric'>Qall = {Qall_pile:.2f} kN</div>", unsafe_allow_html=True)

    st.write("---")

    st.subheader("📊 Load Distribution")
    for i, load in enumerate(pile_loads):
        status = "OK" if load <= Qall_pile else "OVERLOAD"
        st.write(f"Pile {i+1}: {load:.2f} kN → {status}")

    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.write("---")
st.caption("Geotechnical Tool | Terzaghi + Pile Group Approximation")
