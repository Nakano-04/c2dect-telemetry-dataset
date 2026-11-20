# Ejecutable Zig — `dataset_zig`

Sanitizador de telemetría en Zig 0.17.1. Elimina claves con secretos,
seudonimiza el host con SHA256 y cuenta eventos por técnica.

```powershell
zig build
zig build test
.\zig-out\bin\dataset_zig.exe fixtures\telemetry_raw.jsonl
```

Resultado esperado sobre la fixture: 6 eventos, 3 técnicas distintas
(T1059, T1055, T1071).
