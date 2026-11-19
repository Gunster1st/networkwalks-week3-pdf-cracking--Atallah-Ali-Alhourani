# NetworkWalks — Week 3 Project: PDF Password Cracking

> Cybersecurity & Ethical Hacking Internship (Batch 84) — Week 3 Project Work
> Author: **Atallah Ali Al-Hourani** · GitHub: [@Gunster1st](https://github.com/Gunster1st)

Week 3 is about **password cracking**: how a password-protected file stores its
password as a *hash*, how that hash is extracted, and how a dictionary attack
recovers the original password — proving why weak passwords fail.

Two mandatory modules, both cracking password-protected PDFs:

| Module | Tool | File cracked | Password | Flag |
|--------|------|--------------|----------|------|
| **W3-PM1** | John the Ripper (`pdf2john` + dictionary) | `My Locked PDF1.pdf` | `good-luck` | `nw{cybersecurity_flag_captured_2608}` |
| **W3-PM2** | NetworkWalks Hash Calculator + Password Cracker | `My Locked PDF1 (NW Tools).pdf` | `password1` | `nw{networkwalks_flag1_jtr_270521_1}` |

### Bonus — extra locked PDFs cracked the same way

| File | Password | Flag |
|------|----------|------|
| `My Locked PDF2.pdf` | `password1` | `nw{networkwalks_persistence_jtr_270521}` |
| `My Locked PDF3.pdf` | `1qaz2wsx` | `nw{networkwalks_flag_260821_1}` |

---

## How PDF password cracking works (the big picture)

1. **The file is encrypted, but the password is recoverable.** A password-protected
   PDF stores verification data (the `/O` and `/U` strings, the permissions `/P`,
   the revision `/R` and key length) in its *encryption dictionary*. It never
   stores the password itself — only values derived from it.
2. **Extract a crackable hash.** A tool like `pdf2john` reads those values and
   packs them into a single string starting with `$pdf$…`. This is the same format
   John the Ripper and hashcat understand.
3. **Attack the hash offline.** A dictionary attack hashes every candidate word the
   same way the PDF does and compares. The first match *is* the password. No limit
   on attempts, no lockouts — this is why **offline cracking is so fast against weak
   passwords**.
4. **Verify.** Open the PDF with the recovered password → the flag page appears.

All four passwords here fell in **under a minute** combined. A simple 8-character
lowercase password can fall in minutes; a strong 12+ character mixed password can
take years. **That difference is the whole lesson.**

## Repo layout

```
Week3-Solved/
├── README.md                         ← you are here
├── module1-jtr/                      ← W3-PM1: John the Ripper
│   ├── README.md
│   ├── pdf2john.py                   ← hash extractor (standalone, no install)
│   ├── hash1.txt                     ← extracted $pdf$ hash
│   ├── transcript.txt                ← real run output
│   └── flag_PDF1.png                 ← unlocked flag page
├── module2-nwtools/                  ← W3-PM2: NetworkWalks online tools
│   ├── README.md
│   ├── hash.txt                      ← $pdf$ hash from the Hash Calculator
│   ├── 01_hash_calculator.jpg        ← Hash Calculator extracting the hash (live)
│   ├── 02_password_cracked.jpg       ← Password Cracker → "password1" (live)
│   ├── 03_cracking_live.jpg
│   └── flag_demo.png                 ← unlocked flag page
└── bonus-extra-pdfs/                 ← PDF2 & PDF3 cracked the same way
    ├── README.md
    ├── flag_PDF2.png
    └── flag_PDF3.png
```

## Defensive takeaway

- Weak, common, or dictionary passwords are recovered in seconds once a file leaves
  your control — the attacker cracks **offline**, so rate-limiting never applies.
- Use long passphrases (4+ random words) or a password manager.
- For truly sensitive files, strong encryption + a strong password is the only thing
  standing between the attacker and the contents.

*Educational use only — all files are NetworkWalks training lab material cracked on
my own machine as part of the internship.*
