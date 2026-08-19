# -*- coding: utf-8 -*-
"""CV: iz `cv.html` u `Resad_Spahovic_CV.pdf`.

    python assets/files/_alat/napravi-cv.py

ZASTO OVAKO. Raniji PDF je pravljen ReportLab-om, ali taj alat nije sacuvan —
pa se CV dve godine nije mogao izmeniti, samo prekucati. Sada je izvor obicna
HTML datoteka: otvori `cv.html` u pregledacu, vidis tacno ono sto ce biti u
PDF-u, a ovaj alat to odstampa.

Stampa Chrome koji je vec na racunaru (`--headless --print-to-pdf`), pa nema
sta da se instalira. Zaglavlje i podnozje pregledaca su iskljuceni, inace bi na
svakoj strani stajali datum i adresa datoteke.
"""
import os
import shutil
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IZVOR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cv.html")
IZLAZ = os.path.join(KOREN, "Resad_Spahovic_CV.pdf")

MESTA = [
	r"C:\Program Files\Google\Chrome\Application\chrome.exe",
	r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
	r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def pregledac():
	for p in MESTA:
		if os.path.exists(p):
			return p
	nadjen = shutil.which("chrome") or shutil.which("msedge")
	if nadjen:
		return nadjen
	raise SystemExit("  Chrome nije nadjen — dopuni spisak MESTA u ovom alatu.")


def main() -> int:
	if not os.path.exists(IZVOR):
		raise SystemExit(f"  nema izvora: {IZVOR}")

	# Chrome pise samo u putanju bez razmaka koju sam kontrolise, pa se stampa u
	# privremeni folder i tek onda prenosi na mesto.
	with tempfile.TemporaryDirectory() as privremeni:
		privremeni_pdf = os.path.join(privremeni, "cv.pdf")
		subprocess.run([
			pregledac(),
			"--headless=new", "--disable-gpu", "--no-sandbox",
			"--no-pdf-header-footer",
			f"--print-to-pdf={privremeni_pdf}",
			"file:///" + IZVOR.replace("\\", "/"),
		], check=True, capture_output=True, timeout=180)
		shutil.copyfile(privremeni_pdf, IZLAZ)

	kb = os.path.getsize(IZLAZ) // 1024
	try:
		from pypdf import PdfReader
		strana = len(PdfReader(IZLAZ).pages)
		print(f"  {os.path.basename(IZLAZ)}   {strana} strane, {kb} KB")
		if strana > 2:
			print("  PAZI: CV je duzi od dve strane — skrati sadrzaj u cv.html.")
	except Exception:  # noqa: BLE001
		print(f"  {os.path.basename(IZLAZ)}   {kb} KB")
	return 0


if __name__ == "__main__":
	sys.exit(main())
