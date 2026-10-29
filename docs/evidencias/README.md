# Evidências de navegador — painéis e STL + Desbaste

Capturas reais geradas pelos testes Playwright/Chromium da branch `feat/paineis-stl-desbaste`, baseada na main após o PR #1. Não são renderizações ilustrativas nem validação de execução física em CNC.

| Evidência | Cenário |
| --- | --- |
| [Painéis fixados](paineis-fixados.png) | Peça e máquina à esquerda; operações à direita; centro com edição e simulação. |
| [Painéis recolhidos](paineis-recolhidos.png) | Ambos despinados, área central expandida. |
| [Abertura temporária](painel-temporario.png) | Painel aberto pela aba, com ação Fixar; não ocupa largura permanente. |
| [Vistas recolhidas](vistas-recolhidas.png) | Topo, XY, perfil da ferramenta e seção do corte recolhidos independentemente. |
| [Mobile](mobile.png) | Coluna central prioritária, sem transbordamento horizontal; painel despinado preservado. |
| [STL + Desbaste](stl-desbaste.png) | Referência STL azul tracejada em raio X; material âmbar e ferramenta durante um alojamento. |
| [STL desenrolado](stl-desenrolado.png) | Mesmo instante e mesmo material, com o controle de desenrolamento em zero. A descontinuidade angular da peça desenrolada divide o corte na emenda. |
| [Aspire + alojamentos](stl-aspire-alojamentos.png) | Percurso Aspire XZA e alojamentos sobre o mesmo material, com STL de referência. |

O STL de teste é uma caixa de 120 × 16 × 16 mm para tornar visíveis as diferenças em relação ao bruto cilíndrico Ø30 mm. Seu interior azul não é material removido: a referência é deliberadamente visível através do bruto. A referência não gera CAM nem interfere na remoção calculada. Somente os percursos importados/gerados removem material.

Os testes verificam numericamente a permanência dos valores e da câmera, a identidade e as alturas do campo de material durante redimensionamento, as ferramentas por operação, o avanço/reinício da remoção e a inexistência de remoção quando não há movimentos de corte. As capturas complementam essas verificações.

Para regenerar as capturas em `/tmp`, execute `python3 -m unittest discover -s tests -v`. Os testes não modificam estes arquivos versionados automaticamente. Escolhas de painéis/seções são testadas com recarregamento; configurações de usinagem não são gravadas no armazenamento de layout.
