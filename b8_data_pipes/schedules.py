"""Schedule for weekly booking report generation."""

from datetime import timedelta

from dagster import schedule

from b8_data_pipes.jobs import weekly_bookings_report_job


@schedule(
    job=weekly_bookings_report_job,
    cron_schedule="0 1 * * 1",
    execution_timezone="UTC",
)
def weekly_bookings_report_schedule(context):
    """Schedule to run the weekly booking report"""
    
    scheduled_date = context.scheduled_execution_time
    end_date = scheduled_date.replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = end_date - timedelta(days=7)
    
    return {
        "run_config": {
            "ops": {
                "booking_report_asset": {
                    "config": {
                        "start_date": start_date.strftime("%Y-%m-%d"),
                        "end_date": end_date.strftime("%Y-%m-%d")
                    }
                }
            }
        },
        "tags": {
            "scheduled": "true",
            "report_type": "weekly_booking",
            "source": "automated_schedule",
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }
    }
