"""Dagster definitions for B8 Data Pipes project."""

from dagster import Definitions

from b8_data_pipes.assets.booking_report import booking_report_asset
from b8_data_pipes.jobs.weekly_booking_report import weekly_booking_report_job
from b8_data_pipes.schedules import weekly_booking_report_schedule
from b8_data_pipes.resources import DiscordResource, FirebaseResource


defs = Definitions(
    assets=[booking_report_asset],
    jobs=[weekly_booking_report_job],
    schedules=[weekly_booking_report_schedule],
    resources={
        "discord": DiscordResource(),
        "firebase": FirebaseResource(),
    },
)
