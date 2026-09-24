const { test } = require('node:test');
const assert = require('node:assert/strict');
const { slugify } = require('../src/slugify');

test('slugify lowercases and joins words with dashes', () => {
  assert.equal(slugify('Hello World'), 'hello-world');
});

test('slugify strips accents and punctuation', () => {
  assert.equal(slugify('  Crème Brûlée!!  '), 'creme-brulee');
});
