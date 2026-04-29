def eccentric_footing(P, B, L, e, q_allow):
    """
    P = แรงกด (kN)
    B = ความกว้างฐานราก (m)
    L = ความยาวฐานราก (m)
    e = ระยะเยื้องศูนย์ (m)
    q_allow = กำลังรับน้ำหนักดิน (kN/m^2)
    """

    # พื้นที่
    A = B * L

    # โมเมนต์
    M = P * e

    # ความเค้น
    sigma_max = (P / A) + (6 * M / (B * L**2))
    sigma_min = (P / A) - (6 * M / (B * L**2))

    # เช็คเงื่อนไข
    no_tension = sigma_min >= 0
    safe_bearing = sigma_max <= q_allow
    eccentric_limit = e <= (B / 6)

    # สรุปผล
    result = {
        "Area (m^2)": A,
        "Moment (kN-m)": M,
        "Sigma max (kN/m^2)": sigma_max,
        "Sigma min (kN/m^2)": sigma_min,
        "No tension condition": no_tension,
        "Bearing capacity OK": safe_bearing,
        "Eccentricity OK (e <= B/6)": eccentric_limit
    }

    return result


# 🔹 ตัวอย่างใช้งาน
if __name__ == "__main__":
    P = 1000      # kN
    B = 2.0       # m
    L = 3.0       # m
    e = 0.3       # m
    q_allow = 200 # kN/m^2

    result = eccentric_footing(P, B, L, e, q_allow)

    for k, v in result.items():
        print(f"{k}: {v}")
