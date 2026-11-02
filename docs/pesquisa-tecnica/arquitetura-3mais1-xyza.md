# Arquitetura técnica de evolução — 3+1 indexado e XYZA simultâneo

**Situação:** estudo e proposta conceitual; **nenhuma das camadas novas foi implementada por esta documentação.**

## 1. Regras que o sistema atual já cumpre

- Módulo atual: operações indexadas **3+1**; `A` posiciona a peça e **permanece parado** durante os cortes XYZ; indexações e mudanças de posição exigem retração adequada.
- Aspire 9 Wrapped: arquivo de escultura XZA importado e mantido como referência original, sem reescrever silenciosamente `X/Y/Z/A`. Separar importação, interpretação, simulação e composição.
- `Z0` da escultura e dos alojamentos são referências distintas, que precisam ser confirmadas e conciliadas explicitamente; `A` possui sentido de rotação escolhido pelo usuário.
- Ferramentas por operação: topo plano versus ballnose; não inferir tipo/diâmetro do arquivo salvo como se fosse medido.
- STL é **referência**, não percursos CAM gerados automaticamente. A remoção simulada não equivale à verificação física de colisão.
- Saída Mach3 `.nc` é **experimental**, não homologada na máquina. Preserve a geração atual até decisão de PR específica.
- O editor presente é HTML/JS autossuficiente, sem backend. Qualquer biblioteca adicionada pode afetar uso offline, tamanho, desempenho e licenças.

## 2. Por que separar os módulos

O modo **XYZA simultâneo** não é simplesmente substituir uma sequência de ângulos indexados por valores `A` variáveis. É necessário especificar **a trajetória da ponta e do corpo da ferramenta em um referencial de máquina enquanto a peça gira**, as transformações entre coordenadas, o avanço da ferramenta relativo à superfície, os limites e possíveis colisões.

### Camadas propostas

| Camada | Responsabilidade | Não pode fazer silenciosamente |
|---|---|---|
| **Geometria de entrada** | Normalizar malhas STL, contornos 2D, propriedades de ferramenta, unidades | Corrigir/aproximar STL alterando sem avisar |
| **Referenciais e perfil de máquina** | Pivô do eixo A, sentido, A0, fixações, origem G54, limites, dimensões e tool setup | Inventar valores ausentes |
| **Modelo intermediário de movimento** | Registrar blocos, eixos, estados modais, movimentos, trocas e referências | Converter comentários/códigos desconhecidos como se fossem compreendidos |
| **Planejador indexado 3+1** | Reusar regras de A estacionário nos movimentos XYZ | Mudar saída homologada sem testes de equivalência |
| **Planejador XYZA (novo)** | Gerar pontos coordenados de trajetória e orientação em simulação separada | Exportar programa de máquina antes de verificação do perfil |
| **Pós-processadores** | Converter movimentos explícitos para dialeto/controlador específico | Presumir que G93 em LinuxCNC = operação física aprovada no Mach3 |
| **Simulador geométrico** | Mostrar varredura de ferramenta e material aproximado, inspeção visual | Chamar aparência gráfica de prova de segurança |
| **Verificador independente** | Limites, sequência modal, análise geométrica de porta-ferramentas/fixações e comparação | Garantir ausência de colisões reais sem modelo medido |
| **Interface** | Mostrar dados, decisões, alertas e limites | Acionar mudanças de percurso por efeito visual acidental |

### Fluxo de informação proposto

`STL + ferramentas + perfil de máquina` → `geometria/referenciais` → `planejador 3+1 OU XYZA` → `modelo de movimentos` → `verificador` → `simulação` → `pós-processador específico`.

A **exportação XYZA** deve nascer bloqueada até existirem testes e dados confirmados da máquina. O planejamento e a prévia podem ser explorados sem habilitar a exportação.

## 3. Sistema de coordenadas — perguntas antes do código

1. Em que direção o eixo de rotação físico aponta? A convenção inicial é **A em torno de X**, a confirmar contra a máquina e o Mach3.
2. Qual é o centro/pivô do A em coordenadas de máquina e seu relacionamento com **G54**?
3. Onde estão o **zero de A**, **Z0 da peça**, ponta da fresa, encosto do mandril e contraponto?
4. Qual o sentido positivo de A na máquina? Qual transformação é necessária para expressar um ponto da peça no referencial da fresa?
5. Quais os limites `X/Y/Z/A`, velocidades, acelerações e relação entre graus/mm no controle?
6. Há castanhas, suporte, collet, shank, porta-ferramentas e tailstock com medidas reais verificadas?
7. O controlador efetivo aceita e coordena movimentos `X/Y/Z/A` e avanço em tempo inverso na versão e na interface **realmente instaladas**?

Uma implementação poderá usar transformação matricial homogênea própria, por exemplo **`T_maquina_peca(A) = T_pivo × RotX(sinal × A) × T_montagem`**, mas **essa fórmula é um modelo de projeto**, não uma calibração determinada. O tratamento do pivô, convenção de sinal e referências precisa ser demonstrado em casos sintéticos antes de usar STL real.

## 4. Avanço: G93 e G94 — o que está documentado

O [manual oficial Mach3Mill 1.84, seção 10.7.28](https://www.machsupport.com/wp-content/uploads/2013/02/Mach3Mill_1.84.pdf) descreve `G93` (tempo inverso), `G94` (unidades/minuto), `G95` e exige `F` em cada movimento `G1/G2/G3` no modo `G93`. **Em G93, a interpretação conceitual é `tempo_em_minutos = 1 / F`**. Assim, por exemplo, um bloco `F2` corresponde a uma duração programada de meio minuto.

É **incorreto** calcular avanço concatenando mm e graus como se fossem dimensões iguais; o caminho físico e a taxa de remoção dependem de raio local e geometria de contato. O planejamento simultâneo precisa definir política própria para velocidades/tempo, limites dos eixos e blocos curtos.

A [documentação LinuxCNC sobre G93/G94/G95](https://linuxcnc.org/docs/stable/html/gcode/g-code.html) é útil **para comparação**, não prova compatibilidade do Mach3 ou da controladora do usuário.

**Importante:** suporte de um comando no manual ≠ sincronização precisa no equipamento, nem verificação de acoplamento porta paralela, trajetória, acelerações ou qualidade da peça.

## 5. Modelo de dados mínimo para simulação XYZA

Proposta de **campos** (não é formato pronto nem código a copiar):

- `machineProfile`: controlador/versão; eixos; convenção; unidades; pivot; G54; limites; velocidade/aceleração; perfil de fixações; proveniência de cada medida.
- `setup`: material bruto, dimensões, posição física, ferramental, referência STL, Z0/A0, operações solicitadas.
- `motionBlock`: tipo `rapid|feed|arc|pause|toolChange`, ponto origem/destino `x,y,z,a`, unidades, modos, id da operação, parâmetros da ferramenta e indicador se **A varia durante o corte**.
- `validation`: itens mensurados/pendentes, avisos e bloqueios para exportação; guardar dados não verificados como ausentes, **não zero**.
- `simulation`: modelo de material, tolerância, malha e condições conhecidas de erro.

## 6. Experimentos geométricos indispensáveis

- A=0°, 90°, 180°, 360°: conferir continuidade de posição, referencial e costura da peça.
- Sentido A positivo e invertido: comparar transformações de ponto na máquina e na peça.
- Círculo em área cilíndrica, retângulo, rasgo, bolsão sobre STL com depressões e ressalto; distinguir **superfície alvo** de **material removido**.
- Fresa plana e ballnose, múltiplos diâmetros e passadas, com comparação independente do perfil do corte.
- Rápidos próximos ao mandril/contraponto: verificações devem usar envelope físico medido, não as dimensões apenas ilustrativas do editor.
- Volta angular acima de 360°, no caso em que o controlador aceite, evitando reescrever `A` pela operação `módulo 360` sem regra explícita.
- `G90/G91`, `G90.1/G91.1`, `G93/G94`, mudanças de ferramenta, paradas e unidades.

## 7. Decisões futuras, ainda abertas

1. Usar JS puro para manter HTML offline ou **adaptadores opcionais** JS/WASM/Worker? Medir o custo de cada proposta.
2. Empregar geometria/contorno de biblioteca permissiva ou continuar implementação própria com testes comparativos?
3. Simulação radial e volumétrica: manter duas representações complementares ou migrar por etapas? Não decidir antes de medir erros.
4. Como preservar compatibilidade Aspire 9 sem transmitir suposições de G-code para a camada XYZA?
5. Quais condições documentadas permitiriam criar uma saída experimental separada, sem interferir no `.nc` 3+1 atual?
6. Como validar o controle real Mach3 + porta paralela + controladora indicada como HC74? **Pendente levantamento físico/autorização.**

**Regra de encerramento:** nenhuma decisão técnica neste documento autoriza execução em CNC real. As diretrizes de segurança, testes e homologação do repositório permanecem superiores.
