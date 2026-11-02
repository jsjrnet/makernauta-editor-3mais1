# Catálogo de repositórios e referências técnicas

**Consulta de metadados e páginas de projetos:** 01/11/2026. **Natureza:** triagem documental, não auditoria de segurança, compatibilidade ou execução. As licenças podem mudar; revalidar **versão/commit, arquivo de licença, dependências e avisos** antes de qualquer incorporação.

**Legenda de uso:** **A** = candidato a experimento separado; **R** = estudo de arquitetura ou comparação; **L** = avaliação jurídica/de componentes obrigatória antes de integrar; **N** = não copiar sem autorização. Todos os candidatos abaixo estão **não testados dentro do Makernauta**.

## A. Aproveitamento possível no Editor 3+1

| Fonte (repositório) | Licença/status identificados | O que vale estudar | Encaminhamento |
|---|---|---|---|
| [cncjs/gcode-parser](https://github.com/cncjs/gcode-parser) | MIT, informada por LICENSE | Léxico de G-code, palavras e blocos; não garante interpretação de todos os modos Mach3 | **A**: relatório somente leitura; testar modal, arcos, comentários e eixo A |
| [AngusJohnson/Clipper2](https://github.com/AngusJohnson/Clipper2) | Boost Software License 1.0; repositório consultado **arquivado** | Clipping, offsets e operações booleanas de polígonos | **R/A**: algoritmo de contornos; escolher porta JS/WASM somente depois de examinar sua licença e manutenção |
| [junmer/clipper-lib](https://github.com/junmer/clipper-lib) | README indica Boost 1.0; API GitHub não reconheceu licença canônica | Offset e booleanos em JavaScript; histórico de código antigo | **A/L**: confirmar licença dos arquivos/dependências e comparar estabilidade |
| [gkjohnson/three-mesh-bvh](https://github.com/gkjohnson/three-mesh-bvh) | MIT | Consultas espaciais e raycast acelerado sobre malhas de Three.js | **A**: benchmark STL sem trocar o renderizador principal |
| [mrdoob/three.js](https://github.com/mrdoob/three.js) | MIT | Renderização, importação e manipulação 3D | **R**: eventual cena separada; refatoração do canvas atual é risco alto |
| [GridSpace/grid-apps](https://github.com/GridSpace/grid-apps) — Kiri:Moto | MIT conforme metadados GitHub | Organização de CAM web, operações e estratégias | **R/A**: estudar interfaces e fluxos, nunca transplantar aplicativo inteiro |
| [OneManLabs/cam](https://github.com/OneManLabs/cam) | MIT | Pipeline DXF/SVG → operações → ferramenta → simulação; uso de Web Worker | **R/A**: isolamento de cálculo fora da UI; maturidade ainda a avaliar |
| [aewallin/opencamlib](https://github.com/aewallin/opencamlib) | LGPL-2.1 | Drop-cutter, push-cutter e geometrias de fresas flat, ball, bull e cone; bindings Node/browser | **R/L**: referência de contato em STL; avaliar obrigações de linking/distribuição antes de integrar |
| [ChestnutLabs/gcode-preview](https://github.com/ChestnutLabs/gcode-preview) | MIT declarada no levantamento inicial; **reconfirmar no commit de avaliação** | Parser → representação intermediária → prévia visual, Workers | **R**: foco em prévia de G-code, não validar como interpretador Mach3 |

## B. Base para pesquisas XYZA simultâneas

| Fonte | Licença/status identificados | Valor para nossa documentação | Encaminhamento |
|---|---|---|---|
| [kaa-serpent/3dCamSlicer](https://github.com/kaa-serpent/3dCamSlicer) — RotaryCAM | BSD-3-Clause em LICENSE | Perfis de máquina, pivô e referenciais, volume varrido, bloqueio de G93 sem perfil verificado | **R**: arquitetura e testes sintéticos; perfil Makera Z1 não comprova compatibilidade Mach3 |
| [charlatanshost/OpenMill](https://github.com/charlatanshost/OpenMill) | README informa escolha **MIT ou Apache-2.0**; GitHub marca licença como não classificada | CAM multieixos, voxels, colisão ferramenta/porta-ferramentas, verificações antes da exportação | **R**: estudo em Rust; não transportar backend para HTML diretamente |
| [RicardoJCMarques/EasyCAM5000](https://github.com/RicardoJCMarques/EasyCAM5000) — EasyShape5000 | **AGPL-3.0-ou-posterior** conforme README e LICENSE | Referência próxima ao Makernauta: navegador, STL, indexação e rotary contínuo | **R/L**: estudar conceitos/experimentar separadamente; **não copiar código** para software proprietário sem avaliação jurídica |
| [LinuxCNC/linuxcnc](https://github.com/LinuxCNC/linuxcnc) | GPL-2.0 identificado por GitHub | Modelos de coordenadas, avanço, cinemática e interpolações | **R**: documentação técnica; não incorporar seu código por conveniência |
| [grblHAL/core](https://github.com/grblHAL/core) | GitHub não classificou licença; conferir arquivos e módulos específicos | Arquitetura de interpretador/controlador como possibilidade futura | **R/L**: estudo; não substituir Mach3 nem assumir driver compatível |
| [CauldronDevelopmentLLC/CAMotics](https://github.com/CauldronDevelopmentLLC/CAMotics) | README indica **GPL v2+** (arquivo COPYING); GitHub não classifica | Simulação independente em **3 eixos** | **R**: comparação XYZ, **não** verificador XYZA |
| [LukasMoravansky/gcode-collision-check](https://github.com/LukasMoravansky/gcode-collision-check) | MIT | Separação entre ferramenta, porta-ferramentas, fixação e verificação geométrica | **R**: cenas estáticas XYZ; não inferir cobertura rotativa XYZA |
| [teodoryantcheff/SolidCam-Mach3-Post](https://github.com/teodoryantcheff/SolidCam-Mach3-Post) | **Sem licença explícita localizada** na triagem | Referência comparativa de configurações de pós SolidCAM para Mach3 | **R/N**: não copiar posts ou trechos; nem assumir compatibilidade com Aspire |
| [revjmoney/RotatoCAM](https://github.com/revjmoney/RotatoCAM) | No levantamento inicial, sem licença clara/código reutilizável do motor; **revalidar** | Aplicação de comparação de recursos rotativos anunciados | **R/N**: somente referência pública até verificação de termos |

## C. Ferramentas transversais

| Fonte | Licença | Objetivo limitado |
|---|---|---|
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | Apache-2.0 | Auditoria e vocabulário de qualidade visual, sem dependência obrigatória no site e sem instalar automaticamente |
| [Documentação do Mach3](https://www.machsupport.com/help-learning/product-manuals/) | Documentação do fabricante, não código aberto do projeto | Comandos, modos e configuração; comprovar no sistema real antes de autorizar pós-processamento |
| [Manual Mach3Mill 1.84](https://www.machsupport.com/wp-content/uploads/2013/02/Mach3Mill_1.84.pdf) | Documento externo; **referenciar, não republicar** | Seção 10.7.28 sobre G93/G94/G95; não prova comportamento da controladora física |
| [LinuxCNC G-code](https://linuxcnc.org/docs/stable/html/gcode/g-code.html) | Documentação de outro controlador | Referência para comparar interpretação de G93; não supor equivalência com Mach3 |
| [GitHub — licenças](https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository) | Guia de referência | Ausência de licença não concede permissão geral de reutilização |

## O que não está autorizado por este catálogo

- Nenhuma dependência é aprovada para uso em produção só por constar nesta lista.
- **Permissivas ≠ domínio público:** MIT, BSD, Boost e Apache exigem condições próprias, como manutenção de avisos; LGPL, GPL e AGPL precisam de análise específica conforme distribuição e integração. Mesmo um pacote sob licença permissiva pode incluir arquivos com termos diferentes.
- A licença proprietária do Makernauta **não substitui** licenças de partes externas. Se uma biblioteca for efetivamente incorporada, registrar em inventário de terceiros, atribuições e artefatos distribuídos.
- Referências a ideias, fatos, princípios e interfaces conceituais **não** autorizam copiar expressão protegida, código, imagens ou documentação integral.
- Código sem licença explícita ou condições verificáveis: **não reutilizar** até autorização.
- Metadados de GitHub e READMEs são **declarações documentais dos projetos**, não provas de segurança, maturidade, controle de qualidade ou aptidão para fabricação.

## Ficha obrigatória antes de propor uma incorporação

Preencher no registro de decisão: URL canônica; data; commit/tag de terceiro; `LICENSE`, `NOTICE` e licenças transitivas; proprietário/manutenção; parte exata pretendida; forma de integração (ferramenta externa, dependência, adaptador, conhecimento reimplementado); tamanho/custo; compatibilidade com página HTML offline; risco de regressão; testes; possibilidade de remover; homologador.

**Observação para manutenção:** esta lista é um inventário inicial e deve ser reavaliada quando efetivamente utilizada. Não reclassificar como "compatível" sem verificação de versão e uso concreto.
