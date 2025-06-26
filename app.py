import streamlit as st
import requests

st.markdown("""
    <style>
    .stApp {
        background-color: #FFBF78; /* Main app background */
        color: #7B4019;
        font-family: 'Arial', sans-serif;
    }

    h1, h2, h3, .stMarkdown h1 {
        color: #FF7D29; /* Headers */
    }

    label, .stMarkdown p {
        color: #7B4019 !important; /* Label and paragraph text */
    }

    .stForm {
        background-color: #FFEEA9; /* Form background */
        padding: 20px;
        border-radius: 10px;
    }

    /* Umur label custom */
    label[for^="📅 Umur"] {
        color: #7B4019 !important;
        font-weight: bold;
    }

    /* Selectbox styling */
    div[data-baseweb="select"] > div {
        background-color: #FF7D29 !important; /* Selectbox background */
        color: white !important;
        border-radius: 5px !important;
    }

    /* Dropdown options */
    div[data-baseweb="popover"] {
        background-color: #FF7D29 !important; /* Dropdown options background */
        color: white !important;
    }

    /* Dropdown selected text */
    .css-1wa3eu0-placeholder {
        color: white !important;
    }

    /* Custom styling for primary button (the "Prediksi" button) */
    button[kind="primary"] {
        background-color: #5cb85c !important;  /* Green color */
        color: white !important; /* White text for the button */
        border: none !important;
        border-radius: 10px;
        font-weight: bold;
        padding: 0.6em 1.5em;
        transition: all 0.2s ease-in-out;
        /* Ensure the button takes full width of its container for centering */
        width: 100%;
    }

    /* Hover effect for the button */
    button[kind="primary"]:hover {
        background-color: #4cae4c !important; /* Darker green on hover */
        color: white !important;
    }

    /* Active (clicked) effect for the button */
    button[kind="primary"]:active {
        background-color: red !important; /* Red when clicked, as per your original CSS */
        color: white !important;
    }

    /* Styling for the success message (prediction result) */
    .stSuccess {
        background-color: #D4EDDA !important; /* Lighter green background for success */
        color: #155724 !important; /* Darker green text for success */
        border-radius: 5px;
        padding: 10px;
        border: 1px solid #C3E6CB !important; /* Slightly darker border */
    }

    /* Styling for the error message (if any) */
    .stError {
        background-color: #F8D7DA !important; /* Light red background for error */
        color: #721C24 !important; /* Darker red text for error */
        border-radius: 5px;
        padding: 10px;
        border: 1px solid #F5C6CB !important; /* Slightly darker border */
    }

    </style>
""", unsafe_allow_html=True)

# URL backend FastAPI
API_URL = "http://127.0.0.1:8000/predict"

st.title("Prediksi Obesitas 🍔🥓🍰")
st.write("Isi form di bawah untuk memprediksi kategori obesitas.")

# mapping display (Indonesia) → model value (English)
yn_map = {"Ya": "yes", "Tidak": "no"}
caec_map = {
    "Tidak Pernah": "no",
    "Kadang-kadang": "Sometimes",
    "Sering": "Frequently",
    "Selalu": "Always"
}
calc_map = caec_map
smoke_map = yn_map
scc_map = yn_map
favc_map = yn_map
fhwo_map = yn_map

mtrans_map = {
    "🚍 Transportasi Umum": "Public_Transportation",
    "🚶 Jalan Kaki": "Walking",
    "🚗 Mobil": "Automobile",
    "🏍️ Motor": "Motorbike",
    "🚴 Sepeda": "Bike"
}

with st.form("obesity_form"):
    # create two main columns for the top and bottom halves
    top_col1, top_col2 = st.columns(2)
    bottom_col1, bottom_col2 = st.columns(2)

    # top left: Profil & Riwayat
    with top_col1:
        st.subheader("Profil & Riwayat")
        Gender = st.selectbox("👤 Jenis Kelamin", ["Laki-laki", "Perempuan"])
        Age = st.slider("📅 Umur", min_value=10, max_value=80, step=1)
        Height = st.slider("📏 Tinggi badan (m)", min_value=1.0, max_value=2.0, step=0.01)
        Weight = st.slider("⚖️ Berat badan (kg)", min_value=20.0, max_value=180.0, step=0.1)
        family_history = st.selectbox("🧬 Ada riwayat obesitas di keluarga?", list(fhwo_map.keys()))

    # top right: Kebiasaan Makan & Minum
    with top_col2:
        st.subheader("Pola Makan & Minum")
        FAVC = st.selectbox("🍟 Sering konsumsi makanan tinggi kalori?", list(favc_map.keys()))
        FCVC = st.selectbox("🥦 Frekuensi makan sayur", ["Jarang", "Sedang", "Sering"])
        NCP = st.selectbox("🍽️ Frekuensi makan harian", ["Kurang", "Cukup", "Berlebih"])
        CAEC = st.selectbox("🍫 Sering ngemil di luar waktu makan?", list(caec_map.keys()))
        CH2O = st.selectbox("💧 Konsumsi air putih", ["Kurang", "Cukup", "Banyak"])

    # bottom left: Aktivitas Fisik & Lainnya
    with bottom_col1:
        st.subheader("Aktivitas Fisik & Lainnya")
        FAF = st.selectbox("🏃 Aktivitas fisik mingguan", ["Tidak Aktif", "Kurang Aktif", "Cukup Aktif", "Sangat Aktif"])
        TUE = st.selectbox("💻 Durasi penggunaan teknologi setiap hari", ["Tidak Pernah", "Jarang", "Sering"])
        MTRANS = st.selectbox("🚙 Moda transportasi utama", list(mtrans_map.keys()))

    # bottom right: Konsumsi & Kondisi Khusus
    with bottom_col2:
        st.subheader("Kondisi Khusus")
        SMOKE = st.selectbox("🚬 Merokok?", list(smoke_map.keys()))
        CALC = st.selectbox("🍺 Konsumsi alkohol", list(calc_map.keys()))
        SCC = st.selectbox("🏥 Apakah memantau asupan kalori perhari?", list(scc_map.keys()))

    button_col_left, button_col_center, button_col_right = st.columns([1.5, 1, 1.5]) # Adjusted ratios

    with button_col_center: 
        submitted = st.form_submit_button("🔍 Prediksi", type="primary") # Ensure it's a primary button

    if submitted:
        input_data = {
            "Gender": "Male" if Gender == "Laki-laki" else "Female",
            "Age": Age,
            "Height": Height,
            "Weight": Weight,
            "family_history_with_overweight": fhwo_map[family_history],
            "FAVC": favc_map[FAVC],
            "FCVC": FCVC,
            "NCP": NCP,
            "CAEC": caec_map[CAEC],
            "SMOKE": smoke_map[SMOKE],
            "CH2O": CH2O,
            "SCC": scc_map[SCC],
            "FAF": FAF,
            "TUE": TUE,
            "CALC": calc_map[CALC],
            "MTRANS": mtrans_map[MTRANS]
        }

        try:
            response = requests.post(API_URL, json=input_data)
            if response.status_code == 200:
                result = response.json()
                st.success(f"✅ Hasil Prediksi: **{result['prediction']}**")
            else:
                st.error(f"❌ Gagal mendapatkan hasil. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan: {e}")