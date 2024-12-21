import numpy as np
import tensorflow as tf
from pathlib import Path
import streamlit as st
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

image_base64 = get_base64_image("src/static/background/background.jpg")

background_css = f"""
<style>
body {{
    background-image: url('data:image/jpg;base64,{image_base64}');
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
</style>
"""
st.markdown(background_css, unsafe_allow_html=True)

# Judul aplikasi
st.markdown(    """
    <div style="text-align: center; margin-bottom: 20px; font-size: 40px">
        Klasifikasi Citra Rambu Lalu Lintas
    </div>
    """,
    unsafe_allow_html=True
)

# Tambahkan CSS untuk latar belakang

st.markdown(
    """
    <div style="text-align: justify; margin-bottom: 20px;">
            Rambu lalu lintas merupakan elemen penting dalam sistem transportasi jalan raya yang berfungsi memberikan informasi, peringatan, larangan, atau petunjuk kepada pengguna jalan. 
        Rambu ini berperan menciptakan keteraturan, meningkatkan keselamatan, dan mengurangi risiko kecelakaan di jalan raya.
    </div>

    <div style="text-align: justify; margin-bottom: 20px;">
            Sebagaimana diatur dalam Pasal 28 Ayat (1) Undang-Undang Nomor 22 Tahun 2009 tentang Lalu Lintas dan Angkutan Jalan, yang berbunyi:  
        “Setiap jalan yang digunakan untuk lalu lintas umum wajib dilengkapi dengan perlengkapan jalan berupa rambu lalu lintas, marka jalan, alat pemberi isyarat lalu lintas, alat pengendali dan pengaman pengguna jalan, serta fasilitas pendukung lainnya.”
    </div>

    <div style="text-align: justify; margin-bottom: 20px;">
            Oleh karena itu, aplikasi ini dibuat untuk membantu masyarakat memahami arti dan fungsi rambu lalu lintas secara lebih mudah dan interaktif.  
        Silakan unggah gambar rambu, pilih model yang tersedia, dan tekan tombol Predict untuk mendapatkan hasil prediksi.
    </div>
    """,
    unsafe_allow_html=True
)

# Fungsi prediksi
def predict(uploaded_image, model_path):
    # Daftar kelas
    class_names = [
        "lampu-hijau",
        "lampu-kuning",
        "lampu-merah",
        "larangan-belok-kanan",
        "larangan-belok-kiri",
        "larangan-berhenti",
        "larangan-berjalan-terus-wajib-berhenti-sesaat",
        "larangan-masuk-bagi-kendaraan-bermotor-dan-tidak-bermotor",
        "larangan-memutar-balik",
        "larangan-parkir",
        "peringatan-alat-pemberi-isyarat-lalu-lintas",
        "peringatan-banyak-pejalan-kaki-menggunakan-zebra-cross",
        "peringatan-penegasan-rambu-tambahan",
        "peringatan-pintu-perlintasan-kereta-api",
        "peringatan-simpang-tiga-sisi-kiri",
        "perintah-masuk-jalur-kiri",
        "perintah-pilihan-memasuki-salah-satu-jalur",
        "petunjuk-area-parkir",
        "petunjuk-lokasi-pemberhentian-bus",
        "petunjuk-lokasi-putar-balik",
        "petunjuk-penyeberangan-pejalan-kaki"
    ]

    class_descriptions = [
    "Lampu hijau menunjukkan bahwa kendaraan diperbolehkan melanjutkan perjalanan. Pengemudi harus memastikan tidak ada hambatan di depan sebelum melintas, dan tetap berhati-hati terhadap kemungkinan perubahan sinyal lalu lintas.",
    "Lampu kuning mengindikasikan bahwa pengemudi harus bersiap untuk berhenti. Jika kendaraan terlalu dekat dengan lampu untuk berhenti secara aman, pengemudi diperbolehkan melanjutkan perjalanan dengan kecepatan yang terkendali. Lampu ini berfungsi sebagai peringatan transisi dari hijau ke merah.",
    "Lampu merah menginstruksikan semua kendaraan untuk berhenti sepenuhnya sebelum garis berhenti. Pengemudi harus menunggu hingga lampu berubah menjadi hijau sebelum melanjutkan perjalanan. Lampu ini bertujuan untuk mengatur lalu lintas di persimpangan agar tetap aman.",
    "Rambu ini melarang kendaraan untuk berbelok ke arah kanan. Larangan ini biasanya diterapkan untuk mencegah kemacetan atau risiko kecelakaan di area yang memiliki lalu lintas padat atau jalur yang sempit.",
    "Rambu ini melarang kendaraan untuk berbelok ke arah kiri. Rambu ini sering ditempatkan di area yang membutuhkan alur lalu lintas tertentu untuk menghindari konflik antar kendaraan.",
    "Rambu larangan berhenti menginformasikan bahwa kendaraan tidak diperbolehkan berhenti di sepanjang jalan tersebut. Hal ini bertujuan untuk menjaga kelancaran lalu lintas dan mencegah gangguan di area tertentu.",
    "Rambu ini mewajibkan kendaraan untuk berhenti sesaat di tempat yang ditentukan sebelum melanjutkan perjalanan. Tujuannya adalah untuk memastikan bahwa pengemudi memeriksa kondisi jalan dan mengutamakan kendaraan atau pejalan kaki yang lain.",
    "Rambu ini melarang semua jenis kendaraan, baik bermotor maupun tidak bermotor, untuk memasuki area tertentu. Larangan ini biasanya diterapkan di zona khusus seperti area pejalan kaki atau zona tertutup.",
    "Rambu larangan memutar balik menunjukkan bahwa kendaraan tidak diperbolehkan untuk melakukan manuver putar balik di lokasi tersebut. Rambu ini diterapkan untuk mengurangi risiko kecelakaan dan memastikan kelancaran arus lalu lintas.",
    "Rambu larangan parkir menunjukkan bahwa kendaraan tidak boleh diparkir di area tersebut. Rambu ini biasanya dipasang di area sempit atau area yang membutuhkan kelancaran lalu lintas tanpa hambatan.",
    "Rambu ini memberikan peringatan bahwa terdapat alat pemberi isyarat lalu lintas, seperti lampu lalu lintas, di depan. Pengemudi diharapkan untuk memperhatikan sinyal tersebut dan mengikuti aturan yang berlaku.",
    "Rambu ini memperingatkan bahwa terdapat banyak pejalan kaki yang melintas menggunakan zebra cross. Pengemudi harus mengurangi kecepatan dan memprioritaskan pejalan kaki yang sedang menyeberang.",
    "Rambu ini merupakan penegasan tambahan yang memberikan informasi lebih lanjut mengenai situasi lalu lintas di area tertentu. Penegasan ini bertujuan untuk membantu pengemudi membuat keputusan yang lebih aman.",
    "Rambu ini memperingatkan adanya pintu perlintasan kereta api di depan. Pengemudi harus berhenti ketika sinyal perlintasan aktif dan memastikan tidak ada kereta yang melintas sebelum melanjutkan perjalanan.",
    "Rambu ini memperingatkan adanya simpang tiga dengan cabang di sisi kiri. Pengemudi harus berhati-hati dan mengurangi kecepatan, terutama jika terdapat kendaraan lain yang akan bergabung dari cabang tersebut.",
    "Rambu ini mewajibkan kendaraan untuk masuk ke jalur kiri. Biasanya digunakan untuk mengatur lalu lintas agar lebih terorganisir, terutama di jalan yang memiliki volume kendaraan tinggi.",
    "Rambu ini memberikan perintah kepada pengemudi untuk memilih salah satu jalur yang tersedia. Hal ini bertujuan untuk menghindari kebingungan di area dengan persimpangan kompleks atau jalur bercabang.",
    "Rambu ini menunjukkan lokasi area parkir yang tersedia di depan. Pengemudi dapat menggunakan fasilitas ini untuk memarkir kendaraan dengan aman dan tertib.",
    "Rambu ini menunjukkan lokasi pemberhentian bus di depan. Lokasi ini dirancang khusus untuk penumpang yang naik atau turun dari bus, sehingga pengemudi kendaraan lain harus berhati-hati.",
    "Rambu ini menunjukkan lokasi yang aman untuk kendaraan melakukan putar balik. Biasanya ditempatkan di area dengan visibilitas yang baik dan arus lalu lintas yang terkendali.",
    "Rambu ini memberikan petunjuk tentang lokasi untuk penyeberangan pejalan kaki. Pengemudi harus memprioritaskan keselamatan pejalan kaki yang menggunakan area ini untuk menyeberang."
]


    # Muat dan preprocess citra
    img = tf.keras.utils.load_img(uploaded_image, target_size=(224, 224))  # Pastikan ukuran sesuai dengan model
    img = tf.keras.utils.img_to_array(img) / 255.0  # Normalisasi
    img = np.expand_dims(img, axis=0)  # Tambahkan dimensi batch

    # Muat model
    model = tf.keras.models.load_model(model_path)

    # Prediksi
    output = model.predict(img)
    score = tf.nn.softmax(output[0])  # Hitung probabilitas
    return class_names[np.argmax(score)], class_descriptions[np.argmax(score)], 100 * np.max(score)  # Prediksi label dan confidence

# Pilihan model
model_option = st.selectbox("Pilih model untuk prediksi:", ("InceptionV3", "MobileNetV2"))

# Tentukan path model berdasarkan pilihan
if model_option == "InceptionV3":
    model_path = Path(__file__).parent / "Model/Image/InceptionV3/model.h5"
else:
    model_path = Path(__file__).parent / "Model/Image/MobileNetV2/model.h5"

# Komponen file uploader untuk banyak file
uploads = st.file_uploader("Unggah citra untuk mendapatkan hasil prediksi", type=["png", "jpg"], accept_multiple_files=True)

# Tombol prediksi
if st.button("Predict", type="primary"):
    if uploads:
        st.subheader("Hasil prediksi:")

        for upload in uploads:
            # Tampilkan setiap citra yang diunggah
            st.image(upload, caption=f"Citra yang diunggah: {upload.name}", use_container_width=True)

            with st.spinner(f"Memproses citra {upload.name} untuk prediksi..."):
                # Panggil fungsi prediksi
                try:
                    label, label_description, confidence = predict(upload, model_path)
                    st.write(f"Image: **{upload.name}**")
                    st.write(f"Label : **{label}**")
                    st.write(f"Confidence: **{confidence:.5f}%**")
                    st.write(f"Keterangan Rambu: **{label_description}**")
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat memproses {upload.name}: {e}")
    else:
        st.error("Unggah setidaknya satu citra terlebih dahulu!")
