"""Job definition for weekly booking report generation."""

from dagster import define_asset_job

from b8_data_pipes.assets.booking_report import booking_report_asset


weekly_booking_report_job = define_asset_job(
    name="weekly_booking_report",
    selection=[booking_report_asset],
    description="Generate and send weekly booking report CSV to Discord"
)
