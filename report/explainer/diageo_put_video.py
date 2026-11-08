"""3Blue1Brown-style explainer of the Diageo put over 34% of Moet Hennessy.

Render:  /opt/homebrew/bin/python3.12 -m manim -qh --disable_caching report/explainer/diageo_put_video.py DiageoPut
Figures: data/processed/lvmh_nci_put.csv and report/notes/nci-put-diageo.md.
"""
import wave
from pathlib import Path

from manim import *

AUDIO = Path(__file__).parent / "audio"

config.background_color = "#0f1115"

BL = "#58C4DD"   # blue: Diageo's book equity / reported
OR = "#F28C38"   # orange: goodwill plug / put
YE = "#FFD54F"   # highlight
RD = "#FC6255"
GR = "#83C167"
MUTED = "#8A8F98"
FONT = "Helvetica Neue"


def T(s, size=36, color=WHITE, weight=NORMAL):
    return Text(s, font=FONT, font_size=size, color=color, weight=weight)


def caption(s):
    c = T(s, 26, MUTED)
    c.to_edge(DOWN, buff=0.6)
    return c


def source(s):
    return T("Source: " + s, 14, MUTED).to_edge(DOWN, buff=0.15)


def fmt(n):
    return f"{n:,.0f}"


class DiageoPut(Scene):
    def construct(self):
        self.cap = None
        self.intro()
        self.ownership()
        self.bookkeeping()
        self.history()
        self.fair_value()
        self.net_debt()
        self.profit()
        self.what_to_do()

    # ------------------------------------------------------------------
    def narrate(self, key):
        """Start the narration clip for this scene (made by narration.py)."""
        path = AUDIO / f"{key}.wav"
        self.clip_end = self.renderer.time
        if path.exists():
            with wave.open(str(path)) as w:
                dur = w.getnframes() / w.getframerate()
            self.add_sound(str(path))
            self.clip_end = self.renderer.time + dur

    def clear(self):
        left = getattr(self, "clip_end", 0) - self.renderer.time + 0.4
        if left > 0:
            self.wait(left)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        self.cap = None

    def say(self, s):
        new = caption(s)
        if getattr(self, "cap", None) is None:
            self.play(Write(new))
            self.cap = new
        else:
            self.play(FadeOut(self.cap, shift=UP * 0.2), FadeIn(new, shift=UP * 0.2))
            self.cap = new

    # 1 -----------------------------------------------------------------
    def intro(self):
        self.narrate("intro")
        title = T("The Diageo put", 64, weight=BOLD)
        sub = T("A €6.3bn debt that LVMH does not call debt", 32, OR)
        sub.next_to(title, DOWN, buff=0.4)
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(sub, shift=UP * 0.3))
        self.wait(2)
        self.clear()

    # 2 -----------------------------------------------------------------
    def ownership(self):
        self.narrate("ownership")
        head = T("Who owns Moët Hennessy?", 40).to_edge(UP)
        self.play(Write(head))

        r = 1.8
        lv = Sector(radius=r, angle=0.66 * TAU, start_angle=PI / 2, color=BL, fill_opacity=0.85, stroke_width=0)
        dg = Sector(radius=r, angle=0.34 * TAU, start_angle=PI / 2 + 0.66 * TAU, color=OR, fill_opacity=0.85, stroke_width=0)
        pie = VGroup(lv, dg).shift(LEFT * 3 + DOWN * 0.3)
        lv_l = T("LVMH 66%", 28).move_to(pie.get_center() + LEFT * 0.6 + DOWN * 0.3)
        dg_l = T("Diageo\n34%", 26).move_to(pie.get_center() + RIGHT * 0.9 + UP * 0.8)
        self.play(DrawBorderThenFill(lv), DrawBorderThenFill(dg), run_time=1.5)
        self.play(FadeIn(lv_l), FadeIn(dg_l))
        self.say("Diageo has owned 34% since 1994. LVMH consolidates 100%.")
        self.wait(2)

        # the put
        self.play(dg.animate.shift(RIGHT * 0.4 + UP * 0.2), dg_l.animate.shift(RIGHT * 0.4 + UP * 0.2))
        terms = VGroup(
            T("The put option", 34, OR, BOLD),
            T("Diageo can force LVMH to buy the 34%.", 26),
            T("Notice: 6 months, at any time.", 26),
            T("Price = 80% × fair value of the 34%.", 26, YE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(RIGHT * 2.6 + UP * 0.2)
        arrow = Arrow(dg.get_right(), terms.get_left() + LEFT * 0.1, color=OR, buff=0.2)
        self.play(GrowArrow(arrow))
        for t in terms:
            self.play(FadeIn(t, shift=RIGHT * 0.2), run_time=0.7)
        self.wait(1)
        self.say("IAS 32.23: record this promise as a financial liability.")
        self.add(source("LVMH FY2025 Financial Documents, note 21 (p. 56)"))
        self.wait(3)
        self.clear()

    # 3 -----------------------------------------------------------------
    def bookkeeping(self):
        self.narrate("bookkeeping")
        head = T("How LVMH books it", 40).to_edge(UP)
        self.play(Write(head))

        unit = 0.32  # scene units per €1bn
        base = DOWN * 2.4 + LEFT * 2.0
        w = 2.2
        nci_t = ValueTracker(3.78)
        plug = ValueTracker(9.07)

        nci = always_redraw(lambda: Rectangle(
            width=w, height=nci_t.get_value() * unit, fill_color=BL, fill_opacity=0.9, stroke_width=0)
            .move_to(base, aligned_edge=DOWN))
        plug_rect = always_redraw(lambda: Rectangle(
            width=w, height=max(plug.get_value(), 0.01) * unit, fill_color=OR, fill_opacity=0.9, stroke_width=0)
            .next_to(nci, UP, buff=0.04))
        nci_l = always_redraw(lambda: T("Diageo's share of\nMH book equity", 22).next_to(nci, LEFT, buff=0.3))
        plug_l = always_redraw(lambda: T("Goodwill\n\"plug\"", 22, OR).next_to(plug_rect, LEFT, buff=0.3))
        total = always_redraw(lambda: T(f"Diageo put €{nci_t.get_value() + plug.get_value():.1f}bn", 26, YE)
                              .next_to(plug_rect, UP, buff=0.2))

        self.play(FadeIn(nci), FadeIn(nci_l))
        self.say("Step 1. LVMH cancels Diageo's minority interest.")
        self.wait(1.5)
        self.add(plug_rect)
        self.play(FadeIn(plug_rect), FadeIn(plug_l), FadeIn(total))
        self.say("Step 2. The difference goes to goodwill.")
        self.wait(1.5)

        # where do changes go?
        gw = RoundedRectangle(width=3.4, height=1.2, corner_radius=0.15, color=OR).shift(RIGHT * 3.2 + UP * 1.2)
        gw_t = T("Goodwill", 30, OR).move_to(gw)
        pl = RoundedRectangle(width=3.4, height=1.2, corner_radius=0.15, color=MUTED).shift(RIGHT * 3.2 + DOWN * 1.2)
        pl_t = T("Profit or loss", 30, MUTED).move_to(pl)
        pl_v = T("€0", 30, WHITE).next_to(pl, RIGHT, buff=0.3)
        self.play(Create(gw), Write(gw_t), Create(pl), Write(pl_t), FadeIn(pl_v))
        q = T("Fair value changes. Where do they go?", 26, YE).move_to(RIGHT * 3.2 + UP * 2.6)
        self.play(FadeIn(q))
        arr = Arrow(base + RIGHT * 1.3 + UP * 2.2, gw.get_left(), color=OR, buff=0.1)
        self.play(GrowArrow(arr))

        # Animate the 2021 -> 2025 fall
        year = ValueTracker(2021)
        yr = always_redraw(lambda: T(str(int(round(year.get_value()))), 30).next_to(nci, DOWN, buff=0.25))
        self.play(FadeIn(yr))
        for y, n, v in [(2022, 4.27, 6.90), (2023, 4.28, 5.68), (2024, 4.33, 1.24), (2025, 4.34, 0.39)]:
            self.play(plug.animate.set_value(v), nci_t.animate.set_value(n), year.animate.set_value(y), run_time=1.2)
        self.play(Indicate(pl_v, color=RD, scale_factor=1.6))
        self.say("The plug fell by €8.7bn. Profit or loss did not change.")
        self.add(source("LVMH FD FY2021–25, notes 1.13, 4 and 18"))
        self.wait(3)
        self.clear()

    # 4 -----------------------------------------------------------------
    def history(self):
        self.narrate("history")
        head = T("The put, year by year (EUR m)", 40).to_edge(UP)
        self.play(Write(head))
        data = [("2021", 3775, 9070), ("2022", 4265, 6899), ("2023", 4281, 5682),
                ("2024", 4332, 1239), ("2025", 4341, 386), ("H1 26", 4369, 382)]
        ax = Axes(x_range=[0, 6.5, 1], y_range=[0, 14000, 3500], x_length=10, y_length=4.6,
                  axis_config={"color": MUTED, "include_ticks": False},
                  y_axis_config={"include_numbers": False}).shift(DOWN * 0.4)
        ylabels = VGroup(*[T(fmt(v), 18, MUTED).next_to(ax.c2p(0, v), LEFT, buff=0.15) for v in range(0, 14001, 3500)])
        grid = VGroup(*[DashedLine(ax.c2p(0, v), ax.c2p(6.5, v), color=MUTED, stroke_width=1, stroke_opacity=0.4)
                        for v in range(3500, 14001, 3500)])
        self.play(Create(ax), FadeIn(ylabels), FadeIn(grid))
        bars = VGroup()
        bw = 0.9
        for i, (k, a, b) in enumerate(data):
            x = i + 0.75
            r1 = Rectangle(width=bw, height=ax.c2p(0, a)[1] - ax.c2p(0, 0)[1], fill_color=BL, fill_opacity=0.9, stroke_width=0)
            r1.move_to(ax.c2p(x, 0), aligned_edge=DOWN)
            r2 = Rectangle(width=bw, height=ax.c2p(0, b)[1] - ax.c2p(0, 0)[1], fill_color=OR, fill_opacity=0.9, stroke_width=0)
            r2.next_to(r1, UP, buff=0.03)
            lab = T(fmt(a + b), 20).next_to(r2, UP, buff=0.1)
            xl = T(k, 20, MUTED).next_to(ax.c2p(x, 0), DOWN, buff=0.2)
            bars.add(VGroup(r1, r2, lab, xl))
        key = VGroup(
            VGroup(Square(0.25, fill_color=BL, fill_opacity=1, stroke_width=0), T("Diageo's share of MH book equity", 20)).arrange(RIGHT, buff=0.15),
            VGroup(Square(0.25, fill_color=OR, fill_opacity=1, stroke_width=0), T("Goodwill plug", 20)).arrange(RIGHT, buff=0.15),
        ).arrange(RIGHT, buff=0.6).next_to(head, DOWN, buff=0.3)
        self.play(FadeIn(key))
        self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(g[0], DOWN), GrowFromEdge(g[1], DOWN), FadeIn(g[2]), FadeIn(g[3])) for g in bars],
                              lag_ratio=0.35), run_time=4)
        self.say("Blue stays flat. Orange almost disappears.")
        self.add(source("LVMH FD FY2021–25 notes 4, 18; H1-2026 report"))
        self.wait(3)
        self.clear()

    # 5 -----------------------------------------------------------------
    def fair_value(self):
        self.narrate("fair_value")
        head = T("What LVMH thinks Moët Hennessy is worth", 40).to_edge(UP)
        self.play(Write(head))
        formula = T("fair value of 100% = put ÷ 0.8 ÷ 0.34", 28, YE).next_to(head, DOWN, buff=0.35)
        self.play(FadeIn(formula))
        pts = [47.2, 41.0, 36.6, 20.5, 17.4, 17.5]
        yrs = ["2021", "2022", "2023", "2024", "2025", "H1 26"]
        ax = Axes(x_range=[0, 5.5, 1], y_range=[0, 50, 10], x_length=9, y_length=3.8,
                  axis_config={"color": MUTED, "include_ticks": False}).shift(DOWN * 0.5 + LEFT * 0.6)
        ylabels = VGroup(*[T(f"€{v}bn", 18, MUTED).next_to(ax.c2p(0, v), LEFT, buff=0.15) for v in range(0, 51, 10)])
        xl = VGroup(*[T(y, 20, MUTED).next_to(ax.c2p(i + 0.25, 0), DOWN, buff=0.2) for i, y in enumerate(yrs)])
        self.play(Create(ax), FadeIn(ylabels), FadeIn(xl))
        line = VMobject(color=BL, stroke_width=5).set_points_as_corners([ax.c2p(i + 0.25, v) for i, v in enumerate(pts)])
        dots = VGroup(*[Dot(ax.c2p(i + 0.25, v), color=BL, radius=0.08) for i, v in enumerate(pts)])
        tracker = ValueTracker(0)
        dot = always_redraw(lambda: Dot(line.point_from_proportion(tracker.get_value()), color=YE, radius=0.11))
        val = always_redraw(lambda: T(
            f"€{ax.p2c(line.point_from_proportion(tracker.get_value()))[1]:.0f}bn", 30, YE
        ).next_to(dot, UR, buff=0.1))
        self.add(dot, val)
        self.play(Create(line), FadeIn(dots), tracker.animate.set_value(1), run_time=4, rate_func=linear)
        self.play(FadeOut(val), FadeOut(dot))
        end_l = T("€17bn", 26, BL).next_to(dots[-1], DOWN, buff=0.15)
        start_l = T("€47bn", 26, BL).next_to(dots[0], UP, buff=0.15)
        self.play(FadeIn(end_l), FadeIn(start_l))
        brace = BraceBetweenPoints(ax.c2p(5.6, 47.2), ax.c2p(5.6, 17.4), direction=RIGHT, color=RD)
        bt = T("−€30bn", 30, RD).next_to(brace, RIGHT, buff=0.15)
        guide = DashedLine(ax.c2p(0.25, 47.2), ax.c2p(5.6, 47.2), color=RD, stroke_width=2)
        self.play(Create(guide), GrowFromCenter(brace), Write(bt))
        self.say("A €30bn fall in four years. No charge in the income statement.")
        self.wait(1.5)
        self.say("The cause is real: cognac demand fell in the US and China.")
        self.add(source("calculated from LVMH FD notes 4 and 18; about ±10%"))
        self.wait(3)
        self.clear()

    # 6 -----------------------------------------------------------------
    def net_debt(self):
        self.narrate("net_debt")
        head = T("Is it material?", 40).to_edge(UP)
        self.play(Write(head))
        unit = 0.75  # per €1bn
        left = LEFT * 5
        nfd = Rectangle(width=6.857 * unit, height=0.9, fill_color=BL, fill_opacity=0.9, stroke_width=0)
        nfd.move_to(left + UP * 0.6, aligned_edge=LEFT)
        nfd_l = T("Reported net debt", 24).next_to(nfd, UP, aligned_edge=LEFT, buff=0.15)
        nfd_v = T("€6.9bn", 28).next_to(nfd, RIGHT, buff=0.2)
        self.play(GrowFromEdge(nfd, LEFT), FadeIn(nfd_l), FadeIn(nfd_v))
        put = Rectangle(width=6.331 * unit, height=0.9, fill_color=OR, fill_opacity=0.9, stroke_width=0)
        put.next_to(nfd, RIGHT, buff=0.04)
        put_l = T("+ put liability (LVMH excludes it)", 24, OR).next_to(put, UP, aligned_edge=LEFT, buff=0.15)
        self.play(FadeOut(nfd_v), GrowFromEdge(put, LEFT), FadeIn(put_l))
        tot = T("€13.2bn", 34, YE, BOLD).next_to(put, DOWN, aligned_edge=RIGHT, buff=0.3)
        self.play(Write(tot))
        facts = VGroup(
            T("The put = 92% of reported net debt.", 28),
            T("Diageo can ask for cash in 6 months.", 28),
            T("A buyer must treat it as debt.", 28, YE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).shift(DOWN * 1.9 + LEFT * 1.2)
        for f in facts:
            self.play(FadeIn(f, shift=UP * 0.2), run_time=0.7)
        self.add(source("LVMH FY2025 FD, balance sheet (p. 26), note 19.1 (p. 53)"))
        self.wait(3)
        self.clear()

    # 7 -----------------------------------------------------------------
    def profit(self):
        self.narrate("profit")
        head = T("What if the changes went to profit?", 40).to_edge(UP)
        sub = T("IASB, Sept 2026 (tentative): put remeasurement goes to profit or loss.", 24, MUTED).next_to(head, DOWN, buff=0.25)
        self.play(Write(head), FadeIn(sub))
        data = [("2021", 12036, 9569, "−20%"), ("2022", 14084, 16288, "+16%"), ("2023", 15174, 16409, "+8%"),
                ("2024", 12550, 16928, "+35%"), ("2025", 10878, 11778, "+8%")]
        ax = Axes(x_range=[0, 5, 1], y_range=[0, 18000, 4500], x_length=10, y_length=4,
                  axis_config={"color": MUTED, "include_ticks": False}).shift(DOWN * 0.9)
        ylabels = VGroup(*[T(fmt(v), 18, MUTED).next_to(ax.c2p(0, v), LEFT, buff=0.15) for v in range(0, 18001, 4500)])
        self.play(Create(ax), FadeIn(ylabels))
        key = VGroup(
            VGroup(Square(0.25, fill_color=BL, fill_opacity=1, stroke_width=0), T("Reported net profit (EUR m)", 20)).arrange(RIGHT, buff=0.15),
            VGroup(Square(0.25, fill_color=OR, fill_opacity=1, stroke_width=0), T("With put changes in profit", 20)).arrange(RIGHT, buff=0.15),
        ).arrange(RIGHT, buff=0.6).next_to(sub, DOWN, buff=0.25)
        self.play(FadeIn(key))
        h = lambda v: ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]
        reps, alts, labs = VGroup(), VGroup(), VGroup()
        for i, (k, rep, alt, pct) in enumerate(data):
            x = i + 0.5
            r = Rectangle(width=0.6, height=h(rep), fill_color=BL, fill_opacity=0.9, stroke_width=0).move_to(ax.c2p(x - 0.17, 0), aligned_edge=DOWN)
            a = Rectangle(width=0.6, height=h(alt), fill_color=OR, fill_opacity=0.9, stroke_width=0).move_to(ax.c2p(x + 0.17, 0), aligned_edge=DOWN)
            col = RD if pct.startswith("−") else GR
            labs.add(T(pct, 24, col, BOLD).next_to(a, UP, buff=0.1))
            reps.add(VGroup(r, T(k, 20, MUTED).next_to(ax.c2p(x, 0), DOWN, buff=0.2)))
            alts.add(a)
        self.play(LaggedStart(*[GrowFromEdge(g[0], DOWN) for g in reps], lag_ratio=0.2), FadeIn(VGroup(*[g[1] for g in reps])), run_time=2)
        self.play(LaggedStart(*[GrowFromEdge(a, DOWN) for a in alts], lag_ratio=0.2), run_time=2)
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.2) for l in labs], lag_ratio=0.2))
        self.play(Indicate(labs[3], color=YE, scale_factor=1.4))
        self.say("One line could move profit by −20% to +35%.")
        self.add(source("LVMH income statements and note 4; pre-tax, illustrative"))
        self.wait(3)
        self.clear()

    # 8 -----------------------------------------------------------------
    def what_to_do(self):
        self.narrate("what_to_do")
        head = T("What should we do?", 44).to_edge(UP)
        self.play(Write(head))
        verdict = T("Do not stop the deal. Change the price.", 34, YE, BOLD).next_to(head, DOWN, buff=0.5)
        self.play(FadeIn(verdict, scale=1.1))
        steps = [
            "Add the put (€6.3bn) to net debt.",
            "Use €5–6bn as the minimum cost to own 100% of MH.",
            "Get the 1994 agreement. Check change-of-control terms.",
            "Value Wines & Spirits with our own model.",
            "Remove put changes from covenants and earn-outs.",
        ]
        items = VGroup(*[
            VGroup(Dot(color=OR, radius=0.07), T(s, 28)).arrange(RIGHT, buff=0.25) for s in steps
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(verdict, DOWN, buff=0.6)
        for it in items:
            self.play(FadeIn(it, shift=RIGHT * 0.3), run_time=0.7)
            self.wait(0.6)
        self.wait(1)
        self.clear()
