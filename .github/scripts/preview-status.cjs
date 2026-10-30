'use strict';
const crypto = require('node:crypto');
const { execFileSync } = require('node:child_process');
const fs = require('node:fs');
const BEGIN = '<!-- makernauta-preview:start -->';
const END = '<!-- makernauta-preview:end -->';
const CHECK = 'homologacao-funcional';

function validConfig(config) {
  if (!/^[a-z0-9](?:[a-z0-9-]{0,56}[a-z0-9])?$/.test(config.project || '')) throw new Error('Projeto Cloudflare inválido.');
  if (!/^[a-z0-9-]+$/i.test(config.functionalReviewer || '')) throw new Error('Revisor funcional inválido.');
  if (!Array.isArray(config.cloudflareApps) || !config.cloudflareApps.length) throw new Error('Apps Cloudflare não configurados.');
}
function previewOrigin(value, config) {
  try {
    const url = new URL(value);
    const suffix = '.' + config.project + '.pages.dev';
    if (url.protocol !== 'https:' || url.username || url.password || url.port || !url.hostname.endsWith(suffix)) return null;
    const label = url.hostname.slice(0, -suffix.length);
    if (!/^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$/.test(label)) return null;
    const production = config.productionBranch.toLowerCase().replace(/[^a-z0-9]/g, '-');
    return label === production ? null : url.origin;
  } catch (_) { return null; }
}
function candidates(checks, pr, config) {
  const approved = checks.filter(check => config.cloudflareApps.includes(check.app?.slug) && check.head_sha === pr.head.sha && check.status === 'completed' && check.conclusion === 'success');
  const urls = [];
  for (const check of approved.sort((a, b) => b.id - a.id)) {
    const text = [check.details_url, check.output?.summary, check.output?.text].filter(Boolean).join('\n');
    for (const match of text.matchAll(/https:\/\/[a-zA-Z0-9.-]+\.pages\.dev(?:\/[^\s<>"'\)]*)?/g)) {
      const origin = previewOrigin(match[0], config);
      if (origin) urls.push(origin);
    }
  }
  // Official branch alias fallback, used only after a Cloudflare check succeeds.
  // Do not guess truncation of long branch names or publish unverified aliases.
  if (approved.length && pr.head.repo?.full_name === pr.base.repo.full_name) {
    const alias = pr.head.ref.toLowerCase().replace(/[^a-z0-9]/g, '-');
    const origin = previewOrigin(`https://${alias}.${config.project}.pages.dev`, config);
    if (origin) urls.push(origin);
  }
  return [...new Set(urls)];
}
async function limitedResponse(response, maximum) {
  if (response.status !== 200) throw new Error('A prévia ainda não respondeu com HTTP 200.');
  const chunks = []; let length = 0;
  for await (const chunk of response.body) {
    length += chunk.length;
    if (length > maximum) throw new Error('Resposta da prévia excede o limite.');
    chunks.push(chunk);
  }
  return Buffer.concat(chunks);
}
async function verifyPreview(origin, pr, config, fetcher = fetch) {
  if (!previewOrigin(origin, config)) return false;
  try {
    // No redirect to an authentication page, production site or third-party host.
    const options = { redirect: 'error', signal: AbortSignal.timeout(15000) };
    const manifest = JSON.parse((await limitedResponse(await fetcher(`${origin}/preview-manifest.json?commit=${pr.head.sha}`, options), 65536)).toString('utf8'));
    if (manifest.environment !== 'preview' || manifest.commit !== pr.head.sha || manifest.branch !== pr.head.ref) return false;
    const expected = manifest.files?.['editor-usinagem-indexada.html'];
    if (!/^[a-f0-9]{64}$/.test(expected || '')) return false;
    const html = await limitedResponse(await fetcher(`${origin}/editor-usinagem-indexada.html?commit=${pr.head.sha}`, { ...options, signal: AbortSignal.timeout(15000) }), 4 * 1024 * 1024);
    return crypto.createHash('sha256').update(html).digest('hex') === expected;
  } catch (_) { return false; }
}
function functionalApproval(reviews, sha, reviewer, comments = []) {
  const owner = user => user?.login?.toLowerCase() === reviewer.toLowerCase() && user.type !== 'Bot';
  const votes = reviews.filter(review => owner(review.user) && ['APPROVED', 'CHANGES_REQUESTED', 'DISMISSED'].includes(review.state)).map(review => ({
    time: Date.parse(review.submitted_at) || review.id,
    approved: review.state === 'APPROVED' && review.commit_id === sha && /^Homologado funcionalmente(?:[.:]|\s|$)/i.test((review.body || '').trim().split(/\r?\n/, 1)[0])
  }));
  for (const comment of comments.filter(comment => owner(comment.user))) {
    const match = (comment.body || '').trim().split(/\r?\n/, 1)[0].match(/^(Homologado funcionalmente|Revogar homologação):\s*([a-f0-9]{40})\s*$/i);
    if (match && match[2].toLowerCase() === sha) votes.push({ time: Date.parse(comment.updated_at || comment.created_at) || comment.id, approved: match[1].toLowerCase() === 'homologado funcionalmente' });
  }
  return votes.sort((a, b) => a.time - b.time).at(-1)?.approved === true;
}
function validationRun(runs, pr) {
  return runs.filter(run => run.event === 'pull_request' && run.head_sha === pr.head.sha && (
    run.pull_requests?.some(item => item.number === pr.number) ||
    (!run.pull_requests?.length && run.head_branch === pr.head.ref && run.head_repository?.full_name === pr.head.repo?.full_name)
  )).sort((a, b) => b.id - a.id)[0] || null;
}

function report({ pr, url, run, approved, config, cloudflareFailed = false }) {
  const sha = pr.head.sha;
  const tests = !run ? '⏳ aguardando a CI deste commit' : run.status !== 'completed' ? `[⏳ em execução](${run.html_url})` : run.conclusion === 'success' ? `[✅ aprovados](${run.html_url})` : `[❌ ${run.conclusion}](${run.html_url})`;
  const preview = url ? `[**Abrir prévia do Editor**](${url}/editor-usinagem-indexada.html?commit=${sha})` : cloudflareFailed ? '❌ Cloudflare não concluiu o deploy deste commit. Corrija o deploy; nenhuma prévia antiga foi homologada.' : '⏳ Prévia pendente: conecte/configure o projeto Cloudflare ou aguarde o deploy deste commit. Não há link verificado para esta versão.';
  const functional = approved ? `✅ avaliação funcional registrada por @${config.functionalReviewer} para este commit` : `⏳ aguardando avaliação funcional de @${config.functionalReviewer}`;
  const passed = !!url && run?.status === 'completed' && run.conclusion === 'success' && approved;
  return {
    passed,
    body: `${BEGIN}\n### Homologação funcional — prévia independente\n\n${preview}\n\n- Commit da prévia: \`${sha}\`\n- Testes automatizados: ${tests}.\n- Homologação: ${functional}.\n\n**CI verde não homologa a atualização.** Teste interface, STL, simulação 3D, fresas e geração de G-code. Depois, comente **Homologado funcionalmente: ${sha}** nesta PR, usando sua conta. Também é aceita uma revisão **Approve** com a frase **Homologado funcionalmente** para este commit, quando o GitHub permitir. Novo commit exige nova avaliação. Não há merge automático.\n\nO G-code permanece experimental e não homologado para execução física.\n${END}`
  };
}
function replaceBlock(body, block) {
  const first = body.indexOf(BEGIN), last = body.indexOf(END);
  if (first >= 0 && last >= first) return body.slice(0, first) + block + body.slice(last + END.length);
  return body.trimEnd() + (body.trim() ? '\n\n' : '') + block;
}
// The GitHub CLI inherits its injected authentication; no token is read or printed.
function api(route, method = 'GET', body) {
  const args = ['api', '--method', method, route];
  if (body !== undefined) args.push('--input', '-');
  const result = execFileSync('gh', args, { input: body === undefined ? undefined : JSON.stringify(body), encoding: 'utf8', maxBuffer: 16 * 1024 * 1024 });
  return result.trim() ? JSON.parse(result) : null;
}
function paginate(route, key, request = api) {
  const all = [];
  for (let page = 1; ; page++) {
    const data = request(`${route}${route.includes('?') ? '&' : '?'}per_page=100&page=${page}`);
    const batch = key ? data[key] : data;
    all.push(...batch);
    if (batch.length < 100) return all;
  }
}
async function syncPR(number, { repo, config, request = api, fetcher = fetch, bodyOnly = false }) {
  const root = `repos/${repo}`, pr = request(`${root}/pulls/${number}`);
  if (pr.state !== 'open' || pr.base.ref !== config.productionBranch) return;
  const sha = pr.head.sha;
  if (!/^[a-f0-9]{40}$/.test(sha)) throw new Error('SHA inválido na PR.');
  const checks = paginate(`${root}/commits/${sha}/check-runs`, 'check_runs', request);
  const comments = paginate(`${root}/issues/${number}/comments`, null, request);
  const reviews = paginate(`${root}/pulls/${number}/reviews`, null, request);
  const runs = paginate(`${root}/actions/workflows/${config.validationWorkflow}/runs?event=pull_request&head_sha=${sha}`, 'workflow_runs', request);
  let url = null;
  for (const origin of candidates(checks, pr, config)) if (await verifyPreview(origin, pr, config, fetcher)) { url = origin; break; }
  const result = report({ pr, url, run: validationRun(runs, pr), approved: functionalApproval(reviews, sha, config.functionalReviewer, comments), config, cloudflareFailed: checks.some(check => config.cloudflareApps.includes(check.app?.slug) && check.head_sha === sha && ['failure', 'cancelled', 'timed_out'].includes(check.conclusion)) });
  // Re-read to avoid clobbering human edits or publishing a stale result after a push.
  const fresh = request(`${root}/pulls/${number}`);
  if (fresh.state !== 'open' || fresh.head.sha !== sha) return;
  const body = replaceBlock(fresh.body || '', result.body);
  if (body !== fresh.body) request(`${root}/pulls/${number}`, 'PATCH', { body });
  if (!bodyOnly) {
    const existing = checks.find(check => check.name === CHECK && check.app?.slug === 'github-actions');
    const payload = { name: CHECK, head_sha: sha, status: 'completed', conclusion: result.passed ? 'success' : 'action_required', output: { title: result.passed ? 'CI, prévia e avaliação funcional aprovadas' : 'Avaliação funcional necessária para este commit', summary: result.body }, external_id: `makernauta-functional-${number}-${sha}` };
    if (existing) { delete payload.head_sha; request(`${root}/check-runs/${existing.id}`, 'PATCH', payload); }
    else request(`${root}/check-runs`, 'POST', payload);
  }
  console.log(`PR #${number}: prévia ${url ? 'verificada' : 'pendente'}; homologação ${result.passed ? 'registrada' : 'pendente'}.`);
  return result;
}
async function main() {
  const config = JSON.parse(fs.readFileSync('cloudflare-preview.json', 'utf8')); validConfig(config);
  const repo = process.env.GITHUB_REPOSITORY || 'jsjrnet/makernauta-editor-3mais1';
  if (!/^[\w.-]+\/[\w.-]+$/.test(repo)) throw new Error('Repositório inválido.');
  const event = process.env.GITHUB_EVENT_PATH ? JSON.parse(fs.readFileSync(process.env.GITHUB_EVENT_PATH, 'utf8')) : {};
  if (event.issue && !event.issue.pull_request) return;
  if (event.check_run && !config.cloudflareApps.includes(event.check_run.app?.slug)) return;
  let numbers = [];
  const manual = process.argv.find(arg => arg.startsWith('--pr='))?.slice(5) || event.inputs?.pr;
  if (manual && /^[1-9]\d*$/.test(String(manual))) numbers = [Number(manual)];
  else if (event.pull_request?.number) numbers = [event.pull_request.number];
  else if (event.issue?.pull_request) numbers = [event.issue.number];
  else numbers = paginate(`repos/${repo}/pulls?state=open&base=${config.productionBranch}`, null).map(pr => pr.number);
  for (const number of numbers) await syncPR(number, { repo, config, bodyOnly: process.argv.includes('--body-only') });
}
if (require.main === module) main().catch(error => { console.error(error.message); process.exitCode = 1; });
module.exports = { BEGIN, END, validConfig, previewOrigin, candidates, verifyPreview, functionalApproval, validationRun, report, replaceBlock, syncPR };
