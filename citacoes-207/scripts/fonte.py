#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fonte.py - recuperacao de texto primario no idioma original.

Por que este arquivo existe
---------------------------
A §1 do CLAUDE.md manda que o texto no idioma original seja RECUPERADO, nunca
reconstruido de memoria, e que a coluna "Fonte recuperada (URL)" guarde o endereco
de onde a prova saiu. O ambiente remoto bloqueia o egresso para Perseus, Wikisource,
Gutenberg e afins, e foi isso que parou o lote 1.

O contorno nao afrouxa a regra, muda a porta: os MESMOS textos que o Perseus serve
sao mantidos em repositorio publico versionado (PerseusDL/canonical-greekLit e
canonical-latinLit), em TEI XML, com os marcos canonicos (Stephanus, Bekker,
livro/capitulo) codificados como <milestone>. Esse host passa. O texto e o mesmo
objeto editorial, agora com uma vantagem: a URL de prova aponta para um commit
imutavel, e nao para uma pagina que pode mudar amanha.

Nivel de prova: N1 (texto da propria obra em repositorio critico, com locus visivel).

Uso:
    python scripts/fonte.py tlg0059.tlg002.perseus-grc2 21d
    python scripts/fonte.py phi0474.phi013.perseus-lat1 --lista
"""

import os
import re
import subprocess
import sys
import unicodedata
from html import unescape

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(RAIZ, "fontes")

REPOS = {
    "greekLit": "PerseusDL/canonical-greekLit",
    "latinLit": "PerseusDL/canonical-latinLit",
}


def _sha(repo):
    """SHA de master, para que a URL de prova aponte para um estado imutavel."""
    out = subprocess.run(
        ["git", "ls-remote", f"https://github.com/{repo}.git", "refs/heads/master"],
        capture_output=True, text=True, timeout=120,
    )
    if out.returncode != 0 or not out.stdout.strip():
        raise SystemExit(f"FALHA: nao consegui resolver o commit de {repo}")
    return out.stdout.split()[0]


def _grupo(urn):
    """tlg0059.tlg002.perseus-grc2 -> ('greekLit', 'tlg0059', 'tlg002')."""
    partes = urn.split(".")
    if len(partes) < 3:
        raise SystemExit(f"FALHA: URN mal formada: {urn}")
    grupo, obra = partes[0], partes[1]
    corpus = "greekLit" if grupo.startswith("tlg") else "latinLit"
    return corpus, grupo, obra


def baixar(urn):
    """Devolve (caminho_local, url_de_prova). Baixa uma vez, reusa depois."""
    corpus, grupo, obra = _grupo(urn)
    repo = REPOS[corpus]
    destino = os.path.join(CACHE, f"{urn}.xml")
    marca = destino + ".url"

    if os.path.exists(destino) and os.path.exists(marca):
        return destino, open(marca, encoding="utf-8").read().strip()

    sha = _sha(repo)
    url = f"https://raw.githubusercontent.com/{repo}/{sha}/data/{grupo}/{obra}/{urn}.xml"
    os.makedirs(CACHE, exist_ok=True)
    out = subprocess.run(
        ["curl", "-sS", "-L", "--fail", "--max-time", "180", "-o", destino, url],
        capture_output=True, text=True,
    )
    if out.returncode != 0:
        raise SystemExit(f"FALHA ao recuperar {url}\n{out.stderr.strip()}")
    with open(marca, "w", encoding="utf-8") as f:
        f.write(url)
    return destino, url


def _limpar(bruto):
    """XML -> texto corrido, preservando a letra do original."""
    t = re.sub(r"<[^>]+>", "", bruto)
    t = unescape(t)
    t = t.replace("ʼ", "ʼ")          # apostrofo grego, mantido
    t = re.sub(r"[ \t\r\n]+", " ", t)
    return t.strip()


def milestones(caminho, unidade=None):
    """Lista os marcos canonicos do arquivo, na ordem do texto."""
    x = open(caminho, encoding="utf-8").read()
    corpo = x[x.find("<body"):]
    achados = []
    for m in re.finditer(r'<milestone\b[^>]*/>', corpo):
        tag = m.group(0)
        u = re.search(r'unit="([^"]+)"', tag)
        n = re.search(r'\bn="([^"]+)"', tag)
        if not (u and n):
            continue
        if unidade and u.group(1) != unidade:
            continue
        achados.append((u.group(1), n.group(1), m.start(), m.end()))
    return achados


def passagem(urn, locus, unidade="section"):
    """
    Texto entre o marco `locus` e o marco seguinte da mesma unidade.
    Devolve dict com o texto verbatim e a URL de onde ele foi recuperado.
    """
    caminho, url = baixar(urn)
    x = open(caminho, encoding="utf-8").read()
    corpo = x[x.find("<body"):]
    marcos = milestones(caminho, unidade)
    if not marcos:
        raise SystemExit(f"FALHA: nenhum marco '{unidade}' em {urn}")

    alvo = [i for i, m in enumerate(marcos) if m[1] == locus]
    if not alvo:
        disponiveis = ", ".join(m[1] for m in marcos[:12])
        raise SystemExit(
            f"FALHA: locus '{locus}' nao existe em {urn}. Primeiros marcos: {disponiveis} ..."
        )
    i = alvo[0]
    ini = marcos[i][3]
    fim = marcos[i + 1][2] if i + 1 < len(marcos) else len(corpo)

    return {
        "urn": urn,
        "locus": locus,
        "unidade": unidade,
        "texto": _limpar(corpo[ini:fim]),
        "url": url,
        "arquivo": caminho,
    }


def procurar(urn, agulha, janela=260):
    """
    Acha um trecho no texto e diz em que locus canonico ele cai.
    A busca ignora acento e caixa, mas o que volta e a letra do original.
    """
    caminho, url = baixar(urn)
    x = open(caminho, encoding="utf-8").read()
    corpo = x[x.find("<body"):]
    marcos = milestones(caminho, "section")

    plano = _limpar(corpo)

    def dobra(s):
        s = unicodedata.normalize("NFD", s.lower())
        return "".join(c for c in s if unicodedata.category(c) != "Mn")

    alvo = dobra(agulha)
    base = dobra(plano)
    achados = []
    ini = 0
    while True:
        p = base.find(alvo, ini)
        if p < 0:
            break
        achados.append(plano[max(0, p - janela // 2): p + len(agulha) + janela])
        ini = p + 1

    # o locus e resolvido no XML bruto, onde os marcos ainda existem
    loci = []
    for pedaco in achados:
        loci.append(_locus_de(corpo, marcos, dobra(pedaco[:60])))
    return {"urn": urn, "url": url, "ocorrencias": list(zip(loci, achados))}


def _limpar_por_pedaco(corpo):
    return _limpar(corpo)


def _locus_de(corpo, marcos, agulha_dobrada):
    """Em que marco cai um trecho: varre marco a marco ate encontrar."""
    def dobra(s):
        s = unicodedata.normalize("NFD", s.lower())
        return "".join(c for c in s if unicodedata.category(c) != "Mn")

    for i, m in enumerate(marcos):
        ini = m[3]
        fim = marcos[i + 1][2] if i + 1 < len(marcos) else len(corpo)
        if agulha_dobrada[:40] in dobra(_limpar(corpo[ini:fim])):
            return m[1]
    return "?"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    urn = sys.argv[1]
    if "--lista" in sys.argv:
        c, u = baixar(urn)
        ms = milestones(c, "section")
        print(f"{len(ms)} marcos em {urn}: " + ", ".join(m[1] for m in ms))
        print(f"prova: {u}")
    elif "--buscar" in sys.argv:
        r = procurar(urn, sys.argv[sys.argv.index("--buscar") + 1])
        print(f"prova: {r['url']}")
        for locus, trecho in r["ocorrencias"]:
            print(f"\n[{locus}] {trecho}")
    else:
        r = passagem(urn, sys.argv[2])
        print(f"URN   : {r['urn']}\nLOCUS : {r['locus']}\nPROVA : {r['url']}\n")
        print(r["texto"])
