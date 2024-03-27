""" Application type to Handle all importing of various file types, such
    as sbsar, sbs and sbsprs files."""

import uuid
import json
import jsonschema

from .instance import ConnectorInstance
from .application import BaseApplication


SCHEMA = {
    "type": "object",
    "properties": {
        "path": {"type": "string"},
        "name": {"type": "string"},
        "uuid": {"type": "string"},
        "type": {"type": "string"},
        "takeOwnership": {"type": "boolean"},
    },
    "required": ["path", "uuid"],
}


class MessageSchema:
    """ Message schema data structure """
    def __init__(self, path, asset_type="sbsar"):
        self.path = path
        self.name = ""
        self.uuid = str(uuid.uuid4())
        self.type = asset_type
        self.takeOwnership = False

    def to_json(self):
        """ Returns a json string of this object"""
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True,
                          indent=4)

    def is_valid(self):
        """ Returns a boolean if the json is valid """
        try:
            json_filler = json.loads(self.to_json())
            jsonschema.validate(instance=json_filler, schema=SCHEMA)
            return True
        except jsonschema.exceptions.ValidationError as err:
            print("Json error: {}".format(err))

        return False


class AssetImportApplication(BaseApplication):
    """ Handles all importing and exporting of sbsar, sbs and sbsprs files """
    _IMPORT_ASSET_UUID = uuid.UUID('91e3dfbc-80b8-4b1a-92d5-63ec09ac641a')

    """ Handles all importing and exporting of sbsar, sbs and sbsprs files """
    _IMPORT_SBSAR_UUID = uuid.UUID('72538d04-276f-4254-a45b-d3654f705477')

    @classmethod
    def get_callback_list(cls):
        """ Returns the callback list for substance file imports """
        return [(cls._IMPORT_ASSET_UUID, cls.recv_import_asset)]\
            + super().get_callback_list()

    @classmethod
    def recv_import_asset(cls, context, message_type, message):
        """ Import the asset and parse the schema"""
        json.loads(message)
        print(message)

    @classmethod
    def send_import_asset(cls, context, message):
        """ Send an sbs/sbsar file to another application """
        schema_instance = MessageSchema(message)
        if schema_instance.is_valid() is False:
            print("Faild to send connector message")
            return

        print("\n")
        print(schema_instance.to_json())
        print("\n")

        ConnectorInstance.write_message(
            context, cls._IMPORT_ASSET_UUID, schema_instance.to_json())

    @classmethod
    def original_send_to(cls, context, message):
        """ Sends the path string instead the new schema format """
        ConnectorInstance.write_message(context, cls._IMPORT_SBSAR_UUID, message)

    @classmethod
    def get_feature_ids(cls):
        """ Method called at application registration to return the feature
         id set for the application to build the connection context """
        return [
            cls._IMPORT_ASSET_UUID,
            cls._IMPORT_SBSAR_UUID
        ]
