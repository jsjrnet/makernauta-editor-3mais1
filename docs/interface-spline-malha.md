# Inspeção do eixo A, spline e correção da superfície

## Inspeção

Os botões Left/Right, no canto inferior direito do simulador, aplicam passos visuais de 15°. A peça, chuck, contornos, STL e percursos permanecem alinhados. O contraponto mantém a orientação da máquina. A inspeção não altera coordenadas, referência A0/Z0, material calculado, avanço da reprodução ou G-code. “Vista inicial” também zera a inspeção. Os títulos laterais deixam de ter numeração e as abas recolhidas exibem setas; pinos e abertura temporária continuam disponíveis.

## Spline

“+ Spline” cria uma curva Bézier cúbica aberta, com quatro pares X,Y em mm locais. P0 e P3 são extremidades; P1 e P2 controlam a curva. Os pontos podem ser editados no painel Alojamentos ou arrastados na inspeção XY. Posição X, A, rotação, profundidade e ferramenta continuam independentes por operação.

A spline oferece exclusivamente corte **sobre a linha**, indicado na interface. Não interpreta automaticamente curvas como bolsões nem aplica compensação de raio. Subdivisão adaptativa limita o desvio geométrico a 0,03 mm antes do arredondamento das coordenadas a três casas; o Mach3 recebe movimentos G1. Controles colineares, retornos e curvas degeneradas são tratados na subdivisão. Texto inválido bloqueia exportação, inclusive ao editar outro parâmetro; os pontos precisam ser corrigidos. Outras figuras mantêm suas estratégias.

## Investigação do defeito

Reprodução: bruto Ø30 × 120 mm, A30°, topo reto Ø3, círculo Ø10 em X30, linha transversal de comprimento 20 em X70 e longitudinal X50–X70. Pisos Z14, Z13,5 e Z12 correspondem a profundidades 1, 1,5 e 3 mm com Z0 no centro. Usaram-se dimensões de círculo e linha transversal explícitas porque não foram especificadas no relato.

Na qualidade rápida, o campo radial continha apenas valores finitos, com piso mínimo Z12. O renderizador desenhava 44.597 faces preenchidas onde a superfície radial com tampas exigia 17.376: ocultava células radiais pelo centro e acrescentava uma malha cartesiana independente por operação. Nas interseções havia superfícies sobrepostas; nas transições, as bordas das duas discretizações não compartilhavam vértices. A superfície podia representar material já removido por outra operação.

A visualização agora usa exclusivamente o campo radial acumulado de todas as ferramentas, com uma única superfície e tampas. A costura circular usa o mesmo vértice nas duas extremidades quando o cilindro está enrolado. Foram preservadas as equações de interseção da fresa, amostragem de movimentos, coordenadas importadas e estratégias das operações existentes. A seção cartesiana de 0,15 mm permanece disponível para inspeção detalhada. **O detalhe visual do 3D depende da qualidade da malha radial**: use Alta para inspecionar fresas pequenas; a seção pode mostrar detalhes mais finos. O simulador continua sendo uma aproximação radial, sem representar cavidades internas ou reentrâncias não radiais.

Regressões verificam valores finitos, pisos nas três qualidades, operação cruzada com profundidades diferentes, estabilidade após conclusão/redesenho, retorno ao bruto e reprodução idêntica. A contagem das faces evita reintroduzir malhas independentes; o teste das arestas efetivamente desenhadas exige duas faces por aresta na superfície fechada, incluindo tampas e costura circular. A reprodução incremental também é comparada ao resultado direto. O teste de hash do programa existente normaliza exclusivamente a correção do comentário `retangulo` → `linha`, preservando a comparação dos comandos originais. Testes adicionais cobrem inspeção visual, spline, validação de entradas, arraste, ferramentas e exportação; a suíte existente continua cobrindo STL, Aspire XZA, referências e Mach3.

A aprovação depende da avaliação funcional do usuário na prévia do commit atual. Não há merge automático. O G-code continua experimental e não homologado para execução física.
