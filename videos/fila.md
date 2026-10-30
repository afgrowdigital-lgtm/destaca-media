# Fila de vídeos da Destaca

Os vídeos chegam do Afonso pelo chat; a edição (legendas + final da marca + logo por cima da marca do Gemini)
é feita com `tools/video/` e o resultado fica em `videos/<slug>/` (`video.mp4`, `capa.jpg`, `legenda.txt` nos Reels).

Regra de destino (pela duração do vídeo final):
- **mais de 15 s → reel**: sai num horário de carrossel (ter 20:30, qua 13:00, qui 8:30), alternando com os carrosséis (ver `feed.md`).
- **15 s ou menos → story**: às 12:37, alternando com os stories de imagem — se o último story em `stories/registo.md` foi `vídeo`, hoje é imagem; se foi imagem e há story de vídeo por publicar, hoje é vídeo.
Publica-se sempre o mais antigo "por publicar" do tipo certo. Ao publicar, troca o estado para `publicado AAAA-MM-DD`.

Formato: `slug | tipo | duração | adicionado | estado`

- aparece-primeiro-google | story | 9.9 s | 2026-10-29 | publicado 2026-10-30
- teste-do-mapa-google | reel | 22.0 s | 2026-10-30 | por publicar
- porque-escolheu-o-concorrente | reel | 21.8 s | 2026-10-30 | por publicar
- site-lento-perde-clientes | reel | 21.7 s | 2026-10-30 | por publicar
- mito-so-instagram | reel | 21.9 s | 2026-10-30 | por publicar
- antes-depois-botao-contacto | reel | 21.0 s | 2026-10-30 | por publicar
- dica-telefone-no-topo | story | 11.3 s | 2026-10-30 | por publicar
- mito-mais-paginas | story | 11.1 s | 2026-10-30 | por publicar
- pergunta-chamadas-google | story | 11.9 s | 2026-10-30 | por publicar
- erro-fotos-de-banco | story | 11.5 s | 2026-10-30 | por publicar
- site-que-diz-o-essencial | story | 9.8 s | 2026-10-30 | por publicar
