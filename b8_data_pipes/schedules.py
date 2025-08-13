"""Schedule for weekly booking report generation."""

from dagster import schedule

from b8_data_pipes.jobs.weekly_booking_report import weekly_booking_report_job


@schedule(
    job=weekly_booking_report_job,
    cron_schedule="0 1 * * 1",  # Every Monday at 1:00 AM
    execution_timezone="UTC",
)
def weekly_booking_report_schedule():
    """Schedule to run the weekly booking report"""
    return {}
