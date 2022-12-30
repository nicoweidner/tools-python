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
import pytest

from src.jsonschema.relationship_converter import RelationshipConverter
from src.jsonschema.relationship_properties import RelationshipProperty
from src.model.relationship import Relationship, RelationshipType


@pytest.fixture
def converter() -> RelationshipConverter:
    return RelationshipConverter()


@pytest.mark.parametrize("relationship_property,expected",
                         [(RelationshipProperty.SPDX_ELEMENT_ID, "spdxElementId"),
                          (RelationshipProperty.COMMENT, "comment"),
                          (RelationshipProperty.RELATED_SPDX_ELEMENT, "relatedSpdxElement"),
                          (RelationshipProperty.RELATIONSHIP_TYPE, "relationshipType")])
def test_json_property_names(converter: RelationshipConverter, relationship_property: RelationshipProperty,
                             expected: str):
    assert converter.json_property_name(relationship_property) == expected


def test_json_type(converter: RelationshipConverter):
    assert converter.get_json_type() == RelationshipProperty


def test_data_model_type(converter: RelationshipConverter):
    assert converter.get_data_model_type() == Relationship


def test_successful_conversion(converter: RelationshipConverter):
    relationship = Relationship("spdxElementId", RelationshipType.COPY_OF, "relatedElementId", "comment")

    converted_dict = converter.convert(relationship)

    assert converted_dict == {
        converter.json_property_name(RelationshipProperty.SPDX_ELEMENT_ID): "spdxElementId",
        converter.json_property_name(RelationshipProperty.COMMENT): "comment",
        converter.json_property_name(RelationshipProperty.RELATED_SPDX_ELEMENT): "relatedElementId",
        converter.json_property_name(RelationshipProperty.RELATIONSHIP_TYPE): "COPY_OF"
    }