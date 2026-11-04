import html, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from data import C

OUT = sys.argv[1]
OR, BK, CR, PN, S1, S2 = "#FF7A1F", "#050F16", "#FFF4EA", "#10232F", "#C3CBD0", "#3A4750"
PAL = {
  "dark":   dict(bg=BK, fg=CR, sub=S1, mut="#8E9AA1", pan=PN, line="#1E3442"),
  "cream":  dict(bg=CR, fg=BK, sub=S2, mut="#5B6770", pan="#EFE3D6", line="#E2D5C7"),
  "orange": dict(bg=OR, fg=BK, sub=BK, mut=BK, pan=BK, line=BK),
}
LOGO = '<svg viewBox="0 0 844 845" width="{s}" height="{s}" aria-hidden="true"><rect width="844" height="845" fill="#FF7A1F"/><circle cx="355" cy="517" r="146" fill="none" stroke="#050F16" stroke-width="93"/><rect x="455" y="147" width="92" height="516" fill="#050F16"/><rect x="620" y="570" width="92" height="92" fill="#050F16"/></svg>'
LOGO_BK = '<svg viewBox="0 0 844 845" width="{s}" height="{s}" aria-hidden="true"><rect width="844" height="845" fill="#050F16"/><circle cx="355" cy="517" r="146" fill="none" stroke="#FF7A1F" stroke-width="93"/><rect x="455" y="147" width="92" height="516" fill="#FF7A1F"/><rect x="620" y="570" width="92" height="92" fill="#FF7A1F"/></svg>'
ARROW = '<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
CHECK = '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12.5l5 5L20 6.5"/></svg>'
CROSS = '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="3" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>'
AR = "font-family:Archivo,sans-serif"
e = lambda s: html.escape(s, quote=False).replace(" €", "\u00a0€").replace(" %", "\u00a0%")

def hl(s, fg, bg):
    s = e(s)
    return re.sub(r"\[\[(.+?)\]\]", lambda m: f'<span style="background:{bg};color:{fg};padding:0 12px;-webkit-box-decoration-break:clone;box-decoration-break:clone">{m.group(1)}</span>', s)

def fs(text, steps):
    n = len(re.sub(r"\[\[|\]\]", "", text))
    for lim, size in steps:
        if n <= lim: return size
    return steps[-1][1]

def page(title, body, w=1080, h=1350):
    return f'<!doctype html><html lang="pt-PT"><head><meta charset="utf-8"><title>{e(title)}</title></head><body style="margin:0">{body}</body></html>'

def frame(p, inner, extra=""):
    return f'<div style="width:1080px;height:1350px;box-sizing:border-box;padding:80px;background:{p["bg"]};color:{p["fg"]};font-family:Inter,sans-serif;position:relative;overflow:hidden;display:flex;flex-direction:column;justify-content:space-between">{extra}{inner}</div>'

def header(p, n, accent_num=True, logo=LOGO):
    numc = OR if (accent_num and p["bg"] == BK) else p["fg"]
    return f'<div style="display:flex;justify-content:space-between;align-items:center;position:relative"><div style="display:flex;align-items:center;gap:14px">{logo.format(s=60)}<span style="{AR};font-weight:800;font-size:32px;letter-spacing:-0.02em">destaca</span></div><span style="{AR};font-weight:700;font-size:28px;color:{numc}">{n:02d}/07</span></div>'

def footer(p, left="SEO &amp; Sites de Apresentação"):
    ac = OR if p["bg"] == BK else p["fg"]
    return f'<div style="display:flex;justify-content:space-between;align-items:center;position:relative;{AR};font-weight:700;font-size:26px"><span style="color:{p["mut"]}">{left}</span><span style="display:inline-flex;align-items:center;gap:10px;color:{ac}">Desliza {ARROW.format(c=ac)}</span></div>'

def ring(size, border, color, pos):
    return f'<div aria-hidden="true" style="position:absolute;width:{size}px;height:{size}px;box-sizing:border-box;border:{border}px solid {color};border-radius:50%;{pos}"></div>'

def box(p, label, text, filled):
    if filled:
        return f'<div style="background:{OR};color:{BK};padding:30px 36px;display:flex;flex-direction:column;gap:10px"><span style="{AR};font-weight:800;font-size:24px;letter-spacing:0.12em;text-transform:uppercase">{e(label)}</span><span style="font-size:34px;line-height:1.35;font-weight:600">{e(text)}</span></div>'
    return f'<div style="border:4px solid {OR};padding:28px 34px;display:flex;flex-direction:column;gap:10px"><span style="{AR};font-weight:800;font-size:24px;letter-spacing:0.12em;text-transform:uppercase;color:{OR}">{e(label)}</span><span style="font-size:34px;line-height:1.35;font-weight:600">{e(text)}</span></div>'

TSTEPS = [(24, 88), (34, 80), (44, 72), (999, 64)]

# ---------------- capas ----------------
def cover(c):
    kind = c["cover"]
    h1size = fs(c["h1"], [(26, 132), (38, 116), (52, 100), (999, 88)])
    if kind == "BF":
        p = PAL["dark"]
        extra = ring(760, 140, OR, "right:-300px;bottom:-360px")
        tag = f'<div style="display:flex;gap:16px;align-items:center"><span style="background:{OR};color:{BK};padding:12px 24px;{AR};font-weight:900;font-size:30px;letter-spacing:0.1em">BLACK FRIDAY</span><span style="{AR};font-weight:800;font-size:30px;color:{OR}">27 NOV</span></div>'
        h1 = hl(c["h1"], BK, OR); btn_bg, btn_fg, arr = OR, BK, BK
    elif kind == "A":
        p = PAL["orange"]
        extra = ring(760, 140, BK, "right:-300px;bottom:-360px")
        tag = f'<span style="align-self:flex-start;border:4px solid {BK};padding:10px 22px;{AR};font-weight:800;font-size:26px;letter-spacing:0.12em;text-transform:uppercase">{e(c["tag"])}</span>'
        h1 = hl(c["h1"], OR, BK); btn_bg, btn_fg, arr = BK, CR, OR
    elif kind == "B":
        p = PAL["dark"]
        extra = ring(900, 160, OR, "left:-460px;bottom:-520px")
        tag = f'<span style="align-self:flex-start;color:{OR};{AR};font-weight:800;font-size:28px;letter-spacing:0.14em;text-transform:uppercase">{e(c["tag"])}</span>'
        h1 = hl(c["h1"], BK, OR); btn_bg, btn_fg, arr = OR, BK, BK
    else:  # C
        p = PAL["cream"]
        extra = f'<div aria-hidden="true" style="position:absolute;right:-30px;bottom:-110px;{AR};font-weight:900;font-size:{620 if len(c.get("bignum","5"))==1 else 440}px;line-height:1;letter-spacing:-0.06em;color:{OR}">{e(c.get("bignum","5"))}</div>'
        tag = f'<span style="align-self:flex-start;background:{BK};color:{CR};padding:10px 22px;{AR};font-weight:800;font-size:26px;letter-spacing:0.12em;text-transform:uppercase">{e(c["tag"])}</span>'
        h1 = hl(c["h1"], OR, BK); btn_bg, btn_fg, arr = BK, CR, OR
    quote = ""
    if c.get("quote"):
        qc = p["mut"] if kind != "A" else BK
        quote = f'<p style="margin:0;{AR};font-weight:800;font-size:56px;line-height:1.08;letter-spacing:-0.02em;color:{qc};text-decoration:line-through;text-decoration-color:{OR};text-decoration-thickness:7px;max-width:880px">{e(c["quote"])}</p>'
    sub = f'<p style="margin:0;font-size:38px;line-height:1.32;font-weight:500;max-width:680px;color:{p["fg"] if kind in ("A","C") else S1}">{e(c["sub"])}</p>' if c.get("sub") else ""
    head = f'<div style="display:flex;justify-content:space-between;align-items:center;position:relative"><div style="display:flex;align-items:center;gap:16px">{(LOGO_BK if kind=="A" else LOGO).format(s=76)}<span style="{AR};font-weight:800;font-size:36px;letter-spacing:-0.02em">destaca</span></div><span style="{AR};font-weight:700;font-size:28px;color:{OR if p["bg"]==BK else p["fg"]}">01/07</span></div>'
    mid = f'<div style="display:flex;flex-direction:column;gap:36px;position:relative;margin-bottom:120px">{tag}{quote}<h1 style="margin:0;{AR};font-weight:900;font-size:{h1size}px;line-height:0.95;letter-spacing:-0.04em;max-width:900px">{h1}</h1>{sub}</div>'
    btn = f'<div style="position:relative;display:flex;justify-content:{"flex-end" if kind=="B" else "flex-start"}"><span style="display:inline-flex;align-items:center;gap:14px;background:{btn_bg};color:{btn_fg};padding:20px 32px;{AR};font-weight:800;font-size:30px">Desliza {ARROW.format(c=arr).replace("30","34")}</span></div>'
    return frame(p, head + mid + btn, extra)

# ---------------- slides do meio ----------------
def numblock(p, i):
    col = OR if p["bg"] == BK else p["fg"]
    sq = f'<span aria-hidden="true" style="width:34px;height:34px;background:{OR};display:inline-block;margin-bottom:22px"></span>' if p["bg"] != BK else ""
    return f'<div style="display:flex;align-items:flex-end;gap:22px"><span style="{AR};font-weight:900;font-size:170px;line-height:0.8;letter-spacing:-0.05em;color:{col}">{i:02d}</span>{sq}</div>'

def s_lista(c, it, i, p):
    extra = ring(560, 96, p["pan"], "right:-200px;top:-180px") if p["bg"] == BK else ""
    t = f'<h2 style="margin:0;{AR};font-weight:900;font-size:{fs(it["t"], TSTEPS)}px;line-height:1;letter-spacing:-0.03em">{e(it["t"])}</h2>'
    b = f'<p style="margin:0;font-size:36px;line-height:1.4;color:{p["sub"]};max-width:880px">{e(it["b"])}</p>'
    mid = f'<div style="display:flex;flex-direction:column;gap:34px;position:relative">{numblock(p, i)}{t}{b}{box(p, it["xl"], it["x"], p["bg"] != BK)}</div>'
    return frame(p, header(p, i + 1) + mid + footer(p), extra)

def s_passos(c, it, i, p):
    word = c.get("stepword", "Passo")
    bars = "".join(f'<div style="flex:1;height:14px;background:{OR if k <= i else p["pan"]}"></div>' for k in range(1, 6))
    prog = f'<div style="display:flex;flex-direction:column;gap:18px"><div style="display:flex;gap:10px">{bars}</div><span style="{AR};font-weight:800;font-size:26px;letter-spacing:0.12em;text-transform:uppercase;color:{OR if p["bg"]==BK else p["fg"]}">{e(word)} {i} de 5</span></div>'
    t = f'<h2 style="margin:0;{AR};font-weight:900;font-size:{fs(it["t"], [(24, 96), (34, 86), (999, 76)])}px;line-height:0.98;letter-spacing:-0.035em">{e(it["t"])}</h2>'
    b = f'<p style="margin:0;font-size:38px;line-height:1.4;color:{p["sub"]};max-width:880px">{e(it["b"])}</p>'
    mid = f'<div style="display:flex;flex-direction:column;gap:40px">{prog}{t}{b}{box(p, it["xl"], it["x"], p["bg"] != BK)}</div>'
    return frame(p, header(p, i + 1) + mid + footer(p))

def s_check(c, it, i, p):
    cb = f'<div style="display:flex;align-items:center;gap:28px"><div style="width:120px;height:120px;box-sizing:border-box;border:8px solid {OR};display:flex;align-items:center;justify-content:center;background:{OR if p["bg"]!=BK else "transparent"}">{CHECK.format(s=78, c=BK if p["bg"]!=BK else OR)}</div><span style="{AR};font-weight:800;font-size:28px;letter-spacing:0.12em;text-transform:uppercase;color:{OR if p["bg"]==BK else p["mut"]}">{i} de 5</span></div>'
    t = f'<h2 style="margin:0;{AR};font-weight:900;font-size:{fs(it["t"], TSTEPS)}px;line-height:1;letter-spacing:-0.03em">{e(it["t"])}</h2>'
    b = f'<p style="margin:0;font-size:36px;line-height:1.4;color:{p["sub"]};max-width:880px">{e(it["b"])}</p>'
    mid = f'<div style="display:flex;flex-direction:column;gap:36px">{cb}{t}{b}{box(p, it["xl"], it["x"], p["bg"] != BK)}</div>'
    return frame(p, header(p, i + 1) + mid + footer(p))

def s_mito(c, it, i, p):
    chip = f'<span style="align-self:flex-start;background:{BK};color:{CR};padding:10px 22px;{AR};font-weight:800;font-size:26px;letter-spacing:0.14em">MITO {i}</span>'
    m = f'<h2 style="margin:0;{AR};font-weight:900;font-size:{fs(it["m"], [(30, 104), (42, 90), (999, 78)])}px;line-height:0.98;letter-spacing:-0.04em;text-decoration:line-through;text-decoration-color:{OR};text-decoration-thickness:9px">{e(it["m"])}</h2>'
    r = f'<div style="background:{OR};padding:52px;display:flex;flex-direction:column;gap:22px"><span style="{AR};font-weight:800;font-size:26px;letter-spacing:0.14em">REALIDADE</span><p style="margin:0;{AR};font-weight:800;font-size:58px;line-height:1.05;letter-spacing:-0.02em">{e(it["r"])}</p><p style="margin:0;font-size:34px;line-height:1.4;font-weight:500">{e(it["b"])}</p></div>'
    top = f'<div style="display:flex;flex-direction:column;gap:28px">{chip}{m}</div>'
    return frame(p, header(p, i + 1) + top + r + footer(p))

def s_antesdepois(c, it, i, p):
    dark = p["bg"] == BK
    lab = f'<span style="{AR};font-weight:800;font-size:26px;letter-spacing:0.12em;text-transform:uppercase;color:{OR if dark else p["mut"]}">{i} de 5 · {e(it["t"])}</span>'
    ante = f'<div style="background:{p["pan"]};padding:34px 38px;display:flex;flex-direction:column;gap:16px"><span style="display:flex;align-items:center;gap:14px;{AR};font-weight:800;font-size:24px;letter-spacing:0.14em;color:{p["mut"]}">{CROSS.format(s=34, c=p["mut"])}ANTES</span><span style="font-size:44px;line-height:1.25;color:{p["mut"]};text-decoration:line-through;text-decoration-thickness:3px">{e(it["a"])}</span></div>'
    dep = f'<div style="background:{OR};color:{BK};padding:34px 38px;display:flex;flex-direction:column;gap:16px"><span style="display:flex;align-items:center;gap:14px;{AR};font-weight:800;font-size:24px;letter-spacing:0.14em">{CHECK.format(s=34, c=BK)}DEPOIS</span><span style="{AR};font-weight:800;font-size:52px;line-height:1.1;letter-spacing:-0.02em">{e(it["d"])}</span></div>'
    b = f'<p style="margin:0;font-size:36px;line-height:1.4;color:{p["sub"]}">{e(it["b"])}</p>'
    mid = f'<div style="display:flex;flex-direction:column;gap:30px">{lab}{ante}{dep}{b}</div>'
    return frame(p, header(p, i + 1) + mid + footer(p))

def s_linha(c, it, i, p):
    rows = ""
    for k, other in enumerate(c["items"], 1):
        on = k == i
        dot = f'<div style="width:{44 if on else 26}px;height:{44 if on else 26}px;background:{OR if k <= i else p["line"]};flex-shrink:0"></div>'
        rows += f'<div style="display:flex;align-items:center;gap:22px;height:128px"><div style="width:44px;display:flex;justify-content:center">{dot}</div><span style="{AR};font-weight:{900 if on else 700};font-size:{38 if on else 30}px;color:{p["fg"] if on else p["mut"]}">{e(other["w"])}</span></div>'
    tl = f'<div style="position:relative;display:flex;flex-direction:column;width:300px;flex-shrink:0"><div style="position:absolute;left:20px;top:48px;bottom:48px;width:4px;background:{p["line"]}"></div><div style="position:relative">{rows}</div></div>'
    right = f'<div style="flex:1;display:flex;flex-direction:column;gap:30px;min-width:0"><span style="{AR};font-weight:900;font-size:76px;line-height:0.9;letter-spacing:-0.04em">{e(it["w"])}</span><div style="height:10px;width:120px;background:{OR}"></div><h2 style="margin:0;{AR};font-weight:900;font-size:{fs(it["t"], [(24, 72), (999, 64)])}px;line-height:1.02;letter-spacing:-0.03em">{e(it["t"])}</h2><p style="margin:0;font-size:36px;line-height:1.42;color:{p["sub"]}">{e(it["b"])}</p></div>'
    mid = f'<div style="display:flex;gap:40px;align-items:center">{tl}{right}</div>'
    return frame(p, header(p, i + 1) + mid + footer(p))

def s_faq(c, it, i, p):
    q = f'<div aria-hidden="true" style="position:absolute;right:40px;top:150px;{AR};font-weight:900;font-size:520px;line-height:1;color:{p["pan"]}">?</div>'
    lab = f'<span style="{AR};font-weight:800;font-size:26px;letter-spacing:0.12em;text-transform:uppercase;color:{OR}">Pergunta {i} de 5</span>'
    t = f'<h2 style="margin:0;{AR};font-weight:900;font-size:{fs(it["t"], [(24, 100), (999, 88)])}px;line-height:0.98;letter-spacing:-0.04em">“{e(it["t"])}”</h2>'
    b = f'<p style="margin:0;font-size:36px;line-height:1.4;color:{p["sub"]};max-width:880px">{e(it["b"])}</p>'
    mid = f'<div style="display:flex;flex-direction:column;gap:36px;position:relative">{lab}{t}{b}{box(p, it["xl"], it["x"], False)}</div>'
    return frame(p, header(p, i + 1) + mid + footer(p), q)

L = dict(lista=s_lista, passos=s_passos, check=s_check, mito=s_mito, antesdepois=s_antesdepois, linha=s_linha, faq=s_faq)

ICONS = [
  '<path d="M6 3h12v18l-6-4-6 4z"/>',
  '<path d="M22 2L11 13M22 2l-7 20-4-9-9-4z"/>',
  '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>',
]
def cta(c):
    p = PAL["orange"]
    extra = ring(480, 90, BK, "right:-200px;top:-260px")
    head = f'<div style="display:flex;align-items:center;gap:16px;position:relative">{LOGO_BK.format(s=76)}<span style="{AR};font-weight:800;font-size:36px;letter-spacing:-0.02em">destaca</span></div>'
    rows = "".join(f'<div style="display:flex;align-items:center;gap:24px;background:{BK};color:{CR};padding:26px 32px"><svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="{OR}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="flex-shrink:0">{ic}</svg><span style="font-size:34px;font-weight:600">{txt}</span></div>'
                   for ic, txt in zip(ICONS, ["Guarda para voltares a ver", "Envia a um amigo empresário", "Manda “SITE” por mensagem"]))
    mid = f'<div style="display:flex;flex-direction:column;gap:38px;position:relative"><h2 style="margin:0;{AR};font-weight:900;font-size:{fs(c["cta"], [(30, 104), (999, 90)])}px;line-height:0.96;letter-spacing:-0.04em">{e(c["cta"])}</h2><p style="margin:0;font-size:38px;line-height:1.35;font-weight:500;max-width:860px">{e(c["ctasub"])}</p><div style="display:flex;flex-direction:column;gap:14px">{rows}</div></div>'
    foot = f'<div style="display:flex;justify-content:space-between;align-items:center;position:relative;{AR};font-weight:800;font-size:28px"><span>Segue a Destaca</span><span>SEO &amp; Sites de Apresentação</span></div>'
    return frame(p, head + mid + foot, extra)

for c in C:
    d = os.path.join(OUT, c["slug"]); os.makedirs(d, exist_ok=True)
    p = PAL[c["bg"]]
    slides = [cover(c)] + [L[c["layout"]](c, it, i, p) for i, it in enumerate(c["items"], 1)] + [cta(c)]
    assert len(slides) == 7
    for k, s in enumerate(slides, 1):
        open(os.path.join(d, f"{k:02d}.html"), "w").write(page(f'{c["slug"]} {k:02d}', s))
    n = len(re.findall(r"#\w+", c["cap"]))
    assert n == 5, (c["slug"], n)
    open(os.path.join(d, "legenda.txt"), "w").write(c["cap"].strip() + "\n")
print(len(C), "carrosséis")
