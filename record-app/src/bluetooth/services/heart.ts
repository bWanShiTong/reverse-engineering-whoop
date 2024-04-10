export function readHeartRateData(buffer: Buffer): {
  heartRate: number;
  rr: number[];
} {
  let flags = buffer[0];

  // format for hr: 1 or 2 bits, little endian
  let uint8Format = (flags & 1) == 0; // bit 0, can change
  let energyExpenditure = (flags & 8) > 0; // bit 3, can change
  let rrIntervals = (flags & 16) > 0; // bit 4, can change

  let heartRate = uint8Format ? buffer[1] : buffer.slice(1, 3).readInt16LE();
  let offset = uint8Format ? 2 : 3;

  if (energyExpenditure) {
    offset += 2;
  }

  let rr = [];
  if (rrIntervals) {
    for (let i = offset; i < buffer.length; i += 2) {
      rr.push(buffer.slice(i, i + 2).readInt16LE());
    }
  }

  return { heartRate, rr };
}
