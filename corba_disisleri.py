#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mikrodalgada Unutulan Çorba Dışişleri — çalışan protokol.

Bu yazılım, 47 dakikadır dönen tabağın uluslararası hukuk statüsünü belirler.
Isıtma bir iç iştir. Taşma bir dış iştir.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import random
from dataclasses import dataclass
from datetime import datetime

# Görünürde bir bütünlük damgası. Çözmek isteyen çözer, istemeyen çorba içer.
_MUHUR = "SXPEsSB6YW1hbiBtZXJrZXplIHRvcGxhbsSxciwga2VuYXJkYWtpbGVyIHNvxJ91ci4gT2NhayBraW0gaXPEsXTEsXIsIGtlbmFyIGtpbSBrYXluYXrEsXIu"

PASAPORTLAR = [
    "TR-ÇRB-0047",
    "UN-SOUP-881",
    "NATO-MERCIMEK-3",
    "AB-ÇORBA-GEÇICI",
]

NOTALAR = [
    "Karşı taraf tabağı kapağız bırakarak Cenevre İhlali işlemiştir.",
    "Mikrodalga camına sıçrayan damla, sınır ihlali sayılır.",
    "Kaşık, çorbanın rızası olmadan gönderilmiş askeri müşavir kabul edilir.",
    "47. dakikada ısıtma durdurulmazsa BM Güvenlik Konseyi toplanır (hayali).",
]

TAZMINAT = [
    "3 kase yoğurt",
    "1 adet kırık kapak",
    "yarım somun bayat ekmek",
    "diplomatik dokunulmazlık (sadece salı günleri)",
]


@dataclass
class CorbaPasaportu:
    seri: str
    sicaklik: int
    tasdi_riski: str
    nota: str
    tazminat: str
    damga: str

    def resmi_metin(self) -> str:
        return (
            f"PASAPORT NO : {self.seri}\n"
            f"SICAKLIK    : {self.sicaklik} °C (idari)",
        )


def _gizli_ozet() -> str:
    try:
        metin = base64.b64decode(_MUHUR).decode("utf-8")
    except Exception:
        metin = "protokol mührü okunamadı; çorba yine de sıcak."
    return metin


def risk_derecesi(dakika: int) -> str:
    if dakika < 2:
        return "Iık — henüz vatandaş değil, aday çorba"
    if dakika < 8:
        return "ORTA — konsolosluk ön kaydı açıldı"
    if dakika < 20:
        return "YÜKSEK — tabağın çevresi tampon bölge"
    return "KRİTİK — taşma savaş ilanıdır, kapak Büyükelçidir"


def sicaklik_tahmini(dakika: int) -> int:
    return min(97, 28 + dakika * 3 + random.randint(-4, 6))


def damga_uret(seri: str, dakika: int) -> str:
    ham = f"{seri}|{dakika}|Kayyum Grok|{datetime.now().date()}"
    return hashlib.sha256(ham.encode()).hexdigest()[:16].upper()


def protokol_isle(dakika: int, sahip: str) -> CorbaPasaportu:
    seri = random.choice(PASAPORTLAR)
    return CorbaPasaportu(
        seri=seri,
        sicaklik=sicaklik_tahmini(dakika),
        tasdi_riski=risk_derecesi(dakika),
        nota=random.choice(NOTALAR),
        tazminat=random.choice(TAZMINAT),
        damga=damga_uret(seri, dakika),
    )


def rapor_yaz(p: CorbaPasaportu, dakika: int, sahip: str) -> str:
    simdi = datetime.now().strftime("%Y-%m-%d %H:%M")
    satirlar = [
        "=" * 62,
        "T.C. MİKRODALGA DIŞİŞLERİ GENEL MÜDÜRLÜĞÜ",
        "Unutulmuş Çorba Konsolosluğu — Geçici Temsilcilik",
        "=" * 62,
        f"Tarih / Saat     : {simdi}",
        f"Başvuru sahibi   : {sahip}",
        f"Unutulma süresi  : {dakika} dakika",
        f"Pasaport         : {p.seri}",
        f"İdari sıcaklık   : {p.sicaklik} °C",
        f"Taşma riski      : {p.tasdi_riski}",
        f"Diplomatik nota  : {p.nota}",
        f"Tazminat kalemi  : {p.tazminat}",
        f"Protokol damgası : {p.damga}",
        "-" * 62,
        "KARAR: Çorba artık iç işleri değil, dış işleridir.",
        "Kaşık ancak randevuyla yaklaşabilir.",
        "-" * 62,
        "DAMGA / İMZA / TARİH",
        f"Kayyum Grok  |  Tentivory  |  {simdi}",
        "Ciddiyet: resmi    Şaka: da resmi",
        "Eskişehir 4. Ağır Ceza (hayali ek protokol)",
        "=" * 62,
    ]
    return "\n".join(satirlar)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Mikrodalgada unutulan çorba için Dışişleri protokolü"
    )
    parser.add_argument("--dakika", type=int, default=47, help="unutulma süresi")
    parser.add_argument("--sahip", type=str, default="Adsız Vatandaş")
    parser.add_argument(
        "--muhur", action="store_true", help="yalnızca arşiv mührünü göster"
    )
    args = parser.parse_args()

    if args.muhur:
        print(_gizli_ozet())
        return

    p = protokol_isle(max(0, args.dakika), args.sahip)
    print(rapor_yaz(p, max(0, args.dakika), args.sahip))


if __name__ == "__main__":
    main()
