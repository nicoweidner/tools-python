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

from src.jsonschema.extracted_licensing_info_converter import ExtractedLicensingInfoConverter
from src.jsonschema.extracted_licensing_info_properties import ExtractedLicensingInfoProperty
from src.model.extracted_licensing_info import ExtractedLicensingInfo


@pytest.fixture
def converter() -> ExtractedLicensingInfoConverter:
    return ExtractedLicensingInfoConverter()


@pytest.mark.parametrize("extracted_licensing_info_property,expected",
                         [(ExtractedLicensingInfoProperty.LICENSE_ID, "licenseId"),
                          (ExtractedLicensingInfoProperty.EXTRACTED_TEXT, "extractedText"),
                          (ExtractedLicensingInfoProperty.NAME, "name"),
                          (ExtractedLicensingInfoProperty.COMMENT, "comment"),
                          (ExtractedLicensingInfoProperty.SEE_ALSOS, "seeAlsos")])
def test_json_property_names(converter: ExtractedLicensingInfoConverter,
                             extracted_licensing_info_property: ExtractedLicensingInfoProperty, expected: str):
    assert converter.json_property_name(extracted_licensing_info_property) == expected


def test_json_type(converter: ExtractedLicensingInfoConverter):
    assert converter.get_json_type() == ExtractedLicensingInfoProperty


def test_data_model_type(converter: ExtractedLicensingInfoConverter):
    assert converter.get_data_model_type() == ExtractedLicensingInfo


def test_successful_conversion(converter: ExtractedLicensingInfoConverter):
    extracted_licensing_info = ExtractedLicensingInfo(license_id="licenseId", extracted_text="Extracted text",
                                                      license_name="license name",
                                                      cross_references=["reference1", "reference2"], comment="comment")

    converted_dict = converter.convert(extracted_licensing_info)

    assert converted_dict[converter.json_property_name(ExtractedLicensingInfoProperty.LICENSE_ID)] == "licenseId"
    assert converted_dict[
               converter.json_property_name(ExtractedLicensingInfoProperty.EXTRACTED_TEXT)] == "Extracted text"
    assert converted_dict[converter.json_property_name(ExtractedLicensingInfoProperty.NAME)] == "license name"
    assert converted_dict[converter.json_property_name(ExtractedLicensingInfoProperty.SEE_ALSOS)] == ["reference1",
                                                                                                      "reference2"]
    assert converted_dict[converter.json_property_name(ExtractedLicensingInfoProperty.COMMENT)] == "comment"
