#!/usr/bin/env python3
"""Build and optionally deploy Klima/ELWA Einsparung Grafana dashboard.

Data source: existing HA → InfluxDB 2 (Unraid, bucket hass/autogen).
Queries follow the same InfluxQL style as grafana_eta_modernize.py.
"""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path

UID = "heizung-einsparung"
TITLE = "Heizung Einsparung Klima + ELWA"
DS = {"type": "influxdb", "uid": "sZvsWQjMk"}
FOLDER_UID = "7Le14QjGk"  # Grafana folder "Heizung"


def q_last(entity: str, measurement: str, field: str = "value", days: int = 3650) -> dict:
    return {
        "datasource": DS,
        "query": (
            f'SELECT last("{field}") FROM "{measurement}" '
            f"WHERE \"entity_id\" = '{entity}' AND time > now() - {days}d"
        ),
        "rawQuery": True,
        "refId": "A",
        "resultFormat": "time_series",
    }


def q_mean(entity: str, measurement: str, field: str = "value", alias: str | None = None) -> dict:
    return {
        "datasource": DS,
        "query": (
            f'SELECT mean("{field}") FROM "{measurement}" '
            f"WHERE \"entity_id\" = '{entity}' AND $timeFilter "
            f"GROUP BY time($__interval) fill(null)"
        ),
        "rawQuery": True,
        "refId": "A",
        "resultFormat": "time_series",
        "alias": alias or entity,
    }


def q_mean_multi(
    series: list[tuple[str, str, str, str]],
) -> list[dict]:
    """series: (entity, measurement, field, alias)"""
    out = []
    for i, (entity, measurement, field, alias) in enumerate(series):
        t = q_mean(entity, measurement, field, alias)
        t["refId"] = chr(ord("A") + i)
        out.append(t)
    return out


def row(title: str, panel_id: int, y: int) -> dict:
    return {
        "collapsed": False,
        "gridPos": {"h": 1, "w": 24, "x": 0, "y": y},
        "id": panel_id,
        "panels": [],
        "title": title,
        "type": "row",
    }


def ts_defaults(*, unit: str | None = None, draw_style: str = "line", fill: int = 20) -> dict:
    defaults: dict = {
        "color": {"mode": "palette-classic"},
        "custom": {
            "axisBorderShow": False,
            "axisCenteredZero": False,
            "axisColorMode": "text",
            "axisLabel": "",
            "axisPlacement": "auto",
            "barAlignment": 0,
            "barWidthFactor": 0.6,
            "drawStyle": draw_style,
            "fillOpacity": fill,
            "gradientMode": "opacity" if draw_style == "line" else "none",
            "hideFrom": {"legend": False, "tooltip": False, "viz": False},
            "insertNulls": False,
            "lineInterpolation": "smooth",
            "lineWidth": 2,
            "pointSize": 5,
            "scaleDistribution": {"type": "linear"},
            "showPoints": "never",
            "spanNulls": True,
            "stacking": {"group": "A", "mode": "none"},
            "thresholdsStyle": {"mode": "off"},
        },
        "mappings": [],
        "thresholds": {
            "mode": "absolute",
            "steps": [{"color": "green", "value": None}],
        },
    }
    if unit:
        defaults["unit"] = unit
    return defaults


def ts_options() -> dict:
    return {
        "legend": {
            "calcs": ["mean", "max", "lastNotNull"],
            "displayMode": "table",
            "placement": "bottom",
            "showLegend": True,
        },
        "tooltip": {"hideZeros": False, "mode": "multi", "sort": "desc"},
    }


def stat(
    panel_id: int,
    title: str,
    target: dict,
    grid: dict,
    *,
    unit: str | None = None,
    decimals: int | None = 1,
    color_mode: str = "value",
) -> dict:
    defaults: dict = {
        "color": {"mode": "thresholds"},
        "mappings": [],
        "thresholds": {
            "mode": "absolute",
            "steps": [
                {"color": "blue", "value": None},
                {"color": "green", "value": 0.01},
            ],
        },
    }
    if unit:
        defaults["unit"] = unit
    if decimals is not None:
        defaults["decimals"] = decimals
    return {
        "datasource": DS,
        "fieldConfig": {"defaults": defaults, "overrides": []},
        "gridPos": grid,
        "id": panel_id,
        "options": {
            "colorMode": color_mode,
            "graphMode": "area",
            "justifyMode": "auto",
            "orientation": "auto",
            "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False},
            "showPercentChange": False,
            "textMode": "auto",
            "wideLayout": True,
        },
        "pluginVersion": "12.1.0",
        "targets": [target],
        "title": title,
        "type": "stat",
    }


def timeseries(
    panel_id: int,
    title: str,
    targets: list[dict],
    grid: dict,
    *,
    unit: str | None = None,
    draw_style: str = "line",
    fill: int = 20,
    stack: bool = False,
) -> dict:
    defaults = ts_defaults(unit=unit, draw_style=draw_style, fill=fill)
    if stack:
        defaults["custom"]["stacking"] = {"group": "A", "mode": "normal"}
        defaults["custom"]["fillOpacity"] = 80
    return {
        "datasource": DS,
        "fieldConfig": {"defaults": defaults, "overrides": []},
        "gridPos": grid,
        "id": panel_id,
        "options": ts_options(),
        "pluginVersion": "12.1.0",
        "targets": targets,
        "title": title,
        "type": "timeseries",
    }


def markdown(panel_id: int, content: str, grid: dict) -> dict:
    return {
        "gridPos": grid,
        "id": panel_id,
        "options": {"code": {"language": "markdown", "showLineNumbers": False, "showMiniMap": False}, "content": content, "mode": "markdown"},
        "pluginVersion": "12.1.0",
        "title": "",
        "type": "text",
    }


def build_dashboard() -> dict:
    panels: list[dict] = []
    y = 0

    panels.append(row("Kennzahlen jetzt (Tag / Monat / Jahr)", 100, y))
    y += 1

    # Tag
    panels.append(
        stat(101, "Gesamt Tag kg", q_last("heizung_einsparung_gesamt_tag", "kg"), {"h": 4, "w": 3, "x": 0, "y": y}, unit="masskg")
    )
    panels.append(
        stat(102, "Netto Tag €", q_last("heizung_einsparung_gesamt_tag", "kg", "netto_ersparnis_eur"), {"h": 4, "w": 3, "x": 3, "y": y}, unit="currencyEUR")
    )
    # Monat
    panels.append(
        stat(103, "Gesamt Monat kg", q_last("heizung_einsparung_gesamt_monat", "kg"), {"h": 4, "w": 3, "x": 6, "y": y}, unit="masskg")
    )
    panels.append(
        stat(104, "Netto Monat €", q_last("heizung_einsparung_gesamt_monat", "kg", "netto_ersparnis_eur"), {"h": 4, "w": 3, "x": 9, "y": y}, unit="currencyEUR")
    )
    # Jahr
    panels.append(
        stat(105, "Gesamt Jahr kg", q_last("heizung_einsparung_gesamt_jahr", "kg"), {"h": 4, "w": 3, "x": 12, "y": y}, unit="masskg")
    )
    panels.append(
        stat(106, "Netto Jahr €", q_last("heizung_einsparung_gesamt_jahr", "kg", "netto_ersparnis_eur"), {"h": 4, "w": 3, "x": 15, "y": y}, unit="currencyEUR")
    )
    panels.append(
        stat(107, "Klima Tag kg", q_last("heizung_einsparung_klima_tag", "kg"), {"h": 4, "w": 3, "x": 18, "y": y}, unit="masskg", color_mode="none")
    )
    panels.append(
        stat(108, "ELWA Tag kg", q_last("heizung_einsparung_elwa_tag", "kg"), {"h": 4, "w": 3, "x": 21, "y": y}, unit="masskg", color_mode="none")
    )
    y += 4

    panels.append(
        markdown(
            109,
            "**Quelle:** Home Assistant → InfluxDB 2 Unraid (`hass/autogen`). "
            "Klima-Wärme modelliert (Feld-COP), ELWA = Strom (COP 1). "
            "Stromkosten: PV/Akku = Einspeisevergütung, Netz = Strompreis. "
            "Live-Sensoren ab ~20.09.2026.",
            {"h": 2, "w": 24, "x": 0, "y": y},
        )
    )
    y += 2

    panels.append(row("Kosten & Ertrag", 200, y))
    y += 1
    panels.append(
        timeseries(
            201,
            "Tageswerte: Brutto Pelletwert / Stromkosten / Netto €",
            q_mean_multi(
                [
                    ("heizung_einsparung_gesamt_tag", "kg", "pellet_wert_brutto_eur", "Brutto Pellet €"),
                    ("heizung_einsparung_gesamt_tag", "kg", "stromkosten_eur", "Stromkosten €"),
                    ("heizung_einsparung_gesamt_tag", "kg", "netto_ersparnis_eur", "Netto €"),
                ]
            ),
            {"h": 8, "w": 12, "x": 0, "y": y},
            unit="currencyEUR",
        )
    )
    panels.append(
        timeseries(
            202,
            "Tageswerte: kg Pellets (Klima / ELWA / Gesamt)",
            q_mean_multi(
                [
                    ("heizung_einsparung_klima_tag", "kg", "value", "Klima kg"),
                    ("heizung_einsparung_elwa_tag", "kg", "value", "ELWA kg"),
                    ("heizung_einsparung_gesamt_tag", "kg", "value", "Gesamt kg"),
                ]
            ),
            {"h": 8, "w": 12, "x": 12, "y": y},
            unit="masskg",
        )
    )
    y += 8

    panels.append(row("Leistung & Wärme (Live-Verlauf)", 300, y))
    y += 1
    panels.append(
        timeseries(
            301,
            "Klima Heizstrom nach Quelle (W)",
            q_mean_multi(
                [
                    ("heizung_klima_heizleistung_pv", "W", "value", "PV"),
                    ("heizung_klima_heizleistung_akku", "W", "value", "Akku"),
                    ("heizung_klima_heizleistung_netz", "W", "value", "Netz"),
                ]
            ),
            {"h": 8, "w": 12, "x": 0, "y": y},
            unit="watt",
            draw_style="bars",
            stack=True,
            fill=80,
        )
    )
    panels.append(
        timeseries(
            302,
            "ELWA Leistung nach Quelle (W)",
            q_mean_multi(
                [
                    ("heizung_elwa_leistung_pv", "W", "value", "PV"),
                    ("heizung_elwa_leistung_akku", "W", "value", "Akku"),
                    ("heizung_elwa_leistung_netz", "W", "value", "Netz"),
                ]
            ),
            {"h": 8, "w": 12, "x": 12, "y": y},
            unit="watt",
            draw_style="bars",
            stack=True,
            fill=80,
        )
    )
    y += 8

    panels.append(
        timeseries(
            303,
            "Klima: elektrisch vs. modellierte Wärme (W)",
            q_mean_multi(
                [
                    ("heizung_klima_heizleistung", "W", "value", "Elektrisch"),
                    ("heizung_klima_waermeleistung", "W", "value", "Wärme (COP-Feld)"),
                ]
            ),
            {"h": 7, "w": 12, "x": 0, "y": y},
            unit="watt",
        )
    )
    panels.append(
        timeseries(
            304,
            "Feld-COP Klima",
            [q_mean("heizung_klima_waermeleistung", "W", "cop_feld", "COP Feld")],
            {"h": 7, "w": 6, "x": 12, "y": y},
        )
    )
    panels.append(
        timeseries(
            305,
            "Haus-Stromquellen Anteile",
            q_mean_multi(
                [
                    ("heizung_stromquellen_anteil", "%", "pv_ratio", "PV"),
                    ("heizung_stromquellen_anteil", "%", "akku_ratio", "Akku"),
                    ("heizung_stromquellen_anteil", "%", "netz_ratio", "Netz"),
                ]
            ),
            {"h": 7, "w": 6, "x": 18, "y": y},
            unit="percentunit",
            stack=True,
            fill=80,
        )
    )
    y += 7

    panels.append(row("Energie kWh (Tages-/Monatszähler)", 400, y))
    y += 1
    panels.append(
        timeseries(
            401,
            "Klima Wärme kWh Tag + Stromquellen Tag",
            q_mean_multi(
                [
                    ("heizung_klima_waerme_kwh_tag", "kWh", "value", "Wärme Tag"),
                    ("heizung_klima_pv_kwh_tag", "kWh", "value", "PV Tag"),
                    ("heizung_klima_akku_kwh_tag", "kWh", "value", "Akku Tag"),
                    ("heizung_klima_netz_kwh_tag", "kWh", "value", "Netz Tag"),
                ]
            ),
            {"h": 8, "w": 12, "x": 0, "y": y},
            unit="kwath",
        )
    )
    panels.append(
        timeseries(
            402,
            "ELWA kWh Tag nach Quelle",
            q_mean_multi(
                [
                    ("heizung_elwa_pv_kwh_tag", "kWh", "value", "PV Tag"),
                    ("heizung_elwa_akku_kwh_tag", "kWh", "value", "Akku Tag"),
                    ("heizung_elwa_netz_kwh_tag", "kWh", "value", "Netz Tag"),
                ]
            ),
            {"h": 8, "w": 12, "x": 12, "y": y},
            unit="kwath",
            stack=True,
            fill=70,
        )
    )
    y += 8

    panels.append(
        timeseries(
            403,
            "Monatszähler kg (Gesamt / Klima / ELWA)",
            q_mean_multi(
                [
                    ("heizung_einsparung_gesamt_monat", "kg", "value", "Gesamt Monat"),
                    ("heizung_einsparung_klima_monat", "kg", "value", "Klima Monat"),
                    ("heizung_einsparung_elwa_monat", "kg", "value", "ELWA Monat"),
                ]
            ),
            {"h": 8, "w": 12, "x": 0, "y": y},
            unit="masskg",
        )
    )
    panels.append(
        timeseries(
            404,
            "Jahreszähler kg + Netto €",
            q_mean_multi(
                [
                    ("heizung_einsparung_gesamt_jahr", "kg", "value", "Gesamt kg Jahr"),
                    ("heizung_einsparung_gesamt_jahr", "kg", "netto_ersparnis_eur", "Netto € Jahr"),
                ]
            ),
            {"h": 8, "w": 12, "x": 12, "y": y},
        )
    )
    y += 8

    panels.append(row("Betrieb / Kontext", 500, y))
    y += 1
    panels.append(
        timeseries(
            501,
            "Klima Heizbetrieb (0/1)",
            # HA writes binary_sensors without UoM under measurement = full entity_id
            [q_mean("heizung_klima_heizbetrieb", "binary_sensor.heizung_klima_heizbetrieb", "value", "Heizbetrieb")],
            {"h": 5, "w": 12, "x": 0, "y": y},
            draw_style="bars",
            fill=80,
        )
    )
    panels.append(
        timeseries(
            502,
            "Integrationszähler (kumuliert kWh)",
            q_mean_multi(
                [
                    ("heizung_klima_waerme", "kWh", "value", "Klima Wärme"),
                    ("heizung_klima_pv_energie", "kWh", "value", "Klima PV"),
                    ("heizung_elwa_pv_energie", "kWh", "value", "ELWA PV"),
                    ("heizung_elwa_netz_energie", "kWh", "value", "ELWA Netz"),
                ]
            ),
            {"h": 5, "w": 12, "x": 12, "y": y},
            unit="kwath",
        )
    )

    return {
        "annotations": {
            "list": [
                {
                    "builtIn": 1,
                    "datasource": {"type": "grafana", "uid": "-- Grafana --"},
                    "enable": True,
                    "hide": True,
                    "iconColor": "rgba(0, 211, 255, 1)",
                    "name": "Annotations & Alerts",
                    "type": "dashboard",
                }
            ]
        },
        "editable": True,
        "fiscalYearStartMonth": 0,
        "graphTooltip": 1,
        "links": [
            {
                "asDropdown": False,
                "icon": "dashboard",
                "includeVars": False,
                "keepTime": True,
                "tags": ["heizung"],
                "targetBlank": False,
                "title": "Heizung-Dashboards",
                "type": "dashboards",
            }
        ],
        "liveNow": False,
        "panels": panels,
        "refresh": "30s",
        "schemaVersion": 42,
        "style": "dark",
        "tags": ["heizung", "einsparung", "klima", "elwa", "pellets", "home-assistant"],
        "templating": {"list": []},
        "time": {"from": "now-7d", "to": "now"},
        "timepicker": {},
        "timezone": "browser",
        "title": TITLE,
        "uid": UID,
        "version": 1,
    }


def api_payload(dashboard: dict) -> dict:
    body = deepcopy(dashboard)
    body.pop("id", None)
    return {
        "dashboard": body,
        "folderUid": FOLDER_UID,
        "message": "Deploy Einsparung Klima/ELWA dashboard",
        "overwrite": True,
    }


def deploy_via_local_api(dashboard: dict, grafana_url: str = "http://127.0.0.1:3000") -> None:
    """POST to Grafana HTTP API (auth proxy: X-WEBAUTH-USER).

    Grafana 13+ stores dashboards in unified storage; raw grafana.db inserts
    are invisible in search/UI. Always use the API for creates/updates.
    """
    import urllib.error
    import urllib.request

    payload = json.dumps(api_payload(dashboard)).encode()
    req = urllib.request.Request(
        f"{grafana_url.rstrip('/')}/api/dashboards/db",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "X-WEBAUTH-USER": "admin",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"Grafana API error {exc.code}: {exc.read().decode()[:500]}") from exc
    print(f"API deploy ok: uid={result.get('uid')} url={result.get('url')} status={result.get('status')}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name("grafana_einsparung_dashboard.json"),
    )
    parser.add_argument(
        "--deploy-api",
        action="store_true",
        help="POST dashboard to local Grafana API (run inside addon or with port-forward)",
    )
    parser.add_argument(
        "--grafana-url",
        default="http://127.0.0.1:3000",
        help="Grafana base URL for --deploy-api",
    )
    parser.add_argument(
        "--write-api-payload",
        type=Path,
        help="Write API import payload JSON (for docker exec curl)",
    )
    args = parser.parse_args()

    dashboard = build_dashboard()
    args.output.write_text(json.dumps(dashboard, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {args.output}")

    if args.write_api_payload:
        args.write_api_payload.write_text(json.dumps(api_payload(dashboard)) + "\n")
        print(f"Wrote API payload {args.write_api_payload}")

    if args.deploy_api:
        deploy_via_local_api(dashboard, args.grafana_url)


if __name__ == "__main__":
    main()
