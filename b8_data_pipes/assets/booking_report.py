"""Asset for generating booking reports."""

import io
import re
from datetime import datetime, timedelta

import pandas as pd
from dagster import asset, AssetExecutionContext

from b8_data_pipes.configs import BookingReportConfig
from b8_data_pipes.resources import FirebaseResource, DiscordResource


def parse_date_string(date_str: str) -> datetime:
    """Parse date string in either YYYY-MM-DD or ISO timestamp format"""

    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    
    if date_pattern.match(date_str):
        return datetime.strptime(date_str, "%Y-%m-%d")
    else:
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))


@asset(
    description="Generate booking report CSV from Firebase data for specified date range",
    group_name="booking_analytics",
)
def booking_report_asset(
    context: AssetExecutionContext,
    config: BookingReportConfig,
    firebase: FirebaseResource,
    discord: DiscordResource,
) -> pd.DataFrame:
    """Generate a DataFrame of bookings within the specified date range"""
    
    if not config.end_date.strip():
        end_timestamp = datetime.now()
    else:
        end_timestamp = parse_date_string(config.end_date)
    
    if not config.start_date.strip():
        start_timestamp = end_timestamp - timedelta(days=7)
    else:
        start_timestamp = parse_date_string(config.start_date)
    
    if end_timestamp < start_timestamp:
        raise ValueError(f"End date ({end_timestamp.strftime('%Y-%m-%d')}) "
                         f"cannot be before start date ({start_timestamp.strftime('%Y-%m-%d')})")

    context.log.info(
        f"Generating booking CSV report from {start_timestamp.strftime('%Y-%m-%d %H:%M:%S')} "
        f"to {end_timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
    )

    bookings = firebase.get_bookings(
        start_date=start_timestamp.isoformat(),
        end_date=end_timestamp.isoformat()
    )

    if not bookings:
        context.log.warning("No bookings found for the specified period")
        discord.send_message(
            f"📊 **Bookings Report**\n"
            f"Period: {start_timestamp.strftime('%Y-%m-%d')} to {end_timestamp.strftime('%Y-%m-%d')}\n"
            f"❌ No bookings found for this period."
        )
        return pd.DataFrame()

    df = pd.DataFrame(bookings)
    if "sessionDate" in df.columns:
        df = df.sort_values("sessionDate")

    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_content = csv_buffer.getvalue()

    discord_success = discord.send_csv_report(
        csv_content=csv_content,
        filename=f"booking_report_{start_timestamp.strftime('%Y%m%d')}_{end_timestamp.strftime('%Y%m%d')}.csv",
        period_start=start_timestamp.strftime('%Y-%m-%d'),
        period_end=end_timestamp.strftime('%Y-%m-%d'),
        total_bookings=len(df),
    )

    if discord_success:
        context.log.info("Successfully sent CSV report to Discord")
    else:
        context.log.error("Failed to send CSV report to Discord")

    context.log.info(f"Generated DataFrame with {len(df)} bookings")
    return df
