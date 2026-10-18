"""
Projek Statistika dan Probabilitas - Kelompok 7 (3TIE)
Analisis Kadar Alkohol dan Keasaman Volatil terhadap Kualitas Anggur Merah
Tahap 3: statistika deskriptif, probabilitas empiris, dan visualisasi data
"""
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

FILE = "3TIE_07_WineQuality-Red.xlsx"
OUT = "gambar/"
os.makedirs(OUT, exist_ok=True)
sns.set_theme(style="whitegrid")
pd.set_option("display.width", 100)

# 1. Membaca data dan pemeriksaan awal
df = pd.read_excel(FILE, sheet_name="Dataset")
n = len(df)
print("=== PEMERIKSAAN DATA ===")
print("Dimensi data  :", df.shape)
print("Nilai kosong  :", df.isna().sum().sum())
print("Baris duplikat:", df.duplicated().sum())
print(df.dtypes, "\n")

# 2. Statistika deskriptif variabel utama
VARS = ["alcohol", "volatile acidity", "quality"]
rows = []
for v in VARS:
    s = df[v]
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    rows.append({
        "Variabel": v, "N": s.count(), "Mean": s.mean(),
        "Median": s.median(), "Modus": s.mode().iloc[0],
        "Min": s.min(), "Max": s.max(), "Rentang": s.max() - s.min(),
        "Std (sampel)": s.std(), "Varians": s.var(),
        "Q1": q1, "Q3": q3, "IQR": q3 - q1, "Skewness": s.skew(),
    })
desk = pd.DataFrame(rows).round(3)
print("=== STATISTIKA DESKRIPTIF ===")
print(desk.set_index("Variabel").T, "\n")
desk.to_csv(OUT + "statistik_deskriptif.csv", index=False)

# 3. Distribusi frekuensi skor quality
frek = df["quality"].value_counts().sort_index().to_frame("Frekuensi")
frek["Proporsi"] = (frek["Frekuensi"] / n).round(4)
frek["Persentase (%)"] = (frek["Proporsi"] * 100).round(2)
print("=== DISTRIBUSI FREKUENSI QUALITY ===")
print(frek, "\n")
frek.to_csv(OUT + "frekuensi_quality.csv")

# 4. Probabilitas empiris
prob = {
    "P(quality >= 7)": (df["quality"] >= 7).sum() / n,
    "P(quality = 6)": (df["quality"] == 6).sum() / n,
    "P(quality <= 5)": (df["quality"] <= 5).sum() / n,
    "P(quality >= 6)": (df["quality"] >= 6).sum() / n,
}
print("=== PROBABILITAS EMPIRIS ===")
for k, v in prob.items():
    print(f"{k} = {v:.4f} ({v * 100:.2f}%)")

# 5. Visualisasi
for v, warna, label in [
    ("alcohol", "#8B1A3A", "Kadar Alkohol (% vol)"),
    ("volatile acidity", "#D98C2B", "Keasaman Volatil (g/dm³)"),
]:
    fig, ax = plt.subplots(figsize=(6.5, 4))
    sns.histplot(df[v], bins=25, kde=True, color=warna, ax=ax)
    ax.axvline(df[v].mean(), color="black", ls="--",
               label=f"Mean = {df[v].mean():.2f}")
    ax.axvline(df[v].median(), color="blue", ls=":",
               label=f"Median = {df[v].median():.2f}")
    ax.set(title=f"Histogram {label}", xlabel=label, ylabel="Frekuensi")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT + f"hist_{v.replace(' ', '_')}.png", dpi=200)
    plt.close(fig)

fig, ax = plt.subplots(figsize=(6.5, 4))
sns.barplot(x=frek.index, y=frek["Frekuensi"], color="#6B2D5C", ax=ax)
for i, f in enumerate(frek["Frekuensi"]):
    ax.text(i, f + 8, str(f), ha="center")
ax.set(title="Distribusi Skor Kualitas Anggur",
       xlabel="Skor quality", ylabel="Frekuensi")
fig.tight_layout()
fig.savefig(OUT + "bar_quality.png", dpi=200)
plt.close(fig)

fig, axes = plt.subplots(1, 2, figsize=(11, 4))
sns.boxplot(data=df, x="quality", y="alcohol", color="#C9A0B4", ax=axes[0])
axes[0].set(title="Kadar Alkohol menurut Skor Quality",
            xlabel="Skor quality", ylabel="Alkohol (% vol)")
sns.boxplot(data=df, x="quality", y="volatile acidity",
            color="#F0C987", ax=axes[1])
axes[1].set(title="Keasaman Volatil menurut Skor Quality",
            xlabel="Skor quality", ylabel="Keasaman volatil (g/dm³)")
fig.tight_layout()
fig.savefig(OUT + "boxplot_per_quality.png", dpi=200)
plt.close(fig)

# 6. Mean dan median per skor quality
grp = df.groupby("quality")[["alcohol", "volatile acidity"]]
rata, median_q = grp.mean().round(3), grp.median().round(3)
print("\n=== MEAN PER SKOR QUALITY ===")
print(rata)
print("\n=== MEDIAN PER SKOR QUALITY ===")
print(median_q)
rata.to_csv(OUT + "rata_per_quality.csv")

# 7. Pencilan (aturan 1,5 x IQR)
pencilan = {}
print("\n=== PENCILAN (1,5 x IQR) ===")
for v in ["alcohol", "volatile acidity"]:
    q1, q3 = df[v].quantile([0.25, 0.75])
    bb, ba = q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1)
    jml = int(((df[v] < bb) | (df[v] > ba)).sum())
    pencilan[v] = {"batas_bawah": round(bb, 3), "batas_atas": round(ba, 3),
                   "jumlah": jml, "persen": round(jml / n * 100, 2)}
    print(f"{v}: batas {bb:.3f} - {ba:.3f}, pencilan = {jml}")

# 8. Distribusi frekuensi berkelompok (acuan jumlah kelas: Sturges)
sturges = 1 + 3.322 * np.log10(n)
print(f"\nJumlah kelas Sturges: {sturges:.2f}")


def berkelompok(v, awal, lebar, n_kelas):
    batas = np.round(awal + lebar * np.arange(n_kelas + 1), 2)
    c = pd.cut(df[v], batas, right=False).value_counts().sort_index()
    return [[f"{a:.2f} - < {b:.2f}", int(f), round(f / n * 100, 2)]
            for a, b, f in zip(batas[:-1], batas[1:], c.values)]


kel_alk = berkelompok("alcohol", 8.4, 0.6, 11)
kel_va = berkelompok("volatile acidity", 0.12, 0.12, 13)

# 9. Ringkasan seluruh variabel
semua = df.describe().T[["mean", "50%", "std", "min", "max"]].round(3)
semua["skewness"] = df.skew().round(3)

# 10. Simpan hasil untuk penyusunan laporan
p_alk = ((df.alcohol >= 9) & (df.alcohol <= 11)).mean() * 100
p_va = ((df["volatile acidity"] >= 0.4)
        & (df["volatile acidity"] <= 0.7)).mean() * 100
hasil = {
    "n": n, "duplikat": int(df.duplicated().sum()),
    "kosong": int(df.isna().sum().sum()),
    "desk": desk.to_dict("records"),
    "frek": frek.reset_index().to_dict("records"),
    "prob": {k: [int(round(v * n)), v] for k, v in prob.items()},
    "rata": rata.reset_index().to_dict("records"),
    "median_q": median_q.reset_index().to_dict("records"),
    "pencilan": pencilan, "kel_alk": kel_alk, "kel_va": kel_va,
    "sturges": round(sturges, 2),
    "semua": semua.reset_index().rename(
        columns={"index": "variabel"}).to_dict("records"),
    "p_alk_9_11": round(p_alk, 1), "p_va_04_07": round(p_va, 1),
}
with open(OUT + "hasil_analisis.json", "w", encoding="utf-8") as fp:
    json.dump(hasil, fp, ensure_ascii=False, indent=1)
print("\nSelesai. Gambar dan tabel tersimpan di folder", OUT)
