const { test } = require('node:test');
const assert = require('node:assert/strict');
const { formatBytes } = require('../src/formatBytes');

test('formatBytes scales to the largest fitting unit', () => {
  assert.equal(formatBytes(0), '0 B');
  assert.equal(formatBytes(512), '512 B');
  assert.equal(formatBytes(1536), '1.5 KB');
  assert.equal(formatBytes(5 * 1024 ** 3), '5 GB');
});

test('formatBytes rejects negative input', () => {
  assert.throws(() => formatBytes(-1), RangeError);
});
