> **Arquivo histórico — levantamento de 01/11/2026.** Preservado como registro da pesquisa original, sem código de terceiros. O catálogo e o roteiro atualizados desta pasta prevalecem para decisões novas. A observação "nenhuma PR" reflete a data do levantamento, não o presente.

# MAKERNAUTA — Pesquisa de repositórios GitHub para CNC 3+1 e XYZA simultâneo

**Data da pesquisa:** 01/11/2026  
**Projeto:** Makernauta — Usinagem Rotativa / Editor de Usinagem Indexada 3+1  
**Fundação oficial verificada:** `63df8e1df537af4cdf969de193395cbafe7f2113` (`main`, protegida)  
**Objetivo:** priorizar tecnologia de terceiros para estudo e experiências isoladas, sem alterar automaticamente a fundação homologada.

## Resumo executivo

Recomendam-se dois caminhos separados:

1. **Aprimorar o editor indexado agora** com auditoria de G-code, algoritmos de contorno/offset, consulta geométrica de STL e testes de regressão. Priorizar componentes pequenos com licença permissiva e fácil isolamento no navegador.
2. **Preparar o XYZA simultâneo** por meio de modelagem explícita de referenciais, cinemática, perfil mensurado da máquina, interpolação e política de avanços (G93/G94), colisões e pós-processador Mach3. Repositórios multieixos servem inicialmente como referências e ferramentas de comparação, não como código CNC aprovado.

**Não houve importação de código externo, commit, PR, instalação ou alteração do Makernauta nesta pesquisa.** A lista abaixo é uma triagem documental; os candidatos não foram compilados nem ensaiados contra a CNC física.

## Candidatos — integração progressiva

| Projeto e URL | Licença verificada | Linguagem/arquitetura | Ganho potencial | Ação recomendada |
|---|---|---|---|---|
| [cncjs/gcode-parser](https://github.com/cncjs/gcode-parser) | MIT | JavaScript, pacote Node | Leitura estruturada de palavras/blocos G-code, base para relatório de comandos | Testar em módulo de auditoria isolado; confirmar suporte aos modos Mach3 e ao A; não substituir parser atual automaticamente |
| [AngusJohnson/Clipper2](https://github.com/AngusJohnson/Clipper2) | Boost 1.0 | C++, C#, Delphi; existem portas/WASM de terceiros | Offset, união e diferença de polígonos, contornos de bolsões e compensação geométrica 2D | Prototipar fora da main; projeto consultado estava arquivado; revisar manutenção do port/WASM pretendido |
| [junmer/clipper-lib](https://github.com/junmer/clipper-lib) | Boost 1.0 segundo README; verificar avisos das dependências | JavaScript | Alternativa JS para offset/booleanos sem C++ | Prototipar com contornos 2D e comparar resultados; código antigo (último push 2023) |
| [gkjohnson/three-mesh-bvh](https://github.com/gkjohnson/three-mesh-bvh) | MIT | JavaScript sobre Three.js | Raycast e consultas de colisão/interseção em STL complexo | Experiência separada de consulta STL; implica avaliar Three.js e custo de dependência; não resolve remoção volumétrica sozinho |
| [mrdoob/three.js](https://github.com/mrdoob/three.js) | MIT | Renderizador JS WebGL | Câmera, STL e cena 3D mais desenvolvida | Somente avaliar uma vista de prova; substituir o canvas atual seria refatoração de maior risco |
| [GridSpace/grid-apps — Kiri:Moto](https://github.com/GridSpace/grid-apps) | MIT | Aplicação CAM JavaScript no navegador | Referência de operações indexadas, trajetórias, visualização e desenho de ferramentas | Estudar organização e testar separadamente; não copiar aplicativo inteiro |
| [OneManLabs/cam](https://github.com/OneManLabs/cam) | MIT | TypeScript, navegador, Vite, WebWorker | Exemplo de simulação de remoção isolada da UI | Benchmark/prova de conceito; repositório recente e pouca adoção, requer avaliação cuidadosa |
| [aewallin/opencamlib](https://github.com/aewallin/opencamlib) | LGPL 2.1 | C++ com bindings Python, Node e navegador | Drop-cutter, push-cutter e modelos de fresas flat/ball/bull/cone | Estudar como referência geométrica; realizar revisão das obrigações LGPL e do processo de integração antes de empacotar |
| [ChestnutLabs/gcode-preview](https://github.com/ChestnutLabs/gcode-preview) | MIT | JS/TypeScript modular + Worker + Three.js | Separação parser → IR neutra → visualização | Referência de arquitetura; foco principal em impressão 3D, requer adaptação de dialeto CNC/XYZA |

## Repositórios para o futuro XYZA simultâneo

| Projeto e URL | Licença/status | Destaques | Limite no Makernauta |
|---|---|---|---|
| [kaa-serpent/3dCamSlicer — RotaryCAM](https://github.com/kaa-serpent/3dCamSlicer) | BSD 3-Clause; Python | Planos XYZA, perfil de máquina, referenciais G54, simulação de volume varrido, bloqueio de G93 sem confirmação de suporte | Voltado a Makera Z1; **não** equivale a certificação para Mach3. Ideias e testes transferíveis só após validação independente |
| [charlatanshost/OpenMill](https://github.com/charlatanshost/OpenMill) | MIT **ou** Apache-2.0; Rust | CAM multieixos, malha/voxels, colisão de porta-ferramentas, perfis de pós-processadores, G93 em operações simultâneas | Projeto maior e com ênfase em 5 eixos; não é componente browser pronto nem pós Mach3 validado |
| [RicardoJCMarques/EasyCAM5000](https://github.com/RicardoJCMarques/EasyCAM5000) | **AGPL-3.0-ou-posterior** | EasyShape5000 inclui rotary contínuo radial e indexado; arquitetura JS no navegador, Clipper2 WASM; lista Mach3 experimental/com relatos da comunidade | **Estudar e testar como programa externo; não copiar código AGPL para a base proprietária sem análise específica de licença** |
| [teodoryantcheff/SolidCam-Mach3-Post](https://github.com/teodoryantcheff/SolidCam-Mach3-Post) | **Sem licença explícita encontrada** | Arquivos e exemplos de pós-processador de SolidCAM, referências de A em X/Y e Mach3 | Útil para estudo/comparação; não copiar código sem permissão; específico do SolidCAM |
| [grblHAL/core](https://github.com/grblHAL/core) | Condições de licença devem ser lidas por componente | Referência de intérprete e coordenação de eixos, com G93/G94 e palavras ABC dependentes de driver | **Não substitui** o Mach3 nem a controladora atual; estudar como controlador alternativo futuro |
| [LinuxCNC/linuxcnc](https://github.com/LinuxCNC/linuxcnc) | GPL-2.0 | Referência madura de interpretação, cinemática e controle coordenado | Estudar especificações e exemplos; não incorporar diretamente ao software proprietário |
| [CauldronDevelopmentLLC/CAMotics](https://github.com/CauldronDevelopmentLLC/CAMotics) | GPL v2+ | Simulação independente para usinagem 3 eixos | O próprio projeto não declara simulação rotativa de 4º eixo pronta; útil como comparação XYZ, não validador XYZA |
| [revjmoney/RotatoCAM](https://github.com/revjmoney/RotatoCAM) | **Sem licença e sem fonte do motor no repositório consultado** | Produto que anuncia CAM rotativo simultâneo e editor de simulação | Aplicação de referência/demonstração; software disponibilizado gratuitamente não significa código reutilizável |
| [LukasMoravansky/gcode-collision-check](https://github.com/LukasMoravansky/gcode-collision-check) | MIT; Python | Verificação de ferramenta/porta-ferramentas contra cena estática por posições XYZ | Não considerar verificador XYZA rotativo sem expansão de referenciais e cinemática |

## Ponto crítico — Mach3 e a CNC existente

O Manual do Mach3Mill descreve `G93` (avanço em tempo inverso), `G94` (unidades/minuto) e movimentos coordenados. Isso **não comprova** que a instalação real com porta paralela e controladora HC74 execute com precisão os percursos XYZA que pretendemos gerar. Precisamos validar a versão do Mach3, a interpretação das palavras A, configuração do eixo rotativo, diâmetro de correção, velocidade/aceleração dos quatro eixos, convenção dos referenciais, sensibilidade a G93 e limitações de servo/stepper. A leitura do manual não substitui teste de mesa, simulação independente e cortes no ar.

Manual de referência: https://www.machsupport.com/wp-content/uploads/2013/02/Mach3Mill_1.84.pdf (seções 10.1.5–10.1.7 e 10.7.28).

## Arquitetura futura recomendada (módulos isoláveis)

1. **Camada de geometria:** STL, normais, contornos 2D, offset e superfície-alvo; não sabe escrever G-code.
2. **Camada de máquina:** referencial peça, pivô A em torno de X, G54, sentido de A, Z0, limites lineares/rotativos, ferramentas e fixação; não assume medidas ausentes.
3. **Camada de movimento:** sequência de eventos geométricos no espaço `x,y,z,a`, tipagem de G0/G1/arco/pausa/ferramenta, sem dependência de Mach3.
4. **Planejador 3+1:** A posiciona, retrai, corta XYZ com A parado; preserva os invariantes atuais.
5. **Planejador XYZA simultâneo (novo):** caminhos coordenados, transformações, verificação de curso e interpolação; inicialmente só prévia, sem exportação de máquina.
6. **Pós-processadores:** Mach3 atual; novos dialetos apenas mediante documentação, golden tests e perfis físicos confirmados.
7. **Simulação e inspeção:** movimento + remoção + cena da máquina com verificação de colisões. Visualização não é atestado de segurança.

**Regra de implementação:** não substituir automaticamente o editor atual nem alterar as rotinas de geração `.nc` homologadas. Construir adaptadores/testes na lateral e só migrar partes comprovadas.

## Experimentos recomendados, em ordem

**Experimento 0 — inventário e regressão (sem mudanças na aplicação).** Fixar a baseline, guardar cenários de teste com o mesmo G-code e STL, preparar hashes dos `.nc` produzidos, capturas desktop/mobile e conjunto de parâmetros de avaliação.

**Experimento 1 — parser e auditoria de G-code.** Testar `cncjs/gcode-parser` como leitor auxiliar para `G0/G1/G2/G3`, `G20/G21`, `G90/G91`, `G90.1/G91.1`, `G93/G94`, Z0, A contínuo, comentários Aspire e `(CUT)`. Sem tocar o texto original importado ou reescrever suas coordenadas.

**Experimento 2 — offset de contornos.** Construir protótipo com Clipper2 ou Clipper JS para círculo/retângulo/linha e bolsão; confrontar com trajetórias e offsets existentes, ambas as estratégias e diferentes diâmetros de fresa. Testar degenerações, autofechamento, tolerâncias e unidades.

**Experimento 3 — consultas em STL.** Comparar a consulta radial existente com BVH ou OpenCAMLib em STL côncavos e sobrepostos, com ferramentas topo reto e ballnose. Medir erro, memória, tempo e impacto visual; não confundir interseção pontual com remoção ao longo do movimento.

**Experimento 4 — modelo XYZA sem corte/exportação.** Inserir uma camada de transformação com pivô, A0, sentido e quadro de coordenadas em protótipo isolado. Executar trajetórias sintéticas com A variando e demonstrar reprodutibilidade em ambas as orientações da máquina.

**Experimento 5 — pós-processador experimental separado.** Só depois de confirmar a geometria e o perfil real da máquina, produzir um `.nc` experimental com configurações explícitas e comparação por backplot independente. Não executar a máquina real antes de validação e homologação de segurança externa.

## Critérios de escolha e licenças

- **MIT, BSD-3 e Boost 1.0:** geralmente compatíveis com software proprietário, mantendo atribuições, avisos e demais obrigações aplicáveis.
- **Apache 2.0:** também permissiva, com obrigações próprias de avisos e patentes; conferir ao distribuir.
- **LGPL:** integração pode ser viável, mas exige exame jurídico e técnico particular (vinculação, substituição/relink e código modificado da biblioteca).
- **GPL / AGPL:** não copiar nem vincular à base proprietária sem análise aprofundada. AGPL pode impor disponibilização do código para usuários que interagem pela rede com versão modificada.
- **Sem licença:** código visível no GitHub **não** significa permissão de reutilização. Utilizar como referência de pesquisa, pedir autorização antes de copiar.
- Guardar registro de origem, versão/commit exato, licença, conteúdo modificado e avisos em um inventário permanente de componentes de terceiros.

## Verificações antes da próxima PR

- GitHub `main` intacta e protegida; branch própria;
- Testes numéricos de invariância do G-code e sintaxe;
- Testes de UI, viewport e importação STL/Aspire;
- Testes de dialeto modal e coordenadas do Mach3;
- Comprovação visual e homologação humana do SHA exato;
- Reversão por branch/PR sem alteração direta de produção;
- Nenhum novo pacote instalado no navegador ou no computador do usuário sem revisar compatibilidade, origem e comportamento.

## Conclusão

**A primeira PR recomendada deve ser apenas de diagnóstico técnico ou protótipo isolado de auditoria**, nunca uma troca completa do motor do Makernauta. Para o longo prazo, os melhores estudos iniciais de XYZA são `3dCamSlicer` e `OpenMill`, enquanto `EasyCAM5000` é uma referência especialmente próxima ao nosso editor web, com restrição importante de licença AGPL.

**Estado da pesquisa:** documental, sem build/teste de terceiros; alterações no repositório Makernauta: **zero**.