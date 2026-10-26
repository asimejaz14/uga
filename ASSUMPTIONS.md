# Project Record — Role & Level (RSTR IQ Basketball Analytics)

Ye file project ka "yaaddasht" hai. Is mein woh sab likha hai jo code parh kar samajh nahi aata: kaunsa faisla kyun liya gaya, kya maana gaya hai (assumption), data ke baare mein kya verify ho chuka hai, kya abhi khula hai, aur hamare results ko kin numbers se match karna hai.

**Is file ko kaise use karein**

- Har entry ka ek ID hai (`A-01`, `D-03`, `Q-07` …). Code comments, commits aur PRs mein yahi ID likhein, jaise `# See A-05`.
- Jab koi assumption confirm ho jaye ya badle, entry delete na karein. Us ka **Status** badlein aur Change Log mein ek line likhein.
- Naya faisla ya assumption aaye to usi waqt yahan likhein, baad mein nahi.

| Prefix | Matlab |
|---|---|
| `F-` | Verified fact: data se check ho chuka |
| `A-` | Assumption: maana gaya, abhi confirm nahi |
| `D-` | Design decision: hum ne chuna, wajah ke saath |
| `L-` | Known limitation: pata hai ke kamzori hai |
| `Q-` | Open question: jawab chahiye |
| `V-` | Validation target: is number se match karna hai |

---

## 1. Project ka khulasa

| Item | Value |
|---|---|
| Kya bana rahe hain | College basketball (NCAA D1, men's) analytics backend |
| Current scope | **Step 1 — Role** aur **Step 2 — Level** |
| Baad mein | Step 3 — Impact on Winning (Role/Level validate hone aur explicit approval ke baad) |
| Scope se bahar | Step 4 Projection, Step 5 Valuation (spec mein tentative) |
| Stack | Python, Django, Django REST Framework, PostgreSQL |
| Spec | `impact-on-winning-readback.html`: Xenoverta ka readback of *Impact on Winning, Model Math Update v9.1 (2 Oct 2026)* |
| Spec version tag | `v9.1` (har result row par save hota hai) |

**Pipeline ka order (kabhi ulta nahi):**

```
raw data → Role (primary, secondary, family) → Level (EPA → surplus → WAR → tier)
```

Level sirf **family** parhta hai Role se. Role badle to Level dobara chalana zaroori hai.

**Phases**

| Phase | Kaam | Status |
|---|---|---|
| 1 | Spec aur basketball concepts samajhna | ✅ |
| 2 | Source data, fields, dependencies, data quality | ✅ |
| 3 | Django models | ⏳ shuru |
| 4 | Role + Level calculations | — |
| 5 | DRF APIs | — |
| 6 | Validation | — |

---

## 2. Environment aur data source

| Item | Value |
|---|---|
| Raw dump | PostgreSQL 18.6 plain-SQL dump (~900 MB), 23 Oct 2026 |
| Restore | `createdb bball_raw && psql -d bball_raw -f dump.sql` |
| Client version | **psql 18 zaroori**: dump mein `\restrict` line hai jo purane clients nahi samajhte |
| Raw DB | `bball_raw`, alag database, sirf parhne ke liye (D-08) |
| App DB | Django ka `default` database |

### Seasons

- **Development:** sirf **2024, 2025, 2026**.
- **Production:** pehle ke seasons bhi aayenge (spec 2015–2026 ki baat karta hai).
- Is liye code mein **koi season hard-code nahi hoga**. "Pehla season", "pichla season mojood hai ya nahi" waghera hamesha data se tay hoga (D-12).
- Production data aane par **saare seasons dobara compute** honge, kyunke pooling, family gap aur 3-season sample purane seasons par depend karte hain (L-02).

### Raw tables ka inventory

| Table | Rows | Istemal | Note |
|---|---|---|---|
| `possessions` | 2,360,279* | ✅ Role (teammate shares) | Sab se bari table |
| `player_season_box` | 29,634 | ✅ Level | minutes, points |
| `player_season_counts` | 28,361 | ✅ Role + Level | Core input |
| `player_season_possessions` | 26,329 | ✅ Role | Rate denominators |
| `games` | 18,866 | ✅ Filter, points per win | |
| `torvik_player_season` | 15,005 | ✅ Role (height, min%, usage, 3PA share); Impact columns Step 3 ke liye | |
| `teams` | 2,147 | ✅ D1 check | Har season ki ek row |
| `players` | 26,105 | ✅ Naam | |
| `national_assist_share` | 9 | ✅ Shrinkage | 3 seasons × 3 zones |
| `player_history` | 27,309 | ❌ | SCD-2 history; `position` Role mein istemal **mana** hai |
| `source_xref` | 16,131 | ❌ | Ids pehle se resolve hain |
| `dummy_truth` | 0 | ❌ | Khaali (A-08) |
| `model_constants` | 0 | ❌ | Constants code mein (D-05) |
| `role_placement`, `player_group_scores`, `player_onfloor_shares`, `player_season_level`, `season_model_values` | 0 | Reference only | Hamare output models ka checklist |
| `impact_menu`, `player_impact`, `player_impact_skills` | 0 | Step 3 | |

\* `n_live_tup` estimate. Join count 2,360,353.

---

## 3. Verified facts (F)

| ID | Fact | Evidence |
|---|---|---|
| F-01 | Dump mein **koi** PK, FK, unique constraint nahi | `pg_constraint` query: 0 rows |
| F-02 | Kisi table mein duplicate nahi: games (`game_id`), players (`player_id`), teams (`team_id, season`), box / possessions-season / torvik (`player_id, season`), possessions (`game_id, possession_no`) | Duplicate query: sab 0 |
| F-03 | Koi orphan nahi: har counts `player_id` `players` mein; har possession `game_id` `games` mein | Orphan query: 0 |
| F-04 | `player_season_counts` mein ek player-season = ek row (team bhi ek) | Query #4: 0 rows |
| F-05 | Games: total 18,866 · `season_type=2`: 18,518 · `season_type=2` aur `tournament_id IS NULL`: **16,665** | Manual check |
| F-06 | Saari possessions regular-season, non-tournament games ki hain; ~141.6 per game (dono teams) | Query #6 |
| F-07 | Counts mein conference tournaments **shamil nahi** (A-03 isi se confirm hua) | Team points comparison: `near_with_tourney` sirf 10 / 11 / 27 teams |
| F-08 | Play-by-play kabhi points **kam** ginta hai, zyada nahi (chand exceptions L-05) | Team ratio (counts ÷ scoreboard): median 1.000 / 0.980 / 1.000 |
| F-09 | Mid-range assists (`assists − ast_to_rim − ast_to_three`) kabhi negative nahi | Query #7: 0 |
| F-10 | `national_assist_share` zones: `rim`, `mid`, `three` (koi `plain_rim` nahi) | Query #5 |
| F-11 | Sirf 2026 mein tagged play types hain; 2026 ki **saari** rows non-null hain | Season counts query |
| F-12 | 2026 mein 3,323 players ka `tagged_off_poss = 0` | Query (d) |
| F-13 | Torvik sirf D1 players cover karta hai (~4,950 / season) | Coverage query |
| F-14 | `torvik.height_in` `numeric(4,1)` hai, yaani half-inch values mumkin hain | Schema |

**Per-season coverage (counts table se)**

| Season | Counts rows | D1 team | Has possessions | Has Torvik | Has height | Qualified |
|---|---|---|---|---|---|---|
| 2024 | 9,546 | 5,003 | 8,676 | 4,948 | 4,935 | 2,264 |
| 2025 | 9,272 | 5,043 | 8,410 | 4,990 | 4,986 | 2,305 |
| 2026 | 9,543 | 4,989 | 8,523 | 4,947 | 4,947 | 2,282 |

**Team points ratio (counts ÷ scoreboard, D1 teams, regular season)**

| Season | min | p10 | median | p90 | max | > 1.02 |
|---|---|---|---|---|---|---|
| 2024 | 0.840 | 0.954 | 1.000 | 1.000 | 1.002 | 0 |
| 2025 | 0.751 | 0.933 | 0.980 | 1.000 | 1.012 | 0 |
| 2026 | 0.909 | 0.998 | 1.000 | 1.000 | 1.029 | 4 |

---

## 4. Assumptions (A)

| ID | Assumption | Asar | Status |
|---|---|---|---|
| A-01 | Readback (v9.1) hi final spec hai; play-type Role banayenge, rulebook v3.3 nahi | Sab | ✅ Owner confirmed |
| A-02 | **Matrix fit nahi hai.** Jin players ke pooled possessions < 300 hain un par bhi wahi v9.1 rules chalenge; `fallback=True`, `confidence='low'`, `decided_by='matrix_fit_placeholder'`. Jis ke paas koi data hi nahi, us ka role `NULL` (Level mein overall replacement lagega) | Role ~26% players (2026); un ki family → Level surplus | ⚠ Temporary; asal matrix fit aane par badlega. Q-01 bhi dekhein |
| A-03 | Saara counts data regular season only hai | Sab | ✅ F-07 se confirm |
| A-04 | Offensive rebound price = **0.785** (engine value), derived 0.774 nahi. Wajah: Blue Cain validation (V-20) engine se aaya hai | Level: har ORB wala player | Default; client se confirm nahi hua |
| A-05 | Mid-range assists = `assists − ast_to_rim − ast_to_three` | Level Creation | ✅ F-09 safe |
| A-06 | Teammate shares (`lead`, `lead2`, `inside`, `inside2`, `front`) sirf **offensive** possessions par gine jate hain | Role | ⚠ Q-03 |
| A-07 | `technicals` count mein offsetting technicals pehle se nikle hue hain | Level Discipline | ⚠ Data engineer se confirm karna hai |
| A-08 | `dummy_truth` istemal nahi ho raha | Validation | Owner ka faisla |
| A-09 | Cut & roll ka assisted share `rim` national share ki taraf shrink hoga | Role 2026 | F-10 ki wajah se |
| A-10 | Tagged play types: agar `tagged_off_poss` 0 ya NULL ho to tagged values **NULL**, 0 nahi | Role 2026 | Spec ke mutabiq; F-12 |
| A-11 | Pull-up range 2s ka rate `off_poss` par (full season), baaqi tagged types `tagged_off_poss` par | Role 2026 | Spec ka "full season" jumla |
| A-12 | Percentile scale 0–1 hai; spec ka "DREB percentile ≥ 60" matlab ≥ 0.60 | Role (Shooting rule) | ⚠ |
| A-13 | "60%+ shots threes" = `torvik.three_pa_share ≥ 0.60` (usi season ka) | Role (Shooting rule) | ⚠ |
| A-14 | Pooling mein counts **aur** possessions dono ko same weight milta hai (0.5 ya 1.0), phir rate banta hai | Role | ⚠ Q-08 |
| A-15 | Tier bars spec ke constants hain (0.1489 / 0.0913 / 0.0340), hum recompute nahi karte | Level tier | Dev mein majboori (12 seasons nahi); production ke liye Q-10 |
| A-16 | Replacement = overall bench level (is season) + family gap (season ±1 pooled, bench players se weighted) | Level | ⚠ Q-09 |

---

## 5. Design decisions (D)

| ID | Faisla | Wajah | Rad kiye gaye alternatives |
|---|---|---|---|
| D-01 | Har model ka `id` = BigAutoField. ESPN ids (`espn_player_id`, `espn_team_id`, `espn_game_id`) alag unique fields | Django convention; external id badle to hamara PK safe | ESPN id ko PK banana |
| D-02 | **Composite primary key nahi.** Lekin **composite unique constraints** lagenge, jaise (player, season), (team, season), (run, player) | Duplicate import / processing database khud rok dega | Duplicates sirf code se rokna |
| D-03 | Season ka koi model nahi; har jagah `SmallIntegerField` | Season ke saath koi extra data nahi | `Season` model + FK |
| D-04 | Roles, families, groups, tiers, zones Django `TextChoices` | Typo database mein na jaye | Free text |
| D-05 | Spec ke constants `analytics/constants.py` mein, database mein nahi | Git history, tests, spec badalna = code badalna | `model_constants` table |
| D-06 | Har calculation ek `CalculationRun` banati hai (`kind`, `season`, `spec_version`, `status`, `constants_snapshot`). Results run se FK. **API = is season + kind ki latest `success` run** | Recalc ke dauraan API purana sahi data deti rahe; fail run kuch nahi torti; audit trail | Results overwrite + `computed_at` |
| D-07 | Calculations API request ke andar **kabhi nahi**. Shuru mein management commands (`compute_role`, `compute_level`); scheduling / workers sirf zaroorat par | Simplicity; Celery/Redis ki abhi zaroorat nahi | Celery shuru se |
| D-08 | Raw dump alag DB (`bball_raw`) mein; Django apni clean tables rakhta hai; import command raw → clean | Naya dump aaye to sirf raw restore; migrations safe | `inspectdb` / `managed=False` raw tables par |
| D-09 | `Possession` ke 10 player columns = ForeignKey with `db_index=False`; sirf `season` par index | 2.36M rows par 10 indexes faltu hain; poori season ek saath parhte hain | Plain integers; normalized `PossessionPlayer` (23.6M rows) |
| D-10 | Source tables alag models: `PlayerSeasonCounts`, `PlayerSeasonPossessions`, `PlayerSeasonBox`, `TorvikPlayerSeason` | Coverage alag hai (28k/26k/29k/15k); data ka source wazeh rehta hai | Ek wide `PlayerSeason` model |
| D-11 | `player_onfloor_shares` ko `RolePlacement` mein milaya; `GroupScore` alag model (har player 7 groups × 2 samples) | Duplication khatam; group scores queryable | Engineer ka 3-table design; JSON |
| D-12 | Saare seasons compute honge; har result par `history_complete` flag | Client ko saare seasons chahiyein; dev data mein history adhuri hai | Sirf 2026 |
| D-13 | Analytics code (`analytics/`) plain Python functions; database read/write sirf management commands mein; `api/` kabhi `analytics/` import nahi karta | Unit tests bina DB ke; separation of concerns | Logic models / views mein |
| D-14 | Regular-season filter (`season_type=2`, `tournament_id IS NULL`, `is_completed`) code mein **ek jagah**: `Game.objects.regular_season()` | Filter ka ghalat / bhoola hua istemal na ho | Har query mein dobara likhna |
| D-15 | Foreign keys par `on_delete=PROTECT` | Analytics history ghalti se cascade delete na ho | `CASCADE` |
| D-16 | `PlayerSeasonLevel` mein `role_placement` FK | Har Level row bataye ke family kis Role run se aayi | Sirf `family` text |

**App structure**

```
bball/        project settings, urls (databases: default + raw)
core/         input models + import command
analytics/    role/, level/, constants.py, compute commands — koi HTTP nahi
api/          DRF serializers, views, urls — sirf saved results parhta hai
```

---

## 6. Known limitations (L)

| ID | Limitation | Asar / handling |
|---|---|---|
| L-01 | Dump mein event-level play-by-play **nahi**; sirf player-season aggregates. Event rules (8-sec transition, 3-sec putback, FT→foul linking) data engineer ki aggregation mein hain, hum verify nahi kar sakte | Level linear hai, is liye aggregates se poora ban jata hai. Event rules trusted |
| L-02 | Dev mein sirf 3 seasons: 2024 ki pichle season ki pooling nahi; 2025 ka "season before" aur 3-season sample adhoora; 2024 ka family gap adhoora | `history_complete=False`; production data par dobara compute |
| L-03 | Tier bars aur (baad mein) Impact colouring 12-season pooled hain, dev data se nahi ban sakte | A-15 |
| L-04 | 2025 mein pbp coverage kamzor (team median 0.980, min 0.751) | Level ka coverage < 0.80 → not rated; ye spec ka hissa hai |
| L-05 | 2026 mein 4 teams ka counts total scoreboard se 2–2.9% **zyada** | Choti baat; Q-12 |
| L-06 | Pre-2026 seasons coarse rules par: spec ke mutabiq 2026 par full vs coarse 92.7% same role, Wing aur Combo Guard par kamzor | `rules_mode` har row par |
| L-07 | Misses ka Self-creation / Shooting / Finishing mein split ek **estimate** hai (assisted share se) | Is par depend karne wali har display par label |
| L-08 | Defense sirf steals aur blocks; contested shots waghera data mein nahi | Defensive grades par caveat |
| L-09 | (Production) 2018: 368 games mein free throws hain lekin fouls nahi (~7% FTs) | 2018 Discipline flag / exclude |
| L-10 | Role stability 62.3% (target 70%); 38% placements close calls | Secondary role zaroori output |
| L-11 | Matrix fit nahi (A-02) | Fallback players low confidence |

---

## 7. Open questions (Q)

| ID | Sawal | Kis se | Blocking? |
|---|---|---|---|
| Q-01 | Fallback rulebook **v3.2 ya v3.3**? | Owner | Nahi (A-02) |
| Q-02 | Asal matrix fit ki definition kab milegi? | Client | Nahi |
| Q-03 | Teammate shares sirf offensive possessions par, ya `inside` ke liye defensive bhi? | Client | Role ke shares |
| Q-04 | Percentile mein **ties** kaise? ("lower" strict hai) Non-qualified player ka percentile qualified population ke against? | Client | Role |
| Q-05 | Teammate ranking mein do players ka rate barabar ho to rank kaise? | Client | Role |
| Q-06 | League values (xPTS, zone FG%, league FT%, national jumper share) kis population se: sab players ya sirf D1 teams? | Client / V-10–V-13 se test | Level |
| Q-07 | Points per win: sirf regular season (`tournament_id IS NULL`) scoreboard? | Client / V-17 se test | Level |
| Q-08 | Half-weight pooling mein possessions bhi half weight? | Client | Role |
| Q-09 | Replacement family gap ka exact formula aur weighting | Client / V-14 se test | Level |
| Q-10 | Production mein naye seasons aane par tier bars fix rahein ya recompute? | Client | Production |
| Q-11 | Tiebreaker 4 (3-season sample) ke group scores kis population ke against re-percentile? | Client | Role |
| Q-12 | 2026 ki 4 teams jin ka counts total > scoreboard (L-05) | Data engineer | Nahi |
| Q-13 | Offsetting technicals counts se nikle hue hain? (A-07) | Data engineer | Nahi |
| Q-14 | `lead2` kisi rule mein use nahi hota; sirf display / audit ke liye? | Client | Nahi |
| Q-15 | Height boundaries: "taller than 6′8″" = `> 80`, "6′8″+" = `≥ 80`, "under 6′5″" = `< 77`, half-inch ke saath bhi? | Client | Role; Blue Cain (77.0) boundary par hai |
| Q-16 | Readback ke Questions 10–18 (ORB price, block value, rolling environment switch, per-role tier bars, alley-oops, schedule-adjusted lens, returner close-call, height as gate, stability floor) | Client | Kuch (A-04) default ke saath |

---

## 8. Validation targets (V) — sab 2026, spec se

Hamari implementation ko in numbers se match karna hai. "Ours" column kaam ke saath bharte jayenge.

### Population

| ID | Item | Spec | Ours |
|---|---|---|---|
| V-01 | Qualified players | 2,284 | 2,282 (Phase 2 query) |
| V-02 | Players in frame | 4,978 | 4,989 D1 (Phase 2 query) |
| V-03 | Read at normal confidence | 3,350 | |
| V-04 | Read from pooled seasons | 319 | |
| V-05 | Matrix-fit fallback | 1,309 | (A-02 ki wajah se method alag) |

### Role shares (qualified players)

| ID | Archetype | Spec | Ours |
|---|---|---|---|
| V-06a | Floor General | 15.8% | |
| V-06b | Combo Guard | 12.9% | |
| V-06c | Guard | 10.1% | |
| V-06d | 3pt Specialist | 11.8% | |
| V-06e | 3 and D Wing | 7.5% | |
| V-06f | Wing | 5.5% | |
| V-06g | Traditional Forward | 18.0% | |
| V-06h | UGA Big | 10.9% | |
| V-06i | Traditional Big | 7.5% | |

### Kis stage ne faisla kiya

| ID | Stage | Spec | Ours |
|---|---|---|---|
| V-07a | Clear top group | 2,310 | |
| V-07b | Tiebreaker 1: creator | 280 | |
| V-07c | Tiebreaker 2: interior | 262 | |
| V-07d | Tiebreaker 3: length | 152 | |
| V-07e | Tiebreaker 4: larger sample | 175 | |
| V-07f | Tiebreaker 5: higher volume | 490 | |

### Level ke season values

| ID | Item | Spec | Ours |
|---|---|---|---|
| V-10 | xPTS rim | 1.3100 | |
| V-11 | xPTS three | 1.2139 | |
| V-12 | xPTS mid-range | 0.9548 | |
| V-13 | League FT% | .7223 | |
| V-14 | Replacement: overall / guards / wings / bigs | −1.75 / −2.16 / −1.63 / −1.31 | |
| V-15 | Bench players / D1 teams | 556 / 365 | |
| V-16 | PPW teams | 365 | |
| V-17 | PPW fit | y = 14.75 + 0.02399·x, r .933, **41.69** | |
| V-18 | Tier bars (constants) | 0.1489 / 0.0913 / 0.0340 | n/a |

### Blue Cain, 2026 (`espn_player_id 5174661`)

| ID | Item | Spec | Ours |
|---|---|---|---|
| V-20a | Minutes | 808 | 808 ✅ |
| V-20b | Height | — | 77.0 in (6′5″) |
| V-20c | EPA total | 100.631 | |
| V-20d | EPA/40 | 4.982 | |
| V-20e | Family | Wing (3 and D Wing) | |
| V-20f | Replacement (wings) | −1.634 | |
| V-20g | Surplus/40 | +6.616 | |
| V-20h | WAR per 40 | 0.1587 | |
| V-20i | WAR · tier | 3.21 · Dark Green | |

Target: Level ke numbers **cent tak** match hon (spec ka apna standard).

---

## 9. Recalculation notes (abhi tak ki samajh)

Spec mein refresh schedule **nahi** likha. Ye hamari samajh hai, Phase 4 mein final hogi.

- Role aur Level **season-level batch** hain: percentiles, usage median, replacement, points per win sab poori season ki population par bante hain. Ek player ko alag se compute nahi kiya ja sakta.
- Order: Role → Level. Role ki nayi run ke baad Level ki run zaroori.
- Season *s* ka Role season *s−1* (aur kabhi *s−2*) par depend karta hai. Season *s* ka replacement *s+1* par bhi (family gap ±1). Is liye naya season aane par **pichla season bhi recompute** hoga.
- Raw data dobara aaye (naya dump) → import → saare affected seasons ki Role + Level runs.
- API hamesha latest `success` run parhti hai (D-06).

---

## 10. Mukhtasar glossary

| Term | Matlab |
|---|---|
| Possession | Jab tak ek team ke paas ball hai |
| Qualified | Torvik minutes % ≥ 40 aur 300+ offensive possessions (is season) |
| Read / No read | Pooling ke baad 300+ offensive possessions hain / nahi |
| Play type | Ginne wala kaam (assists, steals, pull-ups …) |
| Group | 7 kaam ke gucchay (Creation, Self-creation, Shooting, Steals, Defensive glass, Blocks, Inside) |
| Proposal | Har group ka rule jo role propose karta hai |
| Close call | Top proposal ke 0.10 ke andar alag role wali proposal |
| Family | Guards / Wings / Bigs (primary role se) |
| Rules mode | `full` (2026 tags) / `coarse` (pre-2026 proxies) |
| EPA | Expected Points Added: average possession (1.075) ke muqable extra points |
| Replacement | D1 bench (50–149 minutes) ka average EPA/40 |
| Surplus/40 | EPA/40 − replacement |
| Points per win | Season mein kitne extra points = ek extra jeet |
| WAR per 40 | Quality (tier isi par) |
| WAR | Quality × minutes × reliability |
| Coverage | pbp points ÷ box-score points; < 0.80 → not rated |

---

## 11. Change log

| Date | Change |
|---|---|
| 2026-10-25 | File banayi: Phase 1–2 ke facts, assumptions, decisions, questions, validation targets |
