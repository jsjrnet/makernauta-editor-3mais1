# DIRETRIZ OPERACIONAL — Makernauta / Usinagem Rotativa

**Vigência:** após aprovação e incorporação desta diretriz à `main`.  
**Autoridade:** proprietário do projeto (`jsjrnet`).  
**Fundação de referência da ocorrência:** `main` no commit `3cdbca1ab2e57e442beadda8ec84998edd10fca7`.  
**Âmbito:** ChatGPT, Codex Cloud, GitHub, GitHub Actions, prévias Cloudflare e eventuais outros agentes.

## 1. Motivo e lições da PR #7 (31/10/2026)

A PR #7 foi encerrada **sem merge** após erros visuais no simulador 3D. Os testes de CI foram aprovados, mas **não comprovaram qualidade visual** no cenário real Aspire + operações indexadas. A tentativa de transferir correções complexas ao Codex falhou antes do início da execução com `No usable execution environment`, inclusive no comando `pwd`.

**Causa operacional comprovada:** a passagem ao Codex foi recomendada sem uma verificação efetiva da disponibilidade do seu ambiente. **Não há evidência de que a falha do ambiente do Codex tenha sido causada pelo projeto.** A causa interna do serviço não foi diagnosticada. GitHub API, GitHub Actions e Codex Cloud são ambientes diferentes; o funcionamento de um não prova o do outro.

A PR encerrada fica somente como referência de auditoria; suas alterações **não compõem a fundação validada**. Nenhuma tarefa poderá presumir que um ambiente de desenvolvimento está disponível apenas porque outros serviços estão funcionando.

## 2. Regras inegociáveis

1. **Fundação imutável até aprovação:** registrar antes de cada trabalho o SHA completo da `main`, a branch de origem e o estado das PRs. É proibido desenvolver diretamente na `main` quando houver exigência de revisão.
2. **Uma mudança identificável por vez:** usar branch específica e PR revisável; não reutilizar uma branch encerrada com código reprovado sem nova autorização e auditoria.
3. **Sem merge automático:** CI verde, prévia publicada, agente satisfeito ou checklist preenchido não substituem homologação humana. Somente o proprietário autoriza a integração do **SHA exato** testado.
4. **Preservar G-code:** mudança gráfica não pode modificar trajetórias, Z0, A, estratégias de usinagem, comandos Mach3 nem formato de exportação. Provar invariância por testes de comparação quando pertinente.
5. **Sem garantia física:** simulação, folga visual e testes automatizados não homologam colisões, ferramentas, fixação, ou execução numa CNC real.
6. **Informação honesta:** distinguir claramente implementado, testado, publicado, homologado e integrado. Não declarar "concluído" antes de todos os critérios exigidos.
7. **Falha é bloqueio, não autorização para improvisar:** indisponibilidade de ferramentas impede execução; deve ser declarada com o erro observável. Não prometer reparos futuros ou mudanças que ainda não ocorreram.

## 3. Pré-voo obrigatório ANTES de delegar ou editar

### 3.1 Identificação

Registrar: objetivo, arquivos afetados, branch e SHA de origem, condições de aceite, testes previstos, risco de regressão, responsável e plano de rollback.

### 3.2 Verificação do ambiente executor

O executor deve comprovar **no seu próprio ambiente**, e não por resultados de outro serviço:

- Acesso funcional ao repositório correto;
- Capacidade de ler a árvore de arquivos e branch pretendida;
- Capacidade de executar comandos simples, quando sua tarefa exigir shell;
- Capacidade de executar testes essenciais ou justificativa concreta da limitação.

Para Codex Cloud, começar com **uma única tentativa curta** de:

```bash
pwd
git status -sb
git rev-parse --show-toplevel
git rev-parse HEAD
```

**Se houver "No usable execution environment", "offline" ou falha equivalente: PARAR imediatamente.** Não enviar tarefa longa, não repetir inicializações em sequência, não afirmar que a situação foi resolvida e não orientar criação de novos ambientes sem diagnóstico e consentimento. Registrar erro exato, identificador da tarefa e o que efetivamente foi executado.

**GitHub Actions verde não comprova disponibilidade do Codex Cloud.** ChatGPT conectado ao GitHub também não comprova a disponibilidade do Codex Cloud. Verificação do status geral de um serviço não substitui o teste do ambiente da tarefa.

Se não for possível executar o pré-voo por limitações de acesso, comunicar explicitamente "ambiente não verificado" e **não delegar** até haver verificação efetiva.

## 4. Contrato de desenvolvimento e critérios de aceite

Antes de alterar código, descrever o defeito reproduzível, os passos exatos para reproduzi-lo, dados de entrada, resultado esperado e captura de referência quando visual.

Para simulação 3D, exigir pelo menos:

- Resultado em escultura Aspire isolada, operações indexadas isoladas e modo combinado, conforme escopo;
- Inspeção do alojamento problemático em pelo menos duas orientações de câmera e ao longo do avanço da animação;
- Comparação visual antes/depois do **mesmo cenário e parâmetros**, sem ocultar faces ou sobreposições para mascarar defeitos;
- Evidência de funcionamento das ferramentas ballnose e topo reto quando afetadas;
- Checagem de posição de fresa/chuck/contraponto e distinção entre folga visual e segurança real;
- Comparação do G-code e dos dados geométricos quando uma alteração for exclusivamente visual.

**Testes automatizados demonstram somente o que verificam.** Invariantes numéricas e renderização sem exceções não provam ausência de saliências, colisões aparentes ou defeitos visuais.

O usuário deve ter oportunidade de **enviar capturas, imagens e relatar defeitos antes de fechar a rodada de homologação**. Um checkbox desmarcado significa "não confirmado", e não reprovação automaticamente diagnosticada.

## 5. Fluxo obrigatório de validação

1. **Baseline:** confirmar SHA de `main`, branch e arquivos.
2. **Pré-voo:** comprovar ambiente executor e seus limites.
3. **Diagnóstico:** isolar a causa e fornecer hipótese testável antes de alterar rotinas sensíveis.
4. **Mudança mínima:** registrar commit com escopo; não misturar correções visuais e CAM.
5. **CI/regressão:** todos os testes relevantes aprovados no SHA atual; tratar falhas antes de continuar.
6. **Prova visual:** capturas ou vídeo reproduzível do defeito antes/depois, com parâmetros e arquivo de teste identificados.
7. **Prévia imutável:** publicar URL para o SHA preciso e aguardar avaliação humana **com espaço para anexos**.
8. **Homologação:** somente o proprietário confirma funcionalmente o SHA atual; um novo commit invalida aquela confirmação.
9. **Merge:** somente após confirmação explícita de autorização e verificações finais de HEAD/CI/revisão.
10. **Checkpoint:** registrar resultado, SHA integrado, alterações e limitações para a próxima fundação.

Nenhuma etapa posterior substitui uma anterior não concluída.

## 6. Contenção, rollback e consumo de recursos

- Se um ajuste **piorar** o defeito reportado, interromper novas melhorias e examinar/reverter o commit problemático na própria branch, com comparação antes/depois. Não empilhar remendos sem evidência.
- Após **duas tentativas de correção visual reprovadas**, suspender implementação até haver novo diagnóstico reproduzível. Isso não impede investigação sem alterações.
- Antes de alterar arquivos ou publicar, registrar como será restaurado o último SHA aprovado. Não usar `reset --hard`, `push --force` nem excluir branch compartilhada sem avaliar impacto e receber autorização explícita.
- Fechar uma PR **sem merge** não apaga seu histórico e não é o mesmo que excluir a branch. Nunca declarar "exclusão completa" quando apenas a PR foi encerrada.
- Não repetir chamadas a Codex Cloud indisponível ou executar testes extensos em loops de tentativa. Primeiro comprovar funcionamento com teste mínimo; somente depois consumir recursos no diagnóstico/implementação.
- Quando uma ação depender de ferramenta indisponível, informar a limitação concreta e a ação manual mínima, sem afirmar que já foi realizada.

## 7. Papéis e registros de evidência

**Proprietário:** define requisitos, avalia imagens e software, homologa ou rejeita, autoriza merge e mudanças de proteção.

**ChatGPT/agentes:** analisam, implementam somente no escopo autorizado, preservam evidências, relatam falhas e pedem homologação. Nenhum agente pode declarar aprovação em nome do proprietário.

**GitHub Actions:** executa verificações automatizadas; não homologa ergonomia, defeitos visuais ou segurança física.

**Codex Cloud:** somente recebe tarefa depois de seu próprio pré-voo comprovado; indisponibilidade de Codex não invalida GitHub nem CI, mas bloqueia delegação ao Codex.

Em toda entrega, apresentar SHA, URL da branch/PR, CI correspondente, prévia do mesmo SHA, evidências visuais, itens pendentes e situação de merge.

## 8. Segurança e comunicação

- Não alterar a configuração de acesso, proteção de branch, visibilidade, infraestrutura ou permissões sem autorização expressa.
- Nunca incorporar ao GitHub imagens privadas ou dados de máquina não autorizados.
- Comunicar de forma objetiva, em português, o que foi **realmente feito**, o que **não foi possível** e por quê.
- Caso uma ferramenta ou função não exista, não inventar capacidade nem pedir reinicializações sem evidência.
- Esta diretriz **reduz riscos, mas não garante impossibilidade absoluta de novas falhas**. Qualquer incidente deve gerar revisão documentada desta política, preservando auditoria.

## 9. Relação com outras regras

Esta diretriz complementa `AGENTS.md`, `README.md`, testes e proteção de `main`. Em caso de dúvida, aplicar a exigência de maior proteção, sem alterar regras existentes de homologação. O arquivo principal `editor-usinagem-indexada.html` e a fundação CNC validada permanecem fora do escopo desta mudança documental.
