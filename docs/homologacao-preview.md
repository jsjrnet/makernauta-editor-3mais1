# Homologação funcional por PR — Cloudflare Pages

## Estado e escolha

Esta configuração prepara prévias independentes em **Cloudflare Pages com integração GitHub nativa**. O GitHub Pages oficial continua usando a main e o workflow existente. Não há instalação local para o avaliador, token Cloudflare na CI, nem mudança na lógica do Editor.

A integração **ainda precisa ser conectada na conta Cloudflare do proprietário**. Criar arquivos de workflow não cria um projeto externo e não estabelece uma URL pública. A primeira prévia só pode ser declarada disponível após o deploy real e a verificação HTTP do commit e do HTML.

Comparação avaliada:

| Solução | Configuração externa | Escolha |
| --- | --- | --- |
| Cloudflare Pages + GitHub nativo | Autorizar o app Cloudflare para este repositório e criar um projeto isolado | Recomendada: dispensa API token de deploy e fornece previews/aliases por branch |
| Pages Direct Upload + Actions/Wrangler | Account ID, API token Pages Edit, secrets e separação de jobs privilegiados | Não adotada: maior manutenção e acesso a credenciais |
| GitHub Pages oficial | Alteraria o canal da main ou sua árvore publicada | Não usado para testar PRs |

As prévias nativas são para branches do próprio repositório. **PRs de forks não recebem preview nativo do Cloudflare.** Para avaliá-las, o mantenedor deve revisar a contribuição e abrir uma branch/PR de revisão no próprio repositório. Não se faz espelhamento automático de código externo com token de escrita. Uma PR sem prévia verificada permanece não homologada; não há exceção automática para forks.

## Configuração externa necessária — proprietário

Nenhum segredo deve ser enviado no chat. A consulta às listas de secrets/variables via credencial desta tarefa recebeu HTTP 403; isso não prova que essas listas estejam vazias. O fluxo nativo não exige criar um secret Cloudflare no repositório.

1. Entre no [Cloudflare Dashboard](https://dash.cloudflare.com/), em **Workers & Pages → Create application → Pages → Connect to Git** (os nomes podem variar na interface).
2. Autorize a instalação **Cloudflare Workers and Pages** no GitHub, com acesso somente a `jsjrnet/makernauta-editor-3mais1`. Essa vinculação de contas depende da sua autorização.
3. Crie um projeto separado com o nome **`makernauta-editor-preview`**, sem associar o domínio oficial nem alterar DNS do site atual. Se o nome não estiver disponível, escolha outro e atualize `project` em `cloudflare-preview.json` nesta PR antes de aprovar.
4. Framework: **None**; diretório raiz: `/`; diretório de saída: **`_preview_site`**. Use Node.js 22 ou superior no build image do projeto. Não adicione credenciais ou bindings ao projeto de prévias.
5. Comando de build, incluindo compatibilidade com a main anterior à configuração:

   ```sh
   if test -f scripts/build-preview.cjs; then node scripts/build-preview.cjs; else mkdir -p _preview_site && printf 'Homologacao pendente: aguarde o deploy da branch da PR.\n' > _preview_site/index.html; fi
   ```

   O fallback permite criar o projeto enquanto a main ainda não tem o script desta PR. Essa página provisória não contém o editor nem manifesto e **não é uma prévia verificada para homologação**. Não altera o Pages oficial.
6. Production branch: `main`. Em **Settings → Builds & deployments → Branch deployment controls**, **desative os deploys automáticos de Production** e habilite previews para as branches do repositório. O projeto Cloudflare é só para homologação; sua URL raiz não será usada como link de PR.
7. Deixe os previews acessíveis pelo navegador. Se habilitar Cloudflare Access, o verificador HTTP anônimo não terá acesso e não marcará a prévia como pronta; seria necessária uma configuração adicional aprovada. O padrão desta configuração é preview público em um domínio isolado, com `noindex`, sem dados/segredos de servidor.
8. Após conectar o projeto, solicite uma nova execução do deploy da branch desta PR no Cloudflare. Se a branch ainda não aparecer, informe que a conexão foi concluída para que seja feito um novo push na mesma branch. Não é preciso incorporar o código à main para o Cloudflare construir essa branch.
9. Confirme que a prévia contém `preview-manifest.json` e que o deploy é **Preview**, não Production. A automação aceitará apenas um subdomínio preview do projeto configurado, com SHA, branch e hash do HTML correspondentes à PR.

Não foi efetuada a instalação do app, criação de projeto, alteração de DNS, alteração de proteção de branch nem publicação oficial pelo agente.

## Bootstrap desta PR, antes do primeiro merge

O workflow de metadados é deliberadamente confiável: `pull_request_target`, eventos Cloudflare e agendamento usam somente o código da branch padrão. Por isso **a nova automação ainda não roda a partir da main antes da aprovação desta própria configuração**.

A integração Cloudflare nativa pode publicar a branch desta PR antes do merge. Depois da conexão externa e do deploy, o agente/mantenedor pode executar, com sua autenticação GitHub já configurada:

```sh
node .github/scripts/preview-status.cjs --pr=NUMERO --body-only
```

Esse comando atualiza apenas o bloco da descrição, verifica o conteúdo HTTP real e os resultados de CI, e não cria check, merge ou deploy. Ele não executa código da PR no servidor GitHub, não usa token Cloudflare e não pede seu valor no chat. Na tarefa de configuração, é executado a partir do código que está sendo revisado localmente; futuramente a automação sempre lê o código aprovado da main.

O link desta configuração deve ser testado no navegador pelo proprietário **antes de aprovar/incorporar esta PR**. Se Cloudflare ainda não tiver sido conectado, o bloco exibirá pendência, sem inventar uma URL ativa. Uma exceção de bootstrap não transforma CI verde em avaliação funcional.

## Como funciona após a aprovação da configuração

1. Abrir/atualizar uma PR executa os testes existentes e o build nativo Cloudflare da branch.
2. A descrição recebe um bloco automático com SHA, link e resultados de CI. Uma nova revisão de código remove o link anterior do bloco enquanto aguarda a nova versão.
3. O verificador só aceita checks bem-sucedidos do app Cloudflare configurado para o commit atual. Confere `preview-manifest.json`, branch e SHA, e verifica por SHA-256 que o HTML servido corresponde ao manifesto. Não segue redirecionamentos para outro site, para login ou para a produção.
4. Os testes são associados por SHA e PR; quando a API retorna a lista de PRs vazia, exige SHA, branch e repositório coincidentes. Testes de outro commit não são apresentados como validação da nova versão.
5. Eventos de deploy/CI atualizam o bloco. Um agendamento a cada cinco minutos faz a reconciliação de aprovações e eventos perdidos; o GitHub pode atrasar cron. Também há **Actions → Prévia e homologação funcional → Run workflow**, informando o número da PR.
6. A descrição escrita pelo autor fora do bloco é preservada. Não se faz checkout nem execução do código da PR no job privilegiado de metadados; ele não tem permissão de escrita em contents nem executa deploy/merge.

O build publica apenas `index.html`, `editor-usinagem-indexada.html`, o manifesto e `_headers`. A aplicação é copiada byte a byte, sem injeção de scripts de homologação. STL e G-code continuam sendo processados pelo navegador como na aplicação existente.

## Avaliação funcional obrigatória, por commit

O usuário configurado é **`jsjrnet`**. Após abrir a prévia do SHA atual, confira:

- Interface, pinagem/accordions e redimensionamento;
- Importação STL e XZA, desenrolamento e alinhamento;
- Reprodução, pausa, reinício, barra de progresso e remoção 3D;
- Ballnose/topo reto por alojamento e ferramenta da escultura;
- Referências Z0, bloqueios e geração/download `.nc` (sem executar na CNC).

Para registrar a avaliação na própria PR, comente com sua conta, usando a declaração na primeira linha (sem bloco de código ou citação):

```text
Homologado funcionalmente: SHA_COMPLETO_DO_COMMIT
```

Use o SHA completo de 40 caracteres exibido na descrição; substitua o texto acima. Isso também funciona quando você é autor da PR e o GitHub não permite autoaprovação. Alternativamente, quando permitido, uma revisão **Approve** do mesmo usuário para esse commit com a frase `Homologado funcionalmente` também é aceita.

Para retirar a avaliação, comente:

```text
Revogar homologação: SHA_COMPLETO_DO_COMMIT
```

Bot, checklist do autor, comentário sem SHA completo, avaliação de outro usuário ou de commit antigo não homologam a versão. Excluir/editar uma confirmação também é reconciliado. Uma revisão posterior pedindo alterações, ou uma revogação, impede a homologação até nova avaliação explícita. A automação não preenche essa confirmação pelo usuário.

O check **`homologacao-funcional`** só fica verde quando há **prévia verificada + CI aprovada + avaliação humana para o mesmo SHA**. Sem isso, fica `action_required`, ainda que os testes estejam verdes. **Nunca faz merge automático.**

### Proteção efetiva da main

Para impor a regra pelo GitHub, além de `AGENTS.md` e do template, o administrador deve configurar a regra/ruleset da `main` para exigir PR e os checks **`validate`** e **`homologacao-funcional`**, sem bypass automático. Essa alteração administrativa depende de sua autorização e não foi aplicada nesta tarefa. Faça-a após instalar a automação e confirmar que o check aparece no repositório; requerê-lo antes do bootstrap pode bloquear a própria configuração.

A regra do projeto já proíbe considerar CI verde como homologação. Sem o ruleset, um administrador ainda pode ter meios de fazer merge manual pelo GitHub; a documentação não substitui a proteção administrativa.

## Validação da configuração

```sh
node tests/test_preview.cjs
python3 -m unittest discover -s tests -v
```

Testes Node cobrem pacote estático, exclusão de arquivos privados, repetibilidade, preservação do editor, domínio de preview isolado, checks de commit antigo, manifesto/branch/hash, aprovação humana e revogação, CI verde insuficiente, atualização idempotente da descrição e eventos atrasados. A suíte Playwright existente continua verificando o editor. O teste offline do sincronizador usa mocks; não é evidência de deploy real Cloudflare.

Para reproduzir o build localmente, sem publicar, defina `CF_PAGES_COMMIT_SHA` com um SHA real e `CF_PAGES_BRANCH` com a branch e execute `node scripts/build-preview.cjs`. Esses valores são metadados públicos, não credenciais. O resultado `_preview_site` é ignorado pelo Git.

## Referências oficiais consultadas

- [Integração GitHub](https://developers.cloudflare.com/pages/configuration/git-integration/github-integration/)
- [Preview deployments e aliases](https://developers.cloudflare.com/pages/configuration/preview-deployments/)
- [Branch deployment controls](https://developers.cloudflare.com/pages/configuration/branch-build-controls/)
- [Direct Upload com CI, alternativa avaliada](https://developers.cloudflare.com/pages/how-to/use-direct-upload-with-continuous-integration/)

Homologação aqui significa avaliação funcional do software. **O G-code permanece experimental, sem homologação para execução física em CNC.**
