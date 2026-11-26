#!/usr/bin/env python3
"""Monta as páginas A4 do kit: roteiro.json + ilustrações -> HTML -> PNG + PDF (Chromium headless).

Uso: python3 motor/montar_paginas.py piloto
O texto nunca vai dentro da imagem: a ilustração entra sem letras e o texto vem do roteiro.
"""
import json, html, os, subprocess, sys
from pathlib import Path

PASSO_COR = {"Percebo": "#38bdf8", "Paro": "#f87171", "Penso": "#a78bfa",
             "Faço": "#34d399", "Peço ajuda": "#fb923c", "Consegui": "#FACC15"}

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@600;800&family=Inter:wght@400;600&display=swap');
@page { size: A4; margin: 0 }
* { box-sizing: border-box; margin: 0; padding: 0 }
body { font-family: Inter, sans-serif; color: #221E18; background: #F7F3EA }
.pg { width: 210mm; height: 297mm; padding: 11mm 11mm 9mm; display: flex; flex-direction: column; gap: 4.5mm; page-break-after: always; overflow: hidden }
.pg > * { flex-shrink: 0 }
.pg > .grade { flex-shrink: 1 }
.top { display: flex; justify-content: space-between; align-items: flex-start; gap: 6mm }
.selo { font: 600 9pt Sora; color: #5E5546; letter-spacing: .02em }
.selo b { color: #221E18 }
.num { font: 800 18pt Sora; background: #FACC15; color: #1a1206; border-radius: 50%; width: 15mm; height: 15mm; display: grid; place-items: center; flex: none }
h1 { font: 800 24pt/1.08 Sora; letter-spacing: -.01em }
h1 .mk { background: linear-gradient(transparent 58%, #FACC15 58%) }
.idade { font: 600 9pt Inter; color: #5E5546; margin-top: 1.5mm }
.grade { display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: repeat(3, minmax(0, 1fr)); gap: 4mm; flex: 1; min-height: 0 }
.q { background: #fff; border: 1px solid #E2D9C8; border-radius: 4mm; overflow: hidden; display: flex; flex-direction: column }
.q img { width: 100%; flex: 1 1 0; min-height: 0; object-fit: cover; display: block }
.q .leg { padding: 2mm 3mm 2.4mm; font-size: 10.2pt; line-height: 1.28; flex: none }
.q .tag { display: flex; align-items: center; gap: 1.6mm; font: 800 9pt Sora; margin-bottom: 1mm }
.q .tag i { width: 5.4mm; height: 5.4mm; border-radius: 50%; display: grid; place-items: center; font-style: normal; color: #1a1206; font-size: 8.5pt }
.faixa { display: grid; grid-template-columns: 1.15fr 1fr; gap: 4mm }
.box { background: #fff; border: 1px solid #E2D9C8; border-radius: 4mm; padding: 3mm 4mm; font-size: 10.5pt; line-height: 1.35 }
.box h3 { font: 800 9pt Sora; text-transform: uppercase; letter-spacing: .05em; color: #5E5546; margin-bottom: 1.2mm }
.ideia { background: #FEF9C3; border-color: #EAB308; font: 600 12.5pt/1.3 Sora }
.box ol { padding-left: 4.5mm }
.rod { display: flex; justify-content: space-between; align-items: center; font: 600 9pt Sora; color: #5E5546; border-top: 1px solid #E2D9C8; padding-top: 2.5mm }
.rod .fecho { color: #221E18; font-weight: 800; font-size: 11pt }
/* volume 2 */
.cena { display: grid; grid-template-rows: minmax(0, 1fr); grid-template-columns: 1.35fr 1fr; gap: 4mm; align-items: stretch }
.cena img, .ajuda img { width: 100%; height: 100%; object-fit: cover; border-radius: 4mm; display: block }
.cena .box { display: flex; flex-direction: column; justify-content: center; font-size: 11.5pt }
.escolha { display: grid; gap: 3mm }
.op { display: grid; grid-template-columns: 30mm 1fr; border-radius: 4mm; overflow: hidden; border: 1px solid #E2D9C8; background: #fff }
.op .r { display: grid; place-items: center; text-align: center; font: 800 10pt/1.2 Sora; padding: 2mm; color: #fff }
.op .t { padding: 3mm 4mm; font-size: 11pt; line-height: 1.38 }
.nao .r { background: #b91c1c }
.sim .r { background: #0E6B55 }
.ajuda { display: grid; grid-template-rows: minmax(0, 1fr); grid-template-columns: 1fr 62mm; gap: 4mm; align-items: stretch; margin-bottom: 2mm }
.d2 .q img, .d2 .cena img, .d2 .ajuda img { object-fit: contain; background: #fff }
.valor { text-align: center; font: 800 13pt Sora; padding: 3mm; border-radius: 4mm; background: #FEF9C3; border: 1px solid #EAB308 }
"""


def e(s):
    return html.escape(s)


def titulo(t):
    # marca a 1a palavra-chave depois de "Quando" com marca-texto
    pal = t.split(" ")
    if len(pal) > 2 and pal[0] in ("Quando",):
        return f"{e(pal[0])} <span class='mk'>{e(' '.join(pal[1:3]))}</span> {e(' '.join(pal[3:]))}"
    return f"<span class='mk'>{e(t)}</span>"


def topo(r, pg):
    vol = "Vol. 1 · O que eu sinto" if pg["volume"] == 1 else "Vol. 2 · Eu convivo e me protejo"
    return f"""<div class='top'><div><div class='selo'><b>{e(r['kit'])}</b> · {vol} · {e(pg['capitulo'])}</div>
<h1>{titulo(pg['titulo'])}</h1><div class='idade'>Para ler junto · {e(pg['idade'])}</div></div>
<div class='num'>{int(pg['id'])}</div></div>"""


def rodape(r, pg):
    return f"<div class='rod'><span>inema.club · grátis</span><span class='fecho'>{e(r['fecho'])}</span><span>Situação {pg['id']}</span></div>"


def conversa(pg):
    return "<ol>" + "".join(f"<li>{e(c)}</li>" for c in pg["conversa"]) + "</ol>"


def cls(r):
    return 'd2' if '2D' in r.get('estilo', '') else ''


def pagina_v1(r, pg, img):
    qs = ""
    for i, q in enumerate(pg["quadros"], 1):
        cor = PASSO_COR.get(q["passo"], "#FACC15")
        qs += f"""<div class='q'><img src='{img}/p{pg['id']}-q{i}.jpg'><div class='leg'>
<div class='tag'><i style='background:{cor}'>{i}</i>{e(q['passo'])}</div>{e(q['texto'])}</div></div>"""
    return f"""<section class='pg {cls(r)}'>{topo(r, pg)}<div class='grade'>{qs}</div>
<div class='faixa'><div class='box ideia'><h3>Uma ideia para lembrar</h3>{e(pg['ideia'])}</div>
<div class='box'><h3>Conversa de família</h3>{conversa(pg)}</div></div>{rodape(r, pg)}</section>"""


def pagina_v2(r, pg, img):
    return f"""<section class='pg {cls(r)}'>{topo(r, pg)}
<div class='cena' style='height:70mm'><img src='{img}/p{pg['id']}-cena.jpg'>
<div class='box'><h3>A cena</h3>{e(pg['cena_texto'])}</div></div>
<div class='box'><h3>O que está acontecendo</h3>{e(pg['entenda'])}</div>
<div class='escolha'>
<div class='op nao'><div class='r'>✗<br>Não ajuda</div><div class='t'>{e(pg['piorar'])}</div></div>
<div class='op sim'><div class='r'>✓<br>Experimente dizer</div><div class='t'>{e(pg['saida'])}</div></div></div>
<div class='ajuda' style='height:36mm'><div class='box'><h3>Quem pode ajudar</h3>{e(pg['ajuda'])}</div><img src='{img}/p{pg['id']}-ajuda.jpg'></div>
<div class='valor'>{e(pg['valor'])}</div>
<div class='box'><h3>Conversa de família</h3>{conversa(pg)}</div>
{rodape(r, pg)}</section>"""


def main():
    base = Path(sys.argv[1] if len(sys.argv) > 1 else "piloto").resolve()
    r = json.loads((base / "roteiro.json").read_text())
    jpg = base / "jpg"
    jpg.mkdir(exist_ok=True)
    for png in sorted((base / "img").glob("p*.png")):
        out = jpg / (png.stem + ".jpg")
        if not out.exists() or out.stat().st_mtime < png.stat().st_mtime:
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(png), "-vf", "scale=960:-1", "-q:v", "4", str(out)], check=True)
    outdir = base / "paginas"
    outdir.mkdir(exist_ok=True)
    corpo_todas = ""
    for pg in r["paginas"]:
        fn = pagina_v1 if pg["volume"] == 1 else pagina_v2
        sec = fn(r, pg, "../jpg")
        corpo_todas += sec
        doc = f"<!doctype html><html lang='pt-BR'><meta charset='utf-8'><title>{e(pg['titulo'])}</title><style>{CSS}</style><body>{sec}</body></html>"
        h = outdir / f"p{pg['id']}.html"
        h.write_text(doc)
        png = outdir / f"p{pg['id']}.png"
        subprocess.run(["/snap/bin/chromium", "--headless", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=1.5", "--window-size=794,1123",
                        "--virtual-time-budget=4000", f"--screenshot={png}", h.as_uri()],
                       check=True, capture_output=True)
        print("ok", png.name)
    todas = outdir / "piloto.html"
    todas.write_text(f"<!doctype html><html lang='pt-BR'><meta charset='utf-8'><title>Piloto</title><style>{CSS}</style><body>{corpo_todas}</body></html>")
    pdf = outdir / "piloto.pdf"
    subprocess.run(["/snap/bin/chromium", "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=6000", f"--print-to-pdf={pdf}", todas.as_uri()],
                   check=True, capture_output=True)
    print("ok", pdf.name, pdf.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
