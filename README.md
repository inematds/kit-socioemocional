# Conversa em Casa

[![Conversa em Casa](guia/assets/banner.jpg)](https://inematds.github.io/kit-socioemocional/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## O que é

O Conversa em Casa é um kit grátis de páginas ilustradas para pais, professores e cuidadores lerem com crianças de 3 a 13 anos. Cada página mostra uma situação comum (raiva, um brinquedo que quebra, um colega que provoca) e o que a criança pode fazer, passo a passo, sem revidar e pedindo ajuda quando precisa. Não precisa saber ler: a criança acompanha pelos desenhos e você lê o texto. Hoje estão no ar o mapa com 128 situações em dois volumes e um piloto de 5 páginas para baixar e imprimir, em desenho ou em 3D.

## 📖 Guia

Página completa: **https://inematds.github.io/kit-socioemocional/guia/**

📄 Piloto em PDF (5 páginas, A4): [em desenho](guia/assets/conversa-em-casa-piloto-desenho.pdf) · [em 3D](guia/assets/conversa-em-casa-piloto-3d.pdf) · 🗺️ Mapa das 128 situações: [MAPA.md](MAPA.md)

🎬 Vídeo: em produção.

## Os 5 passos de toda página

**Percebo → Paro → Penso → Faço → Peço ajuda.** No Volume 1 (O que eu sinto) cada passo vira um quadro da tirinha. No Volume 2 (Eu convivo e me protejo) a página mostra a cena, o que não ajuda, o que experimentar dizer e quem pode ajudar.

Regra fixa do Volume 2: nunca ensinar revide nem deboche; segurança vem antes de qualquer objeto; força, ameaça, grupo ou repetição sempre com um adulto junto. O capítulo "Meu corpo é meu" só sai depois de revisão de especialista.

## Quer uma página da situação do seu filho?

Cole no Claude Code ou no Codex:

```
Leia o repositório github.com/inematds/kit-socioemocional, em especial o MAPA.md e o arquivo piloto/roteiro.json.
Meu filho tem [IDADE] anos e está passando por isto: [CONTE A SITUAÇÃO EM 2 OU 3 FRASES].
Escreva uma página nova no mesmo formato do kit (Volume 1 se for emoção ou imprevisto; Volume 2 se for convivência), com os 5 passos, uma frase pronta para a criança dizer, quem pode ajudar e duas perguntas para conversarmos.
Regras: nada de revide ou deboche, linguagem para a idade dele, e me mostre só o texto. Não gere imagens nem altere arquivos antes do meu sim.
```

## Baseado em

- **Histórias Sociais** (Carol Gray, 1993): situação mostrada antes de acontecer, em primeira pessoa.
- **RULER** (Yale): reconhecer, entender, nomear, expressar e regular a emoção.
- **Zonas de Regulação**: estados por cores, estratégias e "problema pequeno ou grande?" — [materiais grátis](https://zonesofregulation.com/free-downloads/).
- **I Notice, I Feel, I Can** (Sesame Workshop) — [página](https://sesameworkshop.org/resources/i-notice-i-feel-i-can-2/).
- **Kidpower** (segurança pessoal) e **Lei 13.185/2015** (combate à intimidação sistemática) — [MEC, Bullying e convivência escolar](https://www.gov.br/mec/pt-br/escola-que-protege/bullying-e-convivencia-escolar-_-entendendo.pdf).

A pesquisa sobre histórias sociais tem resultado misto ([revisão de 2020](https://link.springer.com/article/10.1007/s40489-020-00235-6)). O kit não promete resultado: ele abre a conversa.

---

## Instalação técnica

O motor transforma um roteiro em páginas A4: ilustração sem texto (Agnes) + texto por cima (HTML) → PNG e PDF (Chromium).

**Pré-requisitos:** Python 3.10+, `ffmpeg`, Chromium (`/snap/bin/chromium` no script; troque o caminho se o seu for outro) e, para gerar ilustrações, o projeto `imagens-agnes` com `AGNES_API_KEY` (o `gerar_imagens.py` importa `gerar()` de `~/projetos/imagens-agnes`). Para só montar as páginas a partir das imagens que já estão no repo, não precisa da Agnes.

| Arquivo | O que faz |
|---|---|
| `MAPA.md` | as 128 situações, os capítulos, a espinha dos 5 passos e os modelos de página |
| `piloto/roteiro.json` | texto das 5 páginas do piloto + a descrição em inglês de cada ilustração |
| `piloto/img/ancora-*.png` | folhas de referência dos personagens (Leo, Bia, mãe, professora) e do cavalinho |
| `piloto/img/p*.png` | ilustrações de cada quadro em 3D, sem texto |
| `piloto-desenho/` | o mesmo piloto em desenho 2D (roteiro com outro estilo e âncoras próprias; recortes `ancora-x-1.png` com uma vista só) |
| `motor/gerar_imagens.py` | gera na Agnes as ilustrações que faltam (até 4 em paralelo, 2 referências por imagem) |
| `motor/montar_paginas.py` | monta HTML A4, PNG por página e o PDF do piloto em `piloto/paginas/` |
| `motor/gerar_banners.sh` | capa e banners do guia (Codex `image_gen`) |

```bash
# montar as páginas e o PDF a partir das ilustrações existentes
python3 motor/montar_paginas.py piloto            # 3D
python3 motor/montar_paginas.py piloto-desenho    # desenho 2D
# gerar ilustrações que faltam (apague o PNG para refazer um quadro)
python3 motor/gerar_imagens.py piloto-desenho 009,097   # pasta e páginas
```

## O processo, do início ao fim

| # | Passo | Comando | Quem |
|---|---|---|---|
| 1 | Escolher a situação no mapa e escrever a página no `roteiro.json` (texto PT + cena em inglês) | edição | 🧠 sessão com o Nei |
| 2 | Âncora de cada personagem ou objeto que se repete | `python3 ~/projetos/imagens-agnes/gerar.py "<turnaround>" --ratio 16:9 -o piloto/img/ancora-x.png` | ⚙️ script |
| 3 | Gerar as ilustrações dos quadros | `python3 motor/gerar_imagens.py` | ⚙️ script |
| 4 | Conferir cada quadro (personagem duplicado, folha de referência copiada, ação que não aparece) e apagar o que refazer | olhar | 🧠 sessão |
| 5 | Montar páginas e PDF | `python3 motor/montar_paginas.py piloto` | ⚙️ script |
| 6 | Revisão independente do conteúdo (sem revide, idade certa, sem promessa) | `Agent` novo / `claude -p` | 🤖 revisor |
| 7 | Copiar páginas e PDF para `guia/assets/`, traduzir EN/ES, publicar | `git push` | 🧠 sessão |

## Licença e uso

Grátis para uso pessoal e em escolas. Conteúdo do INEMA.CLUB.
