const Buffer = require("buffer/").Buffer;

export type PackageAA5C = {
  unix: number;
  heartRate: number;
  rrIntervals: number[];
};

export function decode_aa5c(packet: string) {
  const buf = Buffer.from(packet, "hex");
  const unix = buf.slice(11, 15).readUInt32LE();
  const heartRate = buf.slice(21, 22).readUint8();

  let rr = [];
  let rrIntervals = buf.slice(22, 23).readUint8() * 2;
  if (rrIntervals > 0) {
    for (let i = 0; i < rrIntervals; i += 2) {
      rr.push(buf.slice(23 + i, 23 + i + 2).readInt16LE());
    }
  }

  return {
    unix,
    heartRate,
    rrIntervals,
  };
}
