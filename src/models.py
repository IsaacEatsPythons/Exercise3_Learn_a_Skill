from typing import Optional
from pydantic import BaseModel


class RangeSpec(BaseModel):
    min: Optional[float] = None
    max: Optional[float] = None
    unit: str


class CurrentSpec(BaseModel):
    typical: Optional[float] = None
    unit: str


class ComponentSpec(BaseModel):
    part_number: Optional[str] = None
    supply_voltage: Optional[RangeSpec] = None
    operating_temperature: Optional[RangeSpec] = None
    interfaces: list[str] = []
    current_consumption: Optional[CurrentSpec] = None


if __name__ == "__main__":
    example_component = ComponentSpec(
        part_number="EXAMPLE123",
        supply_voltage=RangeSpec(min=1.8, max=3.6, unit="V"),
        operating_temperature=RangeSpec(min=-40, max=85, unit="C"),
        interfaces=["I2C", "SPI"],
        current_consumption=CurrentSpec(typical=0.5, unit="mA"),
    )

    print(example_component.model_dump_json(indent=2))
