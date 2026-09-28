#!/usr/bin/env python3
"""Build build/talk.pptx from this deck's content.

A hand-kept PowerPoint edition of the same 31 slides as index.html (the
reveal.js web deck) and talk.tex (the Beamer edition). Not generated from
either of those — content is kept in sync by hand across all three; see
README.md.

Requires python-pptx and Pillow:
    python3 -m pip install --user python-pptx pillow
"""

import os
import re

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGES = os.path.join(HERE, "images")
OUT_DIR = os.path.join(HERE, "build")
OUT_PATH = os.path.join(OUT_DIR, "talk.pptx")

# ---- Palette: matches index.html's light-mode CSS variables and talk.tex ----
ACCENT = RGBColor(0xB8, 0x86, 0x2F)   # amber  — headings / structure
ACCENT2 = RGBColor(0x3F, 0x7A, 0x52)  # sage   — emphasis / lead
INK = RGBColor(0x1C, 0x1C, 0x1C)
STRONG = RGBColor(0x00, 0x00, 0x00)
MUTED = RGBColor(0x6B, 0x6B, 0x6B)
BORDER = RGBColor(0xE1, 0xDE, 0xD7)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

FONT = "Calibri"

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
MARGIN = Inches(0.6)
TITLE_TOP = Inches(0.35)
TITLE_H = Inches(0.75)
CONTENT_TOP = Inches(1.25)
CHAPTERTAG_Y = Inches(6.75)
PAGENUM_Y = Inches(7.12)

LEFT_X = MARGIN
LEFT_W = Inches(6.9)
RIGHT_X = Inches(7.75)
RIGHT_W = Inches(5.0)
RIGHT_CENTER_X = RIGHT_X + RIGHT_W // 2

FULL_X = MARGIN
FULL_W = SLIDE_W - 2 * MARGIN

# **bold** -> bold black run, ~accent~ -> sage colored run, plain otherwise.
TOKEN_RE = re.compile(r"(\*\*.+?\*\*|~.+?~)")
# _italic_ -> italic run (used only in quote source lines, for book titles).
ITALIC_RE = re.compile(r"(_.+?_)")


def add_runs(paragraph, text, size=16, base_color=INK, italic=False):
    for part in TOKEN_RE.split(text):
        if not part:
            continue
        run = paragraph.add_run()
        if part.startswith("**") and part.endswith("**"):
            run.text = part[2:-2]
            run.font.bold = True
            run.font.color.rgb = STRONG
        elif part.startswith("~") and part.endswith("~"):
            run.text = part[1:-1]
            run.font.color.rgb = ACCENT2
        else:
            run.text = part
            run.font.color.rgb = base_color
        run.font.size = Pt(size)
        run.font.name = FONT
        run.font.italic = italic


def add_source_runs(paragraph, text, size=12, color=MUTED):
    for part in ITALIC_RE.split(text):
        if not part:
            continue
        run = paragraph.add_run()
        if part.startswith("_") and part.endswith("_"):
            run.text = part[1:-1]
            run.font.italic = True
        else:
            run.text = part
            run.font.italic = True
        run.font.size = Pt(size)
        run.font.name = FONT
        run.font.color.rgb = color


def new_slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])  # blank layout


def add_textbox(slide, left, top, width, height, anchor=None):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    if anchor is not None:
        tf.vertical_anchor = anchor
    return tf


def add_title(slide, text, size=28, top=TITLE_TOP, align=PP_ALIGN.LEFT, color=ACCENT):
    tf = add_textbox(slide, MARGIN, top, SLIDE_W - 2 * MARGIN, TITLE_H)
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = True
    run.font.color.rgb = color
    run.font.name = FONT
    return tf


def add_bullets(tf, items, size=16):
    for i, text in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(12)
        bullet = p.add_run()
        bullet.text = "•  "
        bullet.font.color.rgb = ACCENT
        bullet.font.bold = True
        bullet.font.size = Pt(size)
        bullet.font.name = FONT
        add_runs(p, text, size=size)


def add_quote(tf, quote_text, source_text, size=16):
    p = tf.paragraphs[0]
    p.space_after = Pt(6)
    run = p.add_run()
    run.text = "“" + quote_text + "”"
    run.font.italic = True
    run.font.size = Pt(size)
    run.font.color.rgb = INK
    run.font.name = FONT
    p2 = tf.add_paragraph()
    p2.space_before = Pt(4)
    prefix = p2.add_run()
    prefix.text = "— "
    prefix.font.size = Pt(size - 4)
    prefix.font.color.rgb = MUTED
    prefix.font.name = FONT
    add_source_runs(p2, source_text, size=size - 4)


def add_lead(tf, text, size=18, align=PP_ALIGN.LEFT):
    p = tf.paragraphs[0]
    p.alignment = align
    add_runs(p, text, size=size, base_color=ACCENT2)


def add_note_inline(slide, text, top, width=FULL_W, left=FULL_X, size=12):
    tf = add_textbox(slide, left, top, width, Inches(0.6))
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.italic = False
    run.font.color.rgb = MUTED
    run.font.name = FONT


def add_chaptertag(slide, text, size=11):
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, FULL_X, CHAPTERTAG_Y, FULL_W, Pt(0.75))
    line.fill.solid()
    line.fill.fore_color.rgb = BORDER
    line.line.fill.background()
    tf = add_textbox(slide, FULL_X, CHAPTERTAG_Y + Inches(0.06), FULL_W, Inches(0.35))
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = "CHOC — " + text
    run.font.size = Pt(size)
    run.font.color.rgb = MUTED
    run.font.name = FONT


def add_pagenum(slide, n, total):
    tf = add_textbox(slide, SLIDE_W - Inches(1.3), PAGENUM_Y, Inches(1.0), Inches(0.3))
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    run = p.add_run()
    run.text = f"{n}/{total}"
    run.font.size = Pt(10)
    run.font.color.rgb = MUTED
    run.font.name = FONT


def add_image(slide, filename, center_x, top, height):
    """Adds images/<filename> at the given height, centered horizontally on center_x."""
    path = os.path.join(IMAGES, filename)
    pic = slide.shapes.add_picture(path, Emu(0), top, height=height)
    pic.left = Emu(int(center_x - pic.width / 2))
    return pic


def add_caption(slide, text, center_x, top, width=RIGHT_W, size=9):
    tf = add_textbox(slide, Emu(int(center_x - width / 2)), top, width, Inches(0.5))
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.color.rgb = MUTED
    run.font.name = FONT


def image_and_caption(slide, filename, caption, center_x, top, height):
    pic = add_image(slide, filename, center_x, top, height)
    add_caption(slide, caption, center_x, top + pic.height + Inches(0.05), width=max(pic.width, RIGHT_W))
    return pic


def add_qr_slide(prs):
    """Uncounted bookend slide (like the title slide): two QR codes, one to
    this talk's URL and one to the speaker's keylinks page. Used both right
    after the title slide and again as the deck's closing slide."""
    s = new_slide(prs)
    tf = add_textbox(s, Inches(1.0), Inches(0.7), SLIDE_W - Inches(2.0), Inches(0.9))
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = "Follow Along"
    r.font.size = Pt(32); r.font.bold = True; r.font.color.rgb = ACCENT; r.font.name = FONT

    half_w = Inches(5.8)
    left_cx = MARGIN + half_w // 2
    right_cx = SLIDE_W - MARGIN - half_w // 2
    img_top = Inches(1.9)
    img_h = Inches(3.4)

    def qr_block(filename, label, links, center_x):
        """links: list of (display_text, href) lines shown under label."""
        pic = add_image(s, filename, center_x, img_top, img_h)
        cap_top = img_top + pic.height + Inches(0.15)
        cap_h = Inches(0.35 + 0.28 * len(links))
        tfc = add_textbox(s, Emu(int(center_x - Inches(3.0) // 2)), cap_top, Inches(3.0), cap_h)
        p1 = tfc.paragraphs[0]; p1.alignment = PP_ALIGN.CENTER
        r1 = p1.add_run(); r1.text = label
        r1.font.size = Pt(13); r1.font.name = FONT; r1.font.color.rgb = INK
        for text, href in links:
            p = tfc.add_paragraph(); p.alignment = PP_ALIGN.CENTER; p.space_before = Pt(2)
            run = p.add_run(); run.text = text
            run.font.size = Pt(11); run.font.name = FONT; run.font.color.rgb = ACCENT2
            run.font.underline = True
            run.hyperlink.address = href

    qr_block("qr-talk.png", "This talk", [
        ("talks.gkt.sh/luc-digital-ethics-2026", "https://talks.gkt.sh/luc-digital-ethics-2026/"),
        ("DOI: 10.6084/m9.figshare.33944386", "https://doi.org/10.6084/m9.figshare.33944386"),
    ], left_cx)
    qr_block("qr-keylinks.png", "Find me", [
        ("keylinks.gkt.sh", "https://keylinks.gkt.sh"),
    ], right_cx)
    return s


# ============================================================
def build(prs):
    TOTAL = 33
    n = 0

    def next_n():
        nonlocal n
        n += 1
        return n

    # 1 · TITLE
    s = new_slide(prs)
    tf = add_textbox(slide=s, left=Inches(1.0), top=Inches(0.9), width=SLIDE_W - Inches(2.0),
                      height=Inches(1.4), anchor=MSO_ANCHOR.TOP)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = "From Disruption to Agency"
    r.font.size = Pt(40); r.font.bold = True; r.font.color.rgb = ACCENT; r.font.name = FONT
    p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER; p2.space_before = Pt(10)
    r2 = p2.add_run(); r2.text = "AI, Computing Cultures, and the Future of Digital Ethics"
    r2.font.size = Pt(24); r2.font.bold = True; r2.font.color.rgb = ACCENT; r2.font.name = FONT

    tf2 = add_textbox(s, Inches(1.3), Inches(2.5), SLIDE_W - Inches(2.6), Inches(0.9))
    p = tf2.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    add_runs(p, "A talk drawn from _History of Computing and Its Cultures: From Calculating to "
                "Convergence_ (in press for 2026–2027) by David B. Dennis and George K. "
                "Thiruvathukal (speaker)".replace("_", ""), size=15, base_color=ACCENT2)
    # (book title kept unitalicized here to avoid a second markup pass; acceptable for a title slide.)

    tf3 = add_textbox(s, Inches(1.3), Inches(3.5), SLIDE_W - Inches(2.6), Inches(2.8))
    p = tf3.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = "George K. Thiruvathukal, PhD"; r.font.size = Pt(16); r.font.name = FONT; r.font.color.rgb = INK

    def center_line(parts, space_before=8):
        """parts: list of (text, url_or_None) run specs, joined on one centered line."""
        pp = tf3.add_paragraph(); pp.alignment = PP_ALIGN.CENTER; pp.space_before = Pt(space_before)
        for text, url in parts:
            rr = pp.add_run()
            rr.text = text
            rr.font.size = Pt(11); rr.font.name = FONT; rr.font.color.rgb = MUTED
            if url:
                rr.font.color.rgb = ACCENT2
                rr.font.underline = True
                rr.hyperlink.address = url
        return pp

    center_line([
        ("Professor and Chairperson, Computer Science, Loyola University Chicago",
         "https://www.luc.edu/cs/aboutus/people/profiles/thiruvathukalgeorgek.shtml"),
        (" — ", None),
        ("gthiruvathukal@luc.edu", "mailto:gthiruvathukal@luc.edu"),
        (" (preferred)", None),
    ])
    center_line([
        ("Visiting Computer Scientist, Argonne National Laboratory",
         "https://www.alcf.anl.gov/about/people/george-k-thiruvathukal"),
        (" — ", None),
        ("gkt@anl.gov", "mailto:gkt@anl.gov"),
    ], space_before=2)
    center_line([("keylinks.gkt.sh (web)", "https://keylinks.gkt.sh")], space_before=10)
    center_line([
        ("15th Annual International Symposium on Digital Ethics: MAGIS — "
         "September 28–29, 2026",
         "https://www.luc.edu/digitalethics/events/annualsymposium/"),
    ], space_before=10)

    doi_p = tf3.add_paragraph(); doi_p.alignment = PP_ALIGN.CENTER; doi_p.space_before = Pt(10)
    doi_prefix = doi_p.add_run(); doi_prefix.text = "DOI: "
    doi_prefix.font.size = Pt(11); doi_prefix.font.name = FONT; doi_prefix.font.color.rgb = MUTED
    doi_run = doi_p.add_run(); doi_run.text = "10.6084/m9.figshare.33944386"
    doi_run.font.size = Pt(11); doi_run.font.name = FONT; doi_run.font.color.rgb = ACCENT2
    doi_run.font.underline = True
    doi_run.hyperlink.address = "https://doi.org/10.6084/m9.figshare.33944386"
    next_n()

    # 1B · QR CODES (post-title)
    add_qr_slide(prs)

    # 2 · THESIS
    s = new_slide(prs)
    add_title(s, "The Core Thesis")
    tf = add_textbox(s, FULL_X, CONTENT_TOP, FULL_W, Inches(3.0))
    add_bullets(tf, [
        "The opening claim: “Computing came from culture, and then culture increasingly "
        "was shaped by computing.”",
        "A reversal: computation began as a ~cultural artifact~ — tallies, abaci — "
        "before it became a ~world-making environment~.",
        "Digital ethics is not a patch for biased models. It is a question about what "
        "computation has always done to culture.",
    ])
    add_note_inline(s, "If that reversal is right, no computing technology's ethical questions "
                        "arrive from nowhere. They are old questions wearing a new interface — "
                        "and this talk is a history of the interfaces, not a talk about any one of "
                        "them.", top=Inches(4.4))
    add_chaptertag(s, "“The Core Thesis”")
    add_pagenum(s, next_n(), TOTAL)

    # 3 · THEN/NOW BOOKEND
    s = new_slide(prs)
    add_title(s, "Two Thresholds, Both Missed at the Time")
    half_w = Inches(5.8)
    left_cx = MARGIN + half_w // 2
    right_cx = SLIDE_W - MARGIN - half_w // 2
    image_and_caption(s, "ishango-bone.jpg", "Ishango Bone. JhowieNitnek, Wikimedia Commons, CC BY-SA 4.0.",
                       left_cx, CONTENT_TOP, Inches(2.6))
    image_and_caption(s, "alpha-go.jpg", "AlphaGo / reinforcement learning. Wikimedia Commons, public domain.",
                       right_cx, CONTENT_TOP, Inches(2.6))
    tf1 = add_textbox(s, MARGIN, Inches(4.5), half_w, Inches(1.6))
    p = tf1.paragraphs[0]
    add_runs(p, "c. 20,000 BCE — notches that made “one” ~separable from any "
                "particular object~: the first abstraction underlying computation.", size=13)
    tf2 = add_textbox(s, SLIDE_W - MARGIN - half_w, Inches(4.5), half_w, Inches(1.6))
    p = tf2.paragraphs[0]
    add_runs(p, "2010s — deep learning, transformers, BERT, GPT-2: “submerged "
                "infrastructure” that “few… imagined… could become the basis "
                "for general-purpose conversational agents.”", size=13)
    add_chaptertag(s, "“Paleolithic Numbers and Calculating” · “Data, AI, and "
                      "the Edge of Automation”")
    add_pagenum(s, next_n(), TOTAL)

    # 4 · FAUSTIAN-TURING PLANT
    s = new_slide(prs)
    add_title(s, "A Hybrid Figure, Centuries in the Making")
    tf = add_textbox(s, LEFT_X, CONTENT_TOP, LEFT_W, Inches(4.5))
    add_bullets(tf, [
        "The **Faustian Type**: since Babbage's engines, “restless for novelty and "
        "progress” — the drive to build and extend human reach.",
        "The **Turing Type**: since Hollerith's punched cards and Turing's abstract computer, "
        "learned to “think with, design, and command” those machines.",
        "CHOC: the two coexisted through most of the twentieth century — “explorers "
        "and experts… publics and professionals” — and merged into “everyday "
        "fact” only in the 2010s.",
    ], size=15)
    tfq = add_textbox(s, RIGHT_X, CONTENT_TOP, RIGHT_W, Inches(3.0))
    add_quote(tfq, "We are both monstrous and marvelous, born of ambition and algorithm, living "
                   "within a culture that is no longer separable from its machines.",
              "_History of Computing and Its Cultures_", size=15)
    add_chaptertag(s, "“Conclusion: The Cultural-Computing Singularity”")
    add_pagenum(s, next_n(), TOTAL)

    # 5 · PART 2 DIVIDER
    s = new_slide(prs)
    tf = add_textbox(s, Inches(1.0), Inches(2.7), SLIDE_W - Inches(2.0), Inches(2.0))
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = "Six Lenses, One Continuous Argument"
    r.font.size = Pt(32); r.font.bold = True; r.font.color.rgb = ACCENT; r.font.name = FONT
    p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER; p2.space_before = Pt(20)
    add_runs(p2, "Automation · Agency · Accountability · Access · Labor · "
                 "Environmental Cost", size=18, base_color=ACCENT2)
    add_pagenum(s, next_n(), TOTAL)

    def lens_slide(title, bullets, image, caption, tag, bsize=15, img_h=Inches(3.6)):
        s = new_slide(prs)
        add_title(s, title)
        tf = add_textbox(s, LEFT_X, CONTENT_TOP, LEFT_W, Inches(4.0))
        add_bullets(tf, bullets, size=bsize)
        add_chaptertag(s, tag)
        image_and_caption(s, image, caption, RIGHT_CENTER_X, CONTENT_TOP, img_h)
        add_pagenum(s, next_n(), TOTAL)
        return s

    # 6 · CH2 LEIBNIZ
    lens_slide(
        "Automating the Drudgery",
        [
            "Leibniz on hand calculation: “unworthy of excellent men to lose hours like "
            "slaves.”",
            "The oldest automation pitch on record: free minds for _higher_ work.".replace("_", "~"),
            "Three and a half centuries later, the pitch is unchanged — only the machine is.",
        ],
        "leibniz-drum-calculator.png",
        "Leibniz Stepped Reckoner. J. A. V. Turck, Wikimedia Commons, CC0.",
        "“Paleolithic to Scientific Revolution”",
    )

    # 7 · CH2 ACCESS
    lens_slide(
        "Who Was Allowed to Count",
        [
            "Literacy and calculation were restricted to scribal elites for millennia.",
            "Aristotle: mathematics arose where “the priestly class was allowed leisure.”",
            "Access to computation has always tracked access to privilege.",
        ],
        "clay-tablet-cuneiform-2.jpg",
        "Cuneiform tablet, commentary on Enuma Anu Enlil. Wikimedia Commons, CC0.",
        "“Paleolithic to Scientific Revolution”",
    )

    # 8 · CH3 BABBAGE
    lens_slide(
        "The Tables Crisis",
        [
            "Human “computers” produced error-prone astronomical/navigational tables.",
            "Herschel: “an undetected error… is like a sunken rock at sea.”",
            "Babbage's Difference Engine mechanizes an ~existing~ labor pipeline (de Prony's "
            "~100 human computers) — automation formalizes, it doesn't invent.",
        ],
        "difference-engine.jpg",
        "Charles Babbage's Difference Engine No. 2. Wikimedia Commons, public domain.",
        "“Babbage, Lovelace, and the Analytical Engine”",
    )

    # 9 · CH3 LOVELACE (quote instead of first bullet)
    s = new_slide(prs)
    add_title(s, "The Counterpoint: Augmentation, Not Replacement")
    tf = add_textbox(s, LEFT_X, CONTENT_TOP, LEFT_W, Inches(0.4))
    p = tf.paragraphs[0]
    add_runs(p, "CHOC's account of Lovelace's own speculation:", size=13, base_color=MUTED)
    tfq = add_textbox(s, LEFT_X, Inches(1.7), LEFT_W, Inches(1.3))
    add_quote(tfq, "She speculated that, given the right instructions, the Analytical Engine "
                   "might compose music or create art.",
              "_History of Computing and Its Cultures_, on Ada Lovelace", size=14)
    tf2 = add_textbox(s, LEFT_X, Inches(3.1), LEFT_W, Inches(2.2))
    add_bullets(tf2, [
        "CHOC calls this “a vision of computing that anticipates the idea of computers as "
        "creative instruments, not just mathematical engines.”",
        "Written before the Engine was ever built — the earliest case for augmentation "
        "over replacement.",
    ], size=14)
    add_chaptertag(s, "“Babbage, Lovelace, and the Analytical Engine”")
    image_and_caption(s, "ada-lovelace-ppt0-history-slide13.jpg",
                       "Portrait of Ada Lovelace, attr. Alfred Edward Chalon, ca. 1840. "
                       "Wikimedia Commons, public domain.",
                       RIGHT_CENTER_X, CONTENT_TOP, Inches(3.8))
    add_pagenum(s, next_n(), TOTAL)

    # 10 · CH4 HOLLERITH
    lens_slide(
        "Automation Answers an Overload Crisis",
        [
            "The 1880 U.S. census took nearly a decade to tabulate by hand.",
            "Hollerith's punched cards: ~data~, not instructions — a distinction computing "
            "would keep rediscovering for the next 140 years.",
            "“Clerks became operators” — the office workforce reorganized, not "
            "eliminated.",
        ],
        "hollerith-tabulating.jpg",
        "Hollerith tabulating machine, Computer History Museum. Wikimedia Commons, public domain.",
        "“Hollerith, Punched Cards, and Business Machines”",
    )

    # 11 · CH4 ENVIRONMENTAL (text only, full width)
    s = new_slide(prs)
    add_title(s, "The Infrastructure Underneath")
    tf = add_textbox(s, FULL_X, CONTENT_TOP, FULL_W, Inches(3.0))
    add_bullets(tf, [
        "Millions of kilograms of gutta-percha harvested from Southeast Asia to insulate "
        "transatlantic cables.",
        "CHOC's own words: “an early example of how global demand for ‘network "
        "infrastructure’ could create unsustainable environmental and economic "
        "practices.”",
        "Every convergence has had a material cost, paid somewhere else.",
    ])
    add_chaptertag(s, "“Hollerith, Punched Cards, and Business Machines”")
    add_pagenum(s, next_n(), TOTAL)

    # 12 · CH5 LABOR
    lens_slide(
        "The Computers Were Women",
        [
            "Human “computers” at Aberdeen, Bletchley Park, the Moore School — "
            "mostly women, college-educated.",
            "ENIAC's first programmers: Jean Jennings, Betty Snyder, Marlyn Wescoff, and others.",
            "Their labor made the machine practical and flexible; credit did not follow.",
        ],
        "eniac-women-wiring-1.jpg",
        "Women holding parts of the first four Army computers. Wikimedia Commons, public domain.",
        "“WWII: From Ballistics to Electronic Computing”",
    )

    # 12a · CH5 TURING MACHINE
    lens_slide(
        "Computation Gets a Definition",
        [
            "1936: Turing's paper on “computable numbers” introduces an abstract "
            "“universal machine.”",
            "CHOC: it “offered the first rigorous definition of computation itself” "
            "— a vocabulary for calculation as a general process, not a collection of ad "
            "hoc methods.",
            "Decades of augmentation — PCs, networks, the Web — all stand on this one "
            "idea, long before any of them were called AI.",
        ],
        "turing-image-01.jpg",
        "Alan Turing (1951). Wikimedia Commons, public domain.",
        "“WWII: From Ballistics to Electronic Computing”",
    )

    # 13 · CH6 ACCOUNTABILITY
    lens_slide(
        "Who Answers for the Machine's Judgment?",
        [
            "UNIVAC correctly forecasts the 1952 election from early returns.",
            "Broadcasters initially distrust the prediction and downplay it on air.",
            "The first public spectacle of, and public suspicion toward, machine judgment.",
        ],
        "Univac-1952-LIFE-Picture-Collection-Al-Fenn.jpg",
        "Charles Collingwood with UNIVAC, 1952 election broadcast. Al Fenn/LIFE Picture "
        "Collection/Shutterstock.",
        "“Mainframes and Cold War Systems”",
    )

    # 14 · CH6 LABOR
    lens_slide(
        "Same Technology, Reassigned Prestige",
        [
            "CHOC: early programming was “regarded as clerical work, suitable for women "
            "who had previously served as human ‘computers.’”",
            "As complexity grew, it came to be “recognized as a skilled profession.”",
            "The underlying labor — transcription, checking, documentation — didn't "
            "change. Its status did.",
        ],
        "grace-hopper-2.jpg",
        "Grace Murray Hopper. Wikimedia Commons, public domain.",
        "“Mainframes and Cold War Systems”",
    )

    # 15 · CH7 ACCESS+AGENCY
    lens_slide(
        "Machines Leave the Data Center",
        [
            "CHOC on the PDP-8 (1965): a new category of machine that “democratized access "
            "to computing.”",
            "Engelbart's 1968 “Mother of All Demos” — the mouse, hypertext, "
            "windows — embodied his own philosophy: computers as “partners in human "
            "cognition and collaboration.”",
            "Reaches classrooms, small businesses, university labs.",
        ],
        "minicomputers.jpg",
        "DEC PDP-series minicomputers. Various photographers, Wikimedia Commons, CC BY-SA 4.0.",
        "“Time-Sharing and Interactive Computing”",
    )

    # 16 · CH8 ACCESS/LITERACY
    lens_slide(
        "A Market Where None Had Existed",
        [
            "January 1975: the Altair 8800 on the cover of Popular Electronics.",
            "The Homebrew Computer Club — hobbyists trading ideas freely.",
            "CHOC: BASIC, Pascal, C “lowered barriers to entry, creating a broader base of "
            "technical literacy.”",
        ],
        "altair-8800-1.jpg",
        "Altair 8800 and Model 33 ASR Teletype. Tim Colegrove, Wikimedia Commons, CC BY-SA 4.0.",
        "“Personal Computing as Promise”",
    )

    # 17 · CH9 ACCESS
    lens_slide(
        "Elite Power vs. Democratized Access",
        [
            "CHOC's own contrast: supercomputers “embodied elite concentration of power”; "
            "personal computers “democratized access to computing.”",
            "The Macintosh (1984) makes the graphical interface — Engelbart's lineage — "
            "a consumer product.",
            "Two machines, same decade, opposite answers to “who gets to compute.”",
        ],
        "apple-mac.jpg",
        "Original Apple Macintosh, Apple Museum Prague. Benoît Prieur, Wikimedia Commons, CC0.",
        "“Personal Computers, Interfaces, and Early Networks”",
    )

    # 18 · CH9 AGENCY
    lens_slide(
        "Freedom From the Radio Playlist",
        [
            "The Walkman (1979): the first portable cassette player, small enough to carry "
            "everywhere.",
            "Critics called it antisocial; CHOC says users “embraced it as autonomy.”",
            "Elsewhere: “For the first time, media moved with the user, not the other way "
            "around.”",
        ],
        "walkman.jpg",
        "Original Sony Walkman TPS-L2. Binarysequence, Wikimedia Commons, CC BY-SA 4.0.",
        "“Culture: Playback Media and Electronic Spectacle”",
    )

    # 19 · CH10 ACCESS
    lens_slide(
        "The Web Becomes Point-and-Click",
        [
            "1993: NCSA Mosaic — the first browser to combine graphics and text in one "
            "window.",
            "CHOC's assessment: a turning point “as consequential as the IBM PC in 1981 or "
            "Windows 95 in 1995.”",
            "Redefined what it meant to use a computer at all.",
        ],
        "mosaic.png",
        "NCSA Mosaic browser screenshot. Charles Severance, Wikimedia Commons, CC0.",
        "“Browsers, Services, and the New Economy”",
    )

    # 20 · CH10 ACCOUNTABILITY
    lens_slide(
        "The Browser Wars",
        [
            "Netscape Navigator (1994) captures the lion's share of Web traffic; 1995 IPO fuels "
            "the dot-com boom.",
            "Microsoft bundles Internet Explorer into Windows — 1998 DOJ antitrust suit "
            "follows.",
            "Platform accountability disputes did not begin with social media.",
        ],
        "netscape-1994.png",
        "Screenshot of the Netscape website in 1994. Web Design Museum, used with permission.",
        "“Browsers, Services, and the New Economy”",
    )

    # 21 · CH11 ACCOUNTABILITY
    lens_slide(
        "The Networked Society's Janus Face",
        [
            "WikiLeaks/Manning (2010) exposes what governments hide.",
            "The Patriot Act, NSA, and warrantless wiretapping expand what governments see.",
            "CHOC's verdict: “the networked society revealed its Janus face… "
            "transparency and secrecy, empowerment and control, were no longer opposites but "
            "entangled dynamics of the same infrastructures.”",
        ],
        "server-farm.jpg",
        "NASA computer server farm. Wikimedia Commons, public domain.",
        "“Web 2.0, Smartphones, and the Cloud”",
        bsize=13,
    )

    # 22 · CH11 ACCESS
    lens_slide(
        "The Convergence Artifact",
        [
            "The iPhone (2007): camera, browser, phone, and platform in one object.",
            "Castells' “network society” stops being theory and becomes lived "
            "condition.",
            "Smartphones become the primary access point to computing worldwide.",
        ],
        "original-apple-iphone.jpg",
        "iPhone (2007). Avicente05, Wikimedia Commons, CC BY-SA 4.0.",
        "“Web 2.0, Smartphones, and the Cloud”",
    )

    # 22a · MEMEX/WORLD BRAIN (text only)
    s = new_slide(prs)
    add_title(s, "A Library That Was Always Coming")
    tf = add_textbox(s, FULL_X, CONTENT_TOP, FULL_W, Inches(4.0))
    add_bullets(tf, [
        "1945: Vannevar Bush's essay “As We May Think” imagines the memex — a "
        "device for augmenting human memory and association. No AI involved; the idea is 80 "
        "years old.",
        "CHOC returns to this vision three separate times — at the CD-ROM, the Web, and "
        "Wikipedia — each a partial realization of the same 1945 idea.",
        "CHOC's own verdict: singularity “no longer described a hypothetical future in "
        "which artificial intelligence exceeded human cognition, but a present reality in which "
        "human culture and digital systems had become inseparable.”",
    ])
    add_chaptertag(s, "“The Memex/World Brain Throughline”")
    add_pagenum(s, next_n(), TOTAL)

    # 23 · CH12 AUTOMATION
    lens_slide(
        "The Edge of Automation, Before Anyone Called It AI",
        [
            "CHOC's account: “datafication” of ordinary behavior — clicks, GPS "
            "traces, likes — becomes a monetized reservoir; critics (elsewhere) called it "
            "“surveillance capitalism.”",
            "2012: deep learning classifies images with unprecedented accuracy.",
            "By mid-decade, CHOC argues, algorithms were “silently shaping cultural "
            "consumption… They did not merely respond to human choices; they guided "
            "them.”",
        ],
        "quantum-computer.png",
        "Quantum computer. Wikimedia Commons, public domain.",
        "“Data, AI, and the Edge of Automation”",
        bsize=14,
    )

    # 24 · CH12 ACCESS+LABOR
    lens_slide(
        "Global in Reach, Fragmented in Practice",
        [
            "Four models of the 2010s network: U.S. ad-driven, EU regulatory, Chinese "
            "platform-state, Global South mobile-leapfrogging (M-Pesa, Jio).",
            "CHOC's paradox: “communications in the 2010s were global in reach but "
            "fragmented in practice.”",
            "On the creator economy, CHOC: influencer labor was “both artistic performance "
            "and data-driven optimization.”",
        ],
        "tiktok-2017.jpg",
        "Screenshot of TikTok in 2017. Web Design Museum, used with permission.",
        "“Global Divergence” · “Culture: Feed Culture and the Creator "
        "Economy”",
        bsize=14,
    )

    # 25 · CH12 ENVIRONMENTAL (text only)
    s = new_slide(prs)
    add_title(s, "The Modern Gutta-Percha")
    tf = add_textbox(s, FULL_X, CONTENT_TOP, FULL_W, Inches(3.0))
    add_bullets(tf, [
        "CHOC titles this section “The Cloud as Utility and Platform” — "
        "infrastructure at a scale the 2010s took for granted.",
        "Same pattern as the transatlantic-cables story: convergence has a material substrate, "
        "usually invisible.",
        "What was once millions of kilograms of gutta-percha is now data-center power and "
        "water.",
    ])
    add_chaptertag(s, "“The Cloud as Utility and Platform”")
    add_pagenum(s, next_n(), TOTAL)

    # 26 · BRIDGE (text only, with note-inline)
    s = new_slide(prs)
    add_title(s, "One More Entry in a Long List")
    tf = add_textbox(s, FULL_X, CONTENT_TOP, FULL_W, Inches(3.7))
    add_bullets(tf, [
        "From CHOC: the Turing machine, the memex, and the PC already extended human "
        "capability, long before anyone spoke of AI.",
        "From my own course notes, a parallel list: the calculator, high-level languages and "
        "compilers, the Web, Wikipedia, and Stack Overflow each triggered the same “this "
        "makes programming knowledge unnecessary” anxiety — and each time, “deep "
        "knowledge did not become obsolete; it became the thing that distinguished engineers "
        "who directed the tools well from those who were directed by them.” Generative AI "
        "is the latest entry, not a break from the pattern.",
        "Same notes: “AI output is code, and code requires a reader.” Accountability "
        "stays human, as it did for all the others.",
    ], size=14)
    add_note_inline(s, "Two sources on this slide, kept deliberately distinct: CHOC's own "
                        "augmentation throughline (bullet 1), and a course-reading argument of "
                        "mine (bullets 2–3). CHOC ends in 2020, before generative AI.",
                     top=Inches(5.3))
    add_chaptertag(s, "Course notes cited: George K. Thiruvathukal, “A Pattern of "
                      "Disruption? Or Yet Another Disruption?,” Introduction to Computer "
                      "Science in Python: Principles and Practice — "
                      "introcs-python.cs.luc.edu/context/motivation.html", size=9)
    add_pagenum(s, next_n(), TOTAL)

    # 27 · PART 3 DIVIDER
    s = new_slide(prs)
    tf = add_textbox(s, Inches(1.0), Inches(2.3), SLIDE_W - Inches(2.0), Inches(2.8))
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = "Directing the Disruption"
    r.font.size = Pt(32); r.font.bold = True; r.font.color.rgb = ACCENT; r.font.name = FONT
    p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER; p2.space_before = Pt(20)
    add_runs(p2, "CHOC's territory ends in 2020. Computing has already disrupted culture, "
                 "repeatedly, for twenty thousand years.", size=16, base_color=ACCENT2)
    p3 = tf.add_paragraph(); p3.alignment = PP_ALIGN.CENTER; p3.space_before = Pt(14)
    add_runs(p3, "Generative and agentic AI are the latest instance, not a category apart "
                 "— that claim is this talk's, not CHOC's.", size=15)
    add_pagenum(s, next_n(), TOTAL)

    # 28 · RESOLVE FAUSTIAN-TURING
    s = new_slide(prs)
    tf = add_textbox(s, Inches(1.5), Inches(1.5), SLIDE_W - Inches(3.0), Inches(3.5))
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = "The Hybrid We Already Are"
    r.font.size = Pt(30); r.font.bold = True; r.font.color.rgb = ACCENT; r.font.name = FONT
    tfq = add_textbox(s, Inches(2.0), Inches(2.6), SLIDE_W - Inches(4.0), Inches(1.6))
    for p in tfq.paragraphs:
        p.alignment = PP_ALIGN.CENTER
    add_quote(tfq, "The resulting Faustian-Turing Type is both monstrous and marvelous, and we "
                   "are it.",
              "_History of Computing and Its Cultures_, resolving the figure introduced earlier "
              "in this talk", size=17)
    for p in tfq.paragraphs:
        p.alignment = PP_ALIGN.CENTER
    tfl = add_textbox(s, Inches(1.5), Inches(4.3), SLIDE_W - Inches(3.0), Inches(0.6))
    p = tfl.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    add_runs(p, "Not a doom narrative. A responsibility narrative.", size=17, base_color=ACCENT2)
    add_chaptertag(s, "“Conclusion: The Cultural-Computing Singularity”")
    add_pagenum(s, next_n(), TOTAL)

    # 29 · 2020 HAND-OFF
    s = new_slide(prs)
    add_title(s, "CHOC Ends Where This Talk Begins")
    half_w = Inches(5.8)
    left_cx = MARGIN + half_w // 2
    right_cx = SLIDE_W - MARGIN - half_w // 2
    image_and_caption(s, "ishango-bone.jpg", "Ishango Bone. JhowieNitnek, Wikimedia Commons, "
                                              "CC BY-SA 4.0.", left_cx, CONTENT_TOP, Inches(2.2))
    image_and_caption(s, "alpha-go.jpg", "AlphaGo / reinforcement learning. Wikimedia Commons, "
                                          "public domain.", right_cx, CONTENT_TOP, Inches(2.2))
    tf = add_textbox(s, FULL_X, Inches(4.3), FULL_W, Inches(1.8))
    add_bullets(tf, [
        "CHOC's history runs from the Ishango Bone to 2020, and stops there deliberately.",
        "Generative and agentic AI are the next, uncovered chapter — not a rupture from "
        "what came before.",
    ], size=14)
    add_chaptertag(s, "“Conclusion: The Cultural-Computing Singularity”")
    add_pagenum(s, next_n(), TOTAL)

    # 30 · PRACTICAL-HUMANIST CHARGE
    s = new_slide(prs)
    add_title(s, "What CHOC Asks of Its Readers")
    tfq = add_textbox(s, FULL_X, CONTENT_TOP, FULL_W, Inches(2.5))
    add_quote(tfq, "The point is not that everyone must become a computer scientist… To "
                   "ride the currents of change rather than be swamped by them requires a "
                   "working understanding of how these systems shape production, distribution, "
                   "discovery, and memory.",
              "_History of Computing and Its Cultures_, closing charge to readers", size=17)
    add_chaptertag(s, "“Conclusion: The Cultural-Computing Singularity”")
    add_pagenum(s, next_n(), TOTAL)

    # 31 · CLOSING
    s = new_slide(prs)
    tf = add_textbox(s, Inches(1.0), Inches(1.1), SLIDE_W - Inches(2.0), Inches(0.9))
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = "Computing Has Always Disrupted Culture"
    r.font.size = Pt(30); r.font.bold = True; r.font.color.rgb = ACCENT; r.font.name = FONT
    tf2 = add_textbox(s, Inches(1.3), Inches(2.1), SLIDE_W - Inches(2.6), Inches(0.6))
    p2 = tf2.paragraphs[0]; p2.alignment = PP_ALIGN.CENTER
    add_runs(p2, "That's CHOC's evidence — twenty thousand years, no exception.", size=16,
              base_color=ACCENT2)
    tf3 = add_textbox(s, Inches(1.6), Inches(2.9), SLIDE_W - Inches(3.2), Inches(2.6))
    p3 = tf3.paragraphs[0]; p3.alignment = PP_ALIGN.CENTER
    add_runs(p3, "Generative and agentic AI are not a rupture from that pattern; they are its "
                 "newest instance. The question is whether we can direct the disruption toward "
                 "human flourishing — while retaining the knowledge, judgment, and "
                 "responsibility to remain meaningful agents in an increasingly computational "
                 "culture.", size=15)
    tf4 = add_textbox(s, Inches(1.0), Inches(5.8), SLIDE_W - Inches(2.0), Inches(0.5))
    p4 = tf4.paragraphs[0]; p4.alignment = PP_ALIGN.CENTER
    r4 = p4.add_run(); r4.text = "George K. Thiruvathukal  ·  David B. Dennis"
    r4.font.size = Pt(15); r4.font.name = FONT; r4.font.color.rgb = INK
    add_pagenum(s, next_n(), TOTAL)

    # 32 · QR CODES (closing, identical to post-title slide)
    add_qr_slide(prs)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    build(prs)
    prs.save(OUT_PATH)
    print(f"Wrote {OUT_PATH} ({len(list(prs.slides))} slides)")


if __name__ == "__main__":
    main()
