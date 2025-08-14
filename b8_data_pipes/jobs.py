"""Job definitions for B8 Data Pipes."""

from dagster import define_asset_job

from b8_data_pipes.assets.booking_report import booking_report_asset


weekly_bookings_report_job = define_asset_job(
    name="weekly_bookings_report",
    selection=[booking_report_asset],
    description="Generate weekly booking report"
)
