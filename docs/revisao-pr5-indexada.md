# PR #5 — Inspeção A, painéis e malha 3D da usinagem indexada

## Escopo consolidado

Este módulo continua **indexado 3+1**: A posiciona o cilindro e permanece imóvel nos cortes cartesianos XYZ. Não implementar XZA simultâneo nesta PR. O programa CNC permanece experimental e não homologado em máquina física.

- Inspeção visual Left/Right de 15° na vista 3D, sem modificar a programação de A, as dimensões, a remoção, o programa CNC ou o tempo da simulação. Vista inicial também zera a orientação.
- Títulos dos grupos laterais sem numeração. Setas visíveis nas abas recolhidas; manter pinagem, expansão temporária e teclado.
- Corrigir o comentário do G-code de operações do tipo **Linha**, antes identificado incorretamente como `retangulo`. Não mudar as trajetórias da máquina.
- Malha de visualização 3D unificada: a mesma superfície radial é construída a partir da remoção acumulada. Não sobrepor planos cartesianos independentes que poderiam criar fissuras visuais nas interseções. A inspeção cartesiana detalhada de 0,15 mm permanece independente e disponível.
- Tratar a costura angular do cilindro 3D e a estabilidade após concluir, reiniciar ou reproduzir a usinagem.

## Fora do escopo

A spline experimental da PR #5 original foi **retirada integralmente**, inclusive controles, cálculos, ajuda e testes, porque o módulo atual prioriza círculos, retângulos e linhas/rasgos. O eventual módulo de usinagem rotativa XZA será tratado separadamente.

O uso de uma superfície desenrolada como vista editorial não altera os movimentos XYZ nem caracteriza erro de corte: o eixo A continua indexado. A melhoria de malha é uma **melhoria de representação visual**, não uma mudança de estratégia CAM.

## Regressões e homologação

- Validar os controles Left/Right sem modificar `.nc`, trajetória, referência A0/Z0, campo radial e fixação.
- Validar o recolhimento, expansão e persistência dos painéis.
- Reproduzir no simulador o caso Ø30 × 120 mm, fresa topo reto Ø3, A30°, círculo em X30 e duas linhas cruzadas em X60/X70; verificar qualidade rápida/média/alta, recomeço e resultado final.
- Comparar comentário `linha` e coordenadas G-code reais com a versão oficial; preservar todos os movimentos e pós-processamento Mach3.
- Testar importação Aspire e STL, funções de edição e exportação, desktop e mobile.
- Conferir na prévia Cloudflare ligada ao **SHA atual** e aguardar homologação humana. Não fazer merge automático.

Este arquivo substitui a documentação anterior de investigação/spline. A mudança de nomenclatura geral para **Makernauta — Usinagem Rotativa** foi proposta separadamente na PR #6 e não será mesclada aqui, para manter uma linha de homologação independente.
