#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSINT Toolkit - NIK & No HP
By: Fariz OSINT Build
"""

import sys
import re
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style

# ======== CONFIG GOOGLE SEARCH ========
GOOGLE_SEARCH = "https://www.google.com/search?q="

# ======== DATA PROVINSI/KABUPATEN (kode awal NIK) ========
# Hanya contoh sebagian, bisa ditambah
wilayah = {
    "3275": ("Jawa Barat", "Kab. Bandung Barat"),
    "3173": ("DKI Jakarta", "Jakarta Barat"),
    "3174": ("DKI Jakarta", "Jakarta Selatan"),
}

# ======== DETEKSI PROVIDER HP ========
provider_map = {
    "0811": "Telkomsel", "0812": "Telkomsel", "0813": "Telkomsel",
    "0821": "Telkomsel", "0822": "Telkomsel", "0823": "Telkomsel",
    "0852": "Telkomsel", "0853": "Telkomsel", "0851": "Telkomsel",
    "0814": "Indosat", "0815": "Indosat", "0816": "Indosat",
    "0855": "Indosat", "0856": "Indosat", "0857": "Indosat", "0858": "Indosat",
    "0817": "XL", "0818": "XL", "0819": "XL",
    "0859": "XL", "0877": "XL", "0878": "XL",
    "0838": "Axis", "0831": "Axis", "0832": "Axis", "0833": "Axis",
    "0895": "Tri", "0896": "Tri", "0897": "Tri", "0898": "Tri", "0899": "Tri",
    "0881": "Smartfren", "0882": "Smartfren", "0883": "Smartfren",
    "0884": "Smartfren", "0885": "Smartfren", "0886": "Smartfren",
    "0887": "Smartfren", "0888": "Smartfren", "0889": "Smartfren"
}

# ======== CEK APAKAH INPUT NIK ========
def is_nik(input_str):
    return re.fullmatch(r"\d{16}", input_str) is not None

# ======== CEK APAKAH INPUT NO HP ========
def is_phone(input_str):
    return re.fullmatch(r"(\+628\d{8,11}|08\d{8,11})", input_str) is not None

# ======== PARSE NIK ========
def parse_nik(nik):
    kode_wilayah = nik[:4]
    prov, kab = wilayah.get(kode_wilayah, ("Tidak diketahui", "Tidak diketahui"))

    tgl = int(nik[6:8])
    bln = nik[8:10]
    thn = nik[10:12]

    gender = "Laki-laki"
    if tgl > 40:
        tgl -= 40
        gender = "Perempuan"

    lahir = f"{tgl:02d}-{bln}-20{thn}"

    print(f"{Fore.GREEN}[+] Mode: NIK OSINT{Style.RESET_ALL}")
    print(f"Provinsi        : {prov}")
    print(f"Kabupaten/Kota  : {kab}")
    print(f"Kecamatan (kode): {nik[4:6]}")
    print(f"Jenis Kelamin   : {gender}")
    print(f"Tanggal Lahir   : {lahir}")

    google_dork(nik)

# ======== PARSE NO HP ========
def parse_phone(phone):
    if phone.startswith("+62"):
        prefix = "0" + phone[3:7]
    else:
        prefix = phone[:4]

    provider = provider_map.get(prefix, "Tidak diketahui")

    print(f"{Fore.CYAN}[+] Mode: HP OSINT{Style.RESET_ALL}")
    print(f"Provider        : {provider}")
    print(f"Prefix          : {prefix}")
    google_dork(phone)

# ======== GOOGLE DORKING ========
def google_dork(query):
    print(f"\n{Fore.YELLOW}[Dorking] Mencari jejak publik untuk: {query}{Style.RESET_ALL}")
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(GOOGLE_SEARCH + query, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        results = soup.select("a")
        count = 0
        for link in results:
            href = link.get("href")
            if href and "http" in href and not "google.com" in href:
                print(f"- {href}")
                count += 1
        if count == 0:
            print("Tidak ditemukan hasil publik.")
    except Exception as e:
        print(f"Error saat dorking: {e}")

# ======== MAIN ========
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <NIK / NoHP>")
        sys.exit(1)

    target = sys.argv[1]

    if is_nik(target):
        parse_nik(target)
    elif is_phone(target):
        parse_phone(target)
    else:
        print("Format tidak dikenali. Gunakan NIK 16 digit atau nomor HP (+62 / 08).")