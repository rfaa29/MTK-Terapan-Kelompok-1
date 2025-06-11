import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

# Sidebar
st.sidebar.title("Instruksi")
st.sidebar.markdown("Pilih salah satu model dari tab di atas untuk melakukan simulasi perhitungan dan melihat grafik visualisasi.")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Optimasi Produksi", "Model Persediaan (EOQ)", "Model Antrian (M/M/1)", "Model Matematika Lain"])

# 1. Optimasi Produksi (Linear Programming)
with tab1:
    st.header("Optimasi Produksi (Linear Programming)")
    st.markdown("Model sederhana untuk maksimisasi keuntungan")
    
    c = [-40, -30]  # keuntungan per unit produk A dan B
    A = [[1, 1], [2, 1]]  # batasan: waktu mesin 1 dan 2
    b = [40, 60]  # total waktu tersedia

    res = linprog(c, A_ub=A, b_ub=b, method='highs')
    
    if res.success:
        st.success(f"Produksi optimal: Produk A = {res.x[0]:.2f}, Produk B = {res.x[1]:.2f}, Total Profit = {-res.fun:.2f}")

        fig, ax = plt.subplots()
        ax.bar(['Produk A', 'Produk B'], res.x)
        st.pyplot(fig)
    else:
        st.error("Optimisasi gagal.")

# 2. Model Persediaan (EOQ)
with tab2:
    st.header("Model Persediaan (EOQ)")
    D = st.number_input("Permintaan Tahunan (D)", value=1000)
    S = st.number_input("Biaya Pemesanan (S)", value=50)
    H = st.number_input("Biaya Penyimpanan per unit per tahun (H)", value=2)

    EOQ = np.sqrt((2 * D * S) / H)
    st.success(f"Economic Order Quantity (EOQ): {EOQ:.2f} unit")

    fig, ax = plt.subplots()
    q = np.linspace(1, 2 * EOQ, 100)
    TC = (D / q) * S + (q / 2) * H
    ax.plot(q, TC)
    ax.set_title("Total Cost vs Order Quantity")
    ax.set_xlabel("Order Quantity")
    ax.set_ylabel("Total Cost")
    st.pyplot(fig)

# 3. Model Antrian (M/M/1)
with tab3:
    st.header("Model Antrian (M/M/1)")
    λ = st.number_input("Rata-rata kedatangan (λ)", value=2.0)
    μ = st.number_input("Rata-rata pelayanan (μ)", value=4.0)

    if λ < μ:
        ρ = λ / μ
        L = ρ / (1 - ρ)
        W = 1 / (μ - λ)
        st.success(f"Rho (utilisasi): {ρ:.2f}\nJumlah rata-rata pelanggan (L): {L:.2f}\nWaktu rata-rata dalam sistem (W): {W:.2f} jam")

        fig, ax = plt.subplots()
        ax.bar(['Utilisasi (ρ)', 'L', 'W'], [ρ, L, W])
        st.pyplot(fig)
    else:
        st.error("Model tidak valid: λ harus lebih kecil dari μ")

# 4. Model Matematika Lainnya: Break-even Analysis
with tab4:
    st.header("Break-even Analysis")
    FC = st.number_input("Fixed Cost (FC)", value=10000)
    VC = st.number_input("Variable Cost per unit (VC)", value=20)
    P = st.number_input("Harga Jual per unit (P)", value=50)

    if P > VC:
        BEQ = FC / (P - VC)
        st.success(f"Break-even Quantity: {BEQ:.2f} unit")

        q = np.linspace(0, 2 * BEQ, 100)
        total_cost = FC + VC * q
        revenue = P * q

        fig, ax = plt.subplots()
        ax.plot(q, total_cost, label='Total Cost')
        ax.plot(q, revenue, label='Revenue')
        ax.axvline(BEQ, color='gray', linestyle='--', label='Break-even Point')
        ax.legend()
        st.pyplot(fig)
    else:
        st.error("Harga jual harus lebih besar dari biaya variabel.")
