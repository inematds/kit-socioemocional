import json, sys, os
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.expanduser('~/projetos/imagens-agnes'))
from gerar import gerar

BASE = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.expanduser('~/projetos/kit-socioemocional/piloto')
SO = sys.argv[2].split(',') if len(sys.argv) > 2 else None  # só estas páginas
R = json.load(open(f'{BASE}/roteiro.json'))
P = R['personagens']

def job(nome, item, ratio):
    dest = f'{BASE}/img/{nome}.png'
    if os.path.exists(dest):
        return nome, 'ja existe'
    desc = '; '.join(P[k]['desc'] for k in item['p'])
    prompt = f"{item['cena']}. Characters: {desc}. Keep the same character design as the reference. {R['estilo']}"
    refs = [f"{BASE}/{P[k]['ancora']}" for k in item['p'][:2]]
    gerar(prompt, dest, ratio=ratio, size='1K', refs=refs)
    return nome, 'ok' if os.path.exists(dest) else 'FALHOU'

jobs = []
for pg in R['paginas']:
    if SO and pg['id'] not in SO:
        continue
    if 'quadros' in pg:
        for i, q in enumerate(pg['quadros'], 1):
            jobs.append((f"p{pg['id']}-q{i}", q, '4:3'))
    else:
        jobs.append((f"p{pg['id']}-cena", pg['img_cena'], '16:9'))
        jobs.append((f"p{pg['id']}-ajuda", pg['img_ajuda'], '4:3'))

with ThreadPoolExecutor(4) as ex:
    for nome, st in ex.map(lambda j: job(*j), jobs):
        print(nome, st, flush=True)
