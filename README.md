# 📸 Foto Romantis

AI romantic photo editor — ubah foto jadi lebih romantis **tanpa mengubah wajah**.

## 🎯 Cara Pakai

### Opsi 1: Upload via Colab (Otomatis)

Jalankan script Colab → upload foto → otomatis push ke GitHub → Actions jalan.

### Opsi 2: Upload Langsung di GitHub

1. Buka folder `input/`
2. Klik **Add file → Upload files**
3. Upload foto kamu (.jpg / .png)
4. Commit → Actions jalan otomatis

## ⚙️ Setting

Edit `config.json` untuk atur:

| Field | Default | Keterangan |
|-------|---------|------------|
| `strength` | 0.20 | 0.15 = wajah sama persis, 0.35 = lebih romantis |
| `guidance_scale` | 7.5 | Seberapa "kuat" prompt diikuti |
| `num_inference_steps` | 30 | Lebih tinggi = lebih halus (lambat) |
| `max_size` | 768 | Resolusi max (jaga CPU memory) |
| `prompt` | ... | Deskripsi gaya romantis |
| `negative_prompt` | ... | Hal yang dihindari |

## 📥 Hasil

Setelah Actions selesai:
- **Artifacts**: tab Actions → run → Artifacts → download zip
- **Release**: tab Releases → download PNG langsung

## ⏱️ Waktu Proses

- 1 foto: **10-20 menit**
- 5 foto: **50-90 menit**

(CPU only — GitHub Actions gratis tidak ada GPU)

## 🎨 Tips

- **Wajah berubah?** Turunkan `strength` ke 0.15
- **Kurang romantis?** Naikkan ke 0.30-0.35
- **Warna aneh?** Tambah `oversaturated` ke negative_prompt
- **Background berantakan?** Tambah `cluttered background, messy` ke negative

## 🔒 Privacy

- Repo ini **PUBLIC** — foto kamu terlihat siapa saja
- Untuk privasi, fork & jadikan **PRIVATE**

## 📄 Lisensi

Personal use only.
