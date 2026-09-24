const { test } = require('node:test');
const assert = require('node:assert/strict');
const http = require('node:http');
const { checkUrl } = require('../src/checkUrl');

test('checkUrl reports the status of a local server', async (t) => {
  const server = http.createServer((req, res) => {
    res.statusCode = req.url === '/missing' ? 404 : 200;
    res.end();
  });
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  t.after(() => server.close());

  const base = `http://127.0.0.1:${server.address().port}`;
  assert.deepEqual(await checkUrl(`${base}/`), { ok: true, status: 200 });
  assert.deepEqual(await checkUrl(`${base}/missing`), { ok: false, status: 404 });
});
