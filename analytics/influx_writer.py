import os
from datetime import datetime, timezone

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxWriter:
    def __init__(self) -> None:
        self.bucket = os.getenv("INFLUXDB_BUCKET", "comasa")
        self.org = os.getenv("INFLUXDB_ORG", "comasa")
        self.client = InfluxDBClient(
            url=os.getenv("INFLUXDB_URL", "http://localhost:8086"),
            token=os.getenv("INFLUXDB_ADMIN_TOKEN", "comasa-demo-token"),
            org=self.org,
        )
        self.api = self.client.write_api(write_options=SYNCHRONOUS)

    def write_anomaly(self, anomaly: dict) -> None:
        point = (
            Point("anomaly_event")
            .tag("type", anomaly["type"])
            .tag("severity", anomaly["severity"])
            .tag("equipment", anomaly["equipment"])
            .field("score", float(anomaly["score"]))
            .field("message", anomaly["message"])
            .field("probable_cause", anomaly["probable_cause"])
            .field("impacted_kpis", anomaly["impacted_kpis"])
            .field("anomaly_id", anomaly["anomaly_id"])
            .time(_now(), WritePrecision.NS)
        )
        self.api.write(bucket=self.bucket, org=self.org, record=point)

    def write_recommendation(self, recommendation: dict) -> None:
        point = (
            Point("maintenance_recommendation")
            .tag("severity", recommendation["severity"])
            .tag("equipment", recommendation["equipment"])
            .field("recommendation_id", recommendation["recommendation_id"])
            .field("anomaly_id", recommendation["anomaly_id"])
            .field("probable_cause", recommendation["probable_cause"])
            .field("suggested_action", recommendation["suggested_action"])
            .field("due_before", recommendation["due_before"])
            .field("due_minutes", float(recommendation["due_minutes"]))
            .field("expected_impact", recommendation["expected_impact"])
            .field("impacted_kpis", recommendation["impacted_kpis"])
            .field("ack_status", recommendation["ack_status"])
            .time(_now(), WritePrecision.NS)
        )
        self.api.write(bucket=self.bucket, org=self.org, record=point)

    def write_kpis(self, kpis: list[dict]) -> None:
        points = [
            Point("kpi").tag("kpi", item["name"]).tag("unit", item["unit"]).field("value", float(item["value"])).time(_now(), WritePrecision.NS)
            for item in kpis
        ]
        if points:
            self.api.write(bucket=self.bucket, org=self.org, record=points)

    def write_asset_risk(self, risks: list[dict]) -> None:
        points = [
            Point("asset_risk")
            .tag("equipment", item["equipment"])
            .tag("area", item["area"])
            .tag("status", item["status"])
            .tag("severity", item["severity"])
            .tag("probable_anomaly", item["probable_anomaly"])
            .field("risk_score", float(item["risk_score"]))
            .field("dominant_signal", item["dominant_signal"])
            .field("risk_reason", item["risk_reason"])
            .field("suggested_action", item["suggested_action"])
            .field("expected_impact", item["expected_impact"])
            .field("due_minutes", float(item["due_minutes"]))
            .time(_now(), WritePrecision.NS)
            for item in risks
        ]
        if points:
            self.api.write(bucket=self.bucket, org=self.org, record=points)

    def write_segment_status(self, statuses: list[dict]) -> None:
        tag_keys = (
            "segment_id",
            "from_node",
            "to_node",
            "fluid",
            "unit_generator",
            "operating_condition",
            "variable",
            "tag",
            "unit",
            "source",
            "source_sheet",
            "stage",
            "quality",
            "status",
            "impacted_problem",
        )
        points = []
        for item in statuses:
            point = Point("segment_status")
            for key in tag_keys:
                point = point.tag(key, str(item.get(key, "")))
            point = (
                point.field("risk_score", float(item["risk_score"]))
                .field("reason", item["reason"])
                .field("recommendation_cause", item["recommendation_cause"])
                .field("recommendation_link", item["recommendation_link"])
                .field("cost_efficiency_impact", item["cost_efficiency_impact"])
                .field("value", float(item["value"]))
                .field("confidence", float(item["confidence"]))
                .time(_now(), WritePrecision.NS)
            )
            points.append(point)
        if points:
            self.api.write(bucket=self.bucket, org=self.org, record=points)


def _now() -> datetime:
    return datetime.now(timezone.utc)
