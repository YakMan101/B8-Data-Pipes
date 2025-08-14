"""Configuration classes for B8 Data Pipes."""

from typing import Optional

from dagster import Config


class BookingReportConfig(Config):
    start_date: str
    end_date: str
