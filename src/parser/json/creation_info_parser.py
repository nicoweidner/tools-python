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
from typing import Dict

from typeguard import typechecked

from src.model.annotation import Annotation
from src.model.document import CreationInfo
from src.parser.json.dict_parsing_functions import parse_required_property, parse_optional_property
from src.parser.logger import Logger


class CreationInfoParser:
    parent_logger: Logger
    # Used to keep track of errors that occurred inside this parser
    auxiliary_logger: Logger

    def __init__(self, logger: Logger):
        self.parent_logger = logger
        self.auxiliary_logger = Logger()

    def parse_creation_info(self, doc_dict: Dict) -> CreationInfo:
        spdx_version: str = parse_required_property(doc_dict, "spdxVersion", self.auxiliary_logger)
        spdx_id: str = parse_required_property(doc_dict, "SPDXID", self.auxiliary_logger)
        name: str = parse_required_property(doc_dict, "name", self.auxiliary_logger)
        document_namespace: str = parse_required_property(doc_dict, "documentNamespace", self.auxiliary_logger)
        creation_info_dict: Dict = parse_required_property(doc_dict, "creationInfo", self.auxiliary_logger)

        # There are nested required properties. If creationInfo is not set, we cannot continue parsing.
        if creation_info_dict is None:
            self.parent_logger.append_all(self.auxiliary_logger.get_errors())
            self.raise_accumulated_errors()

        creators = parse_required_property(creation_info_dict, "creators", self.auxiliary_logger)
        created = parse_required_property(creation_info_dict, "created", self.auxiliary_logger)

        self.verify_required_properties()
        try:
            creation_info = CreationInfo(spdx_version=spdx_version, spdx_id=spdx_id, name=name,
                                     document_namespace=document_namespace, creators=creators, created=created)
        except ContructorTypeError as err:
            self.parent_logger.append_all(err.get_messages())
            raise ValueError("Boo!")

        creation_info.creator_comment = parse_optional_property(creation_info_dict, "comment")
        creation_info.data_license = parse_optional_property(doc_dict, "dataLicense")
        creation_info.external_document_refs = parse_optional_property(doc_dict, "externalDocumentRefs", [])
        creation_info.license_list_version = parse_optional_property(creation_info_dict, "licenseListVersion")
        creation_info.document_comment = parse_optional_property(doc_dict, "comment")
        return creation_info

    def verify_required_properties(self):
        if self.auxiliary_logger.has_errors():
            self.parent_logger.append_all(self.auxiliary_logger.get_errors())
            self.raise_accumulated_errors()

    def raise_accumulated_errors(self):
        raise ValueError(
            f"Cannot create CreationInfo instance. Missing required properties:\n"
            f"{self.auxiliary_logger.get_errors()}")


@typechecked
def typechecked_function(first_arg: str, second_arg: int) -> int:
    print(locals())
    return 1


if __name__ == "__main__":
    typechecked_function("1", 2)
