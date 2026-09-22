# Electronic Datasheet Parser

Reads a component datasheet PDF and puts a few specifications into JSON.

## What It Extracts

The program looks for these fields:

- Part number
- Supply-voltage range
- Operating-temperature range
- I2C, SPI, and UART interfaces
- Typical current consumption

If the program cannot find a field, it uses `null` instead of inventing a
value.

## Setup

This project uses Python 3, PyMuPDF, and Pydantic. Install them with:

```bash
python3 -m pip install --user PyMuPDF
python3 -m pip install --user pydantic
```

## Run the Program

Put a text-based datasheet PDF in the `datasheets/` folder. Then run:

```bash
python3 -m src.main datasheets/id003278.pdf
```

The program prints the extracted JSON in the terminal and saves it to:

```text
output/id003278.json
```

The output name comes from the PDF name. For example,
`datasheets/sensor.pdf` creates `output/sensor.json`.

## Example Output

```json
{
  "part_number": null,
  "supply_voltage": {
    "min": "1.8",
    "min_unit": "V",
    "max": "3.6",
    "max_unit": "V"
  },
  "operating_temperature": null,
  "interfaces": [
    "SPI"
  ],
  "current_consumption": null
}
```

The values stay in the units written by the datasheet. For example, `1800 mV`
is not converted to `1.8 V`.
