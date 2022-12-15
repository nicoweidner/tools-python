# Copyright (c) 2022 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
from json import JSONDecodeError
from typing import List

from src.model.annotation import Annotation
from src.model.document import Document, CreationInfo
from src.model.extracted_licensing_info import ExtractedLicensingInfo
from src.model.file import File
from src.model.package import Package
from src.model.relationship import Relationship
from src.model.snippet import Snippet
from src.parser.json.annotation_parser import AnnotationParser
from src.parser.json.creation_info_parser import CreationInfoParser
from src.parser.error import SPDXParsingError
from src.parser.json.dict_parsing_functions import raise_parsing_error_if_logger_has_messages, \
    construct_or_raise_parsing_error, parse_field_or_log_error
from src.parser.json.extracted_licensing_info_parser import ExtractedLicensingInfoParser
from src.parser.json.file_parser import FileParser
from src.parser.logger import Logger
from src.parser.json.package_parser import PackageParser
from src.parser.json.relationship_parser import RelationshipParser
from src.parser.json.snippet_parser import SnippetParser


class JsonParser:
    logger: Logger
    creation_info_parser: CreationInfoParser
    package_parser: PackageParser
    file_parser: FileParser
    snippet_parser: SnippetParser
    extracted_licensing_info_parser: ExtractedLicensingInfoParser
    relationship_parser: RelationshipParser
    annotation_parser: AnnotationParser

    def __init__(self):
        self.logger = Logger()
        self.creation_info_parser = CreationInfoParser()
        self.package_parser = PackageParser()
        self.file_parser = FileParser()
        self.snippet_parser = SnippetParser()
        self.extracted_licensing_info_parser = ExtractedLicensingInfoParser()
        self.relationship_parser = RelationshipParser()
        self.annotation_parser = AnnotationParser()

    def parse(self, filename: str) -> Document:
        try:
            with open(filename) as file:
                input_doc_as_dict = json.load(file)
        except FileNotFoundError:
            self.logger.append(f"File {filename} not found.")
            raise SPDXParsingError(self.logger.get_messages())
        except JSONDecodeError:
            self.logger.append(f"File {filename} is not a valid JSON file.")
            raise SPDXParsingError(self.logger.get_messages())

        creation_info: CreationInfo = parse_field_or_log_error(logger=self.logger, field=input_doc_as_dict,
                                                               parsing_method=self.creation_info_parser.parse_creation_info)

        packages: List[Package] = parse_field_or_log_error(logger=self.logger, field=input_doc_as_dict.get("packages"),
                                                           parsing_method=self.package_parser.parse_packages,
                                                           optional=True)

        files: List[File] = parse_field_or_log_error(logger=self.logger, field=input_doc_as_dict.get("files"),
                                                     parsing_method=self.file_parser.parse_files, optional=True)

        annotations: List[Annotation] = parse_field_or_log_error(logger=self.logger, field=input_doc_as_dict,
                                                                 parsing_method=self.annotation_parser.parse_all_annotations,
                                                                 optional=True)
        snippets: List[Snippet] = parse_field_or_log_error(logger=self.logger, field=input_doc_as_dict.get("snippets"),
                                                           parsing_method=self.snippet_parser.parse_snippets,
                                                           optional=True)
        relationships: List[Relationship] = parse_field_or_log_error(logger=self.logger, field=input_doc_as_dict,
                                                                     parsing_method=self.relationship_parser.parse_all_relationships,
                                                                     optional=True)
        extracted_licensing_info: List[ExtractedLicensingInfo] = parse_field_or_log_error(logger=self.logger,
                                                                                          field=input_doc_as_dict.get("hasExtractedLicensingInfos"),
                                                                                          parsing_method=self.extracted_licensing_info_parser.parse_extracted_licensing_infos,
                                                                                          optional=True)

        raise_parsing_error_if_logger_has_messages(self.logger)

        document = construct_or_raise_parsing_error(Document, dict(creation_info=creation_info, packages=packages,
                                                                   files=files,
                                                                   annotations=annotations,
                                                                   snippets=snippets, relationships=relationships,
                                                                   extracted_licensing_info=extracted_licensing_info))

        return document