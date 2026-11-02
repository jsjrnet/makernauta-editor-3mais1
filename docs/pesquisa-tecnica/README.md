# Makernauta — Base de conhecimento e pesquisa técnica CNC

**Base de conhecimento viva, cumulativa e aberta a novas descobertas.** Iniciada em 01/11/2026, a partir da fundação `63df8e1df537af4cdf969de193395cbafe7f2113`. O levantamento inicial **não limita** as tecnologias, os módulos ou as pesquisas futuras. Toda nova investigação relevante poderá ampliar esta documentação por PR.

## Finalidade

Reunir informação verificável e **redação técnica original do Makernauta** para orientar melhorias no editor de **Usinagem Indexada 3+1** e o estudo independente de **usinagem XYZA simultânea**. As referências externas servem para pesquisa, comparação de estratégias, avaliação de bibliotecas e criação de nossas próprias propostas. **Esta pasta não importa código de terceiros, não instala dependências, não modifica o editor nem homologa G-code de máquina.**

## Continuidade e ampliação

Esta pasta foi concebida para **evoluir continuamente mediante novas buscas, revisões de fontes, descobertas e decisões**, inclusive sobre temas que não constam do primeiro relatório. Consulte o [Protocolo de pesquisa contínua](protocolo-pesquisa-continua.md) para saber quando pesquisar, como registrar uma descoberta, como evitar duplicatas, como preservar o histórico e como incorporar novas trilhas sem alterar o código operacional.

**Importante:** ser uma base viva não significa que buscas recorrentes ou alterações automáticas já estejam ativadas. Elas dependerão de rotina ou automação definida separadamente. A PR #11 é o marco inicial; após sua integração, **cada rodada posterior de pesquisa deverá criar uma nova PR**, preservando a rastreabilidade e a revisão do proprietário.

## Comece por aqui

| Documento | Use quando... |
|---|---|
| [Protocolo de pesquisa contínua](protocolo-pesquisa-continua.md) | Abrir novos ciclos de busca, ampliar assuntos, revisar fontes e registrar novidades sem perder o histórico |
| [Catálogo de tecnologias e repositórios](catalogo-repositorios.md) | Procurar ferramentas, confirmar escopo, verificar licenças e selecionar uma referência |
| [Arquitetura e fundamentos CNC 3+1 / XYZA](arquitetura-3mais1-xyza.md) | Planejar a separação entre geometria, trajetória, simulação, máquina e pós-processamento |
| [Roteiro de experimentos e critérios de aceite](roteiro-experimentos.md) | Transformar uma ideia em experimento isolado, teste de regressão e proposta de PR |
| [Proveniência, direitos e governança](governanca-fontes-licencas.md) | Distinguir ideias, código externo reutilizável, obrigações legais e política de incorporação |
| [Modelo de registro de decisão](modelo-registro-de-decisao.md) | Documentar por que uma tecnologia foi aceita, adiada ou rejeitada |
| [ADR-0001 — Estabelecimento da base de pesquisa](decisoes/ADR-0001-base-pesquisa.md) | Ver o escopo de governança proposto para esta área |
| [Relatório original de 01/11/2026](relatorio-original-2026-11-01.md) | Consultar o primeiro levantamento completo, preservado como documento histórico |

## O que é realidade no projeto

- **Implementado e homologado na base referenciada:** editor HTML autossuficiente, operações 3+1 com A indexado/parado no corte XYZ, importação opcional Aspire XZA, referências STL, simulação aproximada, exportação experimental Mach3.
- **Ainda não implementado:** planejar/fresar com movimento simultâneo coordenado X, Y, Z e A.
- **Ainda não comprovado:** execução física segura de programas gerados, colisões físicas e capacidades exatas do Mach3/porta paralela/HC74 em XYZA contínuo.
- **Não confundir:** uma descrição de ferramenta externa, uma hipótese nossa e uma capacidade testada no Makernauta são três níveis diferentes de evidência.

## Regras da base de conhecimento

1. Registrar **origem, URL, data de consulta, licença declarada e ponto do projeto** que inspirou cada análise.
2. Escrever em palavras próprias. **Não reproduzir código-fonte, screenshots, figuras, textos longos ou arquivos externos** nesta base sem avaliação específica de permissão e necessidade.
3. Distinguir `verificado documentalmente`, `hipótese`, `protótipo isolado testado`, `validado por CI`, `homologado pelo proprietário` e `validado fisicamente`.
4. Tratar licenças de terceiros como vigentes **para seus componentes**, mesmo quando houver integração permitida ao software proprietário.
5. Toda mudança executável deve usar **PR própria**. Uma PR de pesquisa não aprova nem implanta automaticamente bibliotecas, algoritmo, pós-processador ou novo recurso.
6. Preservar `AGENTS.md`, `diretriz.md`, `LICENSE.md`, a fundação e as regras de homologação por SHA; esta base complementa esses documentos, nunca os substitui.
7. Não colocar dados particulares da máquina, fotos de terceiros, arquivos protegidos nem informações sensíveis no repositório sem autorização.

## Como atualizar

A base **não é limitada à pesquisa inicial**, nem requer que uma nova tecnologia já conste do catálogo para ser investigada. Para cada novo assunto: buscar a fonte primária; registrar a ficha e data de revisão; escrever **o problema do Makernauta** e a hipótese; abrir registro de decisão quando houver escolha de arquitetura/licença; propor experimento mensurável; guardar resultados; atualizar conclusão e data. Descobertas, alterações de licença, mudanças de manutenção, novas necessidades e revisões periódicas autorizadas podem iniciar outro ciclo.

A manutenção posterior à PR #11 é feita por **novas PRs**, com revisão do proprietário; novos commits nesta PR enquanto estiver aberta alteram seu SHA e devem ser reavaliados. A pesquisa não substitui uma decisão de implementação. O fluxo detalhado está no [protocolo de pesquisa contínua](protocolo-pesquisa-continua.md).

**Rota de adoção inicial recomendada:** auditoria não destrutiva de G-code → offsets 2D → consultas em STL → simulação XYZA independente → estudo de pós-processador condicionado a perfil real de máquina. Isto é um **roteiro de pesquisa**, não autorização de execução.
