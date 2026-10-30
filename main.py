"""Brain Boost 2000 - puzzle engine (pure Python, no Kivy needed).

Every level 1..2000 gets its own puzzle and its own hint.  Puzzles are generated
deterministically (seeded by level number) and de-duplicated, so the game is
identical on every device and no two levels share the same puzzle text.
Difficulty rises smoothly with the level number.
"""
import random
import re
from math import gcd

TOTAL = 2000
CATS = ["Maths", "Sequence", "Algebra", "Memory",
        "Pattern", "Logic", "Riddle", "Reasoning"]


def norm(s):
    """Normalise an answer for comparison."""
    s = str(s).lower().strip()
    s = re.sub(r"^(a|an|the)\s+", "", s)
    return re.sub(r"[^a-z0-9\-]", "", s)


def difficulty_name(lv):
    t = (lv - 1) / (TOTAL - 1)
    for limit, name in ((0.12, "Easy"), (0.35, "Medium"), (0.65, "Hard"),
                        (0.88, "Expert")):
        if t < limit:
            return name
    return "Genius"


def lerp(t, a, b):
    return int(a + (b - a) * t)


def P(cat, q, ans, hint, mem=None, secs=0.0):
    if not isinstance(ans, (list, tuple)):
        ans = [ans]
    return {"cat": cat, "q": q, "a": [norm(x) for x in ans],
            "hint": hint, "mem": mem, "secs": secs}


WORDS = ("apple river cloud tiger piano candle rocket garden planet window "
         "bridge pencil mirror forest island castle dragon silver thunder "
         "pirate puzzle jungle lantern compass harbor meadow falcon marble "
         "violin desert glacier anchor basket button cactus donkey eagle "
         "feather galaxy hammer igloo jacket kettle ladder magnet needle "
         "orange parrot quartz ribbon saddle turtle umbrella velvet walnut "
         "yogurt zipper").split()

NAMES = ("Alex Bella Chris Diana Ethan Fiona George Hannah Ivan Julia Kevin "
         "Laura Mason Nora Oscar Priya Quinn Ravi Sofia Tariq Uma Victor "
         "Wendy Xavier Yara Zane Amir Bruno Chloe Dev Elena Felix Grace "
         "Hugo Isla Jonas Kira Leo Maya Nico").split()

NONSENSE = ("Zorbs Blips Wugs Fleems Gribs Snarfs Tonks Plims Quibs Dorfs "
            "Yarps Mulls Vexes Brims Glorps Hinks Jaxes Kloms Narls Trebs "
            "Wimps Zinks Crads Frobs Spims").split()

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday",
        "Sunday"]

CLASSIC = [
    ("What has keys but cannot open locks?", ["piano", "keyboard"],
     "You can play music on it, or type with it."),
    ("What gets wetter the more it dries?", ["towel"],
     "You use it right after a shower."),
    ("I speak without a mouth and hear without ears. What am I?", ["echo"],
     "Shout in a canyon and listen."),
    ("What has hands but cannot clap?", ["clock", "watch"],
     "It tells you something every minute."),
    ("The more of me you take, the more you leave behind. What am I?",
     ["footsteps", "steps", "footstep", "step"],
     "Think about walking along a sandy beach."),
    ("What can you catch but never throw?", ["cold", "a cold"],
     "Sneezing is a symptom."),
    ("What has a head and a tail but no body?", ["coin"],
     "Flip it to decide something."),
    ("What goes up but never comes down?", ["age", "your age"],
     "Every birthday raises it."),
    ("What has many teeth but cannot bite?", ["comb"],
     "You use it on your hair."),
    ("What begins with T, ends with T, and has T inside it?", ["teapot"],
     "Tea is poured from it."),
    ("What can travel around the world while staying in a corner?",
     ["stamp"], "It sits on the corner of an envelope."),
    ("What has one eye but cannot see?", ["needle"],
     "Tailors thread it."),
    ("What is full of holes but still holds water?", ["sponge"],
     "You use it for washing up."),
    ("What belongs to you but other people use it more than you do?",
     ["name", "your name"], "People say it to get your attention."),
    ("What runs but never walks and has a mouth but never talks?",
     ["river"], "It flows to the sea."),
    ("What has a neck but no head?", ["bottle"],
     "You pour drinks from it."),
    ("What can fill a room but takes up no space?", ["light", "air"],
     "Switch it on."),
    ("What comes once in a minute, twice in a moment, but never in a "
     "thousand years?", ["m", "letter m", "the letter m"],
     "Look at the spelling of the words, not their meaning."),
    ("What word becomes shorter when you add two letters to it?",
     ["short"], "Add 'er' and see."),
    ("Forward I am heavy, backward I am not. What am I?", ["ton"],
     "Read it backwards: you get a word meaning 'not'."),
    ("What has four fingers and a thumb but is not alive?", ["glove"],
     "You wear it in winter."),
    ("What building has the most stories?", ["library"],
     "Think of books, not floors."),
    ("I have cities but no houses, mountains but no trees and water but "
     "no fish. What am I?", ["map"], "You unfold it to find your way."),
    ("What has legs but cannot walk?", ["table", "chair", "bed", "desk"],
     "You find it in a home."),
    ("What can you break without ever touching it?", ["promise", "silence"],
     "Keeping it is the opposite."),
    ("What is always in front of you but cannot be seen?", ["future"],
     "It hasn't happened yet."),
    ("What gets bigger the more you take away from it?", ["hole"],
     "Dig and see."),
    ("Which month has 28 days?", ["all", "every month", "all of them",
                                   "all months"],
     "Does February have the only 28th day?"),
    ("What flies without wings and cries without eyes?", ["cloud", "clouds"],
     "Look up when it rains."),
    ("What has a thumb and four fingers but never needs a manicure?",
     ["glove", "mitten"], "Hands wear it."),
]


# ---------------------------------------------------------------- Maths
def g_maths(lv, r, t, v):
    k = v % 4
    if k == 0:
        n = 2 + int(t * 3.99)
        hi = lerp(t, 9, 400)
        nums = [r.randint(2, hi) for _ in range(n)]
        ops = [r.choice("+-*") for _ in range(n - 1)]
        for i, o in enumerate(ops):
            if o == "*":
                m = lerp(t, 5, 30)
                nums[i], nums[i + 1] = r.randint(2, m), r.randint(2, m)
        expr = str(nums[0])
        for o, x in zip(ops, nums[1:]):
            expr += " %s %d" % (o, x)
        ans = eval(expr)
        shown = expr.replace("*", "\u00d7")
        if "*" in ops:
            i = ops.index("*")
            hint = ("Multiplication comes first: %d \u00d7 %d = %d. Then add "
                    "and subtract from left to right." %
                    (nums[i], nums[i + 1], nums[i] * nums[i + 1]))
        else:
            first = eval("%d %s %d" % (nums[0], ops[0], nums[1]))
            hint = ("Work from left to right. Start with %d %s %d = %d." %
                    (nums[0], ops[0], nums[1], first))
        return P("Maths", "Calculate:\n" + shown, ans, hint)
    if k == 1:
        p = r.choice([5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 80, 120,
                      150][:6 + int(t * 7)])
        m = 100 // gcd(p, 100)
        n = m * r.randint(1, lerp(t, 10, 200))
        return P("Maths", "What is %d%% of %d?" % (p, n), n * p // 100,
                 "%d%% means %d/100. Work out %d \u00d7 %d = %d, then "
                 "divide by 100." % (p, p, n, p, n * p))
    if k == 2:
        a = r.randint(11, lerp(t, 30, 999))
        b = r.randint(3, lerp(t, 12, 99))
        tens, u = a // 10 * 10, a % 10
        return P("Maths", "What is %d \u00d7 %d?" % (a, b), a * b,
                 "Split %d into %d + %d. Then %d \u00d7 %d = %d and "
                 "%d \u00d7 %d = %d. Add them." %
                 (a, tens, u, tens, b, tens * b, u, b, u * b))
    s = (v // 4) % 3
    if s == 0:
        n = r.randint(lerp(t, 20, 200), lerp(t, 60, 5000))
        d = r.randint(3, lerp(t, 9, 60))
        return P("Maths", "What is the remainder when %d is divided by %d?"
                 % (n, d), n % d,
                 "%d \u00d7 %d = %d is the closest multiple below %d. How "
                 "much is left over?" % (d, n // d, d * (n // d), n))
    if s == 1:
        n = r.randint(lerp(t, 8, 30), lerp(t, 15, 300))
        return P("Maths", "Add all whole numbers from 1 to %d." % n,
                 n * (n + 1) // 2,
                 "Pair first and last: 1 + %d = %d. There are %d/2 such "
                 "pairs, i.e. n(n+1)/2." % (n, n + 1, n))
    a = r.randint(12, lerp(t, 25, 199))
    return P("Maths", "What is %d squared?" % a, a * a,
             "Split %d = %d + %d, then use (x+y)\u00b2 = x\u00b2 + 2xy + "
             "y\u00b2." % (a, a // 10 * 10, a % 10))


# ------------------------------------------------------------- Sequence
def g_sequence(lv, r, t, v):
    k = v % 6
    if k == 0:
        d = r.randint(2, lerp(t, 6, 80)) * r.choice([1, -1] if t > .2 else [1])
        s0 = r.randint(-lerp(t, 0, 60), lerp(t, 20, 400))
        seq = [s0 + d * i for i in range(5)]
        ans = s0 + d * 5
        hint = ("Look at the gap between neighbours: %d to %d is a change of "
                "%d. The same step repeats." % (seq[0], seq[1], d))
    elif k == 1:
        ratio = r.randint(2, 3 + int(t * 3))
        s0 = r.randint(1, lerp(t, 5, 12))
        seq = [s0 * ratio ** i for i in range(5)]
        ans = s0 * ratio ** 5
        hint = "Divide each term by the one before: %d \u00f7 %d = %d." % (
            seq[1], seq[0], ratio)
    elif k == 2:
        d1 = r.randint(1, lerp(t, 4, 30))
        c = r.randint(1, lerp(t, 3, 15))
        s0 = r.randint(0, lerp(t, 10, 200))
        seq = [s0]
        for i in range(6):
            seq.append(seq[-1] + d1 + c * i)
        ans = seq.pop()
        gaps = [seq[i + 1] - seq[i] for i in range(len(seq) - 1)]
        hint = ("The gaps are %s. Notice how the gaps themselves grow by the "
                "same amount each time." % ", ".join(map(str, gaps)))
    elif k == 3:
        a, b = r.randint(1, lerp(t, 5, 40)), r.randint(1, lerp(t, 8, 60))
        if t > 0.55:
            c = r.randint(1, lerp(t, 5, 30))
            seq = [a, b, c]
            for _ in range(4):
                seq.append(seq[-1] + seq[-2] + seq[-3])
            ans = seq[-1] + seq[-2] + seq[-3]
            hint = ("Each term is the sum of the previous THREE: %d + %d + "
                    "%d = %d." % (a, b, c, a + b + c))
        else:
            seq = [a, b]
            for _ in range(4):
                seq.append(seq[-1] + seq[-2])
            ans = seq[-1] + seq[-2]
            hint = ("Each term is the sum of the previous two: %d + %d = %d."
                    % (a, b, a + b))
    elif k == 4:
        a0, p = r.randint(1, lerp(t, 10, 100)), r.randint(1, lerp(t, 5, 40))
        b0, q = r.randint(1, lerp(t, 10, 100)), r.randint(2, lerp(t, 8, 50))
        seq = []
        for i in range(4):
            seq += [a0 + p * i, b0 + q * i]
        seq = seq[:7]
        hint = ("Two patterns are mixed together. Take every other number: "
                "%s (step %d) and %s (step %d)." % (
                    ", ".join(str(x) for x in seq[0::2]), p,
                    ", ".join(str(x) for x in seq[1::2]), q))
        ans = b0 + q * 3  # 7 terms shown; the next one is the 4th 'b' term
    else:
        c = r.randint(1, lerp(t, 10, 60))
        o = r.randint(1, lerp(t, 8, 40))
        if t > 0.7 and r.random() < .5:
            seq = [(o + i) ** 3 + c for i in range(5)]
            ans = (o + 5) ** 3 + c
            hint = "These are cubes plus %d. Subtract %d from %d: you get %d = %d\u00b3." % (
                c, c, seq[0], seq[0] - c, o)
        else:
            seq = [(o + i) ** 2 + c for i in range(5)]
            ans = (o + 5) ** 2 + c
            hint = "These are perfect squares plus %d. %d - %d = %d = %d\u00b2." % (
                c, seq[0], c, seq[0] - c, o)
    return P("Sequence", "What number comes next?\n" + ",  ".join(map(str, seq))
             + ",  ?", ans, hint)


# -------------------------------------------------------------- Algebra
def g_algebra(lv, r, t, v):
    k = v % 5
    if k == 0:
        a = r.randint(2, lerp(t, 6, 30))
        x = r.randint(2, lerp(t, 12, 150)) * (-1 if t > .6 and r.random() < .3 else 1)
        b = r.randint(1, lerp(t, 20, 300))
        if r.random() < .5:
            c = a * x + b
            q = "Solve for x:\n%dx + %d = %d" % (a, b, c)
            hint = "Move %d across: %dx = %d. Then divide by %d." % (b, a, c - b, a)
        else:
            c = a * x - b
            q = "Solve for x:\n%dx - %d = %d" % (a, b, c)
            hint = "Add %d to both sides: %dx = %d. Then divide by %d." % (b, a, c + b, a)
        return P("Algebra", q, x, hint)
    if k == 1:
        a = r.randint(2, lerp(t, 9, 40))
        x = r.randint(2, lerp(t, 15, 200))
        b = r.randint(1, lerp(t, 15, 150))
        c = (x + b) * a
        return P("Algebra", "Find x:\n(x + %d) \u00d7 %d = %d" % (b, a, c), x,
                 "Divide both sides by %d first: x + %d = %d." % (a, b, c // a))
    if k == 2:
        x = r.randint(3, lerp(t, 15, 120))
        y = r.randint(1, x - 1)
        s_, d_ = x + y, x - y
        if t > 0.5:
            return P("Algebra", "x + y = %d\nx - y = %d\nWhat is x \u00d7 y?" % (s_, d_),
                     x * y, "Add the equations: 2x = %d, so x = %d. Then find "
                     "y from x + y = %d." % (s_ + d_, (s_ + d_) // 2, s_))
        return P("Algebra", "x + y = %d\nx - y = %d\nWhat is x?" % (s_, d_), x,
                 "Add the two equations: 2x = %d + %d = %d." % (s_, d_, s_ + d_))
    if k == 3:
        a = r.randint(2, lerp(t, 9, 40))
        b = r.randint(1, lerp(t, 15, 150))
        q_ = r.randint(1, lerp(t, 12, 120))
        c = q_ + b
        return P("Algebra", "Solve for x:\nx \u00f7 %d + %d = %d" % (a, b, c), a * q_,
                 "Subtract %d: x \u00f7 %d = %d. Now multiply by %d." % (b, a, q_, a))
    r1 = r.randint(1, lerp(t, 6, 30))
    r2 = r.randint(1, lerp(t, 6, 30))
    return P("Algebra", "Find the larger root of:\nx\u00b2 - %dx + %d = 0" % (
        r1 + r2, r1 * r2), max(r1, r2),
        "Find two numbers that add up to %d and multiply to %d." % (
            r1 + r2, r1 * r2))


# --------------------------------------------------------------- Memory
def g_memory(lv, r, t, v):
    k = v % 5
    if k in (0, 1):
        n = 3 + int(t * 7.99) - (1 if k == 1 else 0)
        digs = "".join(str(r.randint(0, 9)) for _ in range(n))
        secs = 1.2 + 0.6 * n
        if k == 0:
            q = "Type the %d digits you just saw." % n
            hint = ("Chunk them in groups of two or three. It starts with %s "
                    "and ends with %s." % (digs[0], digs[-1]))
            ans = digs
        else:
            q = "Type the %d digits you just saw in REVERSE order." % n
            hint = ("Read the sequence from the end. Your answer starts with "
                    "%s." % digs[-1])
            ans = digs[::-1]
        return P("Memory", q, ans, hint, mem="  ".join(digs), secs=secs)
    if k == 2:
        n = 3 + int(t * 5.99)
        ws = r.sample(WORDS, n)
        p = r.randint(2, n)
        q = "Which word was in position %d of %d?" % (p, n)
        hint = ("Link the words in a little story. Position %d comes right "
                "after '%s'." % (p, ws[p - 2]))
        return P("Memory", q, ws[p - 1], hint, mem="\n".join(ws),
                 secs=1.5 + 0.9 * n)
    if k == 3:
        rows, cols = 3 + int(t * 2.99), 4 + int(t * 2.99)
        syms = r.sample("AKMRTX", 2 + (1 if t > .4 else 0))
        grid = [[r.choice(syms) for _ in range(cols)] for _ in range(rows)]
        target = syms[0]
        cnt = sum(row.count(target) for row in grid)
        if cnt == 0:
            grid[0][0] = target
            cnt = sum(row.count(target) for row in grid)
        text = "\n".join("   ".join(row) for row in grid)
        hint = ("Count row by row. The first row has %d '%s'." %
                (grid[0].count(target), target))
        return P("Memory", "How many times did the letter '%s' appear?" % target,
                 cnt, hint, mem=text, secs=2.5 + rows * cols * 0.35)
    n = 4 + int(t * 5.99)
    digs = [r.randint(1, 9) for _ in range(n)]
    return P("Memory", "What is the SUM of the %d digits you just saw?" % n,
             sum(digs),
             "Add them in pairs. The first two digits add up to %d." %
             (digs[0] + digs[1]),
             mem="  ".join(map(str, digs)), secs=1.5 + 0.7 * n)


# -------------------------------------------------------------- Pattern
ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def g_pattern(lv, r, t, v):
    k = v % 4
    if k == 0:
        s = r.randint(1, lerp(t, 3, 12))
        i0 = r.randint(0, 25)
        items = [ALPHA[(i0 + s * i) % 26] for i in range(5)]
        ans = ALPHA[(i0 + s * 5) % 26]
        return P("Pattern", "Which letter comes next?\n" + ",  ".join(items) + ",  ?",
                 ans, "Each letter jumps %d place(s) forward in the alphabet "
                 "(%s to %s). After Z it wraps around to A." % (s, items[0], items[1]))
    if k == 1:
        s = r.randint(1, lerp(t, 3, 8))
        i0 = r.randint(0, 25 - s * 4) if 25 - s * 4 > 0 else 0
        n0, m = r.randint(1, lerp(t, 9, 60)), r.randint(1, lerp(t, 4, 15))
        items = ["%s%d" % (ALPHA[(i0 + s * i) % 26], n0 + m * i) for i in range(4)]
        ans = "%s%d" % (ALPHA[(i0 + s * 4) % 26], n0 + m * 4)
        return P("Pattern", "What comes next?\n" + ",  ".join(items) + ",  ?",
                 ans, "Two patterns at once: letters jump %d place(s) and the "
                 "numbers go up by %d." % (s, m))
    if k == 2:
        u = 2 + int(t * 3.99)
        unit = r.sample("RGBYPO", u)
        shown = u * 2 + r.randint(0, u - 1)
        n = r.randint(shown + 2, lerp(t, 15, 250))
        seq = [unit[i % u] for i in range(shown)]
        ans = unit[(n - 1) % u]
        pos = (n - 1) % u + 1
        return P("Pattern", "Colour code repeats forever:\n%s ...\nWhich letter is item number %d?" % (
            " ".join(seq), n), ans,
            "The pattern repeats every %d items. %d divided by %d leaves "
            "remainder %d, so look at position %d of the pattern." % (
                u, n, u, n % u, pos))
    maxlen = 4 + int(t * 6)
    pool = [w for w in WORDS if len(w) <= maxlen] or WORDS
    w = r.choice(pool)
    s = r.randint(1, 25)
    enc = "".join(ALPHA[(ALPHA.index(c.upper()) + s) % 26] for c in w)
    return P("Pattern", "Secret code: every letter was moved FORWARD %d places "
             "in the alphabet.\nDecode:  %s" % (s, enc), w,
             "Move each letter BACK %d places. For example %s becomes %s." % (
                 s, enc[0], w[0].upper()))


# ---------------------------------------------------------------- Logic
ORDERS = [("taller", "tallest", "shortest"), ("older", "oldest", "youngest"),
          ("faster", "fastest", "slowest"), ("heavier", "heaviest", "lightest")]
ORD_NAMES = ["", "first", "second", "third", "fourth", "fifth", "sixth", "seventh"]


def g_logic(lv, r, t, v):
    k = v % 4
    if k == 0:
        n = 3 + int(t * 3.99)
        order = r.sample(NAMES, n)            # order[0] is the "most"
        comp, most, least = r.choice(ORDERS)
        st = []
        for i in range(n - 1):
            a, b = order[i], order[i + 1]
            if t > .3 and r.random() < .5:
                st.append("%s is %s than %s." % (b, comp.replace("taller", "shorter")
                          .replace("older", "younger").replace("faster", "slower")
                          .replace("heavier", "lighter"), a))
            else:
                st.append("%s is %s than %s." % (a, comp, b))
        r.shuffle(st)
        if t > .45 and n >= 4:
            p = r.randint(2, n - 1)
            q = "Who is %s in order from the %s?" % (ORD_NAMES[p], most)
            hint = ("Link the statements into one chain from %s to %s. The "
                    "chain starts with %s." % (most, least, order[0]))
            ans = order[p - 1]
        elif r.random() < .5:
            q, ans = "Who is the %s?" % most, orde
