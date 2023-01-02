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
from typing import Type, Any

from src.jsonschema.converter import TypedConverter
from src.jsonschema.external_package_ref_properties import ExternalPackageRefProperty
from src.jsonschema.json_property import JsonProperty
from src.model.document import Document
from src.model.package import ExternalPackageRef
from src.writer.casing_tools import snake_case_to_camel_case


class ExternalPackageRefConverter(TypedConverter[ExternalPackageRef]):
    def json_property_name(self, external_ref_property: ExternalPackageRefProperty) -> str:
        return snake_case_to_camel_case(external_ref_property.name)

    def _get_property_value(self, external_ref: ExternalPackageRef, external_ref_property: ExternalPackageRefProperty,
                            document: Document = None) -> Any:
        if external_ref_property == ExternalPackageRefProperty.COMMENT:
            return external_ref.comment
        elif external_ref_property == ExternalPackageRefProperty.REFERENCE_CATEGORY:
            return external_ref.category.name
        elif external_ref_property == ExternalPackageRefProperty.REFERENCE_LOCATOR:
            return external_ref.locator
        elif external_ref_property == ExternalPackageRefProperty.REFERENCE_TYPE:
            return external_ref.reference_type

    def get_json_type(self) -> Type[JsonProperty]:
        return ExternalPackageRefProperty

    def get_data_model_type(self) -> Type[ExternalPackageRef]:
        return ExternalPackageRef
