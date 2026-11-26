#!/usr/bin/env bash
# Gera capa + 6 banners (live e grade em PT/EN/ES) do guia, em paralelo. Codex image_gen.
R=~/projetos/kit-socioemocional
G=~/.claude/skills/projetos-landing-guia/assets/gerar-banner.sh
L=$R/motor/logs; mkdir -p $L
SIDES="a Brazilian mother and a 7-year-old child sitting on a sofa reading an illustrated picture book together, warm lamp light, cozy living room"

node ~/.claude/skills/capa-inema/assets/gerar-capa.cjs --repo $R --title "Conversa em Casa" --cat "Educação" \
  --save-raw $R/guia/assets/hero.png --gerador auto > $L/capa.log 2>&1 &

bash $G --repo $R --title "CONVERSA EM CASA" --destaque "CASA" --sub "Uma página ilustrada para cada situação que seu filho vai viver" \
  --line "Raiva, amizade, provocação: conversem antes de acontecer" --tiles "Raiva,Imprevistos,Escola,Exclusão,Provocação,Pedir ajuda" \
  --sides "$SIDES" > $L/b-pt.log 2>&1 &
bash $G --repo $R --title "CONVERSA EM CASA" --destaque "CASA" --sub "Situações reais da infância, uma página para cada uma, para ler junto" \
  --line "Grátis no inema.club" --tiles "O que muda em casa,Os 5 passos,Vol. 1 O que eu sinto,Vol. 2 Eu convivo e me protejo,O piloto,Como começar" \
  --estilo grade --saida banner-grade > $L/g-pt.log 2>&1 &
bash $G --repo $R --lang en --saida banner-en --title "TALK AT HOME" --destaque "HOME" --sub "One illustrated page for each situation your child will face" \
  --line "Anger, friendship, teasing: talk before it happens" --tiles "Anger,Mishaps,School,Being left out,Teasing,Asking for help" \
  --sides "$SIDES" > $L/b-en.log 2>&1 &
bash $G --repo $R --lang en --saida banner-grade-en --title "TALK AT HOME" --destaque "HOME" --sub "Real childhood situations, one page each, to read together" \
  --line "Free at inema.club" --tiles "What changes at home,The 5 steps,Vol. 1 What I feel,Vol. 2 Getting along and staying safe,The pilot,How to start" \
  --estilo grade > $L/g-en.log 2>&1 &
bash $G --repo $R --lang es --saida banner-es --title "CHARLA EN CASA" --destaque "CASA" --sub "Una página ilustrada para cada situación que tu hijo va a vivir" \
  --line "Enojo, amistad, burlas: hablen antes de que pase" --tiles "Enojo,Imprevistos,Escuela,Exclusión,Burlas,Pedir ayuda" \
  --sides "$SIDES" > $L/b-es.log 2>&1 &
bash $G --repo $R --lang es --saida banner-grade-es --title "CHARLA EN CASA" --destaque "CASA" --sub "Situaciones reales de la infancia, una página para cada una, para leer juntos" \
  --line "Gratis en inema.club" --tiles "Qué cambia en casa,Los 5 pasos,Vol. 1 Lo que siento,Vol. 2 Convivo y me protejo,El piloto,Cómo empezar" \
  --estilo grade > $L/g-es.log 2>&1 &
wait
ls -la $R/guia/assets $R/capa
