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
| Living outdoor power | `sensor.schlafraume_erdgeschoss_klima_schlafen_phase_a_leistung` (Entity-ID nach Montageort benannt, misst tatsächlich Wohnen/Essen; siehe `sensor.klimaanlagen_gesamtleistung` und `binary_sensor.heizung_klima_wenig_wohnen`) |
| Bedroom outdoor power | `sensor.uv_schupfen_uv_schupfen_terasse_phase_c_leistung` (Entity-ID nach Montageort benannt, misst tatsächlich Schlafräume) |
| Office compressor / power | `sensor.faikin_comp`, `sensor.faikin_power_consumption` |

## tado / hydraulic

| Role | Reference |
|------|-----------|
| Bath | `climate.bad` |
| Office tado (if used) | `climate.buro` |
| Playroom | `climate.spielzimmer` |
| Bedroom tado | `climate.schlafzimmer` |
| Living tado | `climate.wohnzimmer` |
| Kitchen tado (optional Raum-Ist) | `sensor.kuche_temperatur` / `climate.kuche` — derzeit oft unavailable; Fallback `sensor.wohnzimmer_wohnzimmer_temperatur` |
| Wohnen Raum-Ist (Strategie) | `sensor.heizung_raum_ist_wohnen` |
| Wohnen MelCloud Gerät-Soll | `sensor.heizung_klima_geraet_soll_wohnen` |

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
Playroom away (Away Spielzimmer): person C only (`person.person_c` in the reference).

Mode options on `input_select.heizung_modus` stay German: `Aus` = Off, `Übergang` = shoulder season, `Winter` = winter. See `GLOSSARY.md`.

## ETA / buffer / immersion / PV

| Role | Reference |
|------|-----------|
| Outdoor temperature | `sensor.aussen_temperatur` (ETA→Netatmo→DWD) |
| Buffer top / mid / bottom | `sensor.pufferflex_eingange_fuhler_1_oben`, `_fuhler_2`, `_fuhler_3` |
| Heating circuit on/off | `switch.heizkreis_sonstiges_ein_aus_taste` |
| Boiler on/off | `switch.kessel_sonstiges_ein_aus_taste` |
| Force charge (buffer) | `switch.pufferflex_puffer_erzeuger_kessel_puffer_starten_nach_zusatzlichen_kriterien_extra_laden_sofort_laden` |
| Pellet meter (optional) | `sensor.eta_pellet_gesamtverbrauch` |
| ELWA power / temp | `sensor.ac_elwa_2_1_*`, `sensor.elwa_api_*` |
| ELWA / HK viz helpers | `binary_sensor.heizung_elwa_aktiv`, `binary_sensor.heizung_hk_pumpe_aktiv` |
| Anlage dashboard | Sidebar **Anlage** (GUI-/Storage-Modus; Backup `dashboards/heizung_anlage.storage-backup.json`, Icons `/local/eta/`) |
| House load | `sensor.e3dc_berechneter_hausverbrauch_wallbox_elwa` |
| Battery SoC | `sensor.e3dc_battery_state_of_charge` |
| Grid import forecast | `sensor.e3dc_maestro_forecast_netzbezug_nachste_24h` |
| SoC trajectory | `sensor.e3dc_maestro_forecast_soc_trajektorie_24h` |
| Solcast today/tomorrow | `sensor.solcast_pv_forecast_prognose_heute`, `…_morgen` |

## Mold: local risk sources (temp + RH)

| Room | Temperature | Humidity | Result sensor |
|------|-------------|----------|---------------|
| Living room | `sensor.wohnzimmer_temperatur_2` | `sensor.wohnzimmer_luftfeuchtigkeit_2` | `sensor.schimmel_risiko_wohnen` |
| Office | `sensor.netatmo_buero_temperatur` | `sensor.netatmo_buero_luftfeuchtigkeit` | `sensor.schimmel_risiko_buero` |
| Bath | `sensor.netatmo_bad_temperatur` | `sensor.netatmo_bad_luftfeuchtigkeit` | `sensor.schimmel_risiko_bad` |
| Bedroom | `sensor.aqara_temp_schlafen_b_temperature` | `sensor.aqara_temp_schlafen_b_humidity` | `sensor.schimmel_risiko_schlafzimmer` |
| Bedroom C | `sensor.temp_schlafen_c_temperature` | `sensor.temp_schlafen_c_humidity` | `sensor.schimmel_risiko_schlafen_c` |

HA Mold Indicator (percent, analog bedroom B; nach Core-Neustart): `sensor.schimmel_indikator_schlafen_b`.

## Mold: tado risk (if present)

| Room | Reference |
|------|-----------|
| Playroom | `sensor.spielzimmer_spielzimmer_schimmelpilzrisiko` |

Outdoor (with DWD fallback): `sensor.aussen_temperatur` (ETA → Netatmo → DWD nearest station); `sensor.aussen_feuchtigkeit` / `sensor.aussen_taupunkt` (Netatmo → DWD); validation `sensor.aussen_sensor_abgleich`. See `packages/aussen_wetter.yaml`.

Mold-heat flags (`binary_sensor.schimmel_heizen_aktiv_*`) come from `packages/schimmel_templates.yaml`. Without that package, remove the boost conditions in the heating setpoint templates or leave the switches off.

## Einsparung / Kosten (Klima + ELWA vs. Pellets)

Siehe `packages/heizung_einsparung.yaml`.

| Rolle | Reference |
|------|-----------|
| Klima Gesamtleistung (Büro+Wohnen+Schlafen) | `sensor.klimaanlagen_gesamtleistung` (Template, `includes/templates/template_sensors.yaml` auf der Live-Instanz) |
| Klima-Heizbetrieb-Flag | `binary_sensor.heizung_klima_heizbetrieb` (neu; prüft `climate.*` auf `hvac_mode: heat`) |
| ELWA Leistung / PV- / Netzanteil | `sensor.elwa_api_leistung`, `sensor.elwa_api_solaranteil`, `sensor.elwa_api_netzanteil` |
| ELWA Gesamtenergie (bestehend) | `sensor.elwa_2_energie` |
| E3DC PV / Netzbezug / Netzeinspeisung / Akku-Entladung (Leistung) | `sensor.e3dc_solar_power`, `sensor.e3dc_grid_import_power`, `sensor.e3dc_grid_export_power`, `sensor.e3dc_battery_discharge_power` |
| Haus-Gesamtleistung | `sensor.e3dc_power_consumption_house` |
| Pelletpreis (live) | `sensor.pelletpreis_bayern` (€/t) |
| Netzstrompreis (live, optional) | `sensor.electricity_price` (€/kWh); Fallback `input_number.heizung_einsparung_netzpreis_ct` |
| DWD weather entity (fallback) | `weather.dwd_station` | map to your local DWD integration entity |
| Außentemperatur (COP-Kennlinie) | `sensor.aussen_temperatur`, Fallback `sensor.heizkreis_eingange_aussentemperatur` |

Neue Parameter (`input_number`): `heizung_einsparung_heat_per_kg` (kWh Wärme je kg Pellets, Default 5,2 — kalibriert aus ETA-Wärmezähler vs. Pelletverbrauch mehrjährig), `heizung_einsparung_einspeiseverguetung_ct`, `heizung_einsparung_netzpreis_ct`, `heizung_einsparung_feldabschlag`.

Live-Einbindung (auf der eigenen Instanz nicht über HA-`packages:`, sondern über separate Includes):
- `template:`-Block → eigene Datei unter `includes/templates/` (Konvention: `heizung_einsparung.yaml`)
- `input_number:` → eigene Helper (z. B. per UI/Helper statt YAML)
- Integration-Sensoren (`platform: integration`) → anhängen an `includes/sensors.yaml`
- `utility_meter` (daily/monthly/yearly je Quelle) → anhängen an `includes/utility_meter.yaml`

Endergebnis-Sensoren (kg als State, EUR als Attribute `pellet_wert_brutto_eur` / `stromkosten_eur` / `netto_ersparnis_eur`): `sensor.heizung_einsparung_klima_{tag,monat,jahr}`, `sensor.heizung_einsparung_elwa_{tag,monat,jahr}`, `sensor.heizung_einsparung_gesamt_{tag,monat,jahr}`.

Zwischen-Leistungssensoren (Klima-Split PV/Akku/Netz, Klima-Wärme modelliert, ELWA-Split PV/Akku/Netz) haben **keine** `_w`-Suffix-entity_id, obwohl `unique_id` und Kommentare im Package teils `_w` verwenden — HA leitet die entity_id ohne explizite `default_entity_id`-Unterstützung aus dem slugifizierten `name` ab. Tatsächliche IDs: `sensor.heizung_klima_heizleistung`, `sensor.heizung_klima_heizleistung_{pv,akku,netz}`, `sensor.heizung_klima_waermeleistung`, `sensor.heizung_elwa_leistung_{pv,akku,netz}`. Die `source:`-Angaben in `includes/sensors.yaml` und die Templates in `includes/templates/heizung_einsparung.yaml` referenzieren konsistent diese Namen (Fix vom 20.09.2026 nach anfänglichem Mismatch, der alle abgeleiteten kWh-/kg-Werte auf 0 hielt).

## Remap tips

1. Load helpers + templates first and check setpoint sensors in the UI  
2. Test scripts with `heizung_klima_auto` / `heizung_tado_auto` / `heizung_eta_auto` off  
3. Wire one zone (e.g. office climate only), then expand  
4. Adapt the dashboard last
