# Hippie Energy Sales

Password-protected sales dashboard for the Drink Hippie team and investors, published at https://drinkhippie.github.io/team/

`index.html` is encrypted (AES-GCM, key from the password via PBKDF2). It's rebuilt every morning from the Hippie Energy investor dashboard data (Zoho CRM, Zoho Books, Shopline).

- `tools/build_page.py` builds the self-contained page from the dashboard page and its data files.
- `tools/encrypt.py` wraps it behind the password prompt (`PAGE_PASSWORD` env var).
