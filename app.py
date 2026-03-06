"""
Kalkulator GUI & Konversi Suhu
==============================
Aplikasi kalkulator lengkap dengan antarmuka modern menggunakan Tkinter.
Fitur:
    - Kalkulator standar (penjumlahan, pengurangan, perkalian, pembagian,
    persen, tanda kurung, desimal, pangkat)
    - Konversi suhu (Celsius, Fahrenheit, Kelvin, Reamur)
    - Dukungan keyboard penuh
"""

import tkinter as tk
from tkinter import ttk
import math

# ═══════════════════════════════════════════════════════════
#  WARNA & TEMA
# ═══════════════════════════════════════════════════════════

WARNA = {
    "bg_utama": "#1e1e2e",
    "bg_layar": "#181825",
    "teks_utama": "#cdd6f4",
    "teks_redup": "#6c7086",
    "teks_hasil": "#a6e3a1",
    "tombol_angka": "#313244",
    "tombol_angka_hover": "#45475a",
    "tombol_operator": "#585b70",
    "tombol_operator_hover": "#6c7086",
    "tombol_sama_dengan": "#a6e3a1",
    "tombol_sama_dengan_hover": "#94e2d5",
    "teks_sama_dengan": "#1e1e2e",
    "tombol_hapus": "#f38ba8",
    "tombol_hapus_hover": "#eba0ac",
    "teks_hapus": "#1e1e2e",
    "tombol_fungsi": "#fab387",
    "tombol_fungsi_hover": "#f9e2af",
    "teks_fungsi": "#1e1e2e",
    "aksen": "#cba6f7",
    "bg_tab": "#11111b",
    "border": "#45475a",
}

FONT_LAYAR_BESAR = ("Segoe UI", 32, "bold")
FONT_LAYAR_KECIL = ("Segoe UI", 14)
FONT_TOMBOL = ("Segoe UI", 16, "bold")
FONT_TOMBOL_KECIL = ("Segoe UI", 13)
FONT_LABEL = ("Segoe UI", 12)
FONT_JUDUL = ("Segoe UI", 11, "bold")


# ═══════════════════════════════════════════════════════════
#  KELAS TOMBOL KUSTOM
# ═══════════════════════════════════════════════════════════


class TombolKustom(tk.Canvas):
    """Tombol kustom dengan efek hover dan sudut membulat."""

    def __init__(
        self,
        parent,
        teks,
        warna_bg,
        warna_hover,
        warna_teks="#cdd6f4",
        font=FONT_TOMBOL,
        lebar=70,
        tinggi=55,
        command=None,
        radius=12,
    ):
        super().__init__(
            parent,
            width=lebar,
            height=tinggi,
            bg=(
                parent["bg"]
                if isinstance(parent, (tk.Frame, tk.Canvas))
                else WARNA["bg_utama"]
            ),
            highlightthickness=0,
            bd=0,
        )

        self.teks = teks
        self.warna_bg = warna_bg
        self.warna_hover = warna_hover
        self.warna_teks = warna_teks
        self.font = font
        self.lebar = lebar
        self.tinggi = tinggi
        self.command = command
        self.radius = radius
        self._aktif = False

        self._gambar(self.warna_bg)

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_tekan)
        self.bind("<ButtonRelease-1>", self._on_lepas)

    def _rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        """Gambar persegi panjang dengan sudut membulat."""
        points = [
            x1 + r,
            y1,
            x2 - r,
            y1,
            x2,
            y1,
            x2,
            y1 + r,
            x2,
            y2 - r,
            x2,
            y2,
            x2 - r,
            y2,
            x1 + r,
            y2,
            x1,
            y2,
            x1,
            y2 - r,
            x1,
            y1 + r,
            x1,
            y1,
            x1 + r,
            y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def _gambar(self, warna):
        self.delete("all")
        self._rounded_rect(
            2, 2, self.lebar - 2, self.tinggi - 2, self.radius, fill=warna, outline=""
        )
        self.create_text(
            self.lebar // 2,
            self.tinggi // 2,
            text=self.teks,
            fill=self.warna_teks,
            font=self.font,
        )

    def _on_enter(self, event):
        self._gambar(self.warna_hover)

    def _on_leave(self, event):
        self._aktif = False
        self._gambar(self.warna_bg)

    def _on_tekan(self, event):
        self._aktif = True
        self._gambar(self.warna_bg)

    def _on_lepas(self, event):
        if self._aktif and self.command:
            self.command()
        self._aktif = False
        self._gambar(self.warna_hover)


# ═══════════════════════════════════════════════════════════
#  KELAS UTAMA APLIKASI
# ═══════════════════════════════════════════════════════════


class AplikasiKalkulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulator & Konversi Suhu")
        self.root.geometry("400x700")
        self.root.resizable(False, False)
        self.root.configure(bg=WARNA["bg_utama"])

        try:
            self.root.iconbitmap(default="")
        except Exception:
            pass

        self.ekspresi = ""
        self.hasil_terakhir = ""
        self.baru_mulai = True
        self.riwayat = []  # list of (ekspresi, hasil) tuples

        # ── Setup Style ──
        self._setup_style()
        self.notebook = ttk.Notebook(self.root, style="Custom.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        self.tab_kalkulator = tk.Frame(self.notebook, bg=WARNA["bg_utama"])
        self.notebook.add(self.tab_kalkulator, text="  Kalkulator  ")
        self.tab_suhu = tk.Frame(self.notebook, bg=WARNA["bg_utama"])
        self.notebook.add(self.tab_suhu, text="  Konversi Suhu  ")

        # Tab Riwayat
        self.tab_riwayat = tk.Frame(self.notebook, bg=WARNA["bg_utama"])
        self.notebook.add(self.tab_riwayat, text="  Riwayat  ")

        # Bangun semua tab
        self._bangun_tab_kalkulator()
        self._bangun_tab_suhu()
        self._bangun_tab_riwayat()

        # Keyboard binding
        self.root.bind("<Key>", self._handle_keyboard)

    # ───────────────────────────────────────────────────────
    #  SETUP STYLE
    # ───────────────────────────────────────────────────────

    def _setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Custom.TNotebook",
            background=WARNA["bg_utama"],
            borderwidth=0,
            tabmargins=[0, 0, 0, 0],
        )
        style.configure(
            "Custom.TNotebook.Tab",
            background=WARNA["bg_tab"],
            foreground=WARNA["teks_redup"],
            padding=[12, 8],
            font=FONT_JUDUL,
            borderwidth=0,
        )
        style.map(
            "Custom.TNotebook.Tab",
            background=[("selected", WARNA["bg_utama"])],
            foreground=[("selected", WARNA["aksen"])],
            expand=[("selected", [0, 0, 0, 2])],
        )
        style.configure(
            "Custom.TCombobox",
            fieldbackground=WARNA["tombol_angka"],
            background=WARNA["tombol_operator"],
            foreground=WARNA["teks_utama"],
            arrowcolor=WARNA["teks_utama"],
            borderwidth=1,
            relief="flat",
        )
        style.map(
            "Custom.TCombobox",
            fieldbackground=[("readonly", WARNA["tombol_angka"])],
            foreground=[("readonly", WARNA["teks_utama"])],
        )

    # ───────────────────────────────────────────────────────
    #  TAB KALKULATOR
    # ───────────────────────────────────────────────────────

    def _bangun_tab_kalkulator(self):
        frame = self.tab_kalkulator
        frame_layar = tk.Frame(frame, bg=WARNA["bg_layar"], padx=20, pady=10)
        frame_layar.pack(fill=tk.X, padx=10, pady=(10, 5))
        self.var_ekspresi = tk.StringVar(value="")
        self.label_ekspresi = tk.Label(
            frame_layar,
            textvariable=self.var_ekspresi,
            font=FONT_LAYAR_KECIL,
            fg=WARNA["teks_redup"],
            bg=WARNA["bg_layar"],
            anchor="e",
        )
        self.label_ekspresi.pack(fill=tk.X, anchor="e")
        self.var_hasil = tk.StringVar(value="0")
        self.label_hasil = tk.Label(
            frame_layar,
            textvariable=self.var_hasil,
            font=FONT_LAYAR_BESAR,
            fg=WARNA["teks_utama"],
            bg=WARNA["bg_layar"],
            anchor="e",
        )
        self.label_hasil.pack(fill=tk.X, anchor="e")
        frame_tombol = tk.Frame(frame, bg=WARNA["bg_utama"])
        frame_tombol.pack(fill=tk.BOTH, expand=True, padx=8, pady=5)

        baris_tombol = [
            [("C", "hapus"), ("⌫", "hapus"), ("%", "fungsi"), ("÷", "operator")],
            [("7", "angka"), ("8", "angka"), ("9", "angka"), ("×", "operator")],
            [("4", "angka"), ("5", "angka"), ("6", "angka"), ("−", "operator")],
            [("1", "angka"), ("2", "angka"), ("3", "angka"), ("+", "operator")],
            [("±", "fungsi"), ("0", "angka"), (".", "angka"), ("=", "sama_dengan")],
        ]

        for i, baris in enumerate(baris_tombol):
            frame_tombol.grid_rowconfigure(i, weight=1)
            for j, (teks, tipe) in enumerate(baris):
                frame_tombol.grid_columnconfigure(j, weight=1)

                if tipe == "angka":
                    bg, hover, fg = (
                        WARNA["tombol_angka"],
                        WARNA["tombol_angka_hover"],
                        WARNA["teks_utama"],
                    )
                elif tipe == "operator":
                    bg, hover, fg = (
                        WARNA["tombol_operator"],
                        WARNA["tombol_operator_hover"],
                        WARNA["teks_utama"],
                    )
                elif tipe == "fungsi":
                    bg, hover, fg = (
                        WARNA["tombol_fungsi"],
                        WARNA["tombol_fungsi_hover"],
                        WARNA["teks_fungsi"],
                    )
                elif tipe == "hapus":
                    bg, hover, fg = (
                        WARNA["tombol_hapus"],
                        WARNA["tombol_hapus_hover"],
                        WARNA["teks_hapus"],
                    )
                elif tipe == "sama_dengan":
                    bg, hover, fg = (
                        WARNA["tombol_sama_dengan"],
                        WARNA["tombol_sama_dengan_hover"],
                        WARNA["teks_sama_dengan"],
                    )
                else:
                    bg, hover, fg = (
                        WARNA["tombol_angka"],
                        WARNA["tombol_angka_hover"],
                        WARNA["teks_utama"],
                    )

                tombol = TombolKustom(
                    frame_tombol,
                    teks=teks,
                    warna_bg=bg,
                    warna_hover=hover,
                    warna_teks=fg,
                    font=FONT_TOMBOL,
                    lebar=82,
                    tinggi=58,
                    command=lambda t=teks: self._klik_kalkulator(t),
                )
                tombol.grid(row=i, column=j, padx=3, pady=3, sticky="nsew")

    def _klik_kalkulator(self, teks):
        """Handler untuk setiap klik tombol kalkulator."""

        if teks == "C":
            self.ekspresi = ""
            self.var_ekspresi.set("")
            self.var_hasil.set("0")
            self.baru_mulai = True
            return

        if teks == "⌫":
            if self.ekspresi:
                self.ekspresi = self.ekspresi[:-1]
                self.var_hasil.set(self.ekspresi if self.ekspresi else "0")
            return

        if teks == "±":
            if self.ekspresi:
                try:
                    nilai = float(self.ekspresi)
                    nilai = -nilai
                    self.ekspresi = (
                        str(int(nilai)) if nilai == int(nilai) else str(nilai)
                    )
                    self.var_hasil.set(self.ekspresi)
                except ValueError:
                    if self.ekspresi.startswith("-"):
                        self.ekspresi = self.ekspresi[1:]
                    else:
                        self.ekspresi = "-" + self.ekspresi
                    self.var_hasil.set(self.ekspresi)
            return

        if teks == "%":
            if self.ekspresi:
                try:
                    nilai = float(self.ekspresi)
                    nilai = nilai / 100
                    self.ekspresi = str(nilai)
                    self.var_hasil.set(self.ekspresi)
                except ValueError:
                    pass
            return

        if teks == "=":
            if self.ekspresi:
                try:
                    ekspresi_eval = self.ekspresi
                    ekspresi_eval = ekspresi_eval.replace("×", "*")
                    ekspresi_eval = ekspresi_eval.replace("÷", "/")
                    ekspresi_eval = ekspresi_eval.replace("−", "-")

                    hasil = eval(ekspresi_eval)

                    if isinstance(hasil, float):
                        if hasil == int(hasil) and abs(hasil) < 1e15:
                            hasil_str = str(int(hasil))
                        else:
                            hasil_str = f"{hasil:.10g}"
                    else:
                        hasil_str = str(hasil)

                    ekspresi_tampil = self.ekspresi
                    self.var_ekspresi.set(f"{ekspresi_tampil} =")
                    self.var_hasil.set(hasil_str)
                    self.ekspresi = hasil_str
                    self.baru_mulai = True
                    self._tambah_riwayat(ekspresi_tampil, hasil_str)

                except ZeroDivisionError:
                    self.var_ekspresi.set(self.ekspresi + " =")
                    self.var_hasil.set("Tidak bisa dibagi 0")
                    self.ekspresi = ""
                    self.baru_mulai = True
                except Exception:
                    self.var_ekspresi.set(self.ekspresi + " =")
                    self.var_hasil.set("Error")
                    self.ekspresi = ""
                    self.baru_mulai = True
            return

        operator_set = {"+", "−", "×", "÷"}

        if teks in operator_set:
            self.baru_mulai = False
            # Cegah operator ganda
            if self.ekspresi and self.ekspresi[-1] in {"+", "−", "×", "÷"}:
                self.ekspresi = self.ekspresi[:-1]
            self.ekspresi += teks
            self.var_hasil.set(self.ekspresi)
        else:
            if self.baru_mulai and teks not in (".",):
                if self.ekspresi and not any(
                    self.ekspresi.endswith(op) for op in operator_set
                ):
                    self.ekspresi = ""
                self.baru_mulai = False

            if teks == ".":
                bagian = self.ekspresi
                for op in operator_set:
                    bagian = bagian.replace(op, "|")
                angka_terakhir = bagian.split("|")[-1] if bagian else ""
                if "." in angka_terakhir:
                    return

            self.ekspresi += teks
            self.var_hasil.set(self.ekspresi)

    def _handle_keyboard(self, event):
        """Handler keyboard untuk kalkulator."""
        if self.notebook.index("current") != 0:
            return

        key = event.char
        keysym = event.keysym

        peta_tombol = {
            "0": "0",
            "1": "1",
            "2": "2",
            "3": "3",
            "4": "4",
            "5": "5",
            "6": "6",
            "7": "7",
            "8": "8",
            "9": "9",
            ".": ".",
            "+": "+",
            "-": "−",
            "*": "×",
            "/": "÷",
        }

        if key in peta_tombol:
            self._klik_kalkulator(peta_tombol[key])
        elif keysym == "Return" or key == "=":
            self._klik_kalkulator("=")
        elif keysym == "BackSpace":
            self._klik_kalkulator("⌫")
        elif keysym == "Escape" or key.lower() == "c":
            self._klik_kalkulator("C")
        elif key == "%":
            self._klik_kalkulator("%")

    # ───────────────────────────────────────────────────────
    #  TAB KONVERSI SUHU
    # ───────────────────────────────────────────────────────

    def _bangun_tab_suhu(self):
        frame = self.tab_suhu
        header = tk.Label(
            frame,
            text="Konversi Suhu",
            font=("Segoe UI", 18, "bold"),
            fg=WARNA["aksen"],
            bg=WARNA["bg_utama"],
        )
        header.pack(pady=(20, 5))

        sub_header = tk.Label(
            frame,
            text="Celsius  •  Fahrenheit  •  Kelvin  •  Reamur",
            font=FONT_LABEL,
            fg=WARNA["teks_redup"],
            bg=WARNA["bg_utama"],
        )
        sub_header.pack(pady=(0, 15))
        frame_input = tk.Frame(frame, bg=WARNA["bg_utama"])
        frame_input.pack(fill=tk.X, padx=24, pady=5)
        frame_dari_atas = tk.Frame(frame_input, bg=WARNA["bg_utama"])
        frame_dari_atas.pack(fill=tk.X, pady=(0, 4))

        tk.Label(
            frame_dari_atas,
            text="Dari:",
            font=("Segoe UI", 12, "bold"),
            fg=WARNA["teks_utama"],
            bg=WARNA["bg_utama"],
        ).pack(side=tk.LEFT, anchor="w")

        self.var_satuan_dari = tk.StringVar(value="Celsius")
        self.combo_dari = ttk.Combobox(
            frame_dari_atas,
            textvariable=self.var_satuan_dari,
            values=["Celsius", "Fahrenheit", "Kelvin", "Reamur"],
            state="readonly",
            width=16,
            font=("Segoe UI", 12),
            style="Custom.TCombobox",
        )
        self.combo_dari.pack(side=tk.RIGHT, ipady=5)
        self.var_suhu_input = tk.StringVar(value="0")
        self.entry_suhu = tk.Entry(
            frame_input,
            textvariable=self.var_suhu_input,
            font=("Segoe UI", 24, "bold"),
            fg=WARNA["teks_utama"],
            bg=WARNA["tombol_angka"],
            insertbackground=WARNA["teks_utama"],
            relief="flat",
            bd=8,
            justify="center",
        )
        self.entry_suhu.pack(fill=tk.X, ipady=10, pady=(0, 6))

        frame_btn = tk.Frame(frame, bg=WARNA["bg_utama"])
        frame_btn.pack(pady=10)

        tombol_konversi = TombolKustom(
            frame_btn,
            teks="Konversi  ⟶",
            warna_bg=WARNA["tombol_sama_dengan"],
            warna_hover=WARNA["tombol_sama_dengan_hover"],
            warna_teks=WARNA["teks_sama_dengan"],
            font=("Segoe UI", 14, "bold"),
            lebar=200,
            tinggi=48,
            command=self._konversi_suhu,
        )
        tombol_konversi.pack()
        frame_tukar = tk.Frame(frame, bg=WARNA["bg_utama"])
        frame_tukar.pack(pady=(5, 5))

        tombol_tukar = TombolKustom(
            frame_tukar,
            teks="⇅ Tukar",
            warna_bg=WARNA["tombol_operator"],
            warna_hover=WARNA["tombol_operator_hover"],
            warna_teks=WARNA["teks_utama"],
            font=FONT_TOMBOL_KECIL,
            lebar=100,
            tinggi=36,
            command=self._tukar_satuan,
        )
        tombol_tukar.pack()

        frame_output = tk.Frame(frame, bg=WARNA["bg_utama"])
        frame_output.pack(fill=tk.X, padx=24, pady=5)
        frame_ke_atas = tk.Frame(frame_output, bg=WARNA["bg_utama"])
        frame_ke_atas.pack(fill=tk.X, pady=(0, 4))

        tk.Label(
            frame_ke_atas,
            text="Ke:",
            font=("Segoe UI", 12, "bold"),
            fg=WARNA["teks_utama"],
            bg=WARNA["bg_utama"],
        ).pack(side=tk.LEFT, anchor="w")

        self.var_satuan_ke = tk.StringVar(value="Fahrenheit")
        self.combo_ke = ttk.Combobox(
            frame_ke_atas,
            textvariable=self.var_satuan_ke,
            values=["Celsius", "Fahrenheit", "Kelvin", "Reamur"],
            state="readonly",
            width=16,
            font=("Segoe UI", 12),
            style="Custom.TCombobox",
        )
        self.combo_ke.pack(side=tk.RIGHT, ipady=5)
        self.var_suhu_output = tk.StringVar(value="0")
        self.entry_suhu_output = tk.Entry(
            frame_output,
            textvariable=self.var_suhu_output,
            font=("Segoe UI", 24, "bold"),
            fg=WARNA["teks_hasil"],
            bg=WARNA["tombol_angka"],
            relief="flat",
            bd=8,
            justify="center",
            state="readonly",
            readonlybackground=WARNA["tombol_angka"],
        )
        self.entry_suhu_output.pack(fill=tk.X, ipady=10, pady=(0, 6))

        frame_ref = tk.Frame(frame, bg=WARNA["bg_layar"], padx=15, pady=10)
        frame_ref.pack(fill=tk.X, padx=30, pady=(15, 10))

        tk.Label(
            frame_ref,
            text="Referensi Cepat",
            font=FONT_JUDUL,
            fg=WARNA["aksen"],
            bg=WARNA["bg_layar"],
        ).pack(anchor="w")

        referensi = [
            ("Air membeku", "0°C = 32°F = 273.15K = 0°Re"),
            ("Air mendidih", "100°C = 212°F = 373.15K = 80°Re"),
            ("Suhu tubuh", "37°C = 98.6°F = 310.15K = 29.6°Re"),
        ]
        for judul, nilai in referensi:
            f = tk.Frame(frame_ref, bg=WARNA["bg_layar"])
            f.pack(fill=tk.X, pady=1)
            tk.Label(
                f,
                text=f"  {judul}:",
                font=("Segoe UI", 10, "bold"),
                fg=WARNA["teks_utama"],
                bg=WARNA["bg_layar"],
                width=14,
                anchor="w",
            ).pack(side=tk.LEFT)
            tk.Label(
                f,
                text=nilai,
                font=("Consolas", 10),
                fg=WARNA["teks_redup"],
                bg=WARNA["bg_layar"],
                anchor="w",
            ).pack(side=tk.LEFT)

        self.var_suhu_input.trace_add("write", lambda *a: self._konversi_suhu())
        self.var_satuan_dari.trace_add("write", lambda *a: self._konversi_suhu())
        self.var_satuan_ke.trace_add("write", lambda *a: self._konversi_suhu())

    def _konversi_suhu(self):
        """Lakukan konversi suhu antara semua satuan yang didukung."""
        try:
            nilai = float(self.var_suhu_input.get())
        except (ValueError, tk.TclError):
            self.var_suhu_output.set("—")
            return

        dari = self.var_satuan_dari.get()
        ke = self.var_satuan_ke.get()

        if dari == "Celsius":
            celsius = nilai
        elif dari == "Fahrenheit":
            celsius = (nilai - 32) * 5 / 9
        elif dari == "Kelvin":
            celsius = nilai - 273.15
        elif dari == "Reamur":
            celsius = nilai * 5 / 4
        else:
            self.var_suhu_output.set("—")
            return

        if ke == "Celsius":
            hasil = celsius
        elif ke == "Fahrenheit":
            hasil = celsius * 9 / 5 + 32
        elif ke == "Kelvin":
            hasil = celsius + 273.15
        elif ke == "Reamur":
            hasil = celsius * 4 / 5
        else:
            self.var_suhu_output.set("—")
            return

        if hasil == int(hasil):
            self.var_suhu_output.set(str(int(hasil)))
        else:
            self.var_suhu_output.set(f"{hasil:.4f}".rstrip("0").rstrip("."))

    def _tukar_satuan(self):
        """Tukar satuan 'dari' dan 'ke'."""
        dari = self.var_satuan_dari.get()
        ke = self.var_satuan_ke.get()
        self.var_satuan_dari.set(ke)
        self.var_satuan_ke.set(dari)
        # Output lama menjadi input baru
        output_lama = self.var_suhu_output.get()
        if output_lama and output_lama != "—":
            self.var_suhu_input.set(output_lama)
        self._konversi_suhu()

    # ───────────────────────────────────────────────────────
    #  TAB RIWAYAT
    # ───────────────────────────────────────────────────────

    def _bangun_tab_riwayat(self):
        frame = self.tab_riwayat

        # ── Header ──
        frame_header = tk.Frame(frame, bg=WARNA["bg_utama"])
        frame_header.pack(fill=tk.X, padx=15, pady=(15, 5))

        tk.Label(
            frame_header,
            text="Riwayat Perhitungan",
            font=("Segoe UI", 16, "bold"),
            fg=WARNA["aksen"],
            bg=WARNA["bg_utama"],
        ).pack(side=tk.LEFT, anchor="w")

        tombol_hapus_semua = TombolKustom(
            frame_header,
            teks="Hapus Semua",
            warna_bg=WARNA["tombol_hapus"],
            warna_hover=WARNA["tombol_hapus_hover"],
            warna_teks=WARNA["teks_hapus"],
            font=FONT_TOMBOL_KECIL,
            lebar=115,
            tinggi=36,
            command=self._hapus_riwayat,
        )
        tombol_hapus_semua.pack(side=tk.RIGHT)

        # Garis pemisah
        tk.Frame(frame, bg=WARNA["border"], height=1).pack(
            fill=tk.X, padx=15, pady=(5, 0)
        )

        # ── Area scroll ──
        frame_scroll = tk.Frame(frame, bg=WARNA["bg_utama"])
        frame_scroll.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.canvas_riwayat = tk.Canvas(
            frame_scroll,
            bg=WARNA["bg_utama"],
            highlightthickness=0,
            bd=0,
        )
        scrollbar_riwayat = tk.Scrollbar(
            frame_scroll,
            orient="vertical",
            command=self.canvas_riwayat.yview,
        )
        self.canvas_riwayat.configure(yscrollcommand=scrollbar_riwayat.set)

        scrollbar_riwayat.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas_riwayat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.frame_isi_riwayat = tk.Frame(self.canvas_riwayat, bg=WARNA["bg_utama"])
        self.canvas_window_id = self.canvas_riwayat.create_window(
            (0, 0), window=self.frame_isi_riwayat, anchor="nw"
        )

        self.frame_isi_riwayat.bind("<Configure>", self._on_riwayat_configure)
        self.canvas_riwayat.bind("<Configure>", self._on_canvas_configure)

        # Scroll dengan mouse wheel
        self.canvas_riwayat.bind(
            "<MouseWheel>",
            lambda e: self.canvas_riwayat.yview_scroll(-1 * (e.delta // 120), "units"),
        )

        # Pesan awal ketika kosong
        self._refresh_riwayat()

    def _on_riwayat_configure(self, event):
        self.canvas_riwayat.configure(scrollregion=self.canvas_riwayat.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas_riwayat.itemconfig(self.canvas_window_id, width=event.width)

    def _tambah_riwayat(self, ekspresi, hasil):
        """Simpan satu entri ke riwayat lalu perbarui tampilan."""
        self.riwayat.append((ekspresi, hasil))
        self._refresh_riwayat()

    def _refresh_riwayat(self):
        """Render ulang seluruh isi panel riwayat."""
        for widget in self.frame_isi_riwayat.winfo_children():
            widget.destroy()

        if not self.riwayat:
            tk.Label(
                self.frame_isi_riwayat,
                text="Belum ada riwayat perhitungan.",
                font=FONT_LABEL,
                fg=WARNA["teks_redup"],
                bg=WARNA["bg_utama"],
            ).pack(fill=tk.X, pady=30)
            return

        for ekspresi, hasil in reversed(self.riwayat):
            self._buat_item_riwayat(ekspresi, hasil)

    def _buat_item_riwayat(self, ekspresi, hasil):
        """Buat satu kartu entri riwayat yang bisa diklik."""
        frame_item = tk.Frame(
            self.frame_isi_riwayat,
            bg=WARNA["bg_layar"],
            padx=14,
            pady=10,
            cursor="hand2",
        )
        frame_item.pack(fill=tk.X, padx=6, pady=3)

        lbl_ekspresi = tk.Label(
            frame_item,
            text=ekspresi + "  =",
            font=("Segoe UI", 11),
            fg=WARNA["teks_redup"],
            bg=WARNA["bg_layar"],
            anchor="e",
        )
        lbl_ekspresi.pack(fill=tk.X)

        lbl_hasil = tk.Label(
            frame_item,
            text=hasil,
            font=("Segoe UI", 20, "bold"),
            fg=WARNA["teks_hasil"],
            bg=WARNA["bg_layar"],
            anchor="e",
        )
        lbl_hasil.pack(fill=tk.X)

        semua_widget = [frame_item, lbl_ekspresi, lbl_hasil]

        def on_enter(e, fw=frame_item, le=lbl_ekspresi, lh=lbl_hasil):
            fw.configure(bg=WARNA["tombol_angka"])
            le.configure(bg=WARNA["tombol_angka"])
            lh.configure(bg=WARNA["tombol_angka"])

        def on_leave(e, fw=frame_item, le=lbl_ekspresi, lh=lbl_hasil):
            fw.configure(bg=WARNA["bg_layar"])
            le.configure(bg=WARNA["bg_layar"])
            lh.configure(bg=WARNA["bg_layar"])

        def on_click(e, h=hasil):
            self.ekspresi = h
            self.var_hasil.set(h)
            self.var_ekspresi.set("")
            self.baru_mulai = True
            self.notebook.select(0)

        for w in semua_widget:
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)
            w.bind("<Button-1>", on_click)
            w.bind(
                "<MouseWheel>",
                lambda e: self.canvas_riwayat.yview_scroll(
                    -1 * (e.delta // 120), "units"
                ),
            )

    def _hapus_riwayat(self):
        """Kosongkan seluruh riwayat."""
        self.riwayat = []
        self._refresh_riwayat()


# ═══════════════════════════════════════════════════════════
#  JALANKAN APLIKASI
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    root = tk.Tk()
    app = AplikasiKalkulator(root)
    root.mainloop()


# ═══════════════════════════════════════════════════════════
#  finish
# ═══════════════════════════════════════════════════════════
