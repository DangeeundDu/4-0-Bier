import sys

replacements = [
    ("FLOOP", "for"),
    ("LOOP", "do"),
    ("AS_LONG", "while"),
    ("CONSTANT", "const"),
    ("NUMBER", "int"),
    ("CHARACTER", "char"),
    ("STRING", "char *"),
    ("POINTER", "*"),
    ("NOTHING", "void"),
    ("LOGIC", "bool"),
    ("TIME", "time_t"),
    ("EQUAL_TO", "=="),
    ("NOT_EQUAL", "!="),
    ("SMALLERTHAN", "<="),
    ("GREATERTHAN", ">="),
    ("POINT", "->"),
    ("GREATER", ">"),
    ("SMALLER", "<"),
    ("OPTYPE", ""),
    ("IS", "if"),
    ("OTHERWISE", "else"),
    ("ALTERNATE", "switch"),
    ("OPTION", "case"),
    ("STOPHERE", "break"),
    ("NOOPTION", "default"),
    ("GIVEBACK", "return"),
    ("END", "exit"),
    ("LIE", "false"),
    ("TRUTH", "true"),
    ("CB_", "{"),
    ("_CB", "}"),
    ("RB_", "("),
    ("_RB", ")"),
    ("SB_", "["),
    ("_SB", "]"),
    ("_EI", ";")
]

replacements = [(r[0].strip(), r[1]) for r in replacements]

with open(sys.argv[1], "r") as f:
    s = f.read()
    for _ in range(3):
        for r in replacements:
            s = s.replace(r[0], r[1])

    with open(sys.argv[1] + "__out.c", "w") as f2:
        f2.write(s)
