# Plan 7 — Dataset de telemetría etiquetado del laboratorio

**Solo información y resultados.** Sin código fuente.

## Hipótesis

Se puede publicar un dataset de telemetría de un laboratorio aislado, etiquetado
por técnica y con veredictos de detección, lo bastante sanitizado para que
terceros reproduzcan mediciones sin exponer infraestructura.

## Estado actual (brecha)

La matriz de cobertura de la campaña muestra **44 TTPs sin ejecutar**, todos los
hits a 0 y veredictos `sin-registro / sin-probar`. Todavía no hay telemetría real
que publicar: hace falta ejecutar la campaña bajo RoE firmada.

## Diseño

1. Ejecutar campaña en VM con snapshot; cada técnica deja un `DetectionRecord`
   con `RuleID` y `Source`, y un `truth.Outcome` ejecutado.
2. Fuentes: Sysmon/ETW-TI adaptadas al contrato `p3.telemetry.v1`, pcap del canal
   C2, `activity_log` y reglas Sigma.
3. Etiquetado por técnica (ATT&CK ID), host, sesión, marca de tiempo y veredicto
   `landed / caught / blocked / needs_tuning`.
4. Sanitización: rutas y hashes sanitizados, sin secretos ni identificadores
   reales; corpus benigno como controles.
5. Versionado con esquema, reparto train/val/test y *datasheet*.

## Regla de honestidad

Si una técnica no se ejecuta, se marca `no-ejecutada`: **nunca** se rellena con
telemetría sintética como si fuera real.

## Ámbito

Laboratorio aislado, alcance declarado y RoE firmada. Uso exclusivamente
autorizado. Ver `PLANES_INVESTIGACION_4-7.md` y la matriz de cobertura incluida.
