"""Find the target specifications in extracted datasheet text."""

import json
import re


def extract_part_number(text):
    pattern = r"(?:part number|device name)\s*[:#]?\s*([A-Z0-9][A-Z0-9_-]+)"
    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return match.group(1)

    return None


def extract_supply_voltage(text):
    pattern = (
        r"(?:supply voltage|operating voltage|VDD)\s*[:=]?\s*"
        r"([0-9.]+)\s*(mV|V)\s*(?:to|-|–)\s*([0-9.]+)\s*(mV|V)"
    )
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
    pattern = (
        r"(?:operating temperature|temperature range)\s*[:=]?\s*"
        r"(-?[0-9.]+)\s*(?:°?C|C)\s*(?:to|-|–)\s*"
        r"(-?[0-9.]+)\s*(?:°?C|C)"
    )
    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return {
            "min": match.group(1),
            "max": match.group(2),
            "unit": "C",
        }

    return None


def extract_interfaces(text):
    interfaces = []

    i2c_match = re.search(r"\b(I²C|I2C|IIC)\b", text, re.IGNORECASE)
    if i2c_match:
        interfaces.append(i2c_match.group(1))

    spi_match = re.search(r"\b(SPI)\b", text, re.IGNORECASE)
    if spi_match:
        interfaces.append(spi_match.group(1))

    uart_match = re.search(r"\b(UART)\b", text, re.IGNORECASE)
    if uart_match:
        interfaces.append(uart_match.group(1))

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


def extract_fields(text):
    fields = {
        "part_number": extract_part_number(text),
        "supply_voltage": extract_supply_voltage(text),
        "operating_temperature": extract_operating_temperature(text),
        "interfaces": extract_interfaces(text),
        "current_consumption": extract_current_consumption(text),
    }

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
