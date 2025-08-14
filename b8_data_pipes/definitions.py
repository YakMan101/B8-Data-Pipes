"""Dagster definitions for B8 Data Pipes project."""

from datetime import datetime, timedelta

from dagster import Definitions, define_asset_job

from b8_data_pipes.assets.booking_report import booking_report_asset
from b8_data_pipes.schedules import weekly_booking_report_schedule
from b8_data_pipes.resources import DiscordResource, FirebaseResource


weekly_booking_report_job = define_asset_job(
    name="weekly_booking_report",
    selection=[booking_report_asset],
    description="Generate weekly booking report"
)


defs = Definitions(
    assets=[booking_report_asset],
    jobs=[weekly_booking_report_job],
    schedules=[weekly_booking_report_schedule],
    resources={
        "discord": DiscordResource(),
        "firebase": FirebaseResource(),
    },
)
