# Entity map (reference → your house)

All `heizung_*` helpers, timers, and template sensors come from the packages.  
**You must replace hardware and presence entities** in templates, scripts, and the dashboard.

Search `packages/` and `dashboards/` for the reference IDs and put yours in.

## Climate

| Role | Reference entity | Your entity |
|------|------------------|-------------|
| Living room climate | `climate.wohnzimmer_2` | |
| Dining climate | `climate.esszimmer` | |
| Office climate | `climate.faikin_mqtt_hvac` | |
| Bedroom 1 | `climate.schlafen_a` | Bedroom A |
| Bedroom 2 | `climate.schlafen_b` | Bedroom B |
| Bedroom 3 | `climate.schlafen_c` | Bedroom C |
| (legacy / bedroom C tado) | `climate.schlafen_c_tado` | remove or rename if unused |

Power / idle (outdoor units):

| Role | Reference |
|------|-----------|
| Living outdoor power | `sensor.uv_schupfen_uv_schupfen_terasse_phase_c_leistung` |
| Bedroom outdoor power | `sensor.schlafraume_erdgeschoss_klima_schlafen_phase_a_leistung` |
| Office compressor / power | `sensor.faikin_comp`, `sensor.faikin_power_consumption` |

## tado / hydraulic

| Role | Reference |
|------|-----------|
| Bath | `climate.bad` |
| Office tado (if used) | `climate.buro` |
| Playroom | `climate.spielzimmer` |
| Bedroom tado | `climate.schlafzimmer` |
| Living tado | `climate.wohnzimmer` |

## Windows / doors

| Zone | Reference |
|------|-----------|
| Living | `binary_sensor.wohnzimmer_wohnzimmer_fenster`, `binary_sensor.ture_terrasse_contact` |
| Office | `binary_sensor.fenster_buro_contact`, `binary_sensor.dachfenster_buro_contact` |
| Bath | `binary_sensor.fenster_bad_contact`, `binary_sensor.bad_bad_fenster` |
| Playroom | `binary_sensor.spielzimmer_spielzimmer_fenster` |
| Bedroom B | `binary_sensor.schlafzimmer_schlafzimmer_fenster` |
| Bedroom C | `binary_sensor.fenster_schlafen_c_contact`, `binary_sensor.schlafen_c_fenster` |

## Presence / away

| Role | Reference | English |
|------|-----------|---------|
| House person 1 | `person.person_a` | Person A |
| House person 2 | `person.person_b` | Person B |
| House person 3 | `person.person_c` | Person C |

House away (Away Haus): all three not `home`.  
Office away (Away Büro): person A only (`person.person_a` in the reference).

Mode options on `input_select.heizung_modus` stay German: `Aus` = Off, `Übergang` = shoulder season, `Winter` = winter. See `GLOSSARY.md`.

## ETA / buffer / immersion / PV

| Role | Reference |
|------|-----------|
| Outdoor temperature | `sensor.heizkreis_eingange_aussentemperatur` |
| Buffer top / mid / bottom | `sensor.pufferflex_eingange_fuhler_1_oben`, `_fuhler_2`, `_fuhler_3` |
| Heating circuit on/off | `switch.heizkreis_sonstiges_ein_aus_taste` |
| Boiler on/off | `switch.kessel_sonstiges_ein_aus_taste` |
| Force charge (buffer) | `switch.pufferflex_puffer_erzeuger_kessel_puffer_starten_nach_zusatzlichen_kriterien_extra_laden_sofort_laden` |
| Pellet meter (optional) | `sensor.eta_pellet_gesamtverbrauch` |
| ELWA power / temp | `sensor.ac_elwa_2_1_*`, `sensor.elwa_api_*` |
| House load | `sensor.e3dc_berechneter_hausverbrauch_wallbox_elwa` |
| Battery SoC | `sensor.e3dc_battery_state_of_charge` |
| Grid import forecast | `sensor.e3dc_maestro_forecast_netzbezug_nachste_24h` |
| SoC trajectory | `sensor.e3dc_maestro_forecast_soc_trajektorie_24h` |
| Solcast today/tomorrow | `sensor.solcast_pv_forecast_prognose_heute`, `…_morgen` |

## Mold: local risk sources (temp + RH)

| Room | Temperature | Humidity | Result sensor |
|------|-------------|----------|---------------|
| Living room | `sensor.wohnzimmer_temperatur_2` | `sensor.wohnzimmer_luftfeuchtigkeit_2` | `sensor.schimmel_risiko_wohnen` |
| Bedroom C | `sensor.temp_schlafen_c_temperature` | `sensor.temp_schlafen_c_humidity` | `sensor.schimmel_risiko_schlafen_c` |

## Mold: tado risk (if present)

| Room | Reference |
|------|-----------|
| Office | `sensor.buro_buro_schimmelpilzrisiko` |
| Bedroom | `sensor.schlafzimmer_schlafzimmer_schimmelpilzrisiko` |
| Bath | `sensor.bad_bad_schimmelpilzrisiko` |
| Playroom | `sensor.spielzimmer_spielzimmer_schimmelpilzrisiko` |

Outdoor: `weather.home` with `temperature`, `humidity`, `dew_point`.

Mold-heat flags (`binary_sensor.schimmel_heizen_aktiv_*`) come from `packages/schimmel_templates.yaml`. Without that package, remove the boost conditions in the heating setpoint templates or leave the switches off.

## Remap tips

1. Load helpers + templates first and check setpoint sensors in the UI  
2. Test scripts with `heizung_klima_auto` / `heizung_tado_auto` / `heizung_eta_auto` off  
3. Wire one zone (e.g. office climate only), then expand  
4. Adapt the dashboard last
