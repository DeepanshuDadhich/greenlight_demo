const fetch = require('node-fetch');

async function checkUrl(url) {
  const res = await fetch(url);
  return { ok: res.ok, status: res.status };
}

module.exports = { checkUrl };
