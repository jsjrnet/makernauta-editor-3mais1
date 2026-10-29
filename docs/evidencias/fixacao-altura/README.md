# Fixação visual e altura do canvas 3D

Capturas reais do Chromium na branch `feat/fixacao-bruto-altura-3d`, baseada na main `16c7857` (após o PR #2).

| Captura | O que verificar |
| --- | --- |
| [Bruto e fixação](bruto-fixacao.png) | Chuck à esquerda, castanhas junto ao bruto, extremidade direita sólida e contraponto alinhado. |
| [Extremidade sólida](extremidade-solida.png) | Vista ao longo do eixo, com a fixação oculta para inspecionar a face preenchida. O teste verifica pixels âmbar nas duas direções do eixo. |
| [Altura aumentada](altura-ajustada.png) | Canvas ampliado por arraste e teclado, com os painéis despinados e controles mantidos. |
| [STL e alojamentos](stl-fixacao.png) | Referência STL sobreposta ao material, com alojamentos e fixação visual. |
| [Rotação Aspire](rotacao-aspire.png) | Escultura XZA com indexação A, chuck solidário à peça e contraponto fixo no referencial da máquina. |
| [Mobile e alta densidade](mobile.png) | Altura reduzida ao mínimo em janela móvel, renderização DPR=2 e ausência de transbordamento horizontal. |

A geometria visual contém exatamente três castanhas; a perspectiva e a peça podem ocultar parcialmente uma delas. Chuck e castanhas usam a rotação da peça, enquanto o contraponto mantém sua pose de máquina. Estes elementos não são usados para colisões nem para calcular material removido.

Verificações adicionais à suíte existente:

- Centros e posições no eixo X; rotação das castanhas coincide com a superfície do bruto; coordenadas do contraponto não variam com a rotação da peça no referencial da máquina.
- Faces preenchidas em ambas as vistas ao longo do eixo.
- Arraste real da borda inferior; atualização da resolução do canvas; teclado, limites, persistência e mobile DPR=2.
- Identidade e valores do campo de material, percurso, progresso, câmera e G-code preservados ao alternar fixação e redimensionar.
- Exportação byte a byte idêntica à main para duas configurações, verificada por SHA-256 nos testes.
- Comparação adicional realizada entre a main e a implementação: 21 funções do núcleo (geração, interpretação, referências, importação e remoção) com `Function.toString()` idêntico, sem diferenças.

Para regenerar as capturas em `/tmp`, execute `python3 -m unittest discover -s tests -v`. Os testes não sobrescrevem as imagens versionadas. G-code experimental, sem homologação para execução física.
