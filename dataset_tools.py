"""Prototipo extendido: construccion, validacion y reparto de un dataset.

No depende de C2-DECT. Incluye sanitizacion, validacion de contrato, control de
calidad de etiquetas, reparto determinista, exportacion a JSONL, estadisticas y
generacion de datasheet. Los datos incluidos son SINTETICOS y sirven como
contrato de formato, no como telemetria real de ningun laboratorio.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

CONTRACT_FIELDS = {"event_type", "host", "t", "technique"}
SECRET_HINTS = ("password", "token", "secret", "api_key", "apikey")


def pseudonym(value: str) -> str:
    return "host-" + hashlib.sha256(value.encode("utf-8")).hexdigest()[:10]


def sanitize(event: dict) -> dict:
    clean = {
        k: v
        for k, v in event.items()
        if not any(hint in k.lower() for hint in SECRET_HINTS)
    }
    if "host" in clean:
        clean["host"] = pseudonym(str(clean["host"]))
    return clean


def validate(event: dict) -> tuple[bool, list[str]]:
    missing = sorted(CONTRACT_FIELDS - set(event))
    return not missing, missing


def label_quality(events: list[dict]) -> dict:
    """Detecta etiquetas ausentes y claves duplicadas."""
    seen: set[tuple] = set()
    duplicates: list[str] = []
    missing: list[int] = []
    for i, event in enumerate(events):
        if not event.get("technique") or not event.get("event_type"):
            missing.append(i)
        key = (event.get("host"), event.get("t"), event.get("technique"))
        if key in seen:
            duplicates.append(f"{key}")
        seen.add(key)
    return {
        "events": len(events),
        "missing_labels": missing,
        "duplicate_keys": duplicates,
        "ok": not missing and not duplicates,
    }


def split(events: list[dict], seed: int = 11) -> dict:
    """Reparto determinista 60/20/20 por hash del evento."""
    buckets = {"train": [], "val": [], "test": []}
    for event in events:
        key = f"{event.get('host')}|{event.get('t')}|{event.get('technique')}"
        bucket = int(hashlib.sha256(key.encode()).hexdigest(), 16) % 10
        name = "train" if bucket < 6 else ("val" if bucket < 8 else "test")
        buckets[name].append(event)
    return buckets


def export_splits(buckets: dict, outdir: str | Path) -> list[str]:
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    written = []
    for name, events in buckets.items():
        path = outdir / f"{name}.jsonl"
        path.write_text(
            "".join(json.dumps(e, ensure_ascii=False) + "\n" for e in events),
            encoding="utf-8",
        )
        written.append(path.as_posix())
    return written


def stats(events: list[dict]) -> dict:
    by_tech: dict[str, int] = {}
    by_type: dict[str, int] = {}
    for event in events:
        by_tech[event["technique"]] = by_tech.get(event["technique"], 0) + 1
        by_type[event["event_type"]] = by_type.get(event["event_type"], 0) + 1
    return {
        "events": len(events),
        "by_technique": dict(sorted(by_tech.items())),
        "by_event_type": dict(sorted(by_type.items())),
    }


def datasheet(events: list[dict]) -> dict:
    return {
        "name": "c2dect-lab-telemetry-v1 (prototipo sintetico)",
        "motivation": "Contrato de formato y prueba del pipeline de dataset; no telemetria real.",
        "composition": stats(events),
        "capture": "Totalmente sintetico. Generado para este prototipo.",
        "labeling": "Por tecnica ATT&CK, host seudonimizado y marca de tiempo.",
        "limits": [
            "No usar para entrenar detectores que pretendan generalization real.",
            "No representa ninguna campana ejecutada ni ningun laboratorio real.",
        ],
    }


def render_datasheet(sheet: dict) -> str:
    lines = [
        f"# Datasheet: {sheet['name']}",
        "",
        f"**Motivacion.** {sheet['motivation']}",
        "",
        f"**Captura.** {sheet['capture']}",
        "",
        f"**Etiquetado.** {sheet['labeling']}",
        "",
        "## Composicion",
        "",
        "| Grupo | Clave | Eventos |",
        "|---|---|---:|",
    ]
    for group, field in (("Tecnica", "by_technique"), ("Tipo", "by_event_type")):
        for key, count in sheet["composition"][field].items():
            lines.append(f"| {group} | {key} | {count} |")
    lines += ["", "## Limites", ""]
    lines += [f"- {limit}" for limit in sheet["limits"]]
    return "\n".join(lines) + "\n"


def load_jsonl(path: str | Path) -> list[dict]:
    return [
        json.loads(line)
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_report = sub.add_parser("report")
    p_report.add_argument("events")

    p_export = sub.add_parser("export")
    p_export.add_argument("events")
    p_export.add_argument("--out", required=True)

    args = parser.parse_args()
    clean = [sanitize(e) for e in load_jsonl(args.events)]
    if args.command == "report":
        payload = {
            "datasheet": datasheet(clean),
            "quality": label_quality(clean),
            "splits": {k: len(v) for k, v in split(clean).items()},
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(export_splits(split(clean), args.out), indent=2))


if __name__ == "__main__":
    main()
