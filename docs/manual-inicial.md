# Makernauta — Usinagem Rotativa
## Manual inicial de utilização · PR #7 (versão de avaliação)

O módulo atualmente disponível é **Usinagem Indexada 3+1**. O eixo A **posiciona** a peça e permanece **parado** durante cortes XYZ. A importação do G-code rotativo XZA do Vectric Aspire permite simular uma escultura anterior, mas o Makernauta ainda não gera trajetórias XZA simultâneas.

### 1. Preparar trabalho
- Em **Configuração da peça e máquina**, informe **diâmetro e comprimento do material bruto**, e não as dimensões da peça acabada.
- Defina o Z0 da máquina conforme a origem do trabalho. Na importação Aspire, a confirmação da referência é indispensável se não constar explicitamente nos comentários do G-code. **A simples altura dos movimentos não permite determinar com segurança a origem Z0.**
- Importe o programa do Aspire em **Importação Aspire** e configure a fresa da escultura segundo a ferramenta real. O programa original não é convertido.

### 2. Usar STL de referência ou exemplos incorporados
- **Carregar exemplo → Isca Natan** carrega uma **aproximação de baixa resolução** construída por amostragem do STL original de cerca de 63 mm usado no teste. Não é uma cópia exata e **não corresponde necessariamente ao G-code Aspire**. O comprimento da isca real não deve ser confundido com o comprimento do bruto.
- **Carregar exemplo → Peão de xadrez** carrega um modelo didático gerado por revolução de perfil.
- **Baixar arquivo .stl** salva o exemplo selecionado para abrir em outro programa.
- **Escolher ficheiro** importa seu próprio STL; prefira este procedimento para comparar o resultado com a geometria de referência real.
- **Nenhum STL sozinho usina a peça.** A remoção simulada é causada pelos movimentos de ferramenta.
- **Copiar dimensões do STL (avançado)** altera as medidas do bruto; evite esse comando quando as dimensões originais do bruto do Aspire já forem conhecidas. O STL acabado costuma ser menor que o material de partida.
- Os controles **Girar STL** e **Inverter o comprimento** ajudam na orientação; o alinhamento completo por deslocamento X ainda é um aprimoramento previsto.

### 3. Criar operações indexadas
Na vista **Desenho da peça — vista desenrolada**, use **+ Círculo**, **+ Retângulo**, **+ Linha**. Selecione a operação para editar:
- **Geometria**: diâmetro, largura, comprimento e rotação quando aplicável.
- **Posicionamento**: X longitudinal e A em graus para indexação.
- **Estratégia e profundidade**: cavidade, contorno e profundidade. O piso Z é um campo calculado, não uma segunda profundidade a digitar.
- **Ferramenta desta operação**: diâmetro e topo reto ou ponta esférica.

Junto da **vista desenrolada** há as opções **Travar na grade**, **Grade X**, **Grade A** e **Y desenrolado**. Y desenrolado é uma forma auxiliar de expressar a posição angular.

A opção **Usar superfície do STL como referência de profundidade**, dentro de **Avançado**, **modifica o cálculo**; use somente com modelo geometricamente alinhado.

### 4. Simular e inspecionar
Em **Conteúdo da simulação**, escolha:
- **Apenas escultura importada do Aspire**: simula os percursos XZA originais.
- **Apenas operações indexadas**: simula as figuras com A parado durante os cortes XYZ.
- **Escultura Aspire + operações indexadas**: simula a sequência combinada, desde que as referências Z0 sejam compatíveis.

Use **Percurso**, **Contornos**, **Qualidade** e o controle de tempo para inspecionar. **Girar A** modifica **apenas a vista** em incrementos de 15°. O sentido aparente dos botões ainda deve ser avaliado antes da aprovação final.

A sobreposição de malhas no cenário combinado pode produzir pequenas saliências visuais; elas não são prova de rebarba física nem de erro por o eixo A permanecer parado.

### 5. Exportar CNC
Em **Programa CNC gerado**, confira as mensagens de validação, ferramentas e origens, simule no Mach3 (backplot) e valide o comportamento antes de qualquer ensaio a seco. O pós-processamento do Makernauta ainda é **experimental e não homologado para execução física**.

### 6. Sobre valores iniciais
A peça e os parâmetros exibidos inicialmente são apenas **exemplos de interface**, não dados automaticamente reconhecidos de um trabalho real. Um futuro modo **Novo trabalho** deverá separar explicitamente uma demonstração de um projeto novo.

### 7. Próximos refinamentos ainda não concluídos na PR #7
Interpretação assistida dos parâmetros do cabeçalho Aspire, deslocamento longitudinal do STL, caracterização das saliências de sobreposição no 3D e confirmação do sentido de giro dos controles. Nenhum desses itens autoriza mudar a estratégia CAM validada sem teste e nova homologação.
