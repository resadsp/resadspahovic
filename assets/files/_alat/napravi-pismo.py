# -*- coding: utf-8 -*-
"""Propratno pismo: iz podataka o prijavi u PDF.

    python assets/files/_alat/napravi-pismo.py pisma/2026-08-19-firma.json
    python assets/files/_alat/napravi-pismo.py --sve

ZASTO OVAKO. Propratno pismo se pise iznova za svaku prijavu, ali se menja samo
mali deo: firma, pozicija i dva-tri pasusa. Sve ostalo — zaglavlje, izgled,
potpis — mora da ostane isto, inace se posle deset prijava razidje u deset
razlicitih dokumenata.

Zato je izgled u `pismo-predlozak.html` i menja se na jednom mestu, a svaka
prijava je jedna datoteka u `pisma/`. Stara pisma ostaju, pa se vidi sta je vec
poslato i kome.

Datoteka prijave (JSON):

    {
      "firma":    "Company d.o.o.",
      "pozicija": "Senior Python Engineer",
      "primalac": "Hiring Team",            (opciono, podrazumeva se "Hiring Team")
      "grad":     "Belgrade, Serbia",       (opciono)
      "datum":    "19 August 2026",         (opciono, ostavi prazno pa upisi rukom)
      "pozdrav":  "Kind regards,",          (opciono)
      "zvanje":   "Backend Engineer | ...",  (opciono; bez njega stoji red sa CV-ja)
      "pasusi":   ["prvi pasus", "drugi pasus", "..."]
    }
"""
import html
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ALAT = os.path.dirname(os.path.abspath(__file__))
PREDLOZAK = os.path.join(ALAT, "pismo-predlozak.html")
PISMA = os.path.join(ALAT, "pisma")

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


def napravi(put_json):
	podaci = json.load(open(put_json, encoding="utf-8"))
	for obavezno in ("firma", "pozicija", "pasusi"):
		if not podaci.get(obavezno):
			raise SystemExit(f"  {os.path.basename(put_json)}: fali polje '{obavezno}'")

	grad = podaci.get("grad", "").strip()
	# Red sa zvanjem se PODRAZUMEVA isti kao na CV-ju — zaglavlje mora da se
	# poklapa, inace dva dokumenta ne izgledaju kao komplet. Prijava sme da ga
	# promeni kad se javljas na usko odredjenu poziciju: citalac tada odmah vidi
	# da si pisao njima, a ne isto pismo na dvadeset mesta.
	ZVANJE_SA_CVJA = "Python Engineer | AI Systems Engineer | Backend, Data &amp; ML Infrastructure"
	zamene = {
		"naslov": f"Resad Spahovic — {podaci['pozicija']} — {podaci['firma']}",
		"datum": html.escape(podaci.get("datum", "")),
		"primalac": html.escape(podaci.get("primalac") or "Hiring Team"),
		"firma": html.escape(podaci["firma"]),
		"grad": ("<br>" + html.escape(grad)) if grad else "",
		"zvanje": html.escape(podaci["zvanje"]) if podaci.get("zvanje") else ZVANJE_SA_CVJA,
		"predmet": html.escape(f"Application: {podaci['pozicija']}"),
		"pozdrav": html.escape(podaci.get("pozdrav") or "Kind regards,"),
		# Pasusi se ne escape-uju do kraja: dozvoljen je <b> unutar recenice.
		"pasusi": "\n".join(f"<p>{p}</p>" for p in podaci["pasusi"]),
	}

	sadrzaj = open(PREDLOZAK, encoding="utf-8").read()
	for kljuc, vrednost in zamene.items():
		sadrzaj = sadrzaj.replace("{{" + kljuc + "}}", vrednost)

	izlaz = os.path.splitext(put_json)[0] + ".pdf"
	with tempfile.TemporaryDirectory() as privremeni:
		html_put = os.path.join(privremeni, "pismo.html")
		pdf_put = os.path.join(privremeni, "pismo.pdf")
		open(html_put, "w", encoding="utf-8").write(sadrzaj)
		subprocess.run([
			pregledac(), "--headless=new", "--disable-gpu", "--no-sandbox",
			"--no-pdf-header-footer", f"--print-to-pdf={pdf_put}",
			"file:///" + html_put.replace("\\", "/"),
		], check=True, capture_output=True, timeout=180)
		shutil.copyfile(pdf_put, izlaz)

	poruka = f"  {os.path.basename(izlaz):<44} {os.path.getsize(izlaz) // 1024} KB"
	try:
		from pypdf import PdfReader
		strana = len(PdfReader(izlaz).pages)
		poruka += f"   {strana} strana"
		if strana > 1:
			poruka += "   PAZI: pismo mora da stane na JEDNU stranu — skrati pasuse."
	except Exception:  # noqa: BLE001
		pass
	print(poruka)
	return izlaz


def main() -> int:
	argumenti = sys.argv[1:]
	if not argumenti:
		raise SystemExit(__doc__)

	if argumenti[0] == "--sve":
		datoteke = sorted(os.path.join(PISMA, f) for f in os.listdir(PISMA) if f.endswith(".json"))
		if not datoteke:
			raise SystemExit(f"  nema nijedne prijave u {PISMA}")
	else:
		datoteke = [a if os.path.isabs(a) else os.path.join(ALAT, a) for a in argumenti]

	for d in datoteke:
		if not os.path.exists(d):
			raise SystemExit(f"  nema datoteke: {d}")
		napravi(d)
	return 0


if __name__ == "__main__":
	sys.exit(main())
