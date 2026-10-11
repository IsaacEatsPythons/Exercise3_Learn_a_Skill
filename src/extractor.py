"""Find the target specifications in extracted datasheet text."""

import json
import re


def extract_part_number(text):
    """Extract a component part number using common datasheet formats."""

    patterns = [
        r"(?:part number|device name)\s*[:#]?\s*([A-Z0-9][A-Z0-9_-]+)",
        # Generic inclusions for things like the BME280 
        r"\b([A-Z]{2,}[A-Z0-9]*\d{2,}[A-Z0-9_-]*)\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def extract_supply_voltage(text):
    """Extract a supply-voltage range from multiple datasheet formats."""

    patterns = [
        # Original/simple format
        r"(?:supply voltage|operating voltage|VDD)\s*[:=]?\s*"
        r"([0-9.]+)\s*(mV|V)\s*(?:to|-|–)\s*"
        r"([0-9.]+)\s*(mV|V)",

        # adding the flexible format allows text between lagle+values 
        r"(?:supply voltage|operating voltage|VDD)[^\n]{0,100}?"
        r"([0-9.]+)\s*(mV|V)\s*(?:to|-|–|…|\.\.)\s*"
        r"([0-9.]+)\s*(mV|V)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return {
                "min": match.group(1),
                "min_unit": match.group(2),
                "max": match.group(3),
                "max_unit": match.group(4),
            }

    return None


def extract_operating_temperature(text):
    """Extract operating-temperature ranges from multiple formats."""

    patterns = [
        # Original
        r"(?:operating temperature|temperature range)\s*[:=]?\s*"
        r"(-?[0-9.]+)\s*(?:°?C|C)\s*(?:to|-|–)\s*"
        r"(-?[0-9.]+)\s*(?:°?C|C)",

        # more flexibility to allow additional set betide ht range
        r"(?:operating temperature|temperature range)[^\n]{0,100}?"
        r"(-?[0-9.]+)\s*(?:°?C|C)\s*(?:to|-|–|…|\.\.)\s*"
        r"(-?[0-9.]+)\s*(?:°?C|C)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return {
                "min": match.group(1),
                "max": match.group(2),
                "unit": "C",
            }

    return None


def extract_interfaces(text):
    """Detect and normalize supported communication interfaces."""
    interfaces = []

    # normalizeto one representation
    if re.search(r"\b(I²C|I2C|IIC)\b", text, re.IGNORECASE):
        interfaces.append("I2C")

    if re.search(r"\bSPI\b", text, re.IGNORECASE):
        interfaces.append("SPI")

    if re.search(r"\bUART\b", text, re.IGNORECASE):
        interfaces.append("UART")

    return interfaces


def extract_current_consumption(text):
    pattern = (
        r"(?:typical current|current consumption)\s*[:=]?\s*"
        r"(?:typical\s*)?([0-9.]+)\s*(µA|uA|mA|A)"
    )
    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return {
            "typical": match.group(1),
            "unit": match.group(2),
        }

    return None

def calculate_completeness(fields):
    """Calculate the percentage of target specifications successfully extracted."""
    total_fields = 5
    found_fields = 0
    if fields["part_number"] is not None:
        found_fields += 1
    if fields["supply_voltage"] is not None:
        found_fields += 1
    if fields["operating_temperature"] is not None:
        found_fields += 1
    if fields["interfaces"]:
        found_fields += 1
    if fields["current_consumption"] is not None:
        found_fields += 1
    return round((found_fields / total_fields) * 100, 1)


def find_missing_fields(fields):
    """Return specifications that the parser could not identify."""
    missing = []
    if fields["part_number"] is None:
        missing.append("part_number")
    if fields["supply_voltage"] is None:
        missing.append("supply_voltage")
    if fields["operating_temperature"] is None:
        missing.append("operating_temperature")
    if not fields["interfaces"]:
        missing.append("interfaces")
    if fields["current_consumption"] is None:
        missing.append("current_consumption")

    return missing


def extract_fields(text):
    """Extract specifications and evaluate the completeness of the result."""
    fields = {
        "part_number": extract_part_number(text),
        "supply_voltage": extract_supply_voltage(text),
        "operating_temperature": extract_operating_temperature(text),
        "interfaces": extract_interfaces(text),
        "current_consumption": extract_current_consumption(text),
    }
    # evaluate whether enough information was actually taken out
    fields["extraction_completeness"] = calculate_completeness(fields)
    fields["missing_fields"] = find_missing_fields(fields)

    return fields

if __name__ == "__main__":
    sample_text = """
    Part Number: EXAMPLE123
    Supply Voltage: 1800 mV to 3.6 V
    Operating Temperature: -40 C to 85 C
    Interfaces: I²C and SPI
    Typical Current: 4000 µA
    """

    extracted_fields = extract_fields(sample_text)
    print(json.dumps(extracted_fields, indent=2))

