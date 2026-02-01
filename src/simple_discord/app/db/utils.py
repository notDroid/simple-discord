from boto3.dynamodb.types import TypeSerializer, TypeDeserializer

serializer = TypeSerializer()
deserializer = TypeDeserializer()

def to_dynamo_json(python_dict: dict) -> dict:
    return {k: serializer.serialize(v) for k, v in python_dict.items()}

def from_dynamo_json(dynamo_dict: dict) -> dict:
    return {k: deserializer.deserialize(v) for k, v in dynamo_dict.items()}