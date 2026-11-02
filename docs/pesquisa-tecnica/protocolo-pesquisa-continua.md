# Protocolo de pesquisa contínua e evolução do conhecimento

**Status:** proposta documental integrante da PR que institui a base técnica Makernauta. **Este protocolo não instala um robô de pesquisa, não aciona buscas automaticamente e não autoriza mudanças de código.**

## 1. Compromisso: acervo vivo, não estudo encerrado

A pesquisa iniciada em 01/11/2026, sobre 3+1 indexado e XYZA simultâneo, é **a primeira edição**, não um limite de conteúdo ou uma lista definitiva de tecnologias. A pasta `docs/pesquisa-tecnica/` serve como **ponto permanente de partida** para novas descobertas e revisões técnicas relacionadas ao Makernauta — Usinagem Rotativa e a eventuais módulos de fabricação digital que o projeto venha a incorporar.

Não existe data de encerramento do catálogo. Uma tecnologia pode ser descoberta, revista, descartada, retomada, substituída ou tornar-se útil após mudanças no sistema ou na máquina.

**Princípio operacional:** a pesquisa se amplia por ciclos de investigação e **novas PRs documentais**, mantendo a PR inicial como marco histórico. **Não se deve editar ou reabrir a PR #11 depois de integrada** para acumular todo o trabalho futuro.

## 2. Escopo aberto, mas vinculado a problemas reais

As trilhas abaixo são **exemplos de áreas possíveis**, não autorização de implementação nem limitação de assuntos:

| Trilha | Exemplos de perguntas |
|---|---|
| Geometria, CAM e pós-processamento | Há bibliotecas mais robustas para offset, arcos, estratégias, interpolação e interpretação G-code? |
| Simulação e inspeção CNC | Como comparar remoção volumétrica, contato da fresa, visualização de STL, artefatos e colisões? |
| 3+1 e movimento multieixos | Como documentar XYZA, referenciais, transformação cinemática, avanços e perfis de máquina? |
| Interface e acessibilidade | Há métodos e ferramentas que tornem o editor mais legível, responsivo e operável sem regressões? |
| Posicionamento, registro e fabricação | Quais conceitos ajudam a estudar alinhamento por marcas, sensores, laser de referência ou processos híbridos? |
| Qualidade, testes e segurança | Como testar com mais evidências G-code, desempenho, inputs malformados, dependências e publicação? |
| Documentação, licenças e arquitetura | Como melhorar nossas diretrizes, manuais, decisões e compatibilidade com software proprietário? |
| Novas frentes aprovadas pelo proprietário | Adicionar temas conforme surgirem necessidades; registrar justificativa e responsável pela revisão. |

**Critério para abrir uma nova trilha:** conseguir relacioná-la a um problema, hipótese ou objetivo técnico concreto do Makernauta. Informações sobre outros produtos independentes (por exemplo, um ERP) exigem base e governança próprias, não contaminação de escopo.

## 3. Quando realizar novas buscas

Uma rodada de pesquisa pode ser disparada por:

1. **Demanda de desenvolvimento:** antes de iniciar módulo, correção de arquitetura ou solução para problema conhecido.
2. **Descoberta externa:** novo repositório, edição importante, artigo, manual, discussão técnica ou mudança de padrão.
3. **Mudança de risco:** licença alterada, abandono de manutenção, vulnerabilidade, incompatibilidade ou dependência descontinuada.
4. **Resultado experimental:** um teste revela novas perguntas, limitações ou alternativas.
5. **Revisão periódica opcional:** revisão de fontes prioritárias, por exemplo mensal ou trimestral, **somente se agendada/autorizada separadamente**.

**O GitHub não fará pesquisas novas por conta própria apenas porque este documento existe.** A execução de buscas recorrentes precisa de uma rotina humana ou automação efetivamente configurada, com escopo, cadência, permissões e responsável. Um agendamento futuro deve preferir **relatórios e propostas de atualização**, nunca merge automático ou importação de código.

## 4. Ciclo obrigatório de investigação

| Passo | Entrega mínima | Regra |
|---|---|---|
| **Capturar** | Pergunta, trilha, motivação e data | Evitar pesquisa genérica sem propósito |
| **Descobrir** | Fontes primárias: documentação de fabricante, projeto, release, LICENSE/NOTICE, especificação | A fonte pode mudar: conferir a versão |
| **Triar** | Tecnologia, manutenção, licença, dependências, compatibilidade, qualidade da evidência | Ausência de licença **não** é permissão |
| **Sintetizar** | Redação original; conceitos, limitações e hipótese aplicada ao Makernauta | Não transplantar texto/código protegido |
| **Comparar** | Alternativas, benefícios, custos, riscos, teste mínimo e possível reversão | Uma ferramenta famosa não é automaticamente a melhor |
| **Registrar** | Atualizar catálogo, roteiro, ADR e/ou nota de investigação | Evitar duplicatas e preservar histórico |
| **Revisar** | PR exclusivamente documental e aprovação do proprietário | Não alterar `main` diretamente |
| **Experimentar depois** | Nova PR própria, ambiente isolado e testes antes/depois | Uma aprovação de pesquisa **não** homologa código |

## 5. Como manter o catálogo realmente atualizado

Para cada tecnologia estudada, registrar pelo menos:

- **ID estável** (por exemplo, `FONTE-0001`) e nome/URL oficial; nunca reutilizar um ID.
- Categoria/trilha e **problema Makernauta** ao qual se relaciona.
- Data de descoberta, data da **última verificação** e versão/commit analisado quando houver.
- Licença observada, onde foi consultada, ressalvas de terceiros e permissões ainda não examinadas.
- Tipo de evidência: ideia, documentação verificada, experimento, teste, aprovação de produção; não exagerar o estágio.
- Situação: `novo`, `em análise`, `candidato a experimento`, `em teste`, `incorporado`, `descartado`, `arquivado/descontinuado`.
- Ganhos e limitações técnicas, link para ADR/experimento/PR, **próximo passo** e responsável.
- Registro das mudanças relevantes desde a avaliação anterior.

**Revisão de referência não apaga o histórico:** se uma licença ou característica mudar, registrar a data e razão; se a fonte desaparecer, marcar como indisponível sem inventar condições passadas.

As fichas individuais poderão ser criadas conforme o volume justificar; o catálogo existente continua válido como visão resumida.

## 6. Ficha de uma nova descoberta

```text
ID:
Data de descoberta:
Trilha:
Problema/objetivo do Makernauta:
Nome e URL oficial:
Repositório principal / licença / NOTICE:
Versão, tag ou SHA consultado:
Última verificação:
Fatos verificados na fonte:
Ideias e hipóteses nossas (claramente separadas):
Aplicabilidade: 3+1 | XYZA | transversal | outra trilha:
Benefício mensurável:
Complexidade, dependências, riscos e reversibilidade:
Lacunas de informação:
Status e próximo passo:
Referências de relatório, ADR, experimento e PR:
Resultado de revisões futuras:
```

## 7. Política de expansão e de incorporação

- **Adicionar conhecimento:** proposta de arquivo, ficha, ligação entre documentos ou ADR por PR de pesquisa.
- **Pesquisar código externo:** permitido analisar sua documentação e funcionamento; copiar/redistribuir código, diagramas ou trechos exige análise de licença e necessidade.
- **Aproveitar diretamente componentes:** somente em PR de implementação separada, após verificação de direitos, avisos e dependências, com testes e homologação.
- **Melhorar tecnologia já existente:** comparar implementação atual, casos-limite e custo de manutenção antes de trocar componentes.
- **Escopo novo:** cadastrar nova trilha sem remover o histórico anterior; permitir que decisões futuras supersedam uma ADR por outra, sem reescrever o passado.
- **Governança:** `AGENTS.md`, `diretriz.md` e `LICENSE.md` continuam válidos. O catálogo **não concede** direito de merge, publicação ou execução de máquina.

## 8. Como demonstrar que a base continua viva

Em cada ciclo concluído, o registro ou PR deve conseguir responder:

1. **O que foi descoberto ou revisto desde a edição anterior?**
2. **Qual problema nosso a informação pode resolver?**
3. **Qual fonte, licença e evidência justificam a conclusão?**
4. **O que ainda não sabemos e como testar?**
5. **O que foi incorporado realmente — se algo foi — e em qual SHA/PR?**

**Resultado pretendido:** uma biblioteca de conhecimento evolutiva, auditável e útil em novas decisões, sem prometer monitoramento automático que não foi configurado e sem alterar a fundação operacional sem autorização.
