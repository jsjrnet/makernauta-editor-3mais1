# PR #7 — Experiência guiada e importações previsíveis

## Objetivo
Reduzir a confusão dos usuários novos do Makernauta — Usinagem Rotativa. Organizar a interface por tarefas e separar dados importados, opções de edição, cálculos e comandos CNC.

## Escopo aprovado para desenvolvimento incremental
1. Fluxo principal: **Preparar trabalho → Criar operações → Simular → Exportar CNC**. Navegação não deve forçar etapas ou remover o acesso às vistas atuais.
2. **Operação selecionada**: agrupar Geometria, Posicionamento, Estratégia/Profundidade e Ferramenta. O ajuste de grade é do editor desenrolado; Y desenrolado é informação auxiliar; uso do STL para profundidade é opção avançada que *altera* cálculo (não é apenas decoração).
3. **STL de demonstração**: dois exemplos internos (Isca Natan 63 mm simplificada por amostragem do STL original e peão de xadrez), identificados como ilustrações, com ação para carregar e baixar .stl sem internet. Não equipará-los ao STL real do Aspire.
4. **Assistente Aspire**: reconhecer apenas informações explicitamente declaradas no cabeçalho (Ø e L do bruto e ferramenta), apresentá-las para revisão; não inferir origem Z0 a partir de alturas de movimento. A aplicação dos valores deve exigir ação do operador.
5. **STL**: separar dimensões da peça final do material bruto; adicionar translação X e preservar controles de rotação/inversão.
6. **Inspeção**: mudar “A visual” para “Girar A”, preservar passos de 15° e revisar orientação aparente dos botões.
7. **Artefatos da simulação combinada**: caracterizar as pequenas saliências sem presumir erro nas trajetórias XYZ indexadas; verificar representação de superfície por testes comparativos antes de qualquer correção.
8. **Manual introdutório**: explicar conceitos e passos de teste com arquivos internos.

## Regras e limites
- **Não alterar** as trajetórias CAM, o cálculo de usinagem indexada, os modos de máquina, os comandos CNC ou o pós-processamento Mach3 homologados nas PRs #5 e #6.
- Eixo A posiciona e fica parado durante XYZ; escultura rotativa Aspire XZA é importada, não gerada pelo editor indexado.
- Não utilizar o arquivo STL como prova do Z0 do G-code.
- Distinguir **exemplo** de **trabalho real**. Não aplicar medidas aleatórias de demonstração ao programa definitivo.
- Usinar em máquina física não está homologado.

## Estratégia de entrega
Desenvolvimento incremental **na mesma PR #7**, com primeiro incremento: navegação, agrupamento, modelos STL integrados e manual inicial. A leitura assistida de dados Aspire e o deslocamento X do STL já estão no mesmo incremento. A investigação visual das saliências e o modo de projeto novo continuam pendentes. Toda revisão altera SHA, exigindo nova prévia e homologação humana; **sem merge automático**.
