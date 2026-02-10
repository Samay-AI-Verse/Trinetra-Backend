"""
Test script for sending notifications to Trinetra officers
Supports both normal and emergency messages
"""

import requests
import json
from datetime import datetime

# Backend URL - Change this if deployed
BASE_URL = "https://overprosperous-aviana-nontextually.ngrok-free.dev"


def send_normal_notification(title: str, message: str, target_officer_ids: list = None):
    """
    Send a normal notification to officers

    Args:
        title: Notification title
        message: Notification message
        target_officer_ids: List of officer IDs (None = broadcast to all)
    """
    url = f"{BASE_URL}/api/notifications/send"

    payload = {
        "notification_type": "normal",
        "title": title,
        "message": message,
        "target_officer_ids": target_officer_ids,
        "source_officer_id": None,
        "lat": None,
        "lng": None,
        "metadata": {
            "sent_via": "test_script",
            "timestamp": datetime.now().isoformat(),
        },
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        print(f"✅ Normal notification sent successfully!")
        print(f"   Notification ID: {result.get('notification_id')}")
        print(f"   Title: {title}")
        print(f"   Message: {message}")
        print(
            f"   Target: {'All officers' if not target_officer_ids else target_officer_ids}"
        )
        return result
    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending notification: {e}")
        return None


def send_emergency_notification(
    title: str,
    message: str,
    lat: float,
    lng: float,
    source_officer_id: str = "TEST_OFFICER",
    target_officer_ids: list = None,
):
    """
    Send an emergency notification to officers

    Args:
        title: Emergency title
        message: Emergency message
        lat: Latitude of emergency
        lng: Longitude of emergency
        source_officer_id: ID of officer sending emergency
        target_officer_ids: List of officer IDs (None = broadcast to all)
    """
    url = f"{BASE_URL}/api/notifications/send"

    payload = {
        "notification_type": "emergency",
        "title": title,
        "message": message,
        "target_officer_ids": target_officer_ids,
        "source_officer_id": source_officer_id,
        "lat": lat,
        "lng": lng,
        "metadata": {
            "sent_via": "test_script",
            "timestamp": datetime.now().isoformat(),
            "emergency_level": "high",
        },
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        print(f"🚨 Emergency notification sent successfully!")
        print(f"   Notification ID: {result.get('notification_id')}")
        print(f"   Title: {title}")
        print(f"   Message: {message}")
        print(f"   Location: ({lat}, {lng})")
        print(f"   Source: {source_officer_id}")
        print(
            f"   Target: {'All officers' if not target_officer_ids else target_officer_ids}"
        )
        return result
    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending emergency: {e}")
        return None


def get_all_officer_ids():
    """Fetch all registered officer IDs from the backend"""
    url = f"{BASE_URL}/api/officers/ids"

    try:
        response = requests.get(url)
        response.raise_for_status()
        result = response.json()
        officer_ids = result.get("officer_ids", [])
        print(f"📋 Found {len(officer_ids)} registered officers:")
        for oid in officer_ids:
            print(f"   - {oid}")
        return officer_ids
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching officer IDs: {e}")
        return []


def interactive_menu():
    """Interactive menu for testing notifications"""
    print("\n" + "=" * 60)
    print("🔔 TRINETRA NOTIFICATION TEST SCRIPT")
    print("=" * 60)

    while True:
        print("\n📱 Select an option:")
        print("1. Send Normal Notification (Broadcast to all)")
        print("2. Send Normal Notification (Specific officers)")
        print("3. Send Emergency Alert (Broadcast to all)")
        print("4. Send Emergency Alert (Specific officers)")
        print("5. View all registered officer IDs")
        print("6. Quick Test - Send sample notifications")
        print("0. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            title = input("Enter notification title: ").strip()
            message = input("Enter notification message: ").strip()
            send_normal_notification(title, message)

        elif choice == "2":
            title = input("Enter notification title: ").strip()
            message = input("Enter notification message: ").strip()
            officer_ids = (
                input("Enter officer IDs (comma-separated): ").strip().split(",")
            )
            officer_ids = [oid.strip() for oid in officer_ids if oid.strip()]
            send_normal_notification(title, message, officer_ids)

        elif choice == "3":
            title = input("Enter emergency title: ").strip()
            message = input("Enter emergency message: ").strip()
            lat = float(input("Enter latitude: ").strip())
            lng = float(input("Enter longitude: ").strip())
            send_emergency_notification(title, message, lat, lng)

        elif choice == "4":
            title = input("Enter emergency title: ").strip()
            message = input("Enter emergency message: ").strip()
            lat = float(input("Enter latitude: ").strip())
            lng = float(input("Enter longitude: ").strip())
            officer_ids = (
                input("Enter officer IDs (comma-separated): ").strip().split(",")
            )
            officer_ids = [oid.strip() for oid in officer_ids if oid.strip()]
            send_emergency_notification(
                title, message, lat, lng, target_officer_ids=officer_ids
            )

        elif choice == "5":
            get_all_officer_ids()

        elif choice == "6":
            print("\n🧪 Running quick tests...")
            print("\n1️⃣ Sending normal notification...")
            send_normal_notification(
                "Shift Update",
                "Your shift starts in 30 minutes. Please report to station.",
            )

            print("\n2️⃣ Sending emergency alert...")
            send_emergency_notification(
                "🚨 OFFICER IN DISTRESS",
                "Officer needs immediate backup at location!",
                lat=28.6139,  # Example: New Delhi coordinates
                lng=77.2090,
                source_officer_id="TEST_OFFICER_001",
            )

            print("\n✅ Quick test completed!")

        elif choice == "0":
            print("\n👋 Exiting... Stay safe!")
            break

        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    # Check if backend is running
    try:
        response = requests.get(f"{BASE_URL}/api/officers/ids", timeout=3)
        print(f"✅ Backend is running at {BASE_URL}")
    except requests.exceptions.RequestException:
        print(f"❌ Cannot connect to backend at {BASE_URL}")
        print("   Please make sure the backend is running (python main.py)")
        print("   Or update BASE_URL in this script if deployed elsewhere")
        exit(1)

    interactive_menu()
