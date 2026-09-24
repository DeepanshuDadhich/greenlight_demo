const UNITS = ['B', 'KB', 'MB', 'GB', 'TB'];

function formatBytes(bytes, decimals = 1) {
  if (!Number.isFinite(bytes) || bytes < 0) {
    throw new RangeError('bytes must be a non negative finite number');
  }
  if (bytes === 0) return '0 B';
  const exponent = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), UNITS.length - 1);
  const value = bytes / 1024 ** exponent;
  return `${Number(value.toFixed(decimals))} ${UNITS[exponent]}`;
}

module.exports = { formatBytes };
