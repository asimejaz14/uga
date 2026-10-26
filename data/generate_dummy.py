"""
Dummy data generator for the Role (Step 1) schema.

Writes seed.sql (COPY blocks) that loads into the `role` schema created by schema.sql.

What it simulates
-----------------
- 12 D1 teams x 3 seasons (2024, 2025, 2026) — 2024/2025 exist so pooling works
- 13 players per team; ~3 leave and ~3 freshmen arrive each season
- each player has a hidden archetype (saved in dummy_truth) that drives his rates
- double round-robin regular season + a few conference-tournament games
  (tournament games are in `games`/`possessions` but EXCLUDED from counts — tests your filter)
- possessions with both fives, lineup changes, some garbage time
- player_season_counts derived from the possessions he actually played
  (possession totals and national_assist_share are NOT written: the pipeline computes them)
- 2026 only: ~64% of games carry shot tags; tagged columns filled from tagged possessions
- ~6% of players have no Torvik height (tests the "no height passes both guardrails" rule)

Usage:  python generate_dummy.py [--seed 42] [--out seed.sql]
"""
import argparse
import datetime as dt
import io

import numpy as np
import pandas as pd

SEASONS = [2024, 2025, 2026]
N_TEAMS = 12
ROSTER = 13

# --------------------------------------------------------------------------
# Archetype profiles.  Offensive rates are per 100 OFFENSIVE possessions;
# stl/blk/drb per 100 DEFENSIVE possessions.  a3/amid/arim = assisted share.
# --------------------------------------------------------------------------
P = {
 #                    h    ast  fga3 mid  rim  ft   trn  orb  stl  blk  drb  a3   amid arim usg
 "Floor General":   (75, 9.0, 7.0, 3.0, 4.0, 3.5, 2.0, 1.0, 2.5, 0.4, 5.0, .45, .20, .30, 22),
 "Combo Guard":     (74, 5.0, 9.0, 5.0, 6.0, 5.0, 2.5, 1.2, 2.2, 0.4, 5.0, .45, .15, .25, 26),
 "Guard":           (75, 3.5, 6.0, 2.0, 3.0, 2.5, 2.0, 1.5, 3.5, 0.6, 6.0, .75, .40, .50, 17),
 "3pt Specialist":  (77, 2.5,11.0, 1.5, 2.0, 1.5, 1.5, 1.2, 1.8, 0.5, 6.0, .90, .50, .55, 18),
 "3 and D Wing":    (78, 2.5, 6.0, 1.5, 3.0, 2.0, 2.0, 2.5, 3.0, 1.5, 9.0, .85, .50, .55, 15),
 "Wing":            (78, 3.5, 5.0, 4.0, 8.0, 5.5, 3.0, 2.5, 2.0, 1.0, 8.0, .60, .30, .35, 24),
 "Traditional Forward": (80, 3.0, 4.0, 3.0, 6.0, 3.5, 1.5, 5.0, 1.8, 2.5,15.0, .80, .45, .55, 20),
 "UGA Big":         (82, 1.5, 0.3, 1.0, 9.0, 3.5, 1.5, 9.0, 1.5, 7.0,16.0, .90, .50, .70, 18),
 "Traditional Big": (82, 2.0, 0.5, 2.5, 9.0, 4.0, 1.0,10.0, 1.2, 3.0,20.0, .90, .40, .60, 21),
}
COLS = ["h","ast","fga3","mid","rim","ft","trn","orb","stl","blk","drb","a3","amid","arim","usg"]
PROFILE = {k: dict(zip(COLS, v)) for k, v in P.items()}
RATE_KEYS = ["ast","fga3","mid","rim","ft","trn","orb","stl","blk","drb"]
ARCHS = list(P)

STARTER_SLOTS = [["Floor General"], ["Combo Guard","Guard"],
                 ["3pt Specialist","3 and D Wing","Wing"],
                 ["Traditional Forward"], ["UGA Big","Traditional Big"]]
NEIGHBOUR = {  # plausible role drift between seasons
 "Floor General":["Combo Guard"], "Combo Guard":["Floor General","Guard"],
 "Guard":["Combo Guard","3 and D Wing"], "3pt Specialist":["3 and D Wing"],
 "3 and D Wing":["3pt Specialist","Wing"], "Wing":["3 and D Wing","Traditional Forward"],
 "Traditional Forward":["Wing","Traditional Big"], "UGA Big":["Traditional Big"],
 "Traditional Big":["UGA Big","Traditional Forward"],
}
FIRST = ["Ali","Bilal","Usman","Hamza","Saad","Zain","Omar","Hassan","Faisal","Danish",
         "Jordan","Marcus","Tyler","Devin","Jalen","Chris","Malik","Andre","Isaiah","Caleb",
         "Noah","Ethan","Luke","Mason","Owen","Ryan","Blake","Trey","Kobe","Darius"]
LAST  = ["Khan","Ahmed","Malik","Sheikh","Raza","Butt","Iqbal","Qureshi","Chaudhry","Mirza",
         "Johnson","Williams","Brown","Davis","Miller","Wilson","Moore","Taylor","Thomas","Jackson",
         "White","Harris","Martin","Clark","Lewis","Walker","Hall","Allen","Young","King"]


class Gen:
    def __init__(self, seed):
        self.rng = np.random.default_rng(seed)
        self.next_pid = 1001
        self.players = {}        # pid -> dict(name, height, mult, arch_by_season, ashare_mult)
        self.rosters = {}        # (team, season) -> [(pid, weight)]

    # ---------------- players ----------------
    def new_player(self, arch):
        r = self.rng
        pid = self.next_pid; self.next_pid += 1
        h = round(float(r.normal(PROFILE[arch]["h"], 1.3)) * 2) / 2
        self.players[pid] = dict(
            name=f"{r.choice(FIRST)} {r.choice(LAST)}",
            height=None if r.random() < 0.06 else h,
            mult={k: float(np.exp(r.normal(0, 0.22))) for k in RATE_KEYS},
            amult=float(np.clip(r.normal(1, 0.08), 0.8, 1.2)),
            arch={},
        )
        return pid

    def build_rosters(self):
        r = self.rng
        for t in range(1, N_TEAMS + 1):
            prev = None
            for s in SEASONS:
                if prev is None:
                    roster = []
                    for slot in STARTER_SLOTS:
                        a = r.choice(slot); pid = self.new_player(a)
                        self.players[pid]["arch"][s] = a
                        roster.append([pid, float(r.uniform(0.85, 1.0))])
                    for i in range(ROSTER - 5):
                        a = r.choice(ARCHS); pid = self.new_player(a)
                        self.players[pid]["arch"][s] = a
                        roster.append([pid, float(max(0.03, 0.55 - 0.07 * i + r.normal(0, 0.05)))])
                else:
                    roster = [[pid, w] for pid, w in prev]
                    # 3 leave (random), 3 freshmen arrive on the bench
                    leave = set(r.choice(len(roster), 3, replace=False))
                    roster = [x for i, x in enumerate(roster) if i not in leave]
                    for _ in range(3):
                        a = r.choice(ARCHS); pid = self.new_player(a)
                        self.players[pid]["arch"][s] = a
                        roster.append([pid, float(r.uniform(0.05, 0.35))])
                    # minutes move a bit; returners grow
                    for x in roster:
                        x[1] = float(np.clip(x[1] * r.uniform(0.9, 1.5), 0.03, 1.0))
                    for pid, _ in roster:
                        p = self.players[pid]
                        if s not in p["arch"]:
                            last = p["arch"].get(s - 1)
                            if last is None:
                                continue
                            p["arch"][s] = (r.choice(NEIGHBOUR[last]) if r.random() < 0.12 else last)
                            for k in RATE_KEYS:
                                p["mult"][k] *= float(np.exp(r.normal(0, 0.08)))
                self.rosters[(t, s)] = roster
                prev = roster

    # ---------------- games & possessions ----------------
    def lineup(self, team, season):
        roster = self.rosters[(team, season)]
        ids = np.array([x[0] for x in roster]); w = np.array([x[1] for x in roster])
        return list(self.rng.choice(ids, 5, replace=False, p=w / w.sum()))

    def build_games(self):
        r = self.rng
        games, poss, gid = [], [], 900000
        for s in SEASONS:
            start = dt.date(s - 1, 11, 5)
            sched = [(h, a) for h in range(1, N_TEAMS + 1) for a in range(1, N_TEAMS + 1) if h != a]
            r.shuffle(sched)
            tagged_p = 0.64 if s == 2026 else 0.0
            extra = [(int(a), int(b), 3) for a, b in r.choice(sched, 6, replace=False)]  # conf. tournament
            for i, (h, a, *kind) in enumerate([(h, a) for h, a in sched] + extra):
                gid += 1
                is_tourn = bool(kind)
                games.append(dict(
                    game_id=gid, season=s,
                    game_date=start + dt.timedelta(days=(i // 6) if not is_tourn else 125 + i % 5),
                    home_team_id=h, away_team_id=a, season_type=2,
                    tournament_id=(77 if is_tourn else None),
                    has_shot_tags=bool(r.random() < tagged_p)))
                n = int(r.normal(68, 4)) * 2
                garbage_from = n - 10 if r.random() < 0.15 else n + 1
                lu = {h: self.lineup(h, s), a: self.lineup(a, s)}
                change = {h: r.integers(4, 12), a: r.integers(4, 12)}
                for k in range(n):
                    off, de = (h, a) if k % 2 == 0 else (a, h)
                    for t in (h, a):
                        change[t] -= 1
                        if change[t] <= 0:
                            lu[t] = self.lineup(t, s); change[t] = r.integers(4, 12)
                    poss.append([gid, k + 1, s, off, de, *lu[off], *lu[de], k >= garbage_from])
        g = pd.DataFrame(games)
        p = pd.DataFrame(poss, columns=["game_id","possession_no","season","off_team_id","def_team_id",
                                        "off_p1","off_p2","off_p3","off_p4","off_p5",
                                        "def_p1","def_p2","def_p3","def_p4","def_p5","garbage_time"])
        return g, p

    # ---------------- counts ----------------
    def build_counts(self, games, poss):
        r = self.rng
        reg = games[(games.season_type == 2) & games.tournament_id.isna()]
        pp = poss[poss.game_id.isin(reg.game_id) & ~poss.garbage_time]
        pp = pp.merge(reg[["game_id","has_shot_tags"]], on="game_id")

        def melt(side):
            cols = [f"{side}_p{i}" for i in range(1, 6)]
            m = pp.melt(id_vars=["season","has_shot_tags", f"{side}_team_id"], value_vars=cols,
                        value_name="player_id")
            return m.rename(columns={f"{side}_team_id": "team_id"})
        off = melt("off"); de = melt("def")
        off_n = off.groupby(["player_id","season","team_id"]).size().rename("off_poss")
        tag_n = off[off.has_shot_tags].groupby(["player_id","season","team_id"]).size().rename("tagged_off_poss")
        def_n = de.groupby(["player_id","season","team_id"]).size().rename("def_poss")
        team_off = pp.groupby(["season","off_team_id"]).size()

        base = pd.concat([off_n, def_n, tag_n], axis=1).fillna(0).astype(int).reset_index()
        rows, torvik, truth = [], [], []
        for row in base.itertuples(index=False):
            pid, s, t = int(row.player_id), int(row.season), int(row.team_id)
            pl = self.players[pid]; arch = pl["arch"][s]; pr = PROFILE[arch]
            rate = {k: pr[k] * pl["mult"][k] for k in RATE_KEYS}
            o, d, tg = row.off_poss, row.def_poss, row.tagged_off_poss
            pois = lambda x, n: int(r.poisson(max(x, 0) * n / 100))
            bino = lambda n, p: int(r.binomial(n, float(np.clip(p, 0, 1))))

            fga_rim, fga_mid, fga3 = pois(rate["rim"], o), pois(rate["mid"], o), pois(rate["fga3"], o)
            fgm_rim, fgm_mid, fgm3 = bino(fga_rim, .58), bino(fga_mid, .38), bino(fga3, .34)
            arim, amid, a3 = (pr["arim"] * pl["amult"], pr["amid"] * pl["amult"], pr["a3"] * pl["amult"])
            ast = pois(rate["ast"], o); ast3 = bino(ast, .38); astr = bino(ast - ast3, .6)
            orb = pois(rate["orb"], o)
            c = dict(player_id=pid, season=s, team_id=t, off_poss=o, def_poss=d,
                     tagged_off_poss=(tg if s == 2026 else None),
                     assists=ast, ast_to_three=ast3, ast_to_rim=astr,
                     ft_trips=pois(rate["ft"], o),
                     transition_fga=min(pois(rate["trn"], o), fga_rim + fga_mid + fga3),
                     steals=pois(rate["stl"], d), blocks=pois(rate["blk"], d), drb=pois(rate["drb"], d),
                     orb=orb, putbacks=min(bino(orb, .35), fga_rim),
                     fga_rim=fga_rim, fgm_rim=fgm_rim, fgm_rim_ast=bino(fgm_rim, arim),
                     fga_mid=fga_mid, fgm_mid=fgm_mid, fgm_mid_ast=bino(fgm_mid, amid),
                     fga_three=fga3, fgm_three=fgm3, fgm_three_ast=bino(fgm3, a3))
            tagged = ["driving_layups","pullups_2","pullup_range_2s","floaters","pullups_3",
                      "plain_rim_fga","plain_rim_fgm","plain_rim_fgm_ast","tip_ins",
                      "hooks_turnarounds","alley_oops"]
            if s == 2026:
                big = arch in ("UGA Big","Traditional Big","Traditional Forward")
                prf = pois(rate["rim"] * 0.7, tg); prm = bino(prf, .6)
                c.update(driving_layups=pois(rate["rim"] * (1 - arim) * 0.6, tg),
                         pullups_2=pois(rate["mid"] * (1 - amid) * 0.6, tg),
                         pullup_range_2s=pois(rate["mid"] * (1 - amid) * 0.5, o),  # full season
                         floaters=pois(rate["rim"] * (1 - arim) * 0.15, tg),
                         pullups_3=pois(rate["fga3"] * (1 - a3) * 0.5, tg),
                         plain_rim_fga=prf, plain_rim_fgm=prm, plain_rim_fgm_ast=bino(prm, arim),
                         tip_ins=pois(rate["orb"] * 0.15, tg),
                         hooks_turnarounds=pois(rate["rim"] * (0.18 if big else 0.02), tg),
                         alley_oops=pois(1.2 if arch == "UGA Big" else 0.2, tg))
            else:
                c.update({k: None for k in tagged})
            rows.append(c)

            fga = fga_rim + fga_mid + fga3
            torvik.append(dict(player_id=pid, season=s, team_id=t, height_in=pl["height"],
                               min_pct=round(100 * o / team_off[(s, t)], 2),
                               usage=round(float(np.clip(r.normal(pr["usg"], 2.5), 8, 35)), 2),
                               three_pa_share=round(fga3 / fga, 4) if fga else 0.0))
            truth.append(dict(player_id=pid, season=s, archetype=arch))
        counts = pd.DataFrame(rows)
        nat = []
        for s, g in counts.groupby("season"):
            for z, a, m in [("rim","fgm_rim_ast","fgm_rim"),("mid","fgm_mid_ast","fgm_mid"),
                            ("three","fgm_three_ast","fgm_three")]:
                nat.append(dict(season=s, zone=z, ast_share=round(g[a].sum() / g[m].sum(), 4)))
        return counts, pd.DataFrame(torvik), pd.DataFrame(nat), pd.DataFrame(truth)


def copy_block(table, df):
    buf = io.StringIO()
    out = df.copy()
    for c in out.columns:
        if out[c].dtype == object or str(out[c].dtype) in ("float64",):
            pass
    buf.write(f"COPY role.{table} ({', '.join(df.columns)}) FROM stdin;\n")
    for rec in out.itertuples(index=False):
        vals = []
        for v in rec:
            if v is None or (isinstance(v, float) and np.isnan(v)):
                vals.append(r"\N")
            elif isinstance(v, (bool, np.bool_)):
                vals.append("t" if v else "f")
            elif isinstance(v, float) and v.is_integer() and table not in ("torvik_player_season", "national_assist_share"):
                vals.append(str(int(v)))
            else:
                vals.append(str(v))
        buf.write("\t".join(vals) + "\n")
    buf.write("\\.\n\n")
    return buf.getvalue()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default="seed.sql")
    args = ap.parse_args()

    g = Gen(args.seed)
    g.build_rosters()
    games, poss = g.build_games()
    counts, torvik, nat, truth = g.build_counts(games, poss)

    teams = pd.DataFrame([dict(team_id=t, season=s, team_name=f"Team {t:02d}", conference_id=10 + (t - 1) // 6)
                          for t in range(1, N_TEAMS + 1) for s in SEASONS])
    used = set(counts.player_id) | set(poss[[c for c in poss.columns if c[-2:-1] == "p"]].values.ravel())
    players = pd.DataFrame([dict(player_id=pid, player_name=g.players[pid]["name"])
                            for pid in sorted(used)])
    int_cols = [c for c in counts.columns if c not in ("tagged_off_poss",)]
    counts = counts.astype({c: "Int64" for c in counts.columns})
    games["tournament_id"] = games["tournament_id"].astype("Int64")

    def nn(df):  # pandas NA -> None for writing
        return df.astype(object).where(df.notna(), None)

    with open(args.out, "w") as f:
        f.write("-- Dummy data for role schema. Generated by generate_dummy.py "
                f"(seed={args.seed}).\nSET search_path TO role;\nBEGIN;\n\n")
        # off_poss / def_poss / tagged_off_poss and national_assist_share are DERIVED:
        # the pipeline computes them, so they are not written here.
        counts_out = counts.drop(columns=["off_poss", "def_poss", "tagged_off_poss"])
        for name, df in [("teams", teams), ("players", players), ("games", games),
                         ("possessions", poss), ("player_season_counts", counts_out),
                         ("torvik_player_season", torvik), ("dummy_truth", truth)]:
            f.write(copy_block(name, nn(df)))
        f.write("COMMIT;\n")

    q = torvik.merge(counts[["player_id","season","off_poss"]], on=["player_id","season"])
    q["qualified"] = (q.min_pct >= 40) & (q.off_poss >= 300)
    print(f"wrote {args.out}")
    print(f"  games: {len(games)}  possessions: {len(poss)}  player-seasons: {len(counts)}")
    print("  qualified per season:", q.groupby("season").qualified.sum().to_dict())
    print("  archetypes 2026:", truth[truth.season == 2026].archetype.value_counts().to_dict())


if __name__ == "__main__":
    main()
