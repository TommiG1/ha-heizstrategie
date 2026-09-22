# Architecture

## Overview

Everything runs through a central tick:

```text
Helpers / templates (setpoints, locks, forecast)
        │
        ▼
automation heizung_takt  (every minute + on changes)
        │
        ▼
script.heizung_tick
        ├── script.heizung_apply_klima   (per climate entity)
        ├── script.heizung_apply_tado    (hydraulic rooms)
        └── ETA / heating circuit / force charge (per tick logic)
```

In mode `Aus` (Off), `script.heizung_failsafe_aus` runs (climate/tado off, cancel manual override timers, boiler/circuits into a safe state).

## Layers

### 1. Helpers

User-facing setpoints and switches: mode, auto flags (climate / tado / ETA), room temperatures, away temperature, window debounce times, climate idle minutes, manual override duration.

### 2. Templates

Derived from helpers and hardware:

- `sensor.heizung_soll_*`: effective setpoint including schedule and away
- `binary_sensor.heizung_fenster_*_roh` / confirmed: window logic
- `binary_sensor.heizung_sperre_*`: room must not heat
- Buffer forecast / “is the buffer enough?” / hydraulic demand
- Climate “low power” (idle detection via outdoor unit power)

### 3. Scripts

- `heizung_apply_klima`: `off` / `heat` + temperature; skips active manual timers; idle off only after enough minutes of low power
- `heizung_apply_tado`: valves / room thermostats
- `heizung_ventile_schliessen`: close all valves
- `heizung_tick`: orchestrates everything
- `heizung_failsafe_aus`: safe state

### 4. Automations

- Minute tick and triggers on setpoint / lock changes
- Windows: confirm open after X minutes; start lockout timer on close
- Climate manual override: non-heat, or heat ≠ strategy setpoint, starts a timer; `off` or heat matching setpoint cancels it
- Outdoor / bedroom cold: debounce confirmation for night logic

## Design choices

**One-minute tick instead of many tiny automations**  
One place for priorities and order. Easier to debug than twenty parallel “if PV then climate” rules.

**Setpoints in templates, apply in scripts**  
Templates are observable (`sensor.heizung_soll_*`). Scripts only write to devices.

**Timed manual override**  
Otherwise the strategy fights the wall remote every minute. Heat with a different temperature counts as override on purpose.

**Idle needs duration, not a single sample**  
Shared outdoor power (e.g. living + dining) can dip briefly. Turn off only after configurable minutes of low power.

**Away split: house vs office**  
House away uses several people; office away uses only the relevant person. No need for tado geofencing.

**ETA rarely, not constant tweaking**  
Short starts burn pellets. Failsafe and clear enable conditions beat endless toggling.

## Zones (reference house)

| Zone | Heat | Note |
|------|------|------|
| Living / dining | Climate (maybe two indoors) | often shared outdoor power |
| Office | Climate (Faikin/Daikin) | own away possible |
| Bedrooms A/B/C | Climate | night logic / cold rooms; aliases for real rooms |
| Bath | tado + circuit / buffer | hydraulic, ETA-relevant |
| Playroom | tado | hydraulic |

## Mold (packages `schimmel_*`)

Three stages:

1. **Risk**: local from temp/RH (margin = room temp − dew point), classes like tado (`Critical` / `High` / `Medium` / `Low`). You can also use tado’s own risk sensors.
2. **Ventilation advice**: compares indoor dew point to `sensor.aussen_taupunkt` (Netatmo→DWD); cold thresholds use `sensor.aussen_temperatur` (ETA→Netatmo→DWD). Local vs DWD sync: `sensor.aussen_sensor_abgleich`.
3. **Mold heat**: only in the configured time window, only when risk is elevated and outdoor air is *not* drier: `binary_sensor.schimmel_heizen_aktiv_*` raises the climate setpoint in the heating templates to `input_number.schimmel_heizen_c`.

Without the mold packages, the heating setpoint templates simply never see those boost flags.
