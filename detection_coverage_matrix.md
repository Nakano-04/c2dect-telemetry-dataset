# Handoff para el equipo azul

Esquema: `blue-team/1`
Generado: 2026-11-19T21:34:45Z

## Fuentes (hashes verificables)

- `campaign.json`: sha256:8339fd5ac08121436f3221d8167a83095b656488d5774aedf28cd1d4ba25f15f
- `campaign_weapons.json`: sha256:1c431512a57c275c51cf40129e78b807b27f542c9a447909627bc8acddd313f1
- `ciperc_report.json`: sha256:e396ca813f6d4ccf761e0a78f051b18278f7291d833894d2862e05a4f7ffdd45
- `records.json`: sha256:no-disponible

## Cobertura por tecnica y regla

| Tecnica | Regla | Hits | Verdict | Estado |
|---|---|---:|---|---|
| T1071.001 | c2lab-android-agent-lab-fingerprint.yml | 0 | sin-registro | sin-probar |
| T1071.001 | c2lab-android-agent-lab-beacon-periodic.yml | 0 | sin-registro | sin-probar |
| T1071.001 | c2lab-android-agent-lab-net-base.yml | 0 | sin-registro | sin-probar |
| T1461 | c2lab-android-agent-lab-fingerprint.yml | 0 | sin-registro | sin-probar |
| T1461 | c2lab-android-agent-lab-beacon-periodic.yml | 0 | sin-registro | sin-probar |
| T1461 | c2lab-android-agent-lab-net-base.yml | 0 | sin-registro | sin-probar |
| T1629 | c2lab-android-agent-lab-fingerprint.yml | 0 | sin-registro | sin-probar |
| T1629 | c2lab-android-agent-lab-beacon-periodic.yml | 0 | sin-registro | sin-probar |
| T1629 | c2lab-android-agent-lab-net-base.yml | 0 | sin-registro | sin-probar |
| T1071.001 | c2lab-c2dect-agent-lab-beacon-periodic.yml | 0 | sin-registro | sin-probar |
| T1071.001 | c2lab-c2dect-agent-lab-fingerprint.yml | 0 | sin-registro | sin-probar |
| T1071.001 | c2lab-cloud-sync-lab-beacon-periodic.yml | 0 | sin-registro | sin-probar |
| T1071.001 | c2lab-cloud-sync-lab-fingerprint.yml | 0 | sin-registro | sin-probar |
| T1071.001 | c2lab-cloud-sync-beacon-periodic.yml | 0 | sin-registro | sin-probar |
| T1071.001 | c2lab-cloud-sync-fingerprint.yml | 0 | sin-registro | sin-probar |
| T1566 | c2lab-first-entry-lure-net-base.yml | 0 | sin-registro | sin-probar |
| T1566 | c2lab-first-entry-lure-beacon-periodic.yml | 0 | sin-registro | sin-probar |
| T1566 | c2lab-first-entry-lure-fingerprint.yml | 0 | sin-registro | sin-probar |
| T1566 | c2lab-first-entry-ta0001.yml | 0 | sin-registro | sin-probar |
| T1189 | c2lab-first-entry-lure-net-base.yml | 0 | sin-registro | sin-probar |
| T1189 | c2lab-first-entry-lure-beacon-periodic.yml | 0 | sin-registro | sin-probar |
| T1189 | c2lab-first-entry-lure-fingerprint.yml | 0 | sin-registro | sin-probar |
| T1189 | c2lab-first-entry-ta0001.yml | 0 | sin-registro | sin-probar |
| T1190 | c2lab-first-entry-lure-net-base.yml | 0 | sin-registro | sin-probar |
| T1190 | c2lab-first-entry-lure-beacon-periodic.yml | 0 | sin-registro | sin-probar |
| T1190 | c2lab-first-entry-lure-fingerprint.yml | 0 | sin-registro | sin-probar |
| T1190 | c2lab-first-entry-ta0001.yml | 0 | sin-registro | sin-probar |
| T1091 | c2lab-first-entry-lure-net-base.yml | 0 | sin-registro | sin-probar |
| T1091 | c2lab-first-entry-lure-beacon-periodic.yml | 0 | sin-registro | sin-probar |
| T1091 | c2lab-first-entry-lure-fingerprint.yml | 0 | sin-registro | sin-probar |
| T1091 | c2lab-first-entry-ta0001.yml | 0 | sin-registro | sin-probar |
| T1078 | c2lab-first-entry-lure-net-base.yml | 0 | sin-registro | sin-probar |
| T1078 | c2lab-first-entry-lure-beacon-periodic.yml | 0 | sin-registro | sin-probar |
| T1078 | c2lab-first-entry-lure-fingerprint.yml | 0 | sin-registro | sin-probar |
| T1078 | c2lab-first-entry-ta0001.yml | 0 | sin-registro | sin-probar |
| SIN-TTP | (sin regla declarada) | 0 | sin-registro | sin-probar |
| T1190 | c2lab-ios-nday-kernel.yml | 0 | sin-registro | sin-probar |
| T1190 | c2lab-ios-nday-webkit.yml | 0 | sin-registro | sin-probar |
| T1190 | c2lab-ios-nday-sandbox.yml | 0 | sin-registro | sin-probar |
| T1203 | c2lab-ios-nday-kernel.yml | 0 | sin-registro | sin-probar |
| T1203 | c2lab-ios-nday-webkit.yml | 0 | sin-registro | sin-probar |
| T1203 | c2lab-ios-nday-sandbox.yml | 0 | sin-registro | sin-probar |
| T1071.001 | c2lab-update-check-beacon-periodic.yml | 0 | sin-registro | sin-probar |
| T1071.001 | c2lab-update-check-fingerprint.yml | 0 | sin-registro | sin-probar |

## Hallazgos

### 44 TTPs sin ejecutar en la campana

- **Evidencia**: tecnicas: SIN-TTP, T1071.001, T1078, T1091, T1189, T1190, T1203, T1461, T1566, T1629
- **Hipotesis / accion**: Planificar un retest que cubra esas tecnicas bajo RoE firmada
- **Responsable**: red-team
- **Criterio de cierre**: C3 DetectionRecord creado con RuleID y Source (G1)

### El equipo azul corrio a ciegas; la trazabilidad esta en activity_log/Sigma

- **Evidencia**: campaign.json + detection_coverage_matrix + hashes sha256
- **Hipotesis / accion**: Usar este handoff para ajustar reglas y cerrar la brecha en el proximo ciclo
- **Responsable**: blue-team
- **Criterio de cierre**: Hallazgo cerrado solo tras retest (G3): nunca auto-cerrar

---

Gobernanza: los hallazgos **no se cierran automaticamente** (G3). La evidencia va como hash/ruta sanitizada (G8). La verdad la tiene el DetectionRecord; esta matriz solo la presenta.
