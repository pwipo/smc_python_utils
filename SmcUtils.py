"""
created by Nikolay V. Ulyanov (ulianownv@mail.ru)
http://www.smcsystem.ru
"""
import base64

import SMCApi
from enum import Enum
from typing import List, Optional


def isNumber(message):
    # type: (SMCApi.IMessage) -> bool
    return message is not None and (
            SMCApi.ValueType.BYTE == message.getType() or SMCApi.ValueType.SHORT == message.getType() or SMCApi.ValueType.INTEGER == message.getType() or
            SMCApi.ValueType.LONG == message.getType() or SMCApi.ValueType.FLOAT == message.getType() or SMCApi.ValueType.DOUBLE == message.getType() or
            SMCApi.ValueType.BIG_INTEGER == message.getType() or SMCApi.ValueType.BIG_DECIMAL == message.getType())


def isString(message):
    # type: (SMCApi.IMessage) -> bool
    return message is not None and SMCApi.ValueType.STRING == message.getType()


def isBytes(message):
    # type: (SMCApi.IMessage) -> bool
    return message is not None and SMCApi.ValueType.BYTES == message.getType()


def getNumber(message):
    # type: (SMCApi.IMessage) -> Optional[int or long or float]
    if isNumber(message):
        return message.getValue()
    else:
        None


def getString(message):
    # type: (SMCApi.IMessage) -> Optional[str]
    if isString(message):
        return message.getValue()
    else:
        None


def getBytes(message):
    # type: (SMCApi.IMessage) -> Optional[bytes]
    if isBytes(message):
        return message.getValue()
    else:
        None


def toString(message):
    # type: (SMCApi.IMessage) -> Optional[str]
    if message is None:
        return None
    if message.getType() == SMCApi.ValueType.STRING:
        return message.getValue()
    elif message.getType() == SMCApi.ValueType.BYTES:
        return base64.b64encode(message.getValue())
    else:
        return str(message.getValue())


def hasErrorsInAction(action):
    # type: (SMCApi.IAction) -> bool
    if action is None:
        return False
    return len(action.getMessages()) > 0 and any(
        message == SMCApi.MessageType.MESSAGE_ERROR_TYPE or message == SMCApi.MessageType.MESSAGE_ACTION_ERROR for message in action.getMessages())


def hasDataInAction(action):
    # type: (SMCApi.IAction) -> bool
    if action is None:
        return False
    return len(action.getMessages()) > 0 and any(message == SMCApi.MessageType.MESSAGE_DATA for message in action.getMessages())


def hasErrors(command):
    # type: (SMCApi.ICommand) -> bool
    if command is None:
        return False
    return len(command.getActions()) > 0 and any(not hasErrorsInAction(action) for action in command.getActions())


def hasData(command):
    # type: (SMCApi.ICommand) -> bool
    if command is None:
        return False
    return len(command.getActions()) > 0 and any(not hasDataInAction(action) for action in command.getActions())


# class ObjectType(Enum):
#     __order__ = 'OBJECT_ARRAY OBJECT_ELEMENT OBJECT_ELEMENT_SIMPLE VALUE_ANY STRING BYTE SHORT INTEGER LONG FLOAT DOUBLE BIG_INTEGER BIG_DECIMAL BYTES'
#     OBJECT_ARRAY = 0
#     OBJECT_ELEMENT = 1
#     OBJECT_ELEMENT_SIMPLE = 2
#     VALUE_ANY = 3
#     STRING = 4
#     BYTE = 5
#     SHORT = 6
#     INTEGER = 7
#     LONG = 8
#     FLOAT = 9
#     DOUBLE = 10
#     BIG_INTEGER = 11
#     BIG_DECIMAL = 12
#     BYTES = 13
ObjectType = Enum('OBJECT_ARRAY', 'OBJECT_ELEMENT', 'OBJECT_ELEMENT_SIMPLE', 'VALUE_ANY', 'STRING', 'BYTE', 'SHORT', 'INTEGER', 'LONG', 'FLOAT',
                  'DOUBLE', 'BIG_INTEGER', 'BIG_DECIMAL', 'BYTES')
ObjectType.OBJECT_ARRAY.value = 0
ObjectType.OBJECT_ELEMENT.value = 1
ObjectType.OBJECT_ELEMENT_SIMPLE.value = 2
ObjectType.VALUE_ANY.value = 3
ObjectType.STRING.value = 4
ObjectType.BYTE.value = 5
ObjectType.SHORT.value = 6
ObjectType.INTEGER.value = 7
ObjectType.LONG.value = 8
ObjectType.FLOAT.value = 9
ObjectType.DOUBLE.value = 10
ObjectType.BIG_INTEGER.value = 11
ObjectType.BIG_DECIMAL.value = 12
ObjectType.BYTES.value = 13

ObjectTypePrivate = Enum('OBJECT_ARRAY', 'OBJECT_ELEMENT', 'OBJECT_ELEMENT_SIMPLE', 'VALUE_ANY', 'STRING', 'BYTE', 'SHORT', 'INTEGER', 'LONG',
                         'FLOAT',
                         'DOUBLE', 'BIG_INTEGER', 'BIG_DECIMAL', 'BYTES', 'OBJECT_ELEMENT_OPTIMIZED', 'OBJECT_ELEMENT_SIMPLE_OPTIMIZED')
ObjectTypePrivate.OBJECT_ARRAY.value = 0
ObjectTypePrivate.OBJECT_ELEMENT.value = 1
ObjectTypePrivate.OBJECT_ELEMENT_SIMPLE.value = 2
ObjectTypePrivate.VALUE_ANY.value = 3
ObjectTypePrivate.STRING.value = 4
ObjectTypePrivate.BYTE.value = 5
ObjectTypePrivate.SHORT.value = 6
ObjectTypePrivate.INTEGER.value = 7
ObjectTypePrivate.LONG.value = 8
ObjectTypePrivate.FLOAT.value = 9
ObjectTypePrivate.DOUBLE.value = 10
ObjectTypePrivate.BIG_INTEGER.value = 11
ObjectTypePrivate.BIG_DECIMAL.value = 12
ObjectTypePrivate.BYTES.value = 13
ObjectTypePrivate.OBJECT_ELEMENT_OPTIMIZED.value = 14
ObjectTypePrivate.OBJECT_ELEMENT_SIMPLE_OPTIMIZED.value = 15


class ObjectField(object):
    def __init__(self, name, value, type=None):
        # type: (str, object) -> None
        self.name = name
        self.type = type
        self.value = value
        self.setValue(value)

    def setValue(self, value):
        # type: (object) -> None
        if value is None:
            raise ValueError("value is None")
        self.value = value
        valueType = type(value)
        if valueType is ObjectArray:
            self.type = ObjectType.OBJECT_ARRAY
        elif valueType is ObjectElement:
            if value.isSimple():
                self.type = ObjectType.OBJECT_ELEMENT_SIMPLE
            else:
                self.type = ObjectType.OBJECT_ELEMENT
        elif valueType is SMCApi.IValue:
            self.type = ObjectType._values[ObjectType._keys.index(str(value.getType()))]
        elif valueType is str or valueType is unicode:
            self.type = ObjectType.STRING
        elif valueType is bytearray:
            self.type = ObjectType.BYTES
        elif valueType is int:
            self.type = ObjectType.INTEGER
        elif valueType is long:
            self.type = ObjectType.LONG
        elif valueType is float:
            self.type = ObjectType.DOUBLE
        else:
            doubleValueFunc = getattr(value, "doubleValue", None)
            if callable(doubleValueFunc):
                self.type = ObjectType.DOUBLE
                self.value = doubleValueFunc()
            else:
                raise ValueError("wrong type {}".format(valueType))

    def isSimple(self):
        # type: () -> bool
        return ObjectType.OBJECT_ARRAY != self.type and ObjectType.OBJECT_ELEMENT != self.type and ObjectType.OBJECT_ELEMENT_SIMPLE != self.type


class ObjectElement(object):
    def __init__(self, fields=None):
        # type: (List[ObjectField]) -> None
        if fields is not None:
            self.fields = list(fields)
        else:
            self.fields = []

    def isSimple(self):
        # type: () -> bool
        isSimple = True
        for field in self.fields:
            if not field.isSimple():
                isSimple = False
                break
        return isSimple

    def findField(self, name):
        # type: (str) -> Optional[ObjectField]
        for f in self.fields:
            if f.name == name:
                return f
        return None


class ObjectArray(object):
    def __init__(self, type=ObjectType.OBJECT_ELEMENT, objects=None):
        # type: (ObjectType, List[object]) -> None
        self.type = type
        self.objects = []
        if objects is not None:
            for obj in objects:
                self.add(obj)

    def check(self, obj):
        # type: (object) -> None
        if obj is None:
            raise ValueError("obj is None")
        if self.type == ObjectType.OBJECT_ARRAY:
            if type(obj) is not ObjectArray:
                raise ValueError("wrong obj type")
        elif self.type == ObjectType.OBJECT_ELEMENT:
            if type(obj) is not ObjectElement:
                raise ValueError("wrong obj type")
        elif self.type == ObjectType.OBJECT_ELEMENT_SIMPLE:
            if type(obj) is not ObjectElement:
                raise ValueError("wrong obj type")
            if not obj.isSimple():
                raise ValueError("wrong obj type")
        elif self.type == ObjectType.STRING:
            if not isinstance(obj, basestring):
                raise ValueError("wrong obj type")
        elif self.type == ObjectType.BYTES:
            if type(obj) is not bytearray:
                raise ValueError("wrong obj type")
        elif self.type == ObjectType.INTEGER:
            if type(obj) is not int:
                raise ValueError("wrong obj type")
        elif self.type == ObjectType.LONG:
            if type(obj) is not long:
                raise ValueError("wrong obj type")
        elif self.type == ObjectType.DOUBLE:
            if type(obj) is not float:
                raise ValueError("wrong obj type")

    def add(self, obj):
        # type: (object) -> None
        self.check(obj)
        self.objects.append(obj)

    def checkType(self, newType, typeForCheck):
        # type: (ObjectType, ObjectType) -> ObjectType
        return newType is not None and newType != typeForCheck if None else typeForCheck

    def isSameFields(self):
        # type: () -> bool
        isSame = True
        fieldNames = None
        fieldTypes = None
        for obj in self.objects:
            if fieldNames is None or fieldTypes is None:
                fieldNames = []
                fieldTypes = []
                for field in obj.fields:
                    fieldNames.append(field.name)
                    fieldTypes.append(field.type)
            else:
                if len(fieldNames) != len(obj.fields):
                    isSame = False
                    break
                sameFields = True
                for i in range(len(fieldNames)):
                    if fieldNames[i] != obj.fields[i].name:
                        sameFields = False
                        break
                    if fieldTypes[i] != obj.fields[i].type:
                        sameFields = False
                        break
                if not sameFields:
                    isSame = False
                    break
        return isSame

    def updateType(self):
        # type: () -> ObjectArray
        if self.type == ObjectType.OBJECT_ELEMENT and len(self.objects) > 1:
            isSimple = True
            fieldNames = None
            for obj in self.objects:
                if fieldNames is None:
                    fieldNames = []
                    for field in obj.fields:
                        fieldNames.append(field.name)
                    if not obj.isSimple():
                        isSimple = False
                        break
                else:
                    if len(fieldNames) != len(obj.fields) or not obj.isSimple():
                        isSimple = False
                        break
                    sameFields = True
                    for field in obj.fields:
                        if field.name not in fieldNames:
                            sameFields = False
                            break
                    if not sameFields:
                        isSimple = False
                    break
            if isSimple:
                self.type = ObjectType.OBJECT_ELEMENT_SIMPLE
        elif self.type == ObjectType.VALUE_ANY:
            newType = None
            for obj in self.objects:
                if isinstance(obj, basestring):
                    newType = self.checkType(newType, ObjectType.STRING)
                elif type(obj) is bytearray or type(obj) is bytes:
                    newType = self.checkType(newType, ObjectType.BYTES)
                elif type(obj) is int:
                    newType = self.checkType(newType, ObjectType.INTEGER)
                elif type(obj) is long:
                    newType = self.checkType(newType, ObjectType.LONG)
                elif type(obj) is float:
                    newType = self.checkType(newType, ObjectType.DOUBLE)
                if newType is None:
                    break
            if newType is not None:
                self.type = newType
        return self


def isArrayContainObjectElements(objectArray):
    # type: (ObjectArray) -> bool
    return objectArray is not None and len(objectArray.objects) > 0 and (
            objectArray.type == ObjectType.OBJECT_ELEMENT or objectArray.type == ObjectType.OBJECT_ELEMENT_SIMPLE)


def isNumberField(field):
    # type: (ObjectField) -> bool
    return field is not None and (
            ObjectType.BYTE == field.type or ObjectType.SHORT == field.type or ObjectType.INTEGER == field.type or
            ObjectType.LONG == field.type or ObjectType.FLOAT == field.type or ObjectType.DOUBLE == field.type or
            ObjectType.BIG_INTEGER == field.type or ObjectType.BIG_DECIMAL == field.type)


def isStringField(field):
    # type: (ObjectField) -> bool
    return field is not None and ObjectType.STRING == field.type


def isBytesField(field):
    # type: (ObjectField) -> bool
    return field is not None and ObjectType.BYTES == field.type


def getNumberField(field):
    # type: (ObjectField) -> Optional[int or float]
    if isNumberField(field):
        return field.value
    else:
        return None


def getStringField(field):
    # type: (ObjectField) -> Optional[str]
    if isStringField(field):
        return field.value
    else:
        return None


def getBytesField(field):
    # type: (ObjectField) -> Optional[bytes]
    if isBytesField(field):
        return field.value
    else:
        return None


def toStringField(field):
    # type: (ObjectField) -> Optional[str]
    if field is None:
        return None
    if field.type == ObjectType.STRING:
        return field.value
    elif field.type == ObjectType.BYTES:
        return base64.b64encode(field.value)
    else:
        return str(field.value)


def getObjectElement(field):
    # type: (ObjectField) -> Optional[ObjectElement]
    if field.type == ObjectType.OBJECT_ARRAY:
        if len(field.value.objects) > 0 and (field.value.type == ObjectType.OBJECT_ELEMENT or field.value.type == ObjectType.OBJECT_ELEMENT_SIMPLE):
            return field.value.objects[0]
    if field.type == ObjectType.OBJECT_ELEMENT or field.type == ObjectType.OBJECT_ELEMENT_SIMPLE:
        return field.value
    return None


class ObjectValuePrivate(object):
    def __init__(self, name, type, value=None):
        # type: (str, ObjectType, object) -> None
        self.name = name
        self.type = type
        self.value = value


def deserializeToObject(messages):
    # type: (List[SMCApi.IMessage]) -> ObjectArray
    """
     * deserialize messages to object array
     * use object serialization format
     * object serialization format:
     *      number - type of elements, may by: 0-ObjectArray, 1-ObjectElement, 2-ObjectElementSimple, 3-AnySimpleTypes, 4-String, 5-Byte, 6-Short, 7-Integer, 8-Long, 9-Float, 10-Double, 11-BigInteger, 12-BigDecimal, 13-byte[], 14-OBJECT_ELEMENT_OPTIMIZED, 15-OBJECT_ELEMENT_SIMPLE_OPTIMIZED
     *      number - number of item in array
     *      items. depend of type. format:
     *          if item type is 0 (ObjectArray): then list of arrays. each has format described above, recursion.
     *          if item type is 1 (ObjectElement): then list of objects:
     *              if all elements hase same fields and size>1 then:
     *                  number - number of fields in object.
     *                  list of fields. format:
     *                      string - field name.
     *                      number - field type, may by: 0-ObjectArray, 1-ObjectElement, 2-ObjectElementSimple, 3-AnySimpleTypes, 4-String, 5-Byte, 6-Short, 7-Integer, 8-Long, 9-Float, 10-Double, 11-BigInteger, 12-BigDecimal, 13-byte[]
     *                  list of values for each element. format:
     *                      field value. depend of type. format:
     *                          if item type is 0-ObjectArray: then list of arrays. each has format described above, recursion.
     *                          if item type is 1-ObjectElement: then list of objects. each has format described above, recursion.
     *                          if item type is 2-ObjectElementSimple: then list of simple objects. each has format described above, recursion.
     *                          else: any type - simple value.
     *              else:
     *                  number - number of fields in object.
     *                  for each element:
     *                      for each field. format:
     *                          string - field name.
     *                          number - field type, may by: 0-ObjectArray, 1-ObjectElement, 2-ObjectElementSimple, 3-AnySimpleTypes, 4-String, 5-Byte, 6-Short, 7-Integer, 8-Long, 9-Float, 10-Double, 11-BigInteger, 12-BigDecimal, 13-byte[]
     *                          field value. depend of type. format:
     *                              if item type is 0-ObjectArray: then list of arrays. each has format described above, recursion.
     *                              if item type is 1-ObjectElement: then list of objects. each has format described above, recursion.
     *                              if item type is 2-ObjectElementSimple: then list of simple objects. each has format described above, recursion.
     *                              else: any type - simple value.
     *          if item type is 2 (ObjectElementSimple): then list of simple objects has format:
     *              if all elements hase same fields and size>1 then:
     *                  number - number of fields in object.
     *                  list of fields. format:
     *                      string - field name.
     *                  list of values for each element. format:
     *                      any type - simple value.
     *              else:
     *                  number - number of fields in each object (one for all).
     *                  list of each object fields. format:
     *                      string - field name.
     *                      any type - simple value.
     *          else: list of simple values, format:
     *              any type - simple value.

    :param messages:
    :return:
    """
    objectArray = ObjectArray()
    if messages is None or len(messages) < 2:
        return objectArray
    message = messages[0]
    typeId = getNumber(message)
    if typeId is None:
        return objectArray
    if typeId < 0 or len(ObjectTypePrivate) <= typeId:
        return objectArray
    messages.pop(0)
    # type = ObjectType[typeId]
    typePrivate = ObjectTypePrivate[typeId]
    message = messages[0]
    size = getNumber(message)
    if typeId is None:
        return objectArray
    messages.pop(0)
    count = size

    type = None
    if typePrivate == ObjectTypePrivate.OBJECT_ELEMENT_OPTIMIZED:
        type = ObjectType.OBJECT_ELEMENT
    elif typePrivate == ObjectTypePrivate.OBJECT_ELEMENT_SIMPLE_OPTIMIZED:
        type = ObjectType.OBJECT_ELEMENT_SIMPLE
    else:
        type = ObjectType[ObjectType._keys.index(typePrivate.key)]
    objectArray = ObjectArray(type)

    try:
        if typePrivate == ObjectTypePrivate.OBJECT_ARRAY:
            for i in range(count):
                objectArray.add(deserializeToObject(messages))
        elif typePrivate == ObjectTypePrivate.OBJECT_ELEMENT:
            for i in range(count):
                objectArray.add(deserializeToObjectElement(messages))
        elif typePrivate == ObjectTypePrivate.OBJECT_ELEMENT_SIMPLE:
            if messages is None or len(messages) < 1:
                return objectArray
            message = messages[0]
            countFields = getNumber(message)
            if countFields is not None:
                messages.pop(0)
                for i in range(count):
                    objectArray.add(deserializeToObjectElement(messages, countFields))
        elif typePrivate == ObjectTypePrivate.OBJECT_ELEMENT_OPTIMIZED:
            if messages is None or len(messages) < 1:
                return objectArray
            message = messages[0]
            countFields = getNumber(message)
            if countFields is None or len(messages) <= countFields * 2 + 1:
                return objectArray
            messages.pop(0)

            definedFields = []
            hasErrors = False
            for i in range(countFields):
                message = messages[0]
                fieldName = toString(message)
                if fieldName is None:
                    hasErrors = True
                    break
                messages.pop(0)
                message = messages[0]
                fieldTypeId = getNumber(message)
                if fieldTypeId is None or fieldTypeId < 0 or len(ObjectType) <= fieldTypeId:
                    hasErrors = True
                    break
                messages.pop(0)
                definedFields.append(ObjectValuePrivate(fieldName, ObjectType[fieldTypeId]))
            if hasErrors:
                return objectArray

            for i in range(count):
                objectArray.add(deserializeToObjectElement(messages, -1, definedFields))

        elif typePrivate == ObjectTypePrivate.OBJECT_ELEMENT_SIMPLE_OPTIMIZED:
            if messages is None or len(messages) < 1:
                return objectArray
            message = messages[0]
            countFields = getNumber(message)
            if countFields is None or len(messages) <= countFields * 2 + 1:
                return objectArray
            messages.pop(0)

            definedFields = []
            hasErrors = False
            for i in range(countFields):
                message = messages[0]
                fieldName = toString(message)
                if fieldName is None:
                    hasErrors = True
                    break
                messages.pop(0)
                definedFields.append(ObjectValuePrivate(fieldName, ObjectType.VALUE_ANY))
            if hasErrors:
                return objectArray

            for i in range(count):
                objectArray.add(deserializeToObjectElement(messages, -1, definedFields))
        else:
            for i in range(count):
                objectArray.add(messages.pop(0).getValue())
    except Exception as e:
        print(e)
    return objectArray


def deserializeToObjectElement(messages, countFields=-1, definedFields=None):
    # type: (List[SMCApi.IMessage], int, List[ObjectValuePrivate]) -> ObjectElement
    objectElement = ObjectElement()

    count = -1
    if messages is None or len(messages) < 1:
        return objectElement
    if countFields < 0:
        if definedFields is None:
            size = getNumber(messages[0])
            if size is None:
                return objectElement
            messages.pop(0)
            count = size
        else:
            count = len(definedFields)
    else:
        count = countFields

    try:
        if definedFields is not None:
            for field in definedFields:
                deserializeToObjectElementValue(messages, objectElement, field.name, field.type)
        else:
            for i in range(count):
                if (countFields > -1 and len(messages) < 2) or (countFields < 0 and len(messages) < 3):
                    break
                fieldName = toString(messages.pop(0))
                type = ObjectType.VALUE_ANY
                if countFields < 0:
                    typeId = getNumber(messages[0])
                    if typeId is None or typeId < 0 or len(ObjectType) <= typeId:
                        break
                    type = ObjectType[typeId]
                    messages.pop(0)
                deserializeToObjectElementValue(messages, objectElement, fieldName, type)
    except Exception as e:
        print(e)

    return objectElement


def deserializeToObjectElementValue(messages, objectElement, fieldName, type):
    # type: (List[SMCApi.IMessage], ObjectElement, str, ObjectType) -> None
    if type == ObjectType.OBJECT_ARRAY:
        objectElement.fields.append(ObjectField(fieldName, deserializeToObject(messages)))
    elif type == ObjectType.OBJECT_ELEMENT:
        objectElement.fields.append(ObjectField(fieldName, deserializeToObjectElement(messages)))
    elif type == ObjectType.OBJECT_ELEMENT_SIMPLE:
        countFields2 = getNumber(messages[0])
        if countFields2 is not None:
            messages.pop(0)
            objectElement.fields.append(ObjectField(fieldName, deserializeToObjectElement(messages, countFields2)))
    else:
        objectElement.fields.append(ObjectField(fieldName, messages.pop(0).getValue()))


def serializeFromObject(objectArray):
    # type: (ObjectArray) -> List[object]
    """
     * serialize objects to messages
     * use object serialization format
     * object serialization format:
     *      number - type of elements, may by: 0-ObjectArray, 1-ObjectElement, 2-ObjectElementSimple, 3-AnySimpleTypes, 4-String, 5-Byte, 6-Short, 7-Integer, 8-Long, 9-Float, 10-Double, 11-BigInteger, 12-BigDecimal, 13-byte[], 14-OBJECT_ELEMENT_OPTIMIZED, 15-OBJECT_ELEMENT_SIMPLE_OPTIMIZED
     *      number - number of item in array
     *      items. depend of type. format:
     *          if item type is 0 (ObjectArray): then list of arrays. each has format described above, recursion.
     *          if item type is 1 (ObjectElement): then list of objects:
     *              if all elements hase same fields and size>1 then:
     *                  number - number of fields in object.
     *                  list of fields. format:
     *                      string - field name.
     *                      number - field type, may by: 0-ObjectArray, 1-ObjectElement, 2-ObjectElementSimple, 3-AnySimpleTypes, 4-String, 5-Byte, 6-Short, 7-Integer, 8-Long, 9-Float, 10-Double, 11-BigInteger, 12-BigDecimal, 13-byte[]
     *                  list of values for each element. format:
     *                      field value. depend of type. format:
     *                          if item type is 0-ObjectArray: then list of arrays. each has format described above, recursion.
     *                          if item type is 1-ObjectElement: then list of objects. each has format described above, recursion.
     *                          if item type is 2-ObjectElementSimple: then list of simple objects. each has format described above, recursion.
     *                          else: any type - simple value.
     *              else:
     *                  number - number of fields in object.
     *                  for each element:
     *                      for each field. format:
     *                          string - field name.
     *                          number - field type, may by: 0-ObjectArray, 1-ObjectElement, 2-ObjectElementSimple, 3-AnySimpleTypes, 4-String, 5-Byte, 6-Short, 7-Integer, 8-Long, 9-Float, 10-Double, 11-BigInteger, 12-BigDecimal, 13-byte[]
     *                          field value. depend of type. format:
     *                              if item type is 0-ObjectArray: then list of arrays. each has format described above, recursion.
     *                              if item type is 1-ObjectElement: then list of objects. each has format described above, recursion.
     *                              if item type is 2-ObjectElementSimple: then list of simple objects. each has format described above, recursion.
     *                              else: any type - simple value.
     *          if item type is 2 (ObjectElementSimple): then list of simple objects has format:
     *              if all elements hase same fields and size>1 then:
     *                  number - number of fields in object.
     *                  list of fields. format:
     *                      string - field name.
     *                  list of values for each element. format:
     *                      any type - simple value.
     *              else:
     *                  number - number of fields in each object (one for all).
     *                  list of each object fields. format:
     *                      string - field name.
     *                      any type - simple value.
     *          else: list of simple values, format:
     *              any type - simple value.

    :param objectArray:
    :return:
    """
    result = []
    if objectArray is None:
        return result
    count = len(objectArray.objects)
    result.append(objectArray.type.index)
    result.append(count)
    if count == 0:
        return result

    if objectArray.type == ObjectType.OBJECT_ARRAY:
        for obj in objectArray.objects:
            result.extend(serializeFromObject(obj))
    elif objectArray.type == ObjectType.OBJECT_ELEMENT:
        definedFields = None
        if count > 1 and objectArray.isSameFields():
            definedFields = []
            objectElement = objectArray.objects[0]
            for field in objectElement.fields:
                definedFields.append(ObjectValuePrivate(field.name, field.type))
            result = [ObjectTypePrivate.OBJECT_ELEMENT_OPTIMIZED.index, count, len(definedFields)]
            for field in definedFields:
                result.append(field.name)
                result.append(field.type.index)
        for obj in objectArray.objects:
            result.extend(serializeFromObjectElement(obj, False, definedFields))
    elif objectArray.type == ObjectType.OBJECT_ELEMENT_SIMPLE:
        definedFields = None
        if count > 1 and objectArray.isSameFields():
            definedFields = []
            objectElement = objectArray.objects[0]
            for field in objectElement.fields:
                definedFields.append(ObjectValuePrivate(field.name, field.type))
            result = [ObjectTypePrivate.OBJECT_ELEMENT_SIMPLE_OPTIMIZED.index, count, len(definedFields)]
            for field in definedFields:
                result.append(field.name)
        else:
            if count > 0:
                result.append(len(objectArray.objects[0].fields))
            else:
                result.append(0)
        for obj in objectArray.objects:
            result.extend(serializeFromObjectElement(obj, True, definedFields))
    else:
        for obj in objectArray.objects:
            result.append(obj)
    return result


def serializeFromObjectElement(objectElement, isSimple=False, definedFields=None):
    # type: (ObjectElement, bool, List[ObjectValuePrivate]) -> List[object]
    result = []
    if objectElement is None:
        return result
    if definedFields is not None:
        # because its check
        for field in objectElement.fields:
            result.extend(serializeFromObjectFieldValue(field.type, field.value))
    else:
        if not isSimple:
            result.append(len(objectElement.fields))

        for f in objectElement.fields:
            if f.value is None:
                continue
            result.append(f.name)
            if not isSimple:
                result.append(f.type.index)
            result.extend(serializeFromObjectFieldValue(f.type, f.value))
    return result


def serializeFromObjectFieldValue(type, value):
    # type: (ObjectType, object) -> List[object]
    if type == ObjectType.OBJECT_ARRAY:
        return serializeFromObject(value)
    elif type == ObjectType.OBJECT_ELEMENT:
        return serializeFromObjectElement(value);
    elif type == ObjectType.OBJECT_ELEMENT_SIMPLE:
        lst = []
        lst.append(len(value.fields))
        lst.extend(serializeFromObjectElement(value, True))
        return lst
    else:
        return [value]
