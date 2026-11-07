// Exports a Figma node (via the FDSL bridge) to a local JPG/PNG file.
// Usage: node tools/export-node.mjs <node id> <out file> [--file "SW - FR"] [--scale 2] [--format JPG]
import { writeFileSync } from "node:fs";
import { makeRpc } from "../../fdsl/tools/web-lib.mjs";

const args = process.argv.slice(2);
const opt = (k, d) => (args.includes(k) ? args[args.indexOf(k) + 1] : d);
const [id, out] = args;
if (!id || !out) throw new Error("usage: export-node.mjs <node id> <out file>");
const rpc = makeRpc(opt("--file", "SW - FR"));
const b64 = await rpc(`
const n = await figma.getNodeByIdAsync(${JSON.stringify(id)});
const bytes = await n.exportAsync({ format: ${JSON.stringify(opt("--format", "JPG"))}, constraint: { type: "SCALE", value: ${Number(opt("--scale", 2))} } });
return figma.base64Encode(bytes);
`);
writeFileSync(out, Buffer.from(b64, "base64"));
console.log(out, Math.round(Buffer.from(b64, "base64").length / 1024) + " KB");
