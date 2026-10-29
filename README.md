# Makernauta — Editor de Usinagem Indexada 3+1

Editor visual estático para Vectric Aspire e Mach3, baseado no **HTML original do protótipo Claude fornecido por Juarez Jr.** A interface, os quatro canvases e os fluxos originais foram mantidos em `editor-usinagem-indexada.html`. Não requer backend, pacotes JavaScript ou serviços externos.

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
- Importação de G-code rotativo Aspire XZA por arquivo ou texto; Z0 no centro do eixo ou na superfície, com confirmação manual da detecção.
- Simulação com pausa, reinício e busca; referenciais da máquina/peça, desenrolamento, câmera e cubo de orientação.
- Exportação Mach3, combinando escultura e alojamentos ou somente alojamentos, com pausa opcional para troca; copiar e baixar `.nc`.

## Ferramentas e alinhamento

A escultura usa exclusivamente **TS/TY** (diâmetro/tipo); os alojamentos usam **T/HT**. Ambas permitem ballnose ou topo reto, com padrões ballnose para escultura e topo reto para alojamentos. Alterar uma ferramenta não altera os parâmetros da outra. O indicador 3D acompanha a etapa simulada.

Os percursos XYZ são transformados em torno de X com o mesmo referencial usado pelos contornos e pelo material. O sentido de A é aplicado tanto à geração quanto à interpretação; Z0 desloca a ponta, não o modelo. Os contornos dos alojamentos mantêm Y cartesiano e piso Z plano, sem a aproximação `ângulo = Y / raio` no 3D. A remoção radial usa a interseção com o volume da ferramenta: base plana para topo reto e esfera para ballnose. Os alojamentos também têm uma malha cartesiana local de 0,15 mm.

A simulação é uma aproximação de superfície radial, não um simulador volumétrico industrial: STL com reentrâncias ou múltiplas superfícies no mesmo raio, cavidades sobrepostas e resolução finita exigem análise externa. Ballnose mantém a curvatura da borda; seu Z é a ponta da ferramenta. Não se promete equivalência com todos os dialetos G-code: o fluxo preservado é Aspire XZA absoluto em milímetros e alojamentos XYZ com arcos XY I/J incrementais. Confirme referências e configurações no Aspire/Mach3.

## Testes

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m playwright install --with-deps chromium
.venv/bin/python -m unittest discover -s tests -v
```

Pode-se selecionar um Chromium já instalado com `CHROMIUM_PATH=/usr/bin/chromium`. Os testes cobrem ferramentas independentes, geometria dos cortadores, alinhamento para os dois sentidos de A e Z0, piso/remoção/reinício da simulação, STL ASCII/binário, importação Aspire, exportação `.nc`, controles e layout móvel. Não são testes de homologação CNC.

## GitHub Pages

O workflow `.github/workflows/pages.yml` testa e publica somente `index.html` e `editor-usinagem-indexada.html` após push na `main`. O job tenta habilitar Pages com fonte GitHub Actions. Se a política do repositório impedir a ativação automática, selecione **Settings → Pages → Source → GitHub Actions** e execute novamente o workflow.

Endereço previsto após a publicação bem-sucedida:

`https://jsjrnet.github.io/makernauta-editor-3mais1/editor-usinagem-indexada.html`

A presença do workflow ou do endereço previsto não confirma uma publicação; confira o job de deploy e a resposta HTTP pública.

Ideia e desenvolvimento: **Juarez Jr. — Makernauta** · https://makernauta.com.br
