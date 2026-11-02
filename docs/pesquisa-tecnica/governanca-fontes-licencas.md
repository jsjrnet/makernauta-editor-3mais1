# Governança de fontes, propriedade intelectual e integrações

**Objetivo:** possibilitar aprendizado amplo e produção de documentação própria a partir de pesquisa, **sem confundir acesso público com autorização de cópia de materiais protegidos**.

## 1. Três atos diferentes

- **Consultar e compreender:** ler repositórios, manuais, estudos e documentações, anotando **fatos técnicos, hipóteses e princípios gerais** em linguagem própria, com links e datas. Este é o padrão da base.
- **Construir solução original inspirada no aprendizado:** escrever nossa própria arquitetura, desenhos e código, com planejamento, casos de teste e validação, evitando tradução/adaptação literal da expressão de terceiros.
- **Incorporar um componente externo:** copiar, empacotar, fazer fork, instalar dependência ou distribuir um módulo identificado de terceiro **somente** com licença válida para a modalidade pretendida, controle de versões, avisos/atribuições e análise da distribuição.

Uma obra pode ser pública, gratuita ou visível no GitHub **e ainda assim ter restrições**. "Licença permissiva" não significa "sem nenhuma obrigação". Ideias gerais e técnicas não transferem por si só os direitos autorais sobre a implementação de outra pessoa.

## 2. Regra padrão de pesquisa (sem importação)

1. Acesse **preferencialmente** README, especificações, documentação de fabricante e seções de princípios técnicos.
2. Registre nome, link canônico, data, seção consultada e o problema concreto do Makernauta.
3. Escreva **síntese original**, destacando: fato conforme fonte, hipótese nossa, consequência potencial, dúvidas não resolvidas e teste que comprovaria a hipótese.
4. Não transcreva arquivos, trechos extensos, diagramas, screenshot, README integral, comentários do autor ou código fonte nas pastas de pesquisa.
5. Ao usar **recurso próprio desenvolvido com base em conceitos**, não declare que código ou tecnologia externa foram incorporados sem que isso efetivamente ocorra; não atribua exclusividade a ideias ou técnicas gerais.
6. Para qualquer artefato distribuído que contenha propriedade de terceiros, consulte os termos próprios antes de publicar.

## 3. Triagem jurídica orientativa (não é parecer)

| Origem | Regra de precaução |
|---|---|
| MIT, BSD-2/3, Boost 1.0 | Permitem vários usos proprietários **sob condições de licença e manutenção de avisos**, conforme caso |
| Apache 2.0 | Geralmente permite integração proprietária, preservando obrigações aplicáveis de avisos, modificações, NOTICE e patentes |
| LGPL 2.1/3 | **Pode** permitir integração proprietária, mas o modo de vinculação, distribuição, substituição/relink, fonte da biblioteca e alterações exigem revisão própria |
| GPL/AGPL | **Não incorporar** à base proprietária sem revisão jurídica específica; AGPL pode criar obrigações quando serviço modificado é acessado em rede |
| Sem licença / licença indeterminada | **Nenhum direito geral de copiar/adaptar/distribuir é presumido**; buscar licença, pedir autorização ou permanecer em estudo conceitual |
| Domínio público/CC0 | Reconfirmar dedicação válida, jurisdição e direitos de terceiros; não presumir ausência de outras obrigações |

**Fontes de apoio:** [GitHub — Licenciar repositório](https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository), [GNU FAQ](https://www.gnu.org/licenses/gpl-faq.en.html), [GNU LGPL 2.1](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html). São **referências**, não contratos que substituem os arquivos distribuídos pelos titulares.

A [Licença Proprietária Makernauta](../../LICENSE.md) protege apenas os componentes originais sob titularidade válida; componentes externos preservam suas licenças. Não é necessário **aplicar** nossa licença a material externo para aproveitar legitimamente uma biblioteca.

## 4. Checklist de componente candidato

Antes de acrescentar um pacote, biblioteca, asset ou ferramenta:
- [ ] Definição do problema atual e do ganho mensurável.
- [ ] Identificação do repositório, autor, versão/commit e arquivos exatos.
- [ ] Revisão de `LICENSE`, `NOTICE`, cabeçalhos dos arquivos, subdependências e recursos de terceiros.
- [ ] Registro de como o componente será usado (ferramenta de build, dependência distribuída, plugin, WASM, serviço externo).
- [ ] Verificação de compatibilidade com navegador local, offline, versão do JavaScript, plataforma e limites do PC.
- [ ] Revisão de segurança de código, cadeia de dependências, atualização e comportamento de rede.
- [ ] Reversibilidade documentada e isolamento em branch.
- [ ] Golden tests `.nc`, casos STL/Aspire, desempenho, erros geométricos, interface responsiva e ausência de regressão.
- [ ] Evidências separadas de **comportamento de código**, **visual**, **interpolação** e **máquina física**.
- [ ] Inventário de terceiros atualizado com autoria, licença, versão e aviso exigido.
- [ ] CI e revisão humana para o commit exato.
- [ ] Autorização explícita do titular do Makernauta para merge.

## 5. Modelo de atribuição (somente quando há incorporação real)

```text
Componente: <nome>
Fonte: https://github.com/<owner>/<repo>
Versão / commit: <SHA>
Licença do componente: <identificador + caminho do texto original>
Uso: <arquivo, pacote ou ferramenta>
Transformações feitas: <descrição>
Dependências/arquivos com outros direitos: <lista>
Como os avisos serão disponibilizados: <caminho e modo>
Revisão de conformidade: <responsável + data>
```

**Não adicionar uma entrada desse tipo por estudar um README apenas.** Nessa situação, registrar somente a **referência bibliográfica e hipótese técnica**.

## 6. Níveis de evidência para preservar nos documentos

- **D0 — Referência identificada:** URL, projeto e assunto.
- **D1 — Informação documental verificada:** comportamento/licença descritos por fonte relevante, sem execução.
- **D2 — Hipótese planejada:** possível aplicação no Makernauta, pendente teste.
- **D3 — Experimento isolado:** teste reproduzível fora da fundação, com entradas e resultados.
- **D4 — PR validada por CI:** testes automatizados do SHA especificado, sem homologação humana presumida.
- **D5 — Homologação humana:** proprietário confirma o SHA específico, somente para o comportamento testado.
- **D6 — Execução física validada:** exigiria protocolo separado, limites, evidências independentes e autorização expressa; **não alcançada** pelo presente projeto.

Uma hipótese D2 **nunca** deve aparecer na interface como recurso D5.

## 7. Integração com as diretrizes do repositório

Esta base é auxiliar a `AGENTS.md`, `diretriz.md` e `LICENSE.md`. Alteração de código requer PR separada, fonte identificada, baseline, testes e homologação. Não habilitar publicação automática, alterar visibilidade do repositório ou fundir uma PR pelo fato de os documentos estarem bem escritos.

## 8. Renovação de fontes e preservação do histórico

Esta base é **evolutiva e aberta a novos temas técnicos relevantes**. Revisitar projetos existentes e descobrir novas fontes são atividades legítimas, mas exigem **data da consulta, URL, versão/commit identificado e distinção entre evidência anterior e nova**. Quando uma fonte muda, registrar o que mudou e se isso afeta a recomendação, a compatibilidade ou as obrigações de licença; não apagar avaliações antigas como se nunca tivessem existido.

Novos estudos devem seguir o [protocolo de pesquisa contínua](protocolo-pesquisa-continua.md), abrir novas PRs documentais e não modificar o sistema por conta própria. Pesquisas automáticas ou programadas não estão habilitadas por este documento; só podem existir com configuração e consentimento específicos. O inventário de componentes realmente **incorporados** deve permanecer separado do catálogo de projetos **apenas estudados**.

## 9. Preservação de autoria do próprio Makernauta

A redação técnica original produzida nesta pasta faz parte da documentação do Makernauta, observadas as licenças e direitos externos. Uma referência/citação não torna automaticamente o texto de terceiro "nosso". O conteúdo desta pasta não é oferta de licenciamento do código de terceiros.
