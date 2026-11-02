# Roteiro de experimentos — Makernauta 3+1 e pesquisa XYZA

**Natureza:** backlog de hipóteses; **nenhum experimento abaixo está aprovado ou implementado por esta PR**. Cada execução exige uma tarefa/branch específica e, antes do merge, os procedimentos descritos em `AGENTS.md` e `diretriz.md`.

## Prioridades iniciais

| ID | Ideia | Valor esperado | Dependências / riscos | Estado |
|---|---|---|---|---|
| E0 | Congelar cenário-base de regressão, resultados de G-code e imagens | Medir consequências de mudanças futuras | Guardar fixtures de teste **não confidenciais**; comparação por SHA | Planejado |
| E1 | Auditoria somente leitura de G-code Aspire + Makernauta | Detectar estados modais, referências não confirmadas e discrepâncias | Parser de terceiro não garante semântica Mach3 | Planejado |
| E2 | Prova de offsets 2D em contornos | Melhorar precisão de bolsões/contornos complexos | Tolerância, curvas pequenas, auto-interseções, compensação da fresa | Planejado |
| E3 | Consultas geométricas em STL e testes da fresa | Comparar erro geométrico e desempenho | BVH, C++/WASM, consumo de RAM, versão offline | Planejado |
| E4 | Modelo de transformação A/XYZ no simulador separado | Iniciar pesquisa XYZA sem tocar na CNC | Pivô, convenção de sinais, origem, contínuo 360° | Planejado |
| E5 | Estudo de tempo inverso G93 e limites da máquina | Fundamentar pós-processador experimental | Capacidade real do Mach3 + controladora não medida | Bloqueado por medições |
| E6 | Simulação volumétrica/colisão com ferramenta completa | Evoluir visualização de material, porta-ferramenta e fixações | Modelo geométrico e calibração físicos; custo de processamento | Pesquisa |
| E7 | Auditoria visual assistida por Impeccable | Refinar UX sem tocar em CAM | Instalação e configuração devem ser revisadas; não mudar código sem PR | Pesquisa |

## E0 — Condições-base antes de escrever código

**Entrada mínima:** cenário de STL demonstrativo, arquivo XZA Aspire anonimizado/autorizado ou sintético, bruto e ferramenta, captura do editor, saída `.nc` conhecida e versão `main` identificada.

**Aceite:** conseguir reproduzir o mesmo cenário; identificar hash e conteúdo relevante do `.nc`; documentar diferenças aceitáveis e não aceitáveis. **Não publicar dados de máquina privada** nem declarar execução física.

## E1 — Auditoria não destrutiva de G-code (primeira PR de protótipo sugerida)

**Hipótese:** um leitor auxiliar consegue explicar, sem alterar, cada trecho do programa e suas condições de interpretação.

**Escopo:** 
- Detectar palavras `G/M`, `X/Y/Z/A`, `F/S`, comentários, modo métrico `G21`, absoluto `G90`, plano `G17`, arcos `I/J/K`, modo dos arcos `G90.1/G91.1`, `G93/G94`, início/fim `M2/M30`, pausas `M0`.
- Marcar referências `Z0` e `A0` que requerem confirmação humana.
- Registrar onde `A` muda e se há movimento simultâneo em `X/Y/Z`; o marcador textual Aspire `(CUT)` pode ser anotado sem assumir significado universal.
- Emitir diagnóstico de avisos por linha, **não corrigir automaticamente** o arquivo e não inventar interpretação de comandos desconhecidos.

**Casos:** programa de escultura isolada, indexado isolado, combinado, milímetros/ polegadas, coordenadas relativas/absolutas, arquivos com Z0 ambíguo, dois sentidos de A, G93 sem F, mudança de ferramenta, comentários mal codificados, arcos absolutos/incrementais.

**Aceite:** nenhum byte do arquivo-fonte ou do `.nc` atual modificado; não interferir no método de exportação, simulação, seleção de ferramenta ou animação. Documentar falsos positivos, cobertura e necessidade de ler o dialeto real. **Leitura estruturada ≠ certificação de G-code.**

## E2 — Offsets e bolsões

**Hipótese:** geometria robusta reduz degenerações na compensação de contornos. **Teste:** círculo, retângulo, linha, polígonos côncavos e auto-intersecções, offset para dentro/fora/sobre, Ø de fresa maior/igual/menor que largura da forma. Comparar número de segmentos, erro dimensional e tempo. Manter geometria antiga até equivalência demonstrada.

**Fonte de estudo:** [Clipper2](https://github.com/AngusJohnson/Clipper2), [clipper-lib](https://github.com/junmer/clipper-lib). Nenhuma instalação autorizada neste plano.

## E3 — STL e contato da ferramenta

**Hipótese:** métodos externos de consulta espacial e contato ajudam a quantificar o erro da simulação atual. **Teste:** STL com concavidade, malha não manifold, superfícies sobrepostas, alinhamento X, sentido de A invertido, múltiplos Z0, superfície de referência versus estoque removido, ballnose e topo plano.

**Métricas:** tempo, pico de memória, número de amostras, diferença dimensional contra referência independente e posição da fresa sobre material.

**Fontes:** [OpenCAMLib](https://github.com/aewallin/opencamlib), [three-mesh-bvh](https://github.com/gkjohnson/three-mesh-bvh). Não equiparar raycast pontual à remoção volumétrica.

## E4 — Experiência XYZA isolada e sem exportação

**Hipótese:** uma trajetória sintética com `A` variando pode ser descrita por transformações contínuas da peça, conservando posição e orientação da ferramenta em máquina.

**Mínimo testável:** rotações em 0/90/180/270/360°, inversão, ponto fora do centro, exemplo com variação simultânea de `X` e `A`, caso de `Y/Z/A`, mesma trajetória descrita no referencial da máquina e da peça. Incluir verificação de limites **com valores sintéticos marcados como tais**. Exportação CNC **desativada**.

**Fontes para estudar:** [RotaryCAM](https://github.com/kaa-serpent/3dCamSlicer), [OpenMill](https://github.com/charlatanshost/OpenMill), [Mach3Mill](https://www.machsupport.com/help-learning/product-manuals/).

## E5 — Perfil real de máquina e pós-processador

**Bloqueio explícito:** antes de testar `G93` em operação física, confirmar no ambiente real (versão do Mach3, controladora HC74 conforme informada, porta paralela, micro-passos, mecânica, limites XYZ+A, velocidade, aceleração, origem e convenção do giro). Validação de comando por manual não equivale a desempenho medido.

**Saída admissível inicialmente:** relatório, simulador e arquivos sintéticos rotulados **NÃO EXECUTAR EM MÁQUINA**, em repositório de testes/branch, sem integrar exportação final. Evolução exige protocolo físico separado e autorização.

## E6 — Colisões e estoque volumétrico

Estudar representação de ferramenta completa (ponta, corpo, haste, porta-ferramentas), mandril com castanhas, contraponto, fixação e retenção da peça. Os elementos FX da interface atual são **ilustrativos**, não medidas da máquina. Simular não significa garantir livre de colisões.

## Cartão padrão de cada experimento

```text
ID:
Título/objetivo:
Fundação SHA:
Problema reproduzível:
Fonte primária + URL + versão/commit + licença:
O que será aprendido (descrição própria):
Hipótese:
Dados de teste (sintéticos/autorizados):
Mudanças permitidas / proibidas:
Métricas e critérios de aceite:
Riscos e limites:
Testes automatizados:
Evidências visuais:
Resultados (distintos de hipóteses):
Decisão (propor / rejeitar / pesquisar mais):
PR / SHA de teste / link de prévia:
Confirmação do proprietário:
```

## Política de priorização

Priorizar tarefas com **alto valor observável, baixo impacto na fundação, capacidade de teste offline e reversibilidade**. Manter o motor CNC atual como referência. Qualquer transição para produção exige check de CI, teste funcional no SHA exato e autorização explícita de merge; a validação física continua uma etapa separada.
