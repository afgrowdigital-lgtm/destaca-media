# Fila de vídeos da Destaca

Os vídeos chegam do Afonso pelo chat; a edição (legendas + final da marca + logo por cima da marca do Gemini)
é feita com `tools/video/` e o resultado fica em `videos/<slug>/` (`video.mp4`, `capa.jpg`, `legenda.txt` nos Reels).

Regra de destino (pela duração do vídeo final):
- **mais de 15 s → reel**: sai num horário de carrossel (ter 20:30, qua 13:00, qui 8:30), alternando com os carrosséis (ver `feed.md`).
- **15 s ou menos → story**: substitui o story de imagem das 12:37 nesse dia.
Publica-se sempre o mais antigo "por publicar" do tipo certo. Ao publicar, troca o estado para `publicado AAAA-MM-DD`.

Formato: `slug | tipo | duração | adicionado | estado`

- aparece-primeiro-google | story | 9.9 s | 2026-10-29 | publicado 2026-10-30
- teste-do-mapa-google | reel | 22.0 s | 2026-10-30 | por publicar
- porque-escolheu-o-concorrente | reel | 21.8 s | 2026-10-30 | por publicar
- site-lento-perde-clientes | reel | 21.7 s | 2026-10-30 | por publicar
- mito-so-instagram | reel | 21.9 s | 2026-10-30 | por publicar
- antes-depois-botao-contacto | reel | 21.0 s | 2026-10-30 | por publicar
