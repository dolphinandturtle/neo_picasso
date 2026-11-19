import os
import sys
from subprocess import call


def build(jobname):
    call(["pdflatex", "-jobname", jobname, jobname + ".tex"])

def make_ch1():
    with open(os.path.join("src", "include.tex"), "r") as file:
        tex_include = file.read()
    with open(os.path.join("src", "ch01.tex"), "r") as file:
        tex_ch1 = file.read()
    with open("picasso_ch01.tex", "w") as file:
        file.write(tex_include + '\n')
        file.write("\\begin{document}\n")
        file.write("\\pagenumbering{arabic}\n")
        file.write(tex_ch1 + '\n')
        file.write("\\end{document}\n")
    build("picasso_ch01")

def make_all():
    with open(os.path.join("src", "include.tex"), "r") as file:
        tex_include = file.read()
    with open(os.path.join("src", "frontmatter.tex"), "r") as file:
        tex_frontmatter = file.read()
    with open(os.path.join("src", "ch01.tex"), "r") as file:
        tex_ch1 = file.read()
    with open("picasso.tex", "w") as file:
        file.write(tex_include + '\n')
        file.write("\\begin{document}\n")
        file.write("\\pagenumbering{roman}\n")
        file.write(tex_frontmatter + '\n')
        file.write("\\pagenumbering{arabic}\n")
        file.write(tex_ch1 + '\n')
        file.write("\\end{document}\n")
    # the second pass fills the indeces
    build("picasso")
    build("picasso")

if len(sys.argv) < 2:
    make_all()

elif sys.argv[1] == "ch1":
    make_ch1()

elif sys.argv[1] == "clean":
    for fname in os.listdir():
        if fname.endswith((".aux", ".log", ".out", ".toc")):
            os.remove(fname)
