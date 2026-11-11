# Fila de carrosséis da Destaca

Carrosséis já prontos em `posts/<slug>/` (`01.jpg` … `07.jpg` + `legenda.txt`). Num horário de feed em que calhe carrossel (ver `feed.md`), publica-se o próximo desta fila em vez de gerar um novo. Só se gera um carrossel novo quando não houver nenhum "por publicar".

**Ordem de publicação:**
1. Primeiro, os itens `por publicar · prioridade até AAAA-MM-DD` cuja data ainda não passou (pela ordem desta lista).
2. Depois, o primeiro `por publicar` normal desta lista (de cima para baixo).
3. Item com `até AAAA-MM-DD` já passada → não publicar; trocar o estado para `expirado`.
Ao publicar, troca o estado para `publicado AAAA-MM-DD` (apagando o resto) e acrescenta a linha a `feed.md`.

Formato: `slug | tipo | adicionado | estado`

- bf-desconto-nao-e-estrategia | carrossel | 2026-11-04 | publicado 2026-11-05
- bf-negocio-local-ganha-as-grandes | carrossel | 2026-11-04 | publicado 2026-11-11
- bf-erros-que-perdem-vendas | carrossel | 2026-11-04 | por publicar · prioridade até 2026-11-27
- boca-a-boca-acaba-no-google | carrossel | 2026-11-04 | por publicar
- descricao-do-perfil-google | carrossel | 2026-11-04 | por publicar
- perguntas-que-o-site-deve-responder | carrossel | 2026-11-04 | por publicar
- mitos-de-seo | carrossel | 2026-11-04 | por publicar
- fotos-que-vendem | carrossel | 2026-11-04 | por publicar
- frases-para-trocar-no-site | carrossel | 2026-11-04 | por publicar
- sinais-de-confianca | carrossel | 2026-11-04 | por publicar
- descobrir-palavras-chave-locais | carrossel | 2026-11-04 | por publicar
- antes-depois-pagina-de-oficina | carrossel | 2026-11-04 | por publicar
- menos-opcoes-mais-pedidos | carrossel | 2026-11-04 | por publicar
- lancaste-o-site-verificacoes | carrossel | 2026-11-04 | por publicar
- seo-local-quanto-tempo-demora | carrossel | 2026-11-04 | por publicar
- kit-minimo-profissional-online | carrossel | 2026-11-04 | por publicar
- erros-que-escondem-o-site | carrossel | 2026-11-04 | por publicar
- o-que-publicar-no-perfil-google | carrossel | 2026-11-04 | por publicar
- instagram-e-google-juntos | carrossel | 2026-11-04 | por publicar
- rotina-mensal-15-minutos | carrossel | 2026-11-04 | por publicar
