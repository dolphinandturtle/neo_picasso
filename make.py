import os
import sys
from subprocess import call


def make_ch1():
    call(["pdflatex", "-jobname", "picasso_ch1.tex", os.path.join("src", "ch1.tex")])

if len(sys.argv) < 2:
    make_ch1()

elif sys.argv[1] == "ch1":
    make_ch1()

elif sys.argv[1] == "clean":
    for fname in os.listdir():
        if ("aux" in fname) or ("log" in fname) or ("out" in fname):
            call(["rm", "-f", fname])
