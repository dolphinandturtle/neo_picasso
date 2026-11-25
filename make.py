import os
import sys
from subprocess import call
from math import log10


CHAPTERS = {
    1: "ch01.tex",
    2: "ch02.tex",
    3: "ch03.tex",
    4: "ch04.tex",
    5: "ch05.tex",
    6: "ch06.tex",
    7: "ch07.tex",
    8: "ch08.tex",
    9: "ch09.tex",
    10: "ch10.tex",
    11: "ch11.tex",
    12: "ch12.tex",
    13: "ch13.tex",
    14: "ch14.tex",
    15: "ch15.tex",
}

COUNT_DIGITS = int(log10(max(CHAPTERS.keys()))) + 1

def read_include(file, mode: str):
    if mode not in {"lowres", "hires"}:
        print("<read_include> Invalid 'mode' argument")
        return 1

    return file.read().replace(
        r"\graphicspath{{fig/hires/}}",
        f"\\graphicspath{{{{fig/{mode}/}}}}"
    )

def build(filename):
    call(["pdflatex", filename])

def make_chapter(n: int, mode: str):
    # check for chapter
    if n not in CHAPTERS:
        print(f"The {n}th chapter isn't available...")
        return 1

    # import tex code
    with open(os.path.join("src", "include.tex"), "r") as file:
        tex_include = read_include(file, mode)
    with open(os.path.join("src", CHAPTERS[n]), "r") as file:
        tex_ch = file.read()

    # generate tex document
    filename = "picasso_ch" + str(n).zfill(COUNT_DIGITS) + ".tex"
    with open(filename, "w") as file:
        file.write(tex_include + '\n')
        file.write("\\begin{document}\n")
        file.write("\\pagenumbering{arabic}\n")
        # keep correct chapter number even when compiled single
        if n > 1:
            file.write(f"\\setcounter{{section}}{{{n-1}}}\n")

        file.write(tex_ch + '\n')
        file.write("\\end{document}\n")

    build(filename)

def make_index(mode: str):
    with open(os.path.join("src", "include.tex"), "r") as file:
        tex_include = read_include(file, mode)
    with open(os.path.join("src", "index.tex"), "r") as file:
        tex_index = file.read()

    with open("picasso_index.tex", "w") as file:
        file.write(tex_include + '\n')
        file.write("\\begin{document}\n")
        file.write("\\pagenumbering{arabic}\n")
        file.write(tex_index + '\n')
        file.write("\\end{document}\n")

    build("picasso_index.tex")

def make_constants(mode: str):
    with open(os.path.join("src", "include.tex"), "r") as file:
        tex_include = read_include(file, mode)
    with open(os.path.join("src", "constants.tex"), "r") as file:
        tex_constants = file.read()

    with open("picasso_constants.tex", "w") as file:
        file.write(tex_include + '\n')
        file.write("\\begin{document}\n")
        file.write("\\pagenumbering{arabic}\n")
        file.write(tex_constants + '\n')
        file.write("\\end{document}\n")

    build("picasso_constants.tex")

def make_cover(mode: str):
    with open(os.path.join("src", "include.tex"), "r") as file:
        tex_include = read_include(file, mode)
    with open(os.path.join("src", "cover.tex"), "r") as file:
        tex_cover = file.read()

    with open("picasso_cover.tex", "w") as file:
        file.write(tex_include + '\n')
        file.write("\\begin{document}\n")
        file.write(tex_cover + '\n')
        file.write("\\end{document}\n")

    build("picasso_cover.tex")

def make_all(mode: str):
    # import tex code (headers + footers)
    with open(os.path.join("src", "include.tex"), "r") as file:
        tex_include = read_include(file, mode)
    with open(os.path.join("src", "cover.tex"), "r") as file:
        tex_cover = file.read()
    with open(os.path.join("src", "frontmatter.tex"), "r") as file:
        tex_frontmatter = file.read()
    with open(os.path.join("src", "index.tex"), "r") as file:
        tex_index = file.read()
    with open(os.path.join("src", "constants.tex"), "r") as file:
        tex_constants = file.read()

    # import tex code (unordered chapters)
    tex_book_unordered = []
    for n, filename in CHAPTERS.items():
        with open(os.path.join("src", filename), "r") as file:
            # keep correct chapter number even when missing chapters
            code = f"\\setcounter{{section}}{{{n-1}}}\n" if n > 1 else ""

            code += file.read()
            tex_book_unordered.append((n, code))

    # order chapters
    tex_book = [code for n, code in sorted(tex_book_unordered, key=lambda x: x[0])]

    # generate tex document
    with open("picasso.tex", "w") as file:
        file.write(tex_include + '\n')
        file.write("\\begin{document}\n")
        file.write(tex_cover + '\n')
        file.write("\\pagenumbering{roman}\n")
        file.write(tex_frontmatter + '\n')
        file.write("\\pagenumbering{arabic}\n")
        for tex_ch in tex_book:
            file.write(tex_ch + '\n')
        file.write(tex_index + '\n')
        file.write(tex_constants + '\n')
        file.write("\\end{document}\n")

    # the second pass fills the indeces
    build("picasso.tex")
    build("picasso.tex")


# default mode
mode = "hires"

# mode-setting (quality)
if len(sys.argv) == 2 and sys.argv[1] in {"lowres", "hires"}:
    mode = sys.argv[1]

elif len(sys.argv) == 3 and sys.argv[2] in {"lowres", "hires"}:
    mode = sys.argv[2]

# command
if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] in {"lowres", "hires"}):
    make_all(mode)

elif "ch" in sys.argv[1][:2]:
    make_chapter(int(sys.argv[1][2:]), mode)

elif sys.argv[1] == "index":
    make_index(mode)

elif sys.argv[1] == "constants":
    make_constants(mode)

elif sys.argv[1] == "cover":
    make_cover(mode)

elif sys.argv[1] == "clean":
    for fname in os.listdir():
        if fname.endswith((".aux", ".log", ".out", ".toc")):
            os.remove(fname)
