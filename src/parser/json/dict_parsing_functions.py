from typing import Dict, Any

from src.parser.logger import Logger


def parse_required_property(source: Dict, property_name: str, logger: Logger) -> Any:
    property_value = source.get(property_name)
    if property_value is None:
        logger.append(f"Required property {property_name} not specified!")
    return property_value


def parse_optional_property(source: Dict, property_name: str, default: Any = None) -> Any:
    property_value = source.get(property_name)
    return property_value or default
