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

from src.datetime_conversions import datetime_to_iso_string
from src.jsonschema.annotation_properties import AnnotationProperty
from src.jsonschema.converter import TypedConverter
from src.jsonschema.json_property import JsonProperty
from src.model.annotation import Annotation
from src.model.document import Document
from src.writer.casing_tools import snake_case_to_camel_case


class AnnotationConverter(TypedConverter[Annotation]):
    def json_property_name(self, annotation_property: AnnotationProperty) -> str:
        return snake_case_to_camel_case(annotation_property.name)

    def _get_property_value(self, annotation: Annotation, annotation_property: AnnotationProperty,
                            document: Document = None) -> Any:
        if annotation_property == AnnotationProperty.ANNOTATION_DATE:
            return datetime_to_iso_string(annotation.annotation_date)
        elif annotation_property == AnnotationProperty.ANNOTATION_TYPE:
            return annotation.annotation_type.name
        elif annotation_property == AnnotationProperty.ANNOTATOR:
            return annotation.annotator.to_serialized_string()
        elif annotation_property == AnnotationProperty.COMMENT:
            return annotation.annotation_comment

    def get_json_type(self) -> Type[JsonProperty]:
        return AnnotationProperty

    def get_data_model_type(self) -> Type[Annotation]:
        return Annotation
