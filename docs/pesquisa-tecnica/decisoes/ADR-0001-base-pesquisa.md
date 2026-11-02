# ADR-0001 — Base de conhecimento e pesquisa CNC 3+1 / XYZA

- **Data:** 2026-11-01
- **Status:** **Proposta — aguardando revisão e eventual incorporação da PR documental**
- **Origem:** solicitação do proprietário do Makernauta de manter pesquisa útil e permanente no GitHub
- **Fundação de origem:** `63df8e1df537af4cdf969de193395cbafe7f2113`
- **Escopo:** documentação do Editor de Usinagem Indexada 3+1 e pesquisa futura de XYZA simultâneo

## Problema

Repositórios e referências relevantes foram encontrados em pesquisa, mas informações dispersas em conversas e arquivos baixados dificultam comparar soluções, verificar licenças, conservar decisões e selecionar experimentos sem regressões.

## Fontes e contexto

O [relatório inicial de 01/11/2026](../relatorio-original-2026-11-01.md) contém o primeiro levantamento. O [catálogo atualizado](../catalogo-repositorios.md) destaca projetos, documentação de fabricantes e situações de licenças. O repositório Makernauta preserva `AGENTS.md`, `diretriz.md` e licença proprietária.

## Decisão proposta

Estabelecer uma área permanente `docs/pesquisa-tecnica/` que:

1. Preserve resultados de estudos com URLs, datas e estado de evidência.
2. Registre sínteses, análises e documentos **originais** em português, sem cópia de código externo.
3. Separe conhecimento de **incorporação real de dependências e redistribuição**.
4. Classifique cada experimento como isolado, validado, homologado ou pendente.
5. Utilize ADRs para decisões de arquitetura relevantes.
6. Mantenha o Editor 3+1 como base protegida e o XYZA como pesquisa independente.
7. Subordine toda execução e merge às diretrizes existentes.

## Alternativas ponderadas

- **Continuar apenas em conversas e arquivos locais:** rápido, mas dificulta histórico, referências estáveis e busca.
- **Copiar um CAM externo inteiro:** exposição imediata a custo, incompatibilidades, licenças e regressões.
- **Documentação/versionamento no próprio GitHub (proposta):** permite rastreabilidade, revisão por PR e aprendizagem sem mexer no motor.

## Consequências previstas

**Vantagens:** histórico consultável por colaboradores autorizados, melhor rastreio de licenças, testes mais objetivos e menor risco de refatoração precipitada.

**Limites:** referências e licenças mudam; a pesquisa não substitui benchmark, revisão jurídica, ensaio na máquina ou atualizações manuais.

## Critérios de aceite para esta ADR

- Branch separada e somente documentação/README.
- Nenhum novo script, dependência, fonte de terceiro, UI, G-code ou alteração de infraestrutura.
- URLs de referência, critérios de licença, priorização e decisões futuras presentes.
- Revisão pelo titular e merge autorizado; aprovação de texto não implica autorização de outras implementações.

**Situação:** aguardando homologação desta PR documental, sem solicitação de alteração operacional.
