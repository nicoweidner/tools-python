#  Copyright (c) 2022 spdx contributors
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from typing import Type

from src.jsonschema.checksum_properties import ChecksumProperty
from src.jsonschema.converter import TypedConverter
from src.jsonschema.json_property import JsonProperty
from src.model.checksum import Checksum, ChecksumAlgorithm
from src.writer.casing_tools import snake_case_to_camel_case


class ChecksumConverter(TypedConverter):

    def get_data_model_type(self) -> Type[Checksum]:
        return Checksum

    def get_json_type(self) -> Type[JsonProperty]:
        return ChecksumProperty

    def json_property_name(self, checksum_property: ChecksumProperty) -> str:
        return snake_case_to_camel_case(checksum_property.name)

    def get_property_value(self, checksum: Checksum, checksum_property: ChecksumProperty) -> str:
        if checksum_property == ChecksumProperty.ALGORITHM:
            return algorithm_to_json_string(checksum.algorithm)
        elif checksum_property == ChecksumProperty.CHECKSUM_VALUE:
            return checksum.value


def algorithm_to_json_string(algorithm: ChecksumAlgorithm) -> str:
    name_with_dash: str = algorithm.name.replace("_", "-")
    if "BLAKE2B" in name_with_dash:
        return name_with_dash.replace("BLAKE2B", "BLAKE2b")
    return name_with_dash