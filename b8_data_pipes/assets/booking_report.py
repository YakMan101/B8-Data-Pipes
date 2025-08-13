"""Asset for generating weekly booking reports."""

import io
from datetime import datetime, timedelta
from typing import Dict, Any

import pandas as pd
from dagster import asset, AssetExecutionContext

from b8_data_pipes.resources import DiscordResource, FirebaseResource


@asset(
    description="Generate weekly booking report CSV from Firebase data",
    group_name="booking_analytics",
)
def booking_report_asset(
    context: AssetExecutionContext, firebase: FirebaseResource, discord: DiscordResource
) -> Dict[str, Any]:
    """Generate a CSV report of all bookings from the last week."""

    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    context.log.info(
        f"Generating booking CSV report from {start_date.date()} to {end_date.date()}"
    )

    bookings = firebase.get_bookings(
        start_date=start_date.isoformat(), end_date=end_date.isoformat()
    )

    if not bookings:
        context.log.warning("No bookings found for the specified period")

        discord.send_message(
            f"📊 **Weekly Booking Report**\n"
            f"Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}\n"
            f"❌ No bookings found for this period."
        )
        return {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "total_bookings": 0,
            "csv_generated": False,
        }

    df = pd.DataFrame(bookings)

    if "sessionDate" in df.columns:
        df = df.sort_values("sessionDate")

    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_content = csv_buffer.getvalue()

    total_bookings = len(df)
    context.log.info(f"Generated CSV with {total_bookings} bookings")

    discord_success = discord.send_csv_report(
        csv_content=csv_content,
        filename=f"booking_report_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
        period_start=start_date.strftime("%Y-%m-%d"),
        period_end=end_date.strftime("%Y-%m-%d"),
        total_bookings=total_bookings,
    )

    if discord_success:
        context.log.info("Successfully sent CSV report to Discord")
    else:
        context.log.error("Failed to send CSV report to Discord")

    return {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "total_bookings": total_bookings,
        "csv_generated": True,
        "discord_sent": discord_success,
        "generated_at": datetime.now().isoformat(),
    }
