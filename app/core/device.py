from user_agents import parse


def parse_device(user_agent: str) -> dict:
    ua = parse(user_agent or "")

    if ua.is_mobile:
        device_type = "Mobile"
    elif ua.is_tablet:
        device_type = "Tablet"
    elif ua.is_pc:
        device_type = "Desktop"
    elif ua.is_bot:
        device_type = "Bot"
    else:
        device_type = "Unknown"

    browser = f"{ua.browser.family} {ua.browser.version_string}".strip()
    os = f"{ua.os.family} {ua.os.version_string}".strip()
    device_name = f"{ua.browser.family} on {ua.os.family}"

    return {
        "browser": browser,
        "os": os,
        "device_type": device_type,
        "device_name": device_name,
    }