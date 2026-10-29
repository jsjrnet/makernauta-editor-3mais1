'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const crypto = require('node:crypto');
const { buildPreview } = require('../scripts/build-preview.cjs');
const { previewOrigin, candidates, verifyPreview, functionalApproval, validationRun, report, replaceBlock, BEGIN, END, syncPR } = require('../.github/scripts/preview-status.cjs');
const config = require('../cloudflare-preview.json');
const sha = 'a'.repeat(40), older = 'b'.repeat(40);
const pr = { number: 4, state: 'open', body: 'Descrição humana.', head: { sha, ref: 'feat/teste', repo: { full_name: 'jsjrnet/makernauta-editor-3mais1' } }, base: { ref: 'main', repo: { full_name: 'jsjrnet/makernauta-editor-3mais1' } } };
const origin = `https://123abcde.${config.project}.pages.dev`;
const cf = { id: 1, head_sha: sha, app: { slug: 'cloudflare-pages' }, status: 'completed', conclusion: 'success', output: { summary: `Preview: ${origin}` } };
const run = { id: 1, event: 'pull_request', head_sha: sha, status: 'completed', conclusion: 'success', html_url: 'https://github.com/jsjrnet/makernauta-editor-3mais1/actions/runs/1', pull_requests: [{ number: 4 }] };
const review = { id: 1, user: { login: 'jsjrnet' }, state: 'APPROVED', commit_id: sha, body: 'Homologado funcionalmente\nTestei os fluxos.' };
const html = Buffer.from('<html>Editor de usinagem indexada</html>');
const manifest = { environment: 'preview', commit: sha, branch: pr.head.ref, files: { 'editor-usinagem-indexada.html': crypto.createHash('sha256').update(html).digest('hex') } };
const fetcher = async url => new Response(url.includes('preview-manifest') ? JSON.stringify(manifest) : html);

test('build publishes only static editor files and provenance without editing sources', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'makernauta-preview-'));
  try {
    for (const file of ['index.html', 'editor-usinagem-indexada.html']) fs.writeFileSync(path.join(root, file), `<html>${file}</html>`);
    fs.writeFileSync(path.join(root, '.env'), 'do-not-publish');
    const before = fs.readFileSync(path.join(root, 'editor-usinagem-indexada.html'));
    const result = buildPreview({ root, sha, branch: pr.head.ref });
    assert.deepEqual(fs.readdirSync(path.join(root, '_preview_site')).sort(), ['_headers', 'editor-usinagem-indexada.html', 'index.html', 'preview-manifest.json']);
    assert.deepEqual(fs.readFileSync(path.join(root, '_preview_site/editor-usinagem-indexada.html')), before);
    assert.deepEqual(fs.readFileSync(path.join(root, 'editor-usinagem-indexada.html')), before);
    assert.equal(result.commit, sha);
    fs.writeFileSync(path.join(root, '_preview_site/stale.txt'), 'stale');
    buildPreview({ root, sha, branch: pr.head.ref });
    assert.equal(fs.existsSync(path.join(root, '_preview_site/stale.txt')), false);
    assert.match(fs.readFileSync(path.join(root, '_preview_site/_headers'), 'utf8'), /no-store/);
    assert.throws(() => buildPreview({ root, sha: '', branch: 'a' }));
    assert.throws(() => buildPreview({ root, sha, branch: 'a', output: '.' }));
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});
test('only isolated preview HTTPS domains are accepted; production is rejected', () => {
  assert.equal(previewOrigin(origin, config), origin);
  for (const value of [`https://${config.project}.pages.dev`, `https://main.${config.project}.pages.dev`, `http://123.${config.project}.pages.dev`, `https://x.${config.project}.pages.dev.attacker.test`, `https://x:y@123.${config.project}.pages.dev`, 'https://jsjrnet.github.io']) assert.equal(previewOrigin(value, config), null);
});
test('current successful Cloudflare check supplies a link, never unrelated or old checks', () => {
  assert.equal(candidates([cf], pr, config)[0], origin);
  assert.deepEqual(candidates([{ ...cf, head_sha: older }], pr, config), []);
  assert.deepEqual(candidates([{ ...cf, app: { slug: 'github-actions' } }], pr, config), []);
  assert.deepEqual(candidates([{ ...cf, conclusion: 'failure' }], pr, config), []);
});
test('HTTP preview verification requires exact SHA, branch and HTML content hash', async () => {
  assert.equal(await verifyPreview(origin, pr, config, fetcher), true);
  assert.equal(await verifyPreview(origin, { ...pr, head: { ...pr.head, sha: older } }, config, fetcher), false);
  assert.equal(await verifyPreview(origin, { ...pr, head: { ...pr.head, ref: 'other' } }, config, fetcher), false);
  assert.equal(await verifyPreview(origin, pr, config, async url => new Response(url.includes('preview-manifest') ? JSON.stringify(manifest) : 'wrong HTML')), false);
  assert.equal(await verifyPreview(origin, pr, config, async () => new Response('login', { status: 403 })), false);
});
test('functional approval must be human, explicit and for the latest SHA', () => {
  assert.equal(functionalApproval([review], sha, 'jsjrnet'), true);
  for (const replacement of [{ commit_id: older }, { user: { login: 'bot' } }, { state: 'COMMENTED' }, { body: 'Não homologado funcionalmente' }, { body: 'CI verde' }]) assert.equal(functionalApproval([{ ...review, ...replacement }], sha, 'jsjrnet'), false);
  assert.equal(functionalApproval([review, { ...review, id: 2, state: 'CHANGES_REQUESTED' }], sha, 'jsjrnet'), false);
  assert.equal(functionalApproval([review, { ...review, id: 2, state: 'DISMISSED' }], sha, 'jsjrnet'), false);
});
test('CI success alone never homologates; every prerequisite must refer to this commit', () => {
  assert.equal(report({ pr, url: origin, run, approved: false, config }).passed, false);
  assert.equal(report({ pr, url: null, run, approved: true, config }).passed, false);
  assert.equal(report({ pr, url: origin, run: { ...run, conclusion: 'failure' }, approved: true, config }).passed, false);
  assert.equal(report({ pr, url: origin, run, approved: true, config }).passed, true);
  assert.equal(validationRun([{ ...run, head_sha: older }], pr), null);
});
test('description preserves human text, replaces old links, and is idempotent', () => {
  const old = `${BEGIN}\nOLD URL\n${END}`;
  const source = `Human before\n${old}\nHuman after`;
  const block = report({ pr, url: null, run, approved: false, config }).body;
  const result = replaceBlock(source, block);
  assert.match(result, /^Human before/); assert.match(result, /Human after$/);
  assert.doesNotMatch(result, /OLD URL/);
  assert.equal(replaceBlock(result, block), result);
});
test('stale deployment events cannot update a newer PR commit', async () => {
  const writes = []; let reads = 0;
  const request = (route, method = 'GET', body) => {
    if (method !== 'GET') { writes.push({ route, method, body }); return {}; }
    if (/\/pulls\/4$/.test(route)) return reads++ ? { ...pr, head: { ...pr.head, sha: older } } : pr;
    if (route.includes('check-runs')) return { check_runs: [cf] };
    if (route.includes('/comments')) return [];
    if (route.includes('/reviews')) return [review];
    if (route.includes('/runs?')) return { workflow_runs: [run] };
    throw new Error(route);
  };
  await syncPR(4, { repo: pr.base.repo.full_name, config, request, fetcher });
  assert.deepEqual(writes, []);
});
test('verified preview goes directly into PR description and creates a manual approval gate', async () => {
  const writes = [];
  const request = (route, method = 'GET', body) => {
    if (method !== 'GET') { writes.push({ route, method, body }); return {}; }
    if (/\/pulls\/4$/.test(route)) return pr;
    if (route.includes('check-runs')) return { check_runs: [cf] };
    if (route.includes('/comments')) return [];
    if (route.includes('/reviews')) return [];
    if (route.includes('/runs?')) return { workflow_runs: [run] };
    throw new Error(route);
  };
  await syncPR(4, { repo: pr.base.repo.full_name, config, request, fetcher });
  assert.match(writes[0].body.body, new RegExp(origin.replaceAll('.', '\\.') + '/editor-usinagem-indexada.html'));
  assert.equal(writes[1].body.name, 'homologacao-funcional');
  assert.equal(writes[1].body.conclusion, 'action_required');
  assert.equal(writes.some(write => /\/merge$/.test(write.route)), false);
});

test('owner can homologate their own PR by a SHA-specific comment; bots and old SHAs cannot', () => {
  const comment = { id: 10, user: { login: 'jsjrnet', type: 'User' }, body: `Homologado funcionalmente: ${sha}` };
  assert.equal(functionalApproval([], sha, 'jsjrnet', [comment]), true);
  assert.equal(functionalApproval([], older, 'jsjrnet', [comment]), false);
  assert.equal(functionalApproval([], sha, 'jsjrnet', [{ ...comment, user: { login: 'jsjrnet', type: 'Bot' } }]), false);
  assert.equal(functionalApproval([], sha, 'jsjrnet', [comment, { ...comment, id: 11, body: `Revogar homologação: ${sha}` }]), false);
});
test('CI runs with empty PR metadata still require exact SHA, repository and branch', () => {
  const empty = { ...run, pull_requests: [], head_branch: pr.head.ref, head_repository: pr.head.repo };
  assert.equal(validationRun([empty], pr), empty);
  assert.equal(validationRun([{ ...empty, head_branch: 'other' }], pr), null);
  assert.equal(validationRun([{ ...empty, head_repository: { full_name: 'other/repo' } }], pr), null);
});

test('quoted examples and explanatory comments are not functional approvals', () => {
  const user = { login: 'jsjrnet', type: 'User' };
  assert.equal(functionalApproval([], sha, 'jsjrnet', [{ id: 1, user, body: `Exemplo de mensagem:\nHomologado funcionalmente: ${sha}` }]), false);
  assert.equal(functionalApproval([], sha, 'jsjrnet', [{ id: 1, user, body: `> Homologado funcionalmente: ${sha}` }]), false);
});
