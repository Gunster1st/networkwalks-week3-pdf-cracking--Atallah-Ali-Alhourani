# W3-PM1 — Password Cracking with John the Ripper (JTR)

**Task:** Crack the password of `My Locked PDF1.pdf` using John the Ripper.

**Result:** password = **`good-luck`** → flag **`nw{cybersecurity_flag_captured_2608}`**

## The JTR workflow

John the Ripper (and its GUI, **Johnny**) can't read a PDF directly — it cracks a
**hash**. So the flow is always two stages:

### Step 1 — Extract the `$pdf$` hash

`pdf2john` reads the PDF's encryption dictionary and outputs a crackable hash.
On Windows with the JtR "jumbo" build you'd run `pdf2john.exe` (or the Online Hash
Crack PDF extractor the lab links). Here it's done with the included `pdf2john.py`:

```
$ python3 pdf2john.py 'My Locked PDF1.pdf' > hash1.txt
$ cat hash1.txt
$pdf$4*4*128*-1028*1*16*ca7f72f11459cba469f1005a8765ed51*32*f32d8fa1bfbe2648226dffc39f7909ea0021446990b9e4114071a4d9104984c1*32*9322f50c29569712067a775264635e4954ccb1b99e209d664984054ffad30a6a
```

Reading the hash: `$pdf$` · V=4 · **R=4** · **128-bit** key · P=-1028 (permissions) ·
16-byte document ID · 32-byte `/U` · 32-byte `/O`. This is exactly what you'd load
into **Johnny → Open password file → Start new attack**.

### Step 2 — Crack the hash (dictionary attack)

Johnny/JtR hashes every word in a wordlist the same way the PDF does and stops on
the first match. Here the same dictionary attack (JtR `password.lst` + common
passwords + digit/case mangling rules) recovered the password:

```
[*] candidates tried : 482
[+] PASSWORD RECOVERED: good-luck
```

See [`transcript.txt`](transcript.txt) for the full run.

### Step 3 — Open the PDF

Enter `good-luck` → the PDF opens to the flag page:

![flag](flag_PDF1.png)

**Flag: `nw{cybersecurity_flag_captured_2608}`**

## Files
- `pdf2john.py` — standalone hash extractor (R2–R6 Standard security handler)
- `hash1.txt` — the extracted `$pdf$` hash (what Johnny loads)
- `transcript.txt` — real output of extraction + crack + verification
- `flag_PDF1.png` — the unlocked flag page
