"""One-shot patch: completion screen on the brand charter (left aligned, sentence case,
no eyebrow, no grey box, H2 / body / softnote styles of the form steps).

Usage: python3 tools/patch-completion-charte.py
"""
from pathlib import Path

path = Path(__file__).resolve().parent.parent / "html" / "saywho-book-us.html"
html = path.read_text(encoding="utf-8")

REPLACE = [
    ("YOUR REQUEST HAS BEEN SENT.", "Your request has been sent."),
    ("YOUR DISCOVERY CALL IS BOOKED.", "Your discovery call is booked."),
    ("VOTRE DEMANDE A BIEN ÉTÉ ENVOYÉE.", "Votre demande a bien été envoyée."),
    ("VOTRE RENDEZ-VOUS EST CONFIRMÉ.", "Votre rendez-vous est confirmé."),
    ("LA TUA RICHIESTA È STATA INVIATA.", "La tua richiesta è stata inviata."),
    ("LA TUA CALL È CONFERMATA.", "La tua call è confermata."),
    ("SIMULATION ONLY — ", "Simulation only — "),
    ("'SIMULATION — ", "'Simulation — "),
    ("'SIMULAZIONE — ", "'Simulazione — "),
    ('<div class="tiny">THANK YOU · SAY WHO</div>', ""),
]
for old, new in REPLACE:
    if old not in html:
        raise SystemExit(f"not found: {old}")
    html = html.replace(old, new)

CSS = """
/* ---------- Completion screen on the charter ---------- */
#completionArea{margin-top:40px;padding:0;border:0;border-radius:0;text-align:left}
#completionArea .success-mark{width:40px;height:40px;margin:0 0 24px}
#completionArea .success-mark svg{width:18px;height:18px;stroke-width:2}
#completionArea h3{margin:0 0 16px;max-width:none;font-weight:500;font-size:36px;line-height:1.2;letter-spacing:-.02em}
#completionArea .muted{max-width:none;margin:0 0 16px;font-size:15px;line-height:1.3;color:var(--gray)}
#completionArea .demo-note{max-width:none;margin:0 0 16px;padding:0;border:0;border-radius:0;background:none;font-size:14px;line-height:1.17;color:var(--gray-2)}
#completionArea .softnote{margin:0 0 32px}
@media (max-width:720px){#completionArea h3{font-size:28px}}
"""
if "</style>" not in html:
    raise SystemExit("no </style>")
html = html.replace("</style>", CSS + "</style>", 1)
path.write_text(html, encoding="utf-8")
print("patched", path)
