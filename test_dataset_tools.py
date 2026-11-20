"""Tests del prototipo extendido de dataset (datos sinteticos)."""

import json
import tempfile
import unittest
from pathlib import Path

from dataset_tools import (
    datasheet,
    export_splits,
    label_quality,
    load_jsonl,
    pseudonym,
    render_datasheet,
    sanitize,
    split,
    stats,
    validate,
)

HERE = Path(__file__).resolve().parent


class TestSanitizacion(unittest.TestCase):
    def setUp(self):
        self.raw = load_jsonl(HERE / "fixtures" / "telemetry_raw.jsonl")

    def test_sanitize_elimina_secretos_y_seudonimiza(self):
        clean = sanitize(self.raw[0])
        self.assertNotIn("password", clean)
        self.assertNotIn("host_real", clean["host"])
        self.assertEqual(clean["host"], pseudonym("host_real"))
        self.assertEqual(clean["technique"], "T1059")

    def test_validate(self):
        ok, missing = validate(sanitize(self.raw[0]))
        self.assertTrue(ok, missing)

    def test_fixture_valida(self):
        self.assertEqual(len(self.raw), 6)
        self.assertTrue(all(validate(sanitize(e))[0] for e in self.raw))


class TestCalidadYReparto(unittest.TestCase):
    def test_label_quality_sin_problemas(self):
        raw = load_jsonl(HERE / "fixtures" / "telemetry_raw.jsonl")
        q = label_quality([sanitize(e) for e in raw])
        self.assertTrue(q["ok"])
        self.assertEqual(q["events"], 6)

    def test_label_quality_detecta_duplicados_y_faltantes(self):
        events = [
            {"host": "h", "t": 1, "technique": "T1", "event_type": "x"},
            {"host": "h", "t": 1, "technique": "T1", "event_type": "x"},
            {"host": "h", "t": 2, "technique": "", "event_type": "x"},
        ]
        q = label_quality(events)
        self.assertFalse(q["ok"])
        self.assertEqual(len(q["duplicate_keys"]), 1)
        self.assertEqual(q["missing_labels"], [2])

    def test_split_determinista_y_completo(self):
        clean = [sanitize(e) for e in load_jsonl(HERE / "fixtures" / "telemetry_raw.jsonl")]
        a, b = split(clean), split(clean)
        self.assertEqual(a, b)
        self.assertEqual(sum(len(v) for v in a.values()), len(clean))

    def test_export_splits(self):
        clean = [sanitize(e) for e in load_jsonl(HERE / "fixtures" / "telemetry_raw.jsonl")]
        with tempfile.TemporaryDirectory() as tmp:
            paths = export_splits(split(clean), tmp)
            self.assertEqual(len(paths), 3)
            total = sum(len(load_jsonl(p)) for p in paths)
            self.assertEqual(total, len(clean))


class TestDatasheet(unittest.TestCase):
    def test_datasheet_y_markdown(self):
        clean = [sanitize(e) for e in load_jsonl(HERE / "fixtures" / "telemetry_raw.jsonl")]
        sheet = datasheet(clean)
        self.assertEqual(sheet["composition"]["events"], 6)
        md = render_datasheet(sheet)
        self.assertIn("# Datasheet", md)
        self.assertIn("## Limites", md)
        self.assertIn("sintetico", sheet["capture"].lower())

    def test_stats(self):
        clean = [sanitize(e) for e in load_jsonl(HERE / "fixtures" / "telemetry_raw.jsonl")]
        s = stats(clean)
        self.assertEqual(s["events"], 6)
        self.assertIn("T1059", s["by_technique"])


if __name__ == "__main__":
    unittest.main()
