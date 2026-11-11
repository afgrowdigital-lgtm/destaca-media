# Registo do feed da Destaca (carrosséis e Reels)

Uma linha por publicação no feed: `AAAA-MM-DD | carrossel|reel | pasta`.
Regra de alternância: num horário de feed, se a última linha for `carrossel` e houver um reel "por publicar" em `videos/fila.md`, publica-se o reel; caso contrário, carrossel — o próximo de `posts/fila.md` (só se gera um novo quando essa fila estiver vazia).

- 2026-10-28 | carrossel | posts/2026-10-28-invisivel-no-google
- 2026-10-28 | carrossel | posts/2026-10-28-4-mitos-sites
- 2026-10-28 | carrossel | posts/2026-10-28-anatomia-pagina-que-vende
- 2026-11-04 | reel | videos/teste-do-mapa-google
- 2026-11-04 | reel | videos/porque-escolheu-o-concorrente
- 2026-11-05 | carrossel | posts/bf-desconto-nao-e-estrategia
- 2026-11-10 | reel | videos/bf-promocao-que-ninguem-ve
- 2026-11-11 | carrossel | posts/bf-negocio-local-ganha-as-grandes
