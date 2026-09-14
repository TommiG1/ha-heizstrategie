# Installation

## 1. Package folder

Copy files into Home Assistant, for example:

```text
config/
  packages/
    heizung_helpers.yaml
    heizung_templates.yaml
    heizung_scripts.yaml
    heizung_automations.yaml
    schimmel_helpers.yaml      # optional, recommended with heating
    schimmel_templates.yaml
  dashboards/
    heizung.yaml          # optional
```

## 2. Enable packages

In `configuration.yaml` (if not already present):

```yaml
homeassistant:
  packages: !include_dir_named packages
```

If you already load packages another way, drop the `heizung_*.yaml` / `schimmel_*.yaml` files there.

## 3. Avoid conflicts

If you already define the same keys under `script:`, `automation:`, or `input_*:`:

- keep heating only in packages, or
- remove duplicates from older includes

Duplicate `unique_id` values on template sensors will block a clean start.

## 4. Remap entities

Before the first restart, work through `ENTITY_MAP.md`. Unknown entity IDs cause template errors or dead automations.

## 5. Check and load

Developer tools → Check configuration, then restart Home Assistant (templates/packages often need a full restart, not only a reload).

Suggested order after start:

1. Mode `Aus`, all `*_auto` flags off  
2. Inspect setpoint sensors and window binaries  
3. Exercise one climate entity manually and watch the override timer  
4. Enable auto flags one by one  

## 6. Dashboard (optional)

Load `dashboards/heizung.yaml` as a YAML dashboard or paste it into a UI dashboard. Pull card dependencies (e.g. `mushroom`, `card-mod`) via HACS if needed.

## Rollback

Remove or rename the package files, check config, restart. Helpers often keep state in the entity registry; clean up there if needed.
