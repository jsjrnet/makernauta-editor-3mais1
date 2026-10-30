'use strict';
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');

function buildPreview({ root = process.cwd(), output = '_preview_site', sha, branch }) {
  if (!/^[a-f0-9]{40}$/i.test(sha || '')) throw new Error('CF_PAGES_COMMIT_SHA ausente ou inválido.');
  if (!branch || branch.length > 256 || /[\x00-\x1f\x7f]/.test(branch)) throw new Error('CF_PAGES_BRANCH ausente ou inválida.');
  const destination = path.resolve(root, output);
  if (path.dirname(destination) !== path.resolve(root) || path.basename(destination) !== '_preview_site') {
    throw new Error('A saída deve ser _preview_site, sem sobrepor arquivos do projeto.');
  }
  // Remove stale build outputs; never delete or rewrite source files.
  fs.rmSync(destination, { recursive: true, force: true });
  fs.mkdirSync(destination, { recursive: true });
  const files = {};
  for (const name of ['index.html', 'editor-usinagem-indexada.html']) {
    const bytes = fs.readFileSync(path.join(root, name));
    fs.writeFileSync(path.join(destination, name), bytes);
    files[name] = crypto.createHash('sha256').update(bytes).digest('hex');
  }
  const manifest = { environment: 'preview', commit: sha.toLowerCase(), branch, files };
  fs.writeFileSync(path.join(destination, 'preview-manifest.json'), JSON.stringify(manifest, null, 2) + '\n');
  fs.writeFileSync(path.join(destination, '_headers'), '/*\n  Cache-Control: no-store\n  X-Robots-Tag: noindex, nofollow\n  X-Makernauta-Environment: preview\n');
  return manifest;
}
if (require.main === module) {
  try { buildPreview({ sha: process.env.CF_PAGES_COMMIT_SHA, branch: process.env.CF_PAGES_BRANCH }); }
  catch (error) { console.error(error.message); process.exitCode = 1; }
}
module.exports = { buildPreview };
