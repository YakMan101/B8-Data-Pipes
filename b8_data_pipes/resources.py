"""Discord resource for sending messages to Discord channels."""

from os import getenv, environ
from typing import Dict, Any, List

import firebase_admin
from firebase_admin import credentials, firestore
import requests
from dagster import ConfigurableResource
from dotenv import load_dotenv

load_dotenv()


class DiscordResource(ConfigurableResource):
    """Resource for sending messages to Discord via webhook"""

    

    def get_webhook_url(self) -> str:
        """Retrieve the Discord webhook URL from environment variables."""

        webhook_url = getenv("DISCORD_WEBHOOK_URL", "")
        if not webhook_url:
            raise ValueError("DISCORD_WEBHOOK_URL not found in environment variables")
        
        return webhook_url

    def send_message(self, content: str, embeds: list = []) -> bool:
        """Send a message to Discord channel"""
        
        webhook_url = self.get_webhook_url()

        if not webhook_url:
            raise ValueError("DISCORD_WEBHOOK_URL not found in environment variables")

        payload = {
            "content": content,
            "embeds": embeds,
        }

        response = requests.post(webhook_url, json=payload)

        return response.status_code == 204

    def send_csv_report(
        self,
        csv_content: str,
        filename: str,
        period_start: str,
        period_end: str,
        total_bookings: int,
    ) -> bool:
        """Send a CSV file with booking data to Discord"""

        webhook_url = self.get_webhook_url()

        if not webhook_url:
            raise ValueError("DISCORD_WEBHOOK_URL not found in environment variables")

        message_content = (
            f"📊 **Weekly Bookings Report**\n"
            f"📅 Period: {period_start} to {period_end}\n"
            f"📈 Total Bookings: {total_bookings}\n"
            f"📎 CSV file attached below"
        )

        files = {"file": (filename, csv_content, "text/csv")}

        data = {"content": message_content}

        response = requests.post(webhook_url, data=data, files=files)

        return response.status_code == 200


class FirebaseResource(ConfigurableResource):
    """Resource for connecting to Firebase Firestore"""

    def setup_for_execution(self, context) -> None:
        """Initialize Firebase connection"""

        if not firebase_admin._apps:
            cred_dict = {
                "type": "service_account",
                "project_id": getenv("FIREBASE_PROJECT_ID"),
                "private_key_id": getenv("FIREBASE_PRIVATE_KEY_ID"),
                "private_key": getenv("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n"),
                "client_email": getenv("FIREBASE_CLIENT_EMAIL"),
                "client_id": getenv("FIREBASE_CLIENT_ID"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": getenv("FIREBASE_CLIENT_CERT_URL"),
            }

            if getenv("USE_EMULATORS") == "true":
                environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
                cred = credentials.ApplicationDefault()
            else:
                cred = credentials.Certificate(cred_dict)

            firebase_admin.initialize_app(cred)

        self._db = firestore.client()

    def get_bookings(
        self, start_date: str = "", end_date: str = ""
    ) -> List[Dict[str, Any]]:
        """Fetch bookings from Firestore"""

        bookings_ref = self._db.collection("bookings")

        query = bookings_ref
        if start_date:
            query = query.where("sessionDate", ">=", start_date)
        if end_date:
            query = query.where("sessionDate", "<=", end_date)

        docs = query.stream()
        bookings = []

        for doc in docs:
            booking_data = doc.to_dict()
            booking_data["booking_uid"] = doc.id
            bookings.append(booking_data)

        return bookings
