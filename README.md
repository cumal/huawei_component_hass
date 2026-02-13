# Huawei Router Service Sync

A custom component for Home Assistant to integrate with Huawei LTE routers. This integration allows you to monitor device status, signal strength, and DHCP settings, as well as configure DNS servers and reboot the router directly from Home Assistant.

## Features

*   **Sensors**:
    *   Device Information (Name, Software Version)
    *   DHCP Settings (IP Address, Netmask, Range)
    *   DNS Settings (Current Primary & Secondary DNS)
    *   Signal Strength (RSSI)
    *   Monitoring Status (Connection Status)
*   **Configuration**:
    *   Text entities to view and update **Primary DNS** and **Secondary DNS**.
*   **Controls**:
    *   Button to **Reboot** the router.
*   **Services**:
    *   `huawei_service_sync.get_info`: Fetches router information and displays it in a persistent notification.

## Installation

1.  Copy the `huawei_service_sync` folder to your Home Assistant `custom_components` directory.
2.  Restart Home Assistant.

## Configuration

This integration supports configuration via the Home Assistant UI.

1.  Go to **Settings** > **Devices & Services**.
2.  Click **Add Integration**.
3.  Search for **Huawei Router Service**.
4.  Enter the following details:
    *   **URL**: The URL of your router (e.g., `http://192.168.8.1`).
    *   **Username**: Your router's login username (usually `admin`).
    *   **Password**: Your router's login password.

## Usage

### Entities

Once configured, the integration will create a device named "Huawei Router" with the following entities:

*   **Sensors**:
    *   `sensor.huawei_router`
    *   `sensor.router_dhcp_settings`
    *   `sensor.router_dns_settings`
    *   `sensor.router_signal`
    *   `sensor.router_monitoring_status`
*   **Text (DNS Configuration)**:
    *   `text.primary_dns`
    *   `text.secondary_dns`
    *   *Changing these values will update the router's DHCP settings immediately.*
*   **Button**:
    *   `button.reboot_router`

### Services

You can call the service `huawei_service_sync.get_info` from Developer Tools or automations to receive a notification with the current device name and software version.

## Dependencies

This component relies on the `huawei-lte-api` library.

---
*Disclaimer: This is a custom component and is not officially supported by Huawei.*