"""efemat.cli — command-line interface.

Every capability is a named command that reproduces its result
(SCRIPTABLE gate). Machine-readable output via --json on data commands
(AUTOMATABLE). Run `python -m efemat --help` for the tree.

    python -m efemat registry list|show|validate
    python -m efemat simulate lca|compare|cost|loop|land|mc
    python -m efemat calculate ledger|mix|scale
    python -m efemat evaluate efe|ladder|risk
    python -m efemat synthesize composite|calibrate
    python -m efemat prototype list|card
    python -m efemat research corpus|web
    python -m efemat detail study|scoresheet
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from . import calculators, detail, evaluate, prototype, research, simulate, synthesize
from .registry import Registry, load_materials, load_pillars, load_processes


def _emit(obj: Any, as_json: bool) -> None:
    if as_json:
        print(json.dumps(obj, indent=2, default=str))
    else:
        if isinstance(obj, dict):
            for key, value in obj.items():
                print(f"{key}: {value}")
        else:
            print(obj)


def _load_all():
    return load_materials(), load_processes(), load_pillars()


# ---------------------------------------------------------------------------
# subcommand builders
# ---------------------------------------------------------------------------

def cmd_registry(args: argparse.Namespace) -> int:
    materials, processes, _ = _load_all()
    if args.cmd == "list":
        reg = materials if args.kind == "materials" else processes
        recs = reg.filter(**({args.by: args.value} if args.value else {}))
        if args.json:
            print(json.dumps([r["id"] for r in recs], indent=2))
        else:
            for r in recs:
                print(f"{r['id']:24s} [{r.get('status', '')}] {r['name']}")
        return 0
    if args.cmd == "show":
        reg = materials if args.kind == "materials" else processes
        _emit(reg.get(args.id), args.json)
        return 0
    if args.cmd == "validate":
        errors = materials.validate() + processes.validate()
        if args.json:
            print(json.dumps({"errors": errors, "valid": not errors}, indent=2))
        else:
            print("VALID" if not errors else "INVALID")
            for e in errors:
                print(f"  - {e}")
        return 0 if not errors else 1
    return 2


def cmd_simulate(args: argparse.Namespace) -> int:
    materials, _, _ = _load_all()
    if args.cmd == "lca":
        row = simulate.lca(materials.get(args.id), grid=args.grid)
        _emit(row, args.json)
        return 0
    if args.cmd == "compare":
        ids = args.ids or materials.ids()
        rows = simulate.compare(materials, ids, grid=args.grid)
        if args.json:
            print(json.dumps(rows, indent=2))
        else:
            print(f"{'id':24s} {'uptake':>8s} {'MJ/kg':>8s} {'net CO2':>9s}")
            for r in rows:
                print(f"{r['id']:24s} {r['uptake']:8.2f} {r['processing_mj_kg']:8.1f} {r['net_carbon']:+9.2f}")
        return 0
    if args.cmd == "cost":
        traj = simulate.cost_trajectory(materials.get(args.id), years=args.years)
        if args.json:
            print(json.dumps(traj, indent=2))
        else:
            for p in traj:
                print(f"Year {p['year']:3d}: {p['multiplier']:.2f}x  ${p['usd_kg']:.2f}/kg")
        return 0
    if args.cmd == "loop":
        result = simulate.loop_dynamics(materials.get(args.id), args.demand, years=args.years)
        result["series"] = [s for s in result["series"] if s["year"] % 5 == 0]
        _emit(result, args.json)
        return 0
    if args.cmd == "land":
        result = simulate.land_ledger(materials.get(args.id), args.demand, materials)
        if result is None:
            print(f"land ledger not applicable to {args.id} (no composition/feedstock_shares)")
            return 1
        _emit(result, args.json)
        return 0
    if args.cmd == "mc":
        result = simulate.monte_carlo_lca(materials.get(args.id), n=args.n, seed=args.seed)
        _emit(result, args.json)
        return 0
    return 2


def cmd_calculate(args: argparse.Namespace) -> int:
    materials, _, _ = _load_all()
    if args.cmd == "ledger":
        result = calculators.resource_ledger(
            materials,
            args.demand,
            grid=args.grid,
            atmospheric_kg_yr=args.atmospheric_kg,
        )
        if not args.json:
            land = result["land"]
            mix = result["mix_lever"]
            carb = result["carbon"]
            cost = result["cost"]
            print(f"resource ledger — {result['id']} @ {result['demand_t_yr']:,.0f} t/yr (grid: {result['grid']})")
            if land:
                print(f"  land (registry mix)   : {land['total_hectares']:,.0f} ha")
            if mix:
                print(f"  mix lever ({mix['best_mix']}): {mix['total_hectares']:,.0f} ha ({mix['reduction_pct']:.0f}% reduction)")
            if result["atmospheric_power"]:
                p = result["atmospheric_power"]
                print(f"  atmospheric power     : {p['mw_nameplate']:.2f} MW nameplate, {p['pv_hectares']:.2f} ha PV")
            print(f"  carbon               : {carb['net_kg_co2_per_kg']:+.2f} kg/kg -> {carb['annual_t_co2']/1000:,.0f} kt CO2/yr")
            print(f"  loop steady virgin    : {result['loop']['steady_state_virgin_t_yr']:,.0f} t/yr (recovery {result['loop']['recovery']:.2f})")
            print(f"  cost                  : ${cost['usd_kg_now']:.2f}/kg now -> ${cost['usd_kg_free']:.2f}/kg by year {cost['free_year']}")
        else:
            print(json.dumps(result, indent=2, default=str))
        return 0
    if args.cmd == "mix":
        result = calculators.mix_ledger(materials, args.demand)
        if result is None:
            print("mix ledger not applicable (no fiber fraction)")
            return 1
        if not args.json:
            print(f"mix ledger — {result['id']} @ {result['demand_t_yr']:,.0f} t/yr (fiber fraction {result['fiber_fraction']:.2f})")
            for s in result["scenarios"]:
                print(f"  {s['mix']:28s} {s['total_hectares']:>12,.0f} ha")
        else:
            print(json.dumps(result, indent=2, default=str))
        return 0
    if args.cmd == "scale":
        result = calculators.scale_path(materials, args.from_t, args.to_t, years=args.years, grid=args.grid)
        if result is None:
            print("scale path not applicable (no land ledger)")
            return 1
        if not args.json:
            print(f"scale path — {result['id']}: {result['start_t_yr']:,.0f} -> {result['end_t_yr']:,.0f} t/yr over {result['years']} yr (grid: {result['grid']})")
            print(f"{'yr':>3s} {'demand t/yr':>12s} {'land ha':>10s} {'virgin t/yr':>12s} {'$/kg':>6s} {'kt CO2/yr':>10s}")
            for r in result["rows"]:
                print(
                    f"{r['year']:3d} {r['demand_t_yr']:12,.0f} {r['land_hectares']:10,.0f} "
                    f"{r['virgin_t_yr']:12,.0f} {r['usd_kg']:6.2f} {r['annual_t_co2']/1000:10,.0f}"
                )
            print(f"  scalable (linear land): {result['scalable_linear_land']} — {result['ha_per_kt']:.1f} ha per kt/yr, constant across the ramp")
        else:
            print(json.dumps(result, indent=2, default=str))
        return 0
    return 2


def cmd_evaluate(args: argparse.Namespace) -> int:
    materials, _, pillars = _load_all()
    m = materials.get(args.id)
    if args.cmd == "efe":
        _emit(evaluate.efe_score(m, pillars), args.json)
        return 0
    if args.cmd == "ladder":
        _emit(evaluate.ladder_info(m), args.json)
        return 0
    if args.cmd == "risk":
        _emit(evaluate.risk_class(m), args.json)
        return 0
    return 2


def cmd_synthesize(args: argparse.Namespace) -> int:
    if args.cmd == "composite":
        fractions = {}
        for name in ("cellulose", "lignin", "graphene", "hemp", "flax", "biochar", "additives"):
            value = getattr(args, name, None)
            if value is not None:
                key = {
                    "cellulose": "cellulose_fiber",
                    "lignin": "lignin_resin",
                    "graphene": "bio_graphene",
                }.get(name, name)
                fractions[key] = value
        if not fractions:
            print("no fractions given; e.g. --cellulose 0.52 --lignin 0.38 --graphene 0.05 --additives 0.05")
            return 2
        result = synthesize.composite(
            fractions, alignment=args.alignment, densification=args.densification, grade=args.grade
        )
        _emit(result, args.json)
        return 0
    if args.cmd == "calibrate":
        materials, _, _ = _load_all()
        _emit(synthesize.calibrate_dlgc(materials), args.json)
        return 0
    return 2


def cmd_prototype(args: argparse.Namespace) -> int:
    _, processes, _ = _load_all()
    if args.cmd == "list":
        for p in processes.records.values():
            print(f"{p['id']:32s} [{p['stage']}] {p['name']}")
        return 0
    if args.cmd == "card":
        print(prototype.process_card(processes.get(args.id)))
        return 0
    return 2


def cmd_research(args: argparse.Namespace) -> int:
    if args.cmd == "corpus":
        matches = research.corpus_search(args.query, limit=args.limit)
        if args.json:
            print(json.dumps(matches, indent=2))
        else:
            if not matches:
                print("no matches")
            for m in matches:
                print(f"{m['file']}:{m['line_no']}: {m['text']}")
        return 0
    if args.cmd == "web":
        _emit(research.web_search_protocol(args.query), args.json)
        return 0
    return 2


def cmd_detail(args: argparse.Namespace) -> int:
    materials, processes, pillars = _load_all()
    if args.cmd == "study":
        stats = detail.generate_study(materials, processes, pillars, out_path=Path(args.out) if args.out else None)
        _emit(stats, args.json)
        return 0
    if args.cmd == "scoresheet":
        print(detail.scoresheet(args.id, materials, processes, pillars))
        return 0
    return 2


# ---------------------------------------------------------------------------
# parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="efemat",
        description="EFE Materials Environment Toolkit (aequchain program)",
    )
    parser.add_argument("--version", action="version", version="efemat 1.0.0")
    sub = parser.add_subparsers(dest="group", required=True)

    # registry ------------------------------------------------------------
    p_reg = sub.add_parser("registry", help="query the JSON registries")
    reg_sub = p_reg.add_subparsers(dest="cmd", required=True)
    p_list = reg_sub.add_parser("list", help="list records")
    p_list.add_argument("--kind", choices=["materials", "processes"], default="materials")
    p_list.add_argument("--by", default="class", help="filter field (default: class)")
    p_list.add_argument("--value", default=None, help="filter value, e.g. replenishable")
    p_list.add_argument("--json", action="store_true")
    p_show = reg_sub.add_parser("show", help="show one record")
    p_show.add_argument("id")
    p_show.add_argument("--kind", choices=["materials", "processes"], default="materials")
    p_show.add_argument("--json", action="store_true")
    p_val = reg_sub.add_parser("validate", help="schema validation")
    p_val.add_argument("--json", action="store_true")

    # simulate ------------------------------------------------------------
    p_sim = sub.add_parser("simulate", help="LCA, cost, loops, land, Monte-Carlo")
    sim_sub = p_sim.add_subparsers(dest="cmd", required=True)
    for name, help_ in (("lca", "carbon accounting for one material"),):
        p = sim_sub.add_parser(name, help=help_)
        p.add_argument("id")
        p.add_argument("--grid", choices=["renewable", "world", "efe", "zero"], default="renewable")
        p.add_argument("--json", action="store_true")
    p_cmp = sim_sub.add_parser("compare", help="LCA table across materials")
    p_cmp.add_argument("ids", nargs="*")
    p_cmp.add_argument("--grid", choices=["renewable", "world", "efe", "zero"], default="renewable")
    p_cmp.add_argument("--json", action="store_true")
    p_cost = sim_sub.add_parser("cost", help="EFE cost trajectory")
    p_cost.add_argument("id")
    p_cost.add_argument("--years", type=int, default=20)
    p_cost.add_argument("--json", action="store_true")
    p_loop = sim_sub.add_parser("loop", help="secondary-supply saturation")
    p_loop.add_argument("id")
    p_loop.add_argument("--demand", type=float, default=1_150_000.0)
    p_loop.add_argument("--years", type=int, default=50)
    p_loop.add_argument("--json", action="store_true")
    p_land = sim_sub.add_parser("land", help="hectares needed per feedstock")
    p_land.add_argument("id")
    p_land.add_argument("--demand", type=float, required=True)
    p_land.add_argument("--json", action="store_true")
    p_mc = sim_sub.add_parser("mc", help="Monte-Carlo LCA band")
    p_mc.add_argument("id")
    p_mc.add_argument("--n", type=int, default=1000)
    p_mc.add_argument("--seed", type=int, default=42)
    p_mc.add_argument("--json", action="store_true")

    # calculate ------------------------------------------------------------
    p_calc = sub.add_parser("calculate", help="unified resource ledgers + scaling paths")
    calc_sub = p_calc.add_subparsers(dest="cmd", required=True)
    p_led = calc_sub.add_parser("ledger", help="one demand in, every resource out")
    p_led.add_argument("--demand", type=float, default=1_150_000.0)
    p_led.add_argument("--grid", choices=["renewable", "world", "efe", "zero"], default="renewable")
    p_led.add_argument("--atmospheric-kg", type=float, default=0.0, help="optional atmospheric-family kg/yr (power ledger)")
    p_led.add_argument("--json", action="store_true")
    p_mixc = calc_sub.add_parser("mix", help="fiber-mix scenarios (the mix lever)")
    p_mixc.add_argument("--demand", type=float, default=1_150_000.0)
    p_mixc.add_argument("--json", action="store_true")
    p_scl = calc_sub.add_parser("scale", help="year-by-year scaling path (1x -> 100x evidence)")
    p_scl.add_argument("--from", dest="from_t", type=float, default=10_000.0)
    p_scl.add_argument("--to", dest="to_t", type=float, default=1_150_000.0)
    p_scl.add_argument("--years", type=int, default=12)
    p_scl.add_argument("--grid", choices=["renewable", "world", "efe", "zero"], default="renewable")
    p_scl.add_argument("--json", action="store_true")

    # evaluate ------------------------------------------------------------
    p_eval = sub.add_parser("evaluate", help="EFE pillars, ladder, risk")
    eval_sub = p_eval.add_subparsers(dest="cmd", required=True)
    for name in ("efe", "ladder", "risk"):
        p = eval_sub.add_parser(name)
        p.add_argument("id")
        p.add_argument("--json", action="store_true")

    # synthesize ------------------------------------------------------------
    p_syn = sub.add_parser("synthesize", help="composite synthesis + calibration")
    syn_sub = p_syn.add_subparsers(dest="cmd", required=True)
    p_comp = syn_sub.add_parser("composite", help="rule-of-mixtures synthesis")
    for comp in ("cellulose", "lignin", "graphene", "hemp", "flax", "biochar", "additives"):
        p_comp.add_argument(f"--{comp}", type=float, default=None)
    p_comp.add_argument("--alignment", type=float, default=0.92)
    p_comp.add_argument("--densification", type=float, default=1.5)
    p_comp.add_argument("--grade", choices=["mid", "hi"], default="mid")
    p_comp.add_argument("--json", action="store_true")
    p_cal = syn_sub.add_parser("calibrate", help="reproduce corpus DLGC spec")
    p_cal.add_argument("--json", action="store_true")

    # prototype ------------------------------------------------------------
    p_pro = sub.add_parser("prototype", help="process spec cards")
    pro_sub = p_pro.add_subparsers(dest="cmd", required=True)
    pro_sub.add_parser("list")
    p_card = pro_sub.add_parser("card")
    p_card.add_argument("id")

    # research ------------------------------------------------------------
    p_res = sub.add_parser("research", help="corpus search + web protocol")
    res_sub = p_res.add_subparsers(dest="cmd", required=True)
    p_corp = res_sub.add_parser("corpus")
    p_corp.add_argument("query")
    p_corp.add_argument("--limit", type=int, default=50)
    p_corp.add_argument("--json", action="store_true")
    p_web = res_sub.add_parser("web")
    p_web.add_argument("query")
    p_web.add_argument("--json", action="store_true")

    # detail ------------------------------------------------------------
    p_det = sub.add_parser("detail", help="study + scoresheet generation")
    det_sub = p_det.add_subparsers(dest="cmd", required=True)
    p_study = det_sub.add_parser("study")
    p_study.add_argument("--out", default=None)
    p_study.add_argument("--json", action="store_true")
    p_sheet = det_sub.add_parser("scoresheet")
    p_sheet.add_argument("id")

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    handlers = {
        "registry": cmd_registry,
        "simulate": cmd_simulate,
        "calculate": cmd_calculate,
        "evaluate": cmd_evaluate,
        "synthesize": cmd_synthesize,
        "prototype": cmd_prototype,
        "research": cmd_research,
        "detail": cmd_detail,
    }
    handler = handlers.get(args.group)
    if handler is None:  # pragma: no cover
        parser.error(f"unknown group {args.group}")
        return 2
    try:
        return handler(args)
    except KeyError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
