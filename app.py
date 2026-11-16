import streamlit as st
from google import genai
from PIL import Image

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="AI.RINA | Smart APA Citation Engine", page_icon="📚", layout="centered")

st.title("📚 AI.RINA: Smart APA Citation Engine")
st.markdown("*Inovasi Pintar Pengurusan Rujukan PhD oleh Dr SS*")
st.write("Muat naik gambar *screenshot*, fail PDF, atau masukkan teks maklumat rujukan. AI akan terus menjana format rujukan **APA 7th Edition** dengan pantas dan tepat.")

# Masukkan API key secara selamat menggunakan Streamlit Secrets
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = ""

# Pilihan mod input
input_type = st.radio("Pilih jenis input rujukan:", ["Muat Naik Gambar / Screenshot", "Teks / Petikan Mentah"])

uploaded_file = None
raw_text = ""

if input_type == "Muat Naik Gambar / Screenshot":
    uploaded_file = st.file_uploader("Pilih fail gambar (PNG, JPG, JPEG):", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Gambar sumber rujukan", use_container_width=True)
else:
    raw_text = st.text_area("Tampal maklumat rujukan mentah / abstrak / tajuk artikel di sini:")

# Butang proses
if st.button("Jana Rujukan APA"):
    if not API_KEY:
        st.error("API Key belum disetkan di dalam tetapan sistem. Sila hubungi pentadbir.")
    elif input_type == "Muat Naik Gambar / Screenshot" and not uploaded_file:
        st.warning("Sila muat naik gambar terlebih dahulu!")
    elif input_type == "Teks / Petikan Mentah" and not raw_text.strip():
        st.warning("Sila masukkan teks rujukan terlebih dahulu!")
    else:
        with st.spinner("Sedang memproses dan memformat mengikut APA 7..."):
            try:
                client = genai.Client(api_key=API_KEY)
                
                prompt_instruction = (
                    "Anda adalah pembantu akademik yang pakar dalam format APA 7th Edition. "
                    "Berdasarkan bahan yang diberikan (imej atau teks), ekstrak maklumat penting "
                    "dan hasilkan SATU rujukan lengkap mengikut format APA 7th Edition yang betul "
                    "(termasuk penggunaan huruf condong/italic pada tajuk jurnal/buku jika berkaitan). "
                    "Berikan HANYA teks rujukan akhir sahaja tanpa sebarang ayat pengantar."
                )
                
                if input_type == "Muat Naik Gambar / Screenshot" and uploaded_file:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=[image, prompt_instruction]
                    )
                else:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=[raw_text, prompt_instruction]
                    )
                
                st.success("Rujukan berjaya dijana!")
                st.markdown("### Hasil Rujukan (APA 7th Edition):")
                st.code(response.text, language="text")
                
            except Exception as e:
                st.error(f"Berlaku ralat: {e}")
