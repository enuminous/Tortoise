#!/usr/bin/env python3
"""Build the Zoo's animal/equation illustrations as editable SVG, without image generation.

Usage: python scripts/build_animal_images.py [--force]
The existing hand-drawn Tortoise SVG is preserved unless --force is passed.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "images/animals"
MANIFEST = OUT / "provenance.json"
PALETTE = ["#9daf78", "#86b4b0", "#d1a45c", "#93a3c7", "#bc8c72", "#93aa87", "#c6ad73"]
EDGE = "#f0d991"


def color_for(name: str) -> str:
    return PALETTE[hashlib.sha256(name.encode()).digest()[0] % len(PALETTE)]


def mammal(name: str, fill: str) -> str:
    """Stylized quadruped, with anatomical details selected by species."""
    e = EDGE
    bits = [
        f'<ellipse cx="-5" cy="20" rx="132" ry="65" fill="{fill}" stroke="{e}" stroke-width="4"/>',
        f'<path d="M55 3 Q89 -54 130 -48 L151 -15 Q128 18 95 34Z" fill="{fill}" stroke="{e}" stroke-width="4"/>',
        f'<ellipse cx="145" cy="-48" rx="52" ry="43" fill="{fill}" stroke="{e}" stroke-width="4"/>',
        f'<path d="M177 -34 L220 -20 L180 -7Z" fill="{fill}" stroke="{e}" stroke-width="3"/>',
        f'<path d="M-94 58 L-91 123 Q-92 141 -108 143 Q-126 142 -125 123 L-121 52 M-40 73 L-34 128 Q-34 144 -51 145 Q-68 144 -68 128 L-69 66 M45 68 L49 128 Q49 144 32 145 Q15 143 16 127 L15 60 M94 47 L104 119 Q106 138 89 141 Q72 140 70 122 L63 48" fill="{fill}" stroke="{e}" stroke-width="5" stroke-linecap="round"/>',
        f'<path d="M-132 4 Q-174 -18 -181 8 Q-181 29 -155 31" fill="none" stroke="{e}" stroke-width="8" stroke-linecap="round"/>',
        '<circle cx="158" cy="-57" r="6" fill="#12201d"/><circle cx="160" cy="-59" r="2" fill="#fff4cf"/>',
    ]
    if name in {"Cat", "Lynx", "Fox", "Wolf", "Shepherd", "Weasel", "Mole", "Bonobo"}:
        ears = 'M112 -79 L105 -128 L142 -91Z M155 -87 L181 -123 L187 -76Z' if name in {"Cat", "Lynx", "Fox", "Wolf", "Weasel"} else 'M108 -76 Q99 -115 126 -98Z M166 -91 Q195 -107 184 -70Z'
        bits.append(f'<path d="{ears}" fill="{fill}" stroke="{e}" stroke-width="4"/>')
    if name == "Elephant":
        bits += [f'<path d="M113 -61 Q55 -132 89 -24 Q95 8 130 2 Q151 -8 144 -32Z" fill="{fill}" stroke="{e}" stroke-width="4"/>',
                 f'<path d="M178 -21 Q191 24 181 66 Q176 82 164 69 Q159 61 166 39 L161 -8Z" fill="{e}" stroke="{e}" stroke-width="2"/>',
                 f'<path d="M134 -3 Q117 19 131 20 M136 -3 Q149 21 160 18" fill="none" stroke="#f7e6b6" stroke-width="5"/>']
    if name == "Bison":
        bits += [f'<path d="M-111 -17 Q-102 -113 -13 -100 Q78 -109 96 -37 L55 50 L-115 49Z" fill="{fill}" stroke="{e}" stroke-width="4"/>',
                 f'<path d="M105 -75 Q71 -111 69 -80 M174 -77 Q206 -111 214 -74" fill="none" stroke="{e}" stroke-width="8"/>']
    if name == "Rhino":
        bits.append(f'<path d="M183 -45 L226 -67 L204 -26Z" fill="{e}" stroke="{e}" stroke-width="2"/>')
    if name in {"Horse", "Phoenix"}:
        bits.append(f'<path d="M84 -70 Q38 -112 57 -44 Q75 -22 101 -37 Q118 -54 84 -70Z" fill="#6a4932" stroke="{e}" stroke-width="3"/>')
    if name in {"Fox", "Wolf", "Lynx"}:
        bits.append(f'<path d="M-151 8 Q-215 -32 -248 13 Q-226 62 -163 37Z" fill="{fill}" stroke="{e}" stroke-width="4"/>')
    if name == "Beaver":
        bits.append(f'<ellipse cx="-207" cy="35" rx="53" ry="28" transform="rotate(-20 -207 35)" fill="#70583d" stroke="{e}" stroke-width="4"/>')
    if name == "Mole":
        bits.append(f'<ellipse cx="207" cy="-27" rx="12" ry="8" fill="#e99694" stroke="{e}" stroke-width="2"/>')
    if name == "Lynx":
        bits.append(f'<path d="M113 -113 L124 -139 L135 -105 M170 -106 L191 -134 L190 -99" fill="none" stroke="#e7e0b8" stroke-width="6"/>')
    if name in {"Cat", "Lynx", "Lion", "Circus"}:
        bits.append(f'<circle cx="143" cy="-45" r="65" fill="none" stroke="#e0b95d" stroke-width="12" stroke-dasharray="8 5"/>')
    if name in {"Lion", "Circus"}:
        bits.append(f'<path d="M203 -23 Q230 -17 223 -5 M203 -18 Q230 -28 236 -17" fill="none" stroke="{e}" stroke-width="3"/>')
    if name == "Shepherd":
        bits.append(f'<path d="M-20 24 Q27 41 71 25" fill="none" stroke="#b65045" stroke-width="13"/><circle cx="28" cy="34" r="5" fill="{e}"/>')
    if name == "Bonobo":
        bits.append(f'<path d="M77 25 Q45 87 28 129 M95 28 Q103 83 124 112" fill="none" stroke="{e}" stroke-width="13" stroke-linecap="round"/>')
    if name == "Harlequinn":
        # Provisional fish-like silhouette because the repository contains only its name.
        bits.append(f'<path d="M-110 -34 L-70 15 L-110 58 M-35 -35 L5 16 L-36 59 M42 -35 L80 12 L43 58" fill="none" stroke="#f6e3a2" stroke-width="12"/>')
    return "".join(bits)


def bird(name: str, fill: str) -> str:
    e = EDGE
    bits = [
        f'<ellipse cx="-5" cy="10" rx="100" ry="67" fill="{fill}" stroke="{e}" stroke-width="4"/>',
        f'<path d="M-30 6 Q10 -72 80 -39 Q48 8 8 46 Q-2 20 -30 6Z" fill="#526854" stroke="{e}" stroke-width="4"/>',
        f'<circle cx="72" cy="-48" r="43" fill="{fill}" stroke="{e}" stroke-width="4"/>',
        f'<path d="M109 -50 L169 -37 L108 -25Z" fill="#d59748" stroke="{e}" stroke-width="3"/>',
        f'<path d="M-95 -4 L-165 -42 L-135 8 L-167 48 L-86 31Z" fill="{fill}" stroke="{e}" stroke-width="4"/>',
        f'<path d="M-42 72 L-48 123 M22 74 L27 123 M-67 125 L-40 125 M8 125 L39 125" fill="none" stroke="{e}" stroke-width="6" stroke-linecap="round"/>',
        '<circle cx="83" cy="-55" r="6" fill="#12201d"/><circle cx="85" cy="-57" r="2" fill="#fff4cf"/>',
    ]
    if name in {"Owl", "Eagle", "Falcon", "Phoenix", "Woodpecker"}:
        bits.append(f'<path d="M49 -78 Q31 -132 58 -106 L76 -79 M90 -81 Q111 -135 116 -99 L104 -67" fill="{fill}" stroke="{e}" stroke-width="4"/>')
    if name == "Owl":
        bits += [f'<circle cx="60" cy="-48" r="20" fill="none" stroke="#ead9a7" stroke-width="5"/><circle cx="101" cy="-48" r="20" fill="none" stroke="#ead9a7" stroke-width="5"/>',
                 f'<path d="M81 -28 L74 -9 L88 -28Z" fill="#e3b655"/>']
    if name in {"Eagle", "Falcon"}:
        bits.append(f'<path d="M105 -44 Q148 -39 133 -11 Q129 -4 119 -9" fill="none" stroke="#e3b655" stroke-width="8"/>')
    if name == "Penguin":
        bits.append('<ellipse cx="-4" cy="22" rx="47" ry="50" fill="#f4ead0" stroke="#cfc29a" stroke-width="2"/>')
    if name == "Woodpecker":
        bits.append(f'<path d="M50 -87 Q35 -123 67 -104 L88 -83Z" fill="#c64f46" stroke="{e}" stroke-width="2"/>')
    if name == "Magpie":
        bits.append(f'<path d="M-80 24 Q-25 1 18 42 L-8 58Z" fill="#e9e1c8"/>')
    if name == "Phoenix":
        bits.append(f'<path d="M-38 -16 Q-118 -112 -183 -103 Q-137 -43 -110 7 Q-155 10 -200 59 Q-115 67 -59 43Z" fill="#d76b42" stroke="#f3be68" stroke-width="4"/>')
    if name in {"Raven", "Nightingale"}:
        bits.append(f'<path d="M130 -20 Q150 -10 171 -24" fill="none" stroke="{e}" stroke-width="3"/>')
    return "".join(bits)


def fish(name: str, fill: str) -> str:
    e = EDGE
    bits = [
        f'<path d="M-180 0 Q-103 -94 45 -71 Q126 -55 157 0 Q126 55 45 71 Q-103 94 -180 0Z" fill="{fill}" stroke="{e}" stroke-width="4"/>',
        f'<path d="M-173 0 L-244 -62 L-231 0 L-244 62Z" fill="{fill}" stroke="{e}" stroke-width="4"/>',
        f'<path d="M-5 -61 L45 -118 L74 -57 M-4 61 L38 111 L73 56 M-68 2 Q-33 41 -68 66" fill="{fill}" stroke="{e}" stroke-width="4"/>',
        '<circle cx="105" cy="-19" r="7" fill="#10201e"/><circle cx="107" cy="-21" r="2" fill="#fff4cf"/>',
    ]
    if name == "Shark":
        bits += [f'<path d="M-4 -59 L30 -144 L69 -57Z" fill="{fill}" stroke="{e}" stroke-width="4"/>',
                 f'<path d="M137 11 Q111 31 84 13" fill="#eee3c4" stroke="#263536" stroke-width="2"/>',
                 f'<path d="M104 14l9 12 8-12 9 12 8-12" fill="none" stroke="#243436" stroke-width="3"/>',
                 f'<path d="M70 -15 Q60 0 70 17 M56 -13 Q46 0 56 14 M42 -10 Q32 0 42 10" fill="none" stroke="{e}" stroke-width="3"/>']
    if name in {"Salmon", "Harlequinn"}:
        bits.append(f'<path d="M-115 -41 Q-70 -5 -115 40 M-42 -57 Q3 -4 -42 57 M35 -57 Q78 -4 35 56" fill="none" stroke="#f2d999" stroke-width="5"/>')
    if name == "Harlequinn":
        bits.append(f'<path d="M-150 -10 L-125 -40 L-100 -10 L-125 20Z M-75 -20 L-48 -50 L-20 -20 L-48 10Z M0 -18 L27 -45 L53 -18 L27 9Z" fill="#f2d999"/>')
    return "".join(bits)


def marine(name: str, fill: str) -> str:
    e = EDGE
    body = f'<path d="M-235 5 Q-170 -83 -22 -67 Q100 -57 156 -11 Q194 5 223 0 Q190 19 164 26 Q80 88 -50 63 Q-165 48 -235 5Z" fill="{fill}" stroke="{e}" stroke-width="4"/>'
    tail = f'<path d="M-218 4 Q-245 -51 -269 -67 Q-261 -24 -289 3 Q-258 27 -267 64 Q-238 43 -218 4Z" fill="{fill}" stroke="{e}" stroke-width="4"/>'
    bits = [body, tail,
            f'<path d="M-8 -55 Q16 -117 63 -115 L45 -49 M4 48 Q40 89 72 95 L45 43" fill="{fill}" stroke="{e}" stroke-width="4"/>',
            '<circle cx="145" cy="-22" r="6" fill="#12201d"/><circle cx="147" cy="-24" r="2" fill="#fff4cf"/>']
    if name == "Dolphin":
        bits.append(f'<path d="M175 -7 Q230 -4 256 -29 Q244 -1 215 12 Q242 31 255 46 Q215 34 176 22Z" fill="{fill}" stroke="{e}" stroke-width="3"/>')
    if name == "Whale":
        bits.append(f'<path d="M-20 -65 Q-32 -108 -23 -124 Q-6 -103 3 -63" fill="none" stroke="#86c8c7" stroke-width="9" stroke-linecap="round"/>')
    if name == "Orca":
        bits += ['<path d="M68 -44 Q105 -65 130 -37 L113 -18 L74 -19Z" fill="#f5efda"/>',
                 '<path d="M57 42 Q100 30 136 32 L119 54 Q86 62 57 42Z" fill="#f5efda"/>',
                 f'<path d="M10 -62 L27 -130 L60 -58Z" fill="#18282c" stroke="{e}" stroke-width="3"/>']
    return "".join(bits)


def lizard(name: str, fill: str) -> str:
    e = EDGE
    bits = [
        f'<ellipse cx="-14" cy="10" rx="116" ry="45" fill="{fill}" stroke="{e}" stroke-width="4"/>',
        f'<path d="M80 2 Q127 -42 175 -26 Q206 -14 215 1 Q188 28 145 25 L88 25Z" fill="{fill}" stroke="{e}" stroke-width="4"/>',
        f'<path d="M-100 15 Q-165 5 -201 48 Q-227 80 -205 92 Q-177 105 -171 75 Q-167 59 -145 68" fill="none" stroke="{fill}" stroke-width="22" stroke-linecap="round"/><path d="M-100 15 Q-165 5 -201 48 Q-227 80 -205 92 Q-177 105 -171 75 Q-167 59 -145 68" fill="none" stroke="{e}" stroke-width="3"/>',
        f'<path d="M-78 36 L-121 83 L-157 87 M-33 42 L-12 92 L15 103 M48 36 L76 80 L108 86 M74 17 L123 57 L153 56" fill="none" stroke="{e}" stroke-width="8" stroke-linecap="round"/>',
        '<circle cx="190" cy="-10" r="6" fill="#12201d"/>',
    ]
    if name == "Chameleon":
        bits += [f'<circle cx="168" cy="-48" r="23" fill="{fill}" stroke="{e}" stroke-width="4"/><circle cx="168" cy="-50" r="7" fill="#17201e"/>',
                 f'<path d="M206 5 Q244 0 251 19 Q257 36 236 37" fill="none" stroke="#db7564" stroke-width="5"/>']
    if name == "Gecko":
        bits.append(f'<g fill="{e}"><circle cx="-157" cy="87" r="9"/><circle cx="-141" cy="91" r="8"/><circle cx="-7" cy="96" r="9"/><circle cx="9" cy="103" r="8"/><circle cx="108" cy="84" r="9"/><circle cx="124" cy="89" r="8"/><circle cx="148" cy="55" r="8"/></g>')
    return "".join(bits)


def crocodile(fill: str) -> str:
    e = EDGE
    return (f'<path d="M-225 23 Q-142 -40 -18 -26 L99 -12 L204 -38 L239 -15 L196 8 L230 31 Q155 58 77 39 Q-66 79 -181 48Z" fill="{fill}" stroke="{e}" stroke-width="4"/>'
            f'<path d="M-158 24 L-203 62 L-236 66 M-70 39 L-97 79 L-128 84 M68 39 L92 78 L122 83 M139 25 L174 61 L204 62" fill="none" stroke="{e}" stroke-width="8" stroke-linecap="round"/>'
            f'<path d="M-140 -16 l12 -17 12 16 12 -18 12 17 12 -17 12 17 12 -17 12 15 12 -14 12 13" fill="none" stroke="#d8c88e" stroke-width="4"/>'
            '<circle cx="171" cy="-25" r="6" fill="#17201e"/>')


def turtle(fill: str) -> str:
    e = EDGE
    return (f'<path d="M-142 35 Q-126 -115 0 -124 Q129 -112 145 35 Q89 79 0 80 Q-86 78 -142 35Z" fill="{fill}" stroke="{e}" stroke-width="5"/>'
            f'<path d="M-83 -84 Q-55 -31 -75 34 M0 -120 Q-20 -49 0 75 M83 -84 Q55 -31 75 34 M-124 -35 Q-60 -15 0 -30 Q62 -15 126 -35" fill="none" stroke="#e4c778" stroke-width="4"/>'
            f'<path d="M-109 30 L-169 76 L-143 18 M-50 69 L-79 119 L-26 76 M50 69 L79 119 L26 76 M109 30 L169 76 L143 18" fill="{fill}" stroke="{e}" stroke-width="5"/>'
            f'<path d="M133 -2 Q180 -39 212 -12 Q232 7 209 30 Q183 50 149 25Z" fill="{fill}" stroke="{e}" stroke-width="4"/><circle cx="207" cy="-5" r="6" fill="#17201e"/>')


def insect(name: str, fill: str) -> str:
    e = EDGE
    if name in {"Butterfly", "Moth"}:
        return (f'<ellipse cx="0" cy="4" rx="15" ry="88" fill="#584a35" stroke="{e}" stroke-width="4"/>'
                f'<path d="M-9 -7 Q-125 -153 -166 -71 Q-187 2 -35 30 Q-155 69 -126 139 Q-95 169 -8 45Z M9 -7 Q125 -153 166 -71 Q187 2 35 30 Q155 69 126 139 Q95 169 8 45Z" fill="{fill}" stroke="{e}" stroke-width="4"/>'
                f'<path d="M-15 -72 Q-47 -113 -68 -125 M15 -72 Q47 -113 68 -125" fill="none" stroke="{e}" stroke-width="5" stroke-linecap="round"/>'
                f'<g fill="none" stroke="#f1d78f" stroke-width="4"><circle cx="-95" cy="-48" r="18"/><circle cx="95" cy="-48" r="18"/><circle cx="-81" cy="82" r="12"/><circle cx="81" cy="82" r="12"/></g>')
    if name == "Mantis":
        return (f'<ellipse cx="0" cy="12" rx="25" ry="83" fill="{fill}" stroke="{e}" stroke-width="4"/><circle cx="0" cy="-85" r="31" fill="{fill}" stroke="{e}" stroke-width="4"/>'
                f'<path d="M-15 -104 Q-58 -154 -83 -133 M15 -104 Q58 -154 83 -133 M-18 -34 L-95 -89 L-62 -2 M18 -34 L95 -89 L62 -2 M-15 31 L-108 84 L-133 108 M15 31 L108 84 L133 108 M-10 58 L-56 136 M10 58 L56 136" fill="none" stroke="{e}" stroke-width="8" stroke-linecap="round"/>')
    wings = "" if name in {"Ant", "Termite"} else f'<ellipse cx="-43" cy="-30" rx="75" ry="27" transform="rotate(-25 -43 -30)" fill="#b7d0ba" fill-opacity=".48" stroke="{e}" stroke-width="3"/><ellipse cx="44" cy="-30" rx="75" ry="27" transform="rotate(25 44 -30)" fill="#b7d0ba" fill-opacity=".48" stroke="{e}" stroke-width="3"/>'
    marks = f'<path d="M-24 0 L-42 87 M0 0 L0 99 M24 0 L42 87 M-28 -41 L-66 -83 M28 -41 L66 -83 M-4 -94 Q-27 -137 -50 -132 M4 -94 Q27 -137 50 -132" fill="none" stroke="{e}" stroke-width="6" stroke-linecap="round"/>'
    parts = f'<ellipse cx="-59" cy="12" rx="49" ry="42" fill="{fill}" stroke="{e}" stroke-width="4"/><ellipse cx="0" cy="0" rx="35" ry="32" fill="{fill}" stroke="{e}" stroke-width="4"/><circle cx="51" cy="-26" r="31" fill="{fill}" stroke="{e}" stroke-width="4"/>'
    if name == "Bee":
        parts += f'<path d="M-99 -12 L-24 14 M-98 8 L-28 32 M-82 35 L-37 51" stroke="#3a3430" stroke-width="10"/>'
    return wings + parts + marks + '<circle cx="59" cy="-32" r="5" fill="#17201e"/>'


def spider(fill: str) -> str:
    e = EDGE
    legs = []
    for side in (-1, 1):
        for i in range(4):
            y = -39 + i * 25
            knee = side * (95 + (i % 2) * 8)
            foot = side * (156 + (i % 2) * 9)
            legs.append(f'<path d="M{side*38} {y} L{knee} {y-32} L{foot} {y+7}" fill="none" stroke="{e}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>')
    return (f'<ellipse cx="-53" cy="4" rx="77" ry="57" fill="{fill}" stroke="{e}" stroke-width="4"/><ellipse cx="52" cy="4" rx="47" ry="47" fill="{fill}" stroke="{e}" stroke-width="4"/>' +
            "".join(legs) + '<circle cx="38" cy="-9" r="5" fill="#17201e"/><circle cx="62" cy="-9" r="5" fill="#17201e"/>')


def crab(fill: str) -> str:
    e = EDGE
    return (f'<ellipse cx="0" cy="20" rx="119" ry="74" fill="{fill}" stroke="{e}" stroke-width="5"/><path d="M-100 8 Q0 -35 100 8 M-78 40 Q0 3 78 40" fill="none" stroke="#f2d58a" stroke-width="4"/>'
            f'<path d="M-80 67 L-133 114 L-164 109 M-45 80 L-77 136 L-111 145 M0 89 L-8 151 M45 80 L76 136 L109 145 M80 67 L132 114 L163 109" fill="none" stroke="{e}" stroke-width="9" stroke-linecap="round"/>'
            f'<path d="M-104 -11 Q-157 -77 -183 -33 L-167 -5 L-202 7 Q-174 39 -143 13 M104 -11 Q157 -77 183 -33 L167 -5 L202 7 Q174 39 143 13" fill="{fill}" stroke="{e}" stroke-width="5"/><circle cx="-39" cy="-39" r="7" fill="#17201e"/><circle cx="39" cy="-39" r="7" fill="#17201e"/>')


def octopus(fill: str) -> str:
    e = EDGE
    tentacles = [
        'M-75 38 Q-180 54 -208 131 Q-216 158 -179 154', 'M-50 50 Q-115 145 -118 182 Q-115 207 -84 189',
        'M-20 56 Q-70 161 -46 198 Q-30 214 -13 192', 'M15 55 Q15 143 39 187 Q58 208 72 180',
        'M46 48 Q92 137 128 164 Q155 178 159 147', 'M70 34 Q164 67 194 120 Q207 148 176 157',
        'M-78 18 Q-155 -10 -195 25 Q-207 47 -182 57', 'M78 10 Q151 -21 198 4 Q218 25 194 43'
    ]
    body=f'<path d="M-108 34 Q-115 -100 -3 -132 Q109 -101 105 34 Q62 79 0 79 Q-69 78 -108 34Z" fill="{fill}" stroke="{e}" stroke-width="5"/>'
    arms="".join(f'<path d="{p}" fill="none" stroke="{fill}" stroke-width="22" stroke-linecap="round"/><path d="{p}" fill="none" stroke="{e}" stroke-width="3" stroke-linecap="round"/>' for p in tentacles)
    suckers="".join(f'<circle cx="{x}" cy="{y}" r="5" fill="#e6d19a"/>' for x,y in [(-171,116),(-111,159),(-47,162),(39,155),(122,139),(174,117),(-179,39),(188,20)])
    return body+arms+suckers+'<circle cx="-32" cy="-37" r="7" fill="#17201e"/><circle cx="31" cy="-37" r="7" fill="#17201e"/>'


def jellyfish(fill: str) -> str:
    e=EDGE
    return (f'<path d="M-153 3 Q-145 -115 0 -126 Q145 -115 153 3 Q123 37 95 6 Q68 43 38 9 Q7 46 -19 10 Q-54 46 -78 9 Q-112 40 -153 3Z" fill="{fill}" stroke="{e}" stroke-width="5"/>'
            f'<path d="M-116 13 Q-148 95 -115 156 M-60 19 Q-85 109 -53 174 M-5 20 Q-20 107 -3 179 M53 18 Q74 102 55 165 M111 12 Q142 88 111 145" fill="none" stroke="{e}" stroke-width="10" stroke-linecap="round"/>')


def snake(fill: str) -> str:
    e=EDGE
    return (f'<path d="M-206 92 Q-142 127 -99 73 Q-60 21 -16 58 Q35 101 72 53 Q107 9 144 24 Q177 37 187 4" fill="none" stroke="{fill}" stroke-width="48" stroke-linecap="round"/><path d="M-206 92 Q-142 127 -99 73 Q-60 21 -16 58 Q35 101 72 53 Q107 9 144 24 Q177 37 187 4" fill="none" stroke="{e}" stroke-width="4" stroke-linecap="round"/>'
            f'<ellipse cx="204" cy="-7" rx="48" ry="35" fill="{fill}" stroke="{e}" stroke-width="4"/><circle cx="214" cy="-18" r="6" fill="#17201e"/><path d="M240 -2 Q270 4 284 -7" fill="none" stroke="#d96d67" stroke-width="4"/>')


def dragon(fill: str) -> str:
    e=EDGE
    return (f'<path d="M-140 21 Q-62 -75 47 -20 L130 -51 L174 -20 L126 10 Q74 61 -32 52 L-91 80Z" fill="{fill}" stroke="{e}" stroke-width="4"/>'
            f'<path d="M-30 -18 Q-92 -162 -175 -137 Q-136 -80 -153 -15 Q-107 -36 -68 6Z M7 -19 Q40 -150 140 -152 Q110 -85 132 -43 Q74 -52 40 3Z" fill="#728e7c" stroke="{e}" stroke-width="4"/>'
            f'<path d="M-140 21 Q-230 45 -221 99 Q-210 126 -184 99 L-159 56" fill="none" stroke="{fill}" stroke-width="22" stroke-linecap="round"/><path d="M-140 21 Q-230 45 -221 99 Q-210 126 -184 99 L-159 56" fill="none" stroke="{e}" stroke-width="3"/>'
            f'<path d="M139 -44 L156 -82 L168 -40 M165 -32 L191 -62 L185 -21" fill="none" stroke="{e}" stroke-width="7"/><circle cx="173" cy="-32" r="5" fill="#17201e"/>')


def art_for(a: dict, fill: str) -> str:
    n, k = a["name"], a["kind"]
    if k in ("mammal", "rhino", "lion"): return mammal(n, fill)
    if k == "bird": return bird(n, fill)
    if k == "fish": return fish(n, fill)
    if k == "marine": return marine(n, fill)
    if k == "lizard": return lizard(n, fill)
    if k == "crocodile": return crocodile(fill)
    if k == "turtle": return turtle(fill)
    if k == "insect": return insect(n, fill)
    if k == "spider": return spider(fill)
    if k == "crab": return crab(fill)
    if k == "octopus": return octopus(fill)
    if k == "jellyfish": return jellyfish(fill)
    if k == "snake": return snake(fill)
    if k == "dragon": return dragon(fill)
    if k == "mythical": return dragon(fill) + '<path d="M-150 40 Q-230 -18 -247 -63 M110 13 Q160 60 190 96" fill="none" stroke="#dbb866" stroke-width="9"/>'
    if k == "monster": return dragon(fill) + '<circle cx="119" cy="-43" r="8" fill="#db5c53"/><circle cx="148" cy="-42" r="6" fill="#db5c53"/>'
    return mammal(n, fill)


def render(a: dict) -> str:
    name = html.escape(a["name"])
    top = html.escape(a["equation_top"])
    bottom = html.escape(a["equation_bottom"])
    fill = color_for(a["name"])
    max_len = max(len(a["equation_top"]), len(a["equation_bottom"]))
    font_size = max(12, min(20, int(880 / max(1, max_len) / 0.56)))
    repo = html.escape(a["repo"])
    path = html.escape(a["source_path"])
    sha = html.escape(a.get("source_blob_sha") or "N/A")
    note = html.escape(a.get("source_note") or "")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1200 900" role="img" aria-labelledby="title desc">
<title id="title">{name} — animal and equation</title>
<desc id="desc">Code-drawn vector portrait of {name}, with its source equation wrapped around it. Source: {repo}/{path}.</desc>
<defs>
 <radialGradient id="bg" cx="50%" cy="44%" r="78%"><stop offset="0" stop-color="#172b2b"/><stop offset="1" stop-color="#091314"/></radialGradient>
 <linearGradient id="body" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{fill}"/><stop offset="1" stop-color="#45634e"/></linearGradient>
 <path id="upper" d="M165 440 C185 235 362 152 600 145 C838 152 1015 235 1035 440"/>
 <path id="lower" d="M165 460 C185 648 362 731 600 738 C838 731 1015 648 1035 460"/>
</defs>
<rect width="1200" height="900" rx="34" fill="url(#bg)"/>
<ellipse cx="600" cy="440" rx="505" ry="345" fill="none" stroke="#c99e52" stroke-opacity=".28" stroke-width="1.6"/>
<ellipse cx="600" cy="440" rx="355" ry="224" fill="none" stroke="#8fb3a1" stroke-opacity=".25" stroke-width="1.4" stroke-dasharray="3 11"/>
<text fill="#f5d991" font-family="Georgia, 'Times New Roman', serif" font-size="{font_size}" letter-spacing=".4"><textPath href="#upper" xlink:href="#upper" startOffset="50%" text-anchor="middle">{top}</textPath></text>
<text fill="#a9c8b7" font-family="Georgia, 'Times New Roman', serif" font-size="{font_size}" letter-spacing=".25"><textPath href="#lower" xlink:href="#lower" startOffset="50%" text-anchor="middle">{bottom}</textPath></text>
<g transform="translate(600 430)" stroke-linejoin="round" stroke-linecap="round">{art_for(a, 'url(#body)')}</g>
<g font-family="Georgia, 'Times New Roman', serif" text-anchor="middle">
 <text x="600" y="796" fill="#f0d78e" font-size="25" letter-spacing="5">{name.upper()}</text>
 <text x="600" y="830" fill="#adc4b3" font-size="15" letter-spacing="1.8">{repo}</text>
 <text x="600" y="855" fill="#718981" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11">SOURCE: {path} · BLOB {sha[:12]}</text>
 {f'<text x="600" y="877" fill="#cf9c80" font-size="12">{note}</text>' if note else ''}
</g>
</svg>
'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="overwrite existing SVGs, including Tortoise")
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    built = skipped = 0
    for animal in manifest["animals"]:
        dest = OUT / (animal["name"].lower().replace(" ", "-") + ".svg")
        if dest.exists() and not args.force:
            skipped += 1
            continue
        dest.write_text(render(animal), encoding="utf-8")
        built += 1
    print(f"Built {built} SVGs; preserved {skipped} existing files in {OUT}")


if __name__ == "__main__":
    main()
