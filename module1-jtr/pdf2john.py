#!/usr/bin/env python3
"""Minimal pdf2john: extract a John-the-Ripper / hashcat compatible $pdf$ hash
from an encrypted PDF (Standard security handler, /R 2,3,4,5,6).
Output format matches JtR jumbo's pdf2john.pl for /R<=4 and the
$pdf$<V>*<R>*<keylen>*<P>*<meta>*<idlen>*<id>*<ulen>*<U>*<olen>*<O> layout.
"""
import sys, re

def find_obj(data, num):
    m = re.search((str(num)+r"\s+0\s+obj").encode(), data)
    if not m: return None
    start = m.end()
    end = data.find(b"endobj", start)
    return data[start:end]

def hx(b): return b.hex()

def parse_encrypt(enc, idhex):
    def grab(key):
        m = re.search((r"/"+key+r"\s*(-?\d+)").encode(), enc)
        return int(m.group(1)) if m else None
    V = grab("V"); R = grab("R"); P = grab("P")
    # take the document encryption key length (top-level /Length, e.g. 128),
    # not the crypt-filter's byte /Length (e.g. 16)
    lens = [int(x) for x in re.findall(rb"/Length\s*(\d+)", enc)]
    length = max(lens) if lens else 40
    def grabstr(key):
        # hex string <...>
        m = re.search((r"/"+key+r"\s*<([0-9A-Fa-f]+)>").encode(), enc)
        if m: return bytes.fromhex(m.group(1).decode())
        # literal string (...) with escapes
        m = re.search((r"/"+key+r"\s*\(").encode(), enc)
        if m:
            i = m.end(); out=b""
            while i < len(enc):
                c = enc[i:i+1]
                if c==b"\\": out+=enc[i+1:i+2]; i+=2; continue
                if c==b")": break
                out+=c; i+=1
            return out
        return b""
    O = grabstr("O"); U = grabstr("U")
    keylen = length//8
    return V,R,P,keylen,O,U

def main(path):
    data = open(path,"rb").read()
    # trailer / xref-stream Encrypt + ID
    mid = re.search(rb"/ID\s*\[\s*<([0-9A-Fa-f]+)>", data)
    idhex = mid.group(1).decode() if mid else ""
    menc = re.search(rb"/Encrypt\s+(\d+)\s+\d+\s+R", data)
    if not menc:
        print("[!] No /Encrypt (not encrypted?)", file=sys.stderr); return 1
    enc = find_obj(data, int(menc.group(1)))
    V,R,P,keylen,O,U = parse_encrypt(enc, idhex)
    idb = bytes.fromhex(idhex) if idhex else b""
    # JtR $pdf$ format (R<=4)
    name = path.split("/")[-1]
    h = "$pdf$%d*%d*%d*%d*%d*%d*%s*%d*%s*%d*%s" % (
        V, R, keylen*8, P, 1, len(idb), hx(idb),
        len(U), hx(U), len(O), hx(O))
    print("%s:%s" % (name, h))
    return 0

if __name__=="__main__":
    for p in sys.argv[1:]:
        main(p)
