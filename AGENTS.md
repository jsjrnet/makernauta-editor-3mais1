# Makernauta — regra de homologação funcional

- Preserve `editor-usinagem-indexada.html` e trabalhe em branch separada; entregue PR para avaliação.
- Nenhuma atualização é homologada apenas porque CI/testes automatizados passaram.
- Antes de propor incorporação à `main`, disponibilize uma prévia navegável do commit atual e aguarde a avaliação funcional de Juarez Jr. (`jsjrnet`).
- A aprovação funcional corresponde ao SHA testado. Novo commit exige nova prévia e nova avaliação; nunca reutilize uma aprovação de versão anterior.
- A automação registra um comentário do usuário configurado `Homologado funcionalmente: <SHA completo>`, ou uma revisão GitHub **Approve** com a frase `Homologado funcionalmente` para o mesmo commit. O comentário permite avaliar PRs do próprio usuário, pois o GitHub não permite autoaprovação. Checklists preenchidos pelo autor ou aprovação de bots não substituem essa avaliação.
- Nunca publique a confirmação funcional em nome do usuário nem interprete testes automatizados como sua avaliação manual.
- Não faça merge automático nem publique o Pages oficial como forma de testar PR. Não altere proteções de branch ou conecte contas externas sem a autorização correspondente.
- A homologação é da interface e do software; o G-code continua experimental e não homologado para execução física em CNC.
