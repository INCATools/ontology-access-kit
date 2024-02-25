"""Constants for use across OAK."""

import pystow

__all__ = [
    "OAKLIB_MODULE",
]

OAKLIB_MODULE = pystow.module("oaklib")

NODE_RENAME = "NodeRename"
CLASS_CREATION = "ClassCreation"
NODE_CREATION = "NodeCreation"
NODE_DELETION = "NodeDeletion"
NODE_TEXT_DEFINITION_CHANGE = "NodeTextDefinitionChange"
NEW_TEXT_DEFINITION = "NewTextDefinition"
