import streamlit as st
import requests
from PIL import Image
import io

API_URL = "http://localhost:8000/predict/"

st.title("Rock-Paper-Scissors Classifier")
st.write("Anda bisa upload gambar atau pakai kamera untuk klasifikasi")

# Pilihan input: kamera atau file upload
input_method = st.radio("Pilih sumber input:", ("Upload Gambar", "Kamera"))

img = None
if input_method == "Upload Gambar":
    uploaded = st.file_uploader("Pilih file gambar", type=["jpg","png","jpeg"])
    if uploaded:
        img = Image.open(uploaded)
elif input_method == "Kamera":
    camera_img = st.camera_input("Ambil foto dengan kamera")
    if camera_img:
        img = Image.open(camera_img)

# Jika ada gambar, tampilkan & tombol Predict
if img:
    st.image(img, caption="Input image", use_container_width=True)
    if st.button("Predict"):
        with st.spinner("Memproses..."):
            # Siapkan file untuk dikirim ke backend
            buf = io.BytesIO()
            img.save(buf, format="JPEG")
            buf.seek(0)
            files = {"file": buf.getvalue()}
            
            try:
                response = requests.post(API_URL, files={"file": ("image.jpg", buf.getvalue(), "image/jpeg")})
                if response.ok:
                    data = response.json()
                    
                    # Tampilkan hasil prediksi dengan formatting yang baik
                    st.success(f"Prediksi: **{data['label'].upper()}** ({data['confidence']*100:.1f}%)")
                    
                    # Tambahkan informasi visual sesuai hasil
                    if data['label'] == "rock":
                        st.write("🪨 Rock detected!")
                    elif data['label'] == "paper":
                        st.write("📄 Paper detected!")
                    elif data['label'] == "scissors":
                        st.write("✂️ Scissors detected!")
                    elif data['label'] == "unknown":
                        st.warning("Confidence too low. Please try again with a clearer image.")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Connection error: {str(e)}")
                st.info("Make sure the FastAPI backend is running at " + API_URL)
