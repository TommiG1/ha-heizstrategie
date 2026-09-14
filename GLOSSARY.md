# Glossary (German labels in the package)

The packages keep German option strings and many entity ID prefixes from the reference install. Use this map when reading YAML, the dashboard, or logs.

## Heating modes (`input_select.heizung_modus`)

| German (in YAML) | English | Meaning |
|------------------|---------|---------|
| `Aus` | Off | Strategy idle; failsafe turns climate/tado off and leaves boiler/circuit safe |
| `Übergang` | Shoulder season / transition | Mild weather: climate-first, avoid pellet starts when possible |
| `Winter` | Winter | Colder season: same stack, more willingness to use buffer/circuit/boiler when needed |

Do not rename these option strings unless you also update every template/script that compares against them.

## Rooms and zones

| German / ID fragment | English |
|----------------------|---------|
| `wohnen` / Wohnen | Living |
| `esszimmer` / Esszimmer | Dining |
| `buero` / Büro | Office |
| `schlafen` / Schlafen | Bedroom |
| `schlafen_a` / Schlafen A | Bedroom A (alias) |
| `schlafen_b` / Schlafen B | Bedroom B (alias) |
| `schlafen_c` / Schlafen C | Bedroom C (alias) |
| `bad` / Bad | Bath |
| `spielzimmer` / Spielzimmer | Playroom |
| `schlafzimmer` | Bedroom (often the tado zone paired with bedroom B) |

## People and away

| German / ID | English |
|-------------|---------|
| `person.person_a` | Person A (house + office away in the reference) |
| `person.person_b` | Person B |
| `person.person_c` | Person C |
| Away Haus | House away (all three not `home`) |
| Away Büro | Office away (person A not `home`) |
| `heizung_away` | House away mode select (`Auto` / `Away` / `Home`) |
| `heizung_away_buero` | Office away mode select |

Person and bedroom names are aliases on purpose. Map them to your real `person.*` and `climate.*` entities in `ENTITY_MAP.md`.

## Other common words in IDs and UI

| German | English |
|--------|---------|
| Heizung | Heating |
| Klima | Climate / AC / heat pump indoor unit |
| Soll | Setpoint |
| Fenster | Window |
| Sperre | Lockout (no heat after airing) |
| Puffer | Buffer tank |
| Heizstab / ELWA | Immersion heater |
| Heizkreis | Heating circuit |
| Kessel | Boiler |
| Schimmel | Mold |
| Lüften | Ventilate |
| Feiertag | Public holiday (treated like weekend) |
| Ventile | Valves (TRVs) |
