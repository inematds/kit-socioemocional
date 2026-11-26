#!/usr/bin/env bash
# Traduz guia/index.html e README.md para EN e ES pelo tradutor central (inema-traduz, assinatura).
R=~/projetos/kit-socioemocional
T="$HOME/projetos/wifi/scripts/inema-traduz --motor codex --modelo gpt-6-luna"
mkdir -p $R/guia/en $R/guia/es $R/motor/logs

regras_html() { # $1 idioma  $2 código  $3 nome do kit  $4 seletor
cat <<EOF
Traduza o HTML abaixo do português do Brasil para $1. Devolva SOMENTE o HTML completo, sem cercas de código e sem comentário antes ou depois.
Regras:
- Mantenha toda a estrutura, CSS, JS, ids, âncoras (href="#..."), classes, URLs externas e números iguais.
- <html lang="pt-BR"> vira <html lang="$2">.
- O nome do kit "Conversa em Casa" vira "$3" em todo lugar (título, nav, hero, rodapé, textos).
- Caminhos de imagem e arquivo: "assets/" vira "../assets/". "assets/banner.jpg" vira "../assets/banner-$2.jpg" e "assets/banner-grade.jpg" vira "../assets/banner-grade-$2.jpg".
- O seletor de idioma <span class="lang">...</span> vira exatamente: $4
- O PDF e as imagens das páginas do piloto continuam em português: acrescente "$5" ao texto do link de download do PDF e à primeira frase da seção #prova.
- O link do README técnico continua https://github.com/inematds/kit-socioemocional#instalação-técnica; troque o texto do link e aponte para README.$2.md: https://github.com/inematds/kit-socioemocional/blob/main/README.$2.md#technical-setup (en) ou #instalación-técnica (es) conforme o idioma.
- Links externos que são só em inglês: em inglês tire "(em inglês)"; em espanhol diga "(en inglés)". Links de documentos brasileiros (MEC, MPRJ) recebem "$5".
- O pedido dentro de <div class="pedido"> também é traduzido (a IA vai receber nesse idioma), mantendo o repositório e os nomes de arquivo.
- "Lei 13.185/2015" fica, com uma explicação curta de que é a lei brasileira contra o bullying.
- Os personagens Leo e Bia mantêm os nomes. Tom simples, caloroso, para pais leigos; frases curtas.
- localStorage KEY e textos do JS ("Copiado ✓") também traduzidos onde forem texto visível.
EOF
}

{ regras_html "inglês (EUA)" en "Talk at Home" '<span class="lang"><a href="../">PT</a><a class="on" href="./">EN</a><a href="../es/">ES</a></span>' "(in Portuguese)"; echo; echo "HTML:"; cat $R/guia/index.html; } \
  | $T -o $R/guia/en/index.html > $R/motor/logs/tr-en.log 2>&1 &
{ regras_html "espanhol (América Latina)" es "Charla en Casa" '<span class="lang"><a href="../">PT</a><a href="../en/">EN</a><a class="on" href="./">ES</a></span>' "(en portugués)"; echo; echo "HTML:"; cat $R/guia/index.html; } \
  | $T -o $R/guia/es/index.html > $R/motor/logs/tr-es.log 2>&1 &

readme() { # $1 idioma $2 código $3 nome $4 título da seção O que é $5 título instalação
cat <<EOF
Traduza o Markdown abaixo do português do Brasil para $1. Devolva SOMENTE o Markdown, sem cercas extras em volta.
Regras: mantenha tabelas, blocos de código (traduza só o texto do pedido em bloco e os comentários #), links e caminhos iguais.
"Conversa em Casa" vira "$3". O banner vira guia/assets/banner-$2.jpg e o link do guia vira https://inematds.github.io/kit-socioemocional/guia/$2/.
"## O que é" vira "## $4". "## Instalação técnica" vira "## $5". MAPA.md e o PDF são em português: marque "(in Portuguese)" ou "(en portugués)".
Mantenha a linha do seletor de idioma igual.

EOF
cat $R/README.md
}
readme "inglês (EUA)" en "Talk at Home" "What it is" "Technical setup" | $T -o $R/README.en.md > $R/motor/logs/tr-ren.log 2>&1 &
readme "espanhol (América Latina)" es "Charla en Casa" "Qué es" "Instalación técnica" | $T -o $R/README.es.md > $R/motor/logs/tr-res.log 2>&1 &
wait
wc -c $R/guia/en/index.html $R/guia/es/index.html $R/README.en.md $R/README.es.md
