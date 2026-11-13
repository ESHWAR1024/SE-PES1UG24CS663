def parse_ride_duration(text):
    """Convert HH:MM to minutes; return 0 for invalid input."""
    if not isinstance(text, str):
        return 0

    parts = text.strip().split(":")
    if len(parts) != 2:
        return 0

    hours_text, minutes_text = parts
    if not hours_text.isdecimal() or not minutes_text.isdecimal():
        return 0

    try:
        hours = int(hours_text)
        minutes = int(minutes_text)
    except ValueError:
        return 0

    if minutes >= 60:
        return 0

    return hours * 60 + minutes
def format_station_code(code):
    """Format a station code as ZONE-NUMBER; return an empty string if invalid."""
    if not isinstance(code, str):
        return ""

    code = code.strip().upper()
    if not code:
        return ""

    return code[0] + "-" + code[1:]

def parse_ride_log(line):
    """Parse type,minutes,subscriber; return a safe default if invalid."""
    default = ("", 0, False)

    if not isinstance(line, str):
        return default

    parts = line.split(",")
    if len(parts) != 3:
        return default

    bike_type, minutes_text, subscriber = (part.strip() for part in parts)

    try:
        minutes = int(minutes_text)
    except ValueError:
        return default

    if minutes < 0:
        return default

    return bike_type, minutes, subscriber.lower() == "yes"

def main():
    print("==== Running parse_ride_duration ====")
    value = input("Enter a ride duration as HH:MM (e.g. 01:15): ")
    print("Duration in minutes:", parse_ride_duration(value))

    print("\n==== Running format_station_code ====")
    value = input("Enter a station code (e.g. a12): ")
    print("Formatted station code:", format_station_code(value))

    print("\n==== Running parse_ride_log ====")
    value = input("Enter a ride log line as type,minutes,subscriber (e.g. electric,45,yes): ")
    print("Parsed ride log:", parse_ride_log(value))

if __name__ == "__main__":
    main()
