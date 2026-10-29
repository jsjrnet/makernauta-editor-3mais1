# Makernauta — Editor de Usinagem Indexada 3+1

Editor visual estático para Vectric Aspire e Mach3, baseado no **HTML original do protótipo Claude fornecido por Juarez Jr.** A interface, os quatro canvases originais e os fluxos foram mantidos em `editor-usinagem-indexada.html`. Não requer backend, pacotes JavaScript ou serviços externos.

**Protótipo: G-code não homologado para execução física.** Os testes deste repositório verificam o software e sua geometria, sem validar máquina, pós-processador, fixação, colisões ou condições de corte.

## Executar

Abra `editor-usinagem-indexada.html` no navegador ou, na raiz do checkout:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

O `index.html` encaminha à página do editor. O HTML é autossuficiente e também pode ser usado offline.

## Funcionalidades preservadas

- Cilindro desenrolado, alojamentos circulares, retangulares e em linha; arraste, grade e rotação da forma.
- Bolsão e contornos sobre a linha, por dentro e por fora; inspeção cartesiana XY e seção transversal.
- Importação de STL ASCII/binário, alinhamento ao eixo X, inversão, rotação e comparação com o material.
- Importação de G-code rotativo Aspire XZA por arquivo ou texto; referência Z0 original identificada em comentários explícitos ou confirmada pelo usuário quando ambígua.
- Simulação com pausa, reinício e busca; referenciais da máquina/peça, desenrolamento, câmera e cubo de orientação.
- Exportação Mach3, combinando escultura e alojamentos ou somente alojamentos, com validação de Z0 e pausas para troca de ferramenta; copiar e baixar `.nc`.

## Ferramentas e alinhamento

As seções organizam os parâmetros por função:

1. **Alojamentos:** cada círculo, retângulo ou linha guarda seu próprio diâmetro e tipo de fresa (`toolDiameter`/`toolType`). Os campos **T/HT** editam somente a figura selecionada. Novas figuras começam com topo reto Ø3 mm. A referência opcional de profundidade no STL fica aqui, desmarcada por padrão.
2. **Peça e máquina:** bruto, avanços, spindle, passadas, folga, sentido de A e **Z0 dos alojamentos/Mach3**.
3. **Escultura Aspire:** importação e ferramenta **TS/TY**, independente de todas as figuras, além da confirmação da referência original do arquivo.
4. **STL:** importação, alinhamento, rotação, inversão, visualização e comparação geométrica. Importar o STL não desbasta material nem altera o percurso dos alojamentos. Copiar suas medidas para o bruto ou usar sua superfície para profundidade exige uma ação explícita.

Percurso, compensação XY, malha de remoção, perfil ampliado e indicação da ferramenta 3D usam a ferramenta da mesma operação. Mudar de tipo não refaz uma estratégia CAM: ballnose pode deixar cristas entre passadas. Entre alojamentos com ferramentas diferentes, o `.nc` retrai em Z, para o spindle e inclui `M0` com tipo/diâmetro antes de prosseguir. Não há troca automática, atribuição de números T ou calibração de comprimento.

Os percursos XYZ são transformados em torno de X com o mesmo referencial usado pelos contornos e pelo material. O sentido de A é aplicado tanto à geração quanto à interpretação; Z0 desloca a ponta, não o modelo. Os contornos dos alojamentos mantêm Y cartesiano e piso Z plano, sem a aproximação `ângulo = Y / raio` no 3D. A remoção radial usa a interseção com o volume da ferramenta: base plana para topo reto e esfera para ballnose. Os alojamentos também têm uma malha cartesiana local de 0,15 mm.

A simulação é uma aproximação de superfície radial, não um simulador volumétrico industrial: STL com reentrâncias ou múltiplas superfícies no mesmo raio, cavidades sobrepostas e resolução finita exigem análise externa. Ballnose mantém a curvatura da borda; seu Z é a ponta da ferramenta. Não se promete equivalência com todos os dialetos G-code: o fluxo preservado é Aspire XZA absoluto em milímetros e alojamentos XYZ com arcos XY I/J incrementais. Confirme referências e configurações no Aspire/Mach3.

## Testes

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m playwright install --with-deps chromium
.venv/bin/python -m unittest discover -s tests -v
```

Pode-se selecionar um Chromium já instalado com `CHROMIUM_PATH=/usr/bin/chromium`. Os testes cobrem ferramentas individuais nos três tipos de figura, organização dos controles, Z0 pendente/incompatível, preservação das coordenadas Aspire, etapas de simulação independentes, STL sem desbaste automático, ferramentas independentes, geometria dos cortadores, alinhamento para os dois sentidos de A e Z0, piso/remoção/reinício da simulação, STL ASCII/binário, importação Aspire, exportação `.nc`, controles e layout móvel. Não são testes de homologação CNC.

## GitHub Pages

Pull requests são validados sem deploy. A incorporação à `main` requer aprovação; esta atualização não é incorporada nem publicada automaticamente pelo agente. O workflow `.github/workflows/pages.yml` testa e publica somente `index.html` e `editor-usinagem-indexada.html` após push na `main`. O job tenta habilitar Pages com fonte GitHub Actions. Se a política do repositório impedir a ativação automática, selecione **Settings → Pages → Source → GitHub Actions** e execute novamente o workflow.

Endereço previsto após a publicação bem-sucedida:

`https://jsjrnet.github.io/makernauta-editor-3mais1/editor-usinagem-indexada.html`

A presença do workflow ou do endereço previsto não confirma uma publicação; confira o job de deploy e a resposta HTTP pública.

Ideia e desenvolvimento: **Juarez Jr. — Makernauta** · https://makernauta.com.br

## Inspeção do corte e ajuda

O botão **Informações dos parâmetros** revela ícones `i` nos campos, seletores, caixas de marcação e ações. Cada ícone abre uma explicação com unidades, efeito das opções e limitações. A ajuda funciona por teclado, fecha com Escape e não altera os valores dos controles.

A seção ampliada abaixo do 3D usa as mesmas alturas da malha detalhada do alojamento, em escala horizontal e vertical iguais. Uma linha isolada produz fundo reto com topo plano e perfil arredondado com ballnose. Bolsões com várias passadas de ballnose podem apresentar fundo quase plano com pequenas cristas. A referência de profundidade não deve ser confundida com o material realmente removido.

A malha detalhada é limitada pela superfície capturada **antes** de executar os alojamentos. Não é achatada pela malha radial mais grosseira já usinada. Trocar a ferramenta reinicia a simulação; avance a barra ou simule novamente. O modo **STL alvo** mostra o modelo desejado e, por definição, não muda com a seleção da fresa.

## Referências Z0 e seleção das etapas

O Z0 da seção **Peça e máquina** governa somente o programa gerado dos alojamentos. Não há seletor para transladar o `.nc` Aspire. Seus valores X/Y/Z/A são mantidos. Ao concatenar, a terminação `M2`/`M30` do Aspire é removida do código executável para permitir a sequência; os comentários e coordenadas permanecem.

Comentários explícitos como `(Z0 = centro do eixo A)` ou `(Z0 = superficie do bruto)` identificam a referência original. Sem indicação explícita, ou com comentários conflitantes, **a exportação combinada e a simulação da escultura ficam bloqueadas** até o usuário conferir no trabalho/pós-processador Aspire e confirmar a referência. Não se infere o Z0 a partir de retrações ou da maior altura Z. Editar o texto invalida a confirmação anterior. O Z0 dos alojamentos precisa coincidir com o confirmado do Aspire para combinar; divergências não são corrigidas por deslocamentos automáticos.

O simulador guarda a referência Z por etapa, independentemente do seletor de Z0 dos alojamentos. O sentido positivo de A é uma convenção comum da máquina, usada na interpretação de todas as etapas; os valores A do Aspire não são reescritos. O fluxo suportado é milimétrico e absoluto; modos explicitamente incompatíveis, como G20/G91/G92 e referências especiais de movimento, são recusados sem conversão silenciosa.

**Etapas simuladas** escolhe a sequência combinada validada, somente escultura Aspire ou somente alojamentos sobre o bruto. Essa seleção é independente do conteúdo exportado. **STL alvo** mostra somente a referência geométrica; **Material** mostra a remoção calculada dos percursos selecionados; **Comparar** compara esse material ao STL. Nenhum desses modos gera desbaste a partir do STL.

A pausa na transição Aspire/alojamentos só pode ser desmarcada se as ferramentas forem iguais. Parâmetros inválidos ou profundidades além do limite bloqueiam a exportação em vez de emitir um programa parcial ou alterar silenciosamente a profundidade pedida. Esses bloqueios não equivalem a uma homologação de segurança CNC.

## Área de trabalho retrátil e STL + Desbaste

A área central prioriza o cilindro desenrolado e o simulador. **Peça e máquina** fica à esquerda; **Alojamentos**, **Aspire** e **STL** ficam à direita. O pino 📌 mantém o painel na lateral; recolher ou desafixar libera espaço central. Clique na aba para abrir temporariamente, use **Fixar** para manter aberto e Escape ou clique fora para fechar a abertura temporária. Em telas pequenas, os painéis fixos ficam abaixo da área central; a abertura temporária fica sobreposta e pode ser fechada.

Cada seção tem um título expansível por clique, toque, Enter ou Espaço. As quatro vistas auxiliares — seção de topo, XY, perfil da ferramenta e seção do corte — são independentes e se distribuem horizontalmente conforme a largura central. Fixação e seções abertas são lembradas no `localStorage` quando disponível. Recolher não altera parâmetros; redimensionar não regenera G-code, não apaga o material e preserva progresso, câmera e zoom. O enquadramento considera largura e altura para evitar cortar a peça quando a área central aumenta.

O aviso integral de segurança está no botão **Aviso de segurança — Protótipo não homologado**, com fechamento por botão ou Escape. A indicação resumida de não homologação permanece visível.

**STL + Desbaste** mostra material âmbar e o STL de referência em azul tracejado, em raio X. A referência azul pode aparecer através do material: não significa que aquele material já foi removido. A remoção continua sendo calculada exclusivamente pelos percursos selecionados e pela ferramenta de cada etapa. A sobreposição usa os triângulos STL transformados, com até aproximadamente 5 mil triângulos amostrados para manter a resposta visual; não altera o STL nem os cálculos de remoção. Material, STL alvo, comparação e só linhas continuam disponíveis.

A regressão após importação vinha da seleção automática de **STL alvo**, uma vista estática que não exibia a ferramenta nem a remoção progressiva. A importação agora entra em **STL + Desbaste**, sem iniciar a reprodução e sem zerar o material/progresso existentes. Iniciar uma reprodução enquanto a vista estática está selecionada também abre STL + Desbaste. Rotação/inversão apenas da referência não reinicia a usinagem, salvo quando existe alojamento explicitamente configurado para usar a superfície STL como referência de profundidade e seu percurso precisa ser recalculado. Essa opção é individual por alojamento e ocupa uma linha inteira.

O controle de desenrolar/enrolar permanece ativo também com STL e durante a simulação. Os controles Simular/Pausar, Reiniciar e progresso atuam no mesmo material calculado, sem criar trajetórias CAM a partir do STL. A geometria de remoção, as estratégias e as validações Z0 do PR #1 são mantidas.

As evidências visuais estão em [docs/evidencias/README.md](docs/evidencias/README.md). Os testes de navegador também cobrem pinagem individual, abertura temporária, persistência, accordions por teclado, modais, layout móvel, redimensionamento sem reinício, progressão STL com/sem Aspire, desenrolamento e ausência de remoção sem percurso de corte.

## Fixação ilustrativa, bruto maciço e altura 3D

A vista totalmente enrolada mostra um chuck escuro no lado X0, com três castanhas que acompanham a rotação da peça, e um contraponto com ponta cônica próximo de X=L. No referencial da máquina o contraponto permanece fixo; no referencial da peça sua posição relativa é transformada pela mesma mudança de referencial. A opção **Fixação visual** permite ocultar esses elementos para inspecionar a peça. No desenrolamento eles ficam ocultos, pois a representação plana não corresponde à montagem física.

Os elementos são apenas uma ilustração: não definem limites de movimento, não participam da remoção de material e não verificam colisões. A geração de percursos, as referências Z0/A0 e a exportação permanecem iguais.

O material enrolado recebe faces de fechamento nas extremidades, com a mesma cor âmbar e os raios do campo visualizado. Elas integram a ordenação de profundidade das faces para que o bruto pareça sólido nas vistas frontal, lateral e isométrica. Não é preenchida uma cavidade fictícia no motor de remoção: apenas se fecha o desenho da superfície existente. STL alvo continua sendo referência, e Só linhas continua sendo uma representação sem superfície do material.

Arraste a **barra pontilhada abaixo do canvas 3D** para ajustar sua altura entre 240 e 1000 px. Com a barra focada, as setas ajustam em passos de 20 px; Home/End selecionam os limites. A altura é lembrada junto das preferências de layout, quando o navegador permite. Canvas e projeção acompanham a altura real, inclusive em telas com densidade de pixels dupla, sem alterar controles, câmera, progresso, campo de material ou `.nc`. Os painéis laterais continuam recolhíveis e fixáveis.

As capturas e verificações desta alteração estão em [docs/evidencias/fixacao-altura/README.md](docs/evidencias/fixacao-altura/README.md). O G-code continua experimental e não homologado para execução física.
