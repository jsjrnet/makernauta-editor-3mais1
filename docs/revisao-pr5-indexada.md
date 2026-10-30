# PR #5 — Interface de inspeção da usinagem indexada

## Definição funcional confirmada

**Não existe defeito de usinagem causado pelo cilindro permanecer parado durante o corte.** Essa é a finalidade do módulo indexado 3+1: A posiciona o cilindro, para, e XYZ executa o corte em geometria cartesiana. O modo XZA simultâneo é uma estratégia diferente, reservada para estudos futuros. O G-code permanece experimental e não homologado em máquina física.

**O simulador e a malha usados na base oficial foram restaurados nesta PR.** A alteração anterior que tentava unir superfícies radiais como uma suposta correção de malha foi retirada porque se baseou numa interpretação equivocada da solicitação. Não alterar a estratégia, a geometria ou o resultado dos cortes para fazê-los parecer usinagem rotativa simultânea.

## Melhorias mantidas

- Controles visuais esquerda/direita da vista 3D, em passos de 15°, sem alterar A0/Z0, geometria, G-code, progressão da simulação ou material removido.
- Painéis laterais sem numeração nos títulos e com setas de expansão visíveis mesmo quando recolhidos; preservar pinos, modo temporário e comandos por teclado.
- Correção textual do comentário de operações do tipo **Linha** no programa CNC, antes rotuladas como `retangulo`, sem mudar movimentos ou trajetórias.
- Correção técnica do verificador de prévias Cloudflare para aceitar apenas a URL canônica do mesmo domínio, sem reduzir a verificação de SHA/manifesto.

## Removido do escopo

- Spline: retiradas edição, desenho por mouse, geração de movimentos, controles e testes; desnecessária para as geometrias básicas do módulo.
- Qualquer mudança de malha, superfície cilíndrica, representação dos alojamentos ou simulação de remoção com pressuposto de que a usinagem indexada seria defeituosa.
- Testes que impunham a nova malha como requisito funcional.

## Homologação

Verificar botões de inspeção do A, setas e recolhimento dos painéis, rotulagem da operação Linha, importação Aspire/STL, comportamento do simulador **inalterado** e programa CNC com mesmos movimentos. Comparar `.nc` da base e da prévia, excetuando apenas o comentário descritivo da Linha.

Esta PR só pode ser incorporada após testes e avaliação funcional humana da prévia Cloudflare do SHA atual. **Sem merge automático**.

A padronização do nome **Makernauta — Usinagem Rotativa** está na PR #6 e será avaliada separadamente.
