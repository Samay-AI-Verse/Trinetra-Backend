import requests
import json
import time

# CONFIGURATION
# ------------------------------------------------------------------
# If running locally with ngrok, put your ngrok URL here
# Example: BASE_URL = "https://your-ngrok-id.ngrok-free.app"
# If testing against live render, use the render URL
BASE_URL = "https://overprosperous-aviana-nontextually.ngrok-free.dev"
# ------------------------------------------------------------------


def send_emergency_alert():
    print("\n🚨 Sending EMERGENCY TEST Alert...")
    target_id = input(
        "Enter Target Officer ID (Press Enter to Broadcast All): "
    ).strip()

    endpoint = f"{BASE_URL}/api/test/emergency"

    payload = {
        "officer_id": "CONTROL_ROOM_TEST",
        "lat": 28.7041,  # Example: Delhi
        "lng": 77.1025,
        "emergency_type": "high_emergency",
        "message": "Officer In Distress! Simulation Test.",
    }

    if target_id:
        payload["target_officers"] = [target_id]
        print(f"🎯 Targeting specific officer: {target_id}")
    else:
        print("🌍 Broadcasting to ALL (if no nearby logic applies)")

    try:
        response = requests.post(endpoint, json=payload)
        if response.status_code == 200:
            print("✅ Emergency Alert Sent Successfully!")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"❌ Failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Error: {e}")


def send_normal_notification():
    print("\n📨 Sending NORMAL Notification...")
    target_id = input(
        "Enter Target Officer ID (Press Enter to Broadcast All): "
    ).strip()

    endpoint = f"{BASE_URL}/api/notifications/send"

    payload = {
        "notification_type": "normal",  # "normal" or "emergency"
        "title": "Team Briefing",
        "message": "All officers please assemble at the main gate at 1400 hours.",
        "target_officer_ids": [target_id] if target_id else None,
        "metadata": {"priority": "high", "department": "traffic"},
    }

    if target_id:
        print(f"🎯 Targeting specific officer: {target_id}")

    try:
        response = requests.post(endpoint, json=payload)
        if response.status_code == 200:
            print("✅ Notification Sent Successfully!")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"❌ Failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("--- TRINETRA NOTIFICATION TESTER ---")
    print(f"Target URL: {BASE_URL}")
    print("1. Send Emergency Alert (Simulate Officer SOS)")
    print("2. Send Standard Notification (Control Room Broadcast)")

    choice = input("\nEnter choice (1 or 2): ").strip()

    if choice == "1":
        send_emergency_alert()
    elif choice == "2":
        send_normal_notification()
    else:
        print("Invalid choice")
