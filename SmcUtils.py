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


def isObjectArray(message):
    # type: (SMCApi.IMessage) -> bool
    return message is not None and SMCApi.ValueType.OBJECT_ARRAY == message.getType()


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


def getObjectArray(message):
    # type: (SMCApi.IMessage) -> Optional[SMCApi.ObjectArray]
    if isObjectArray(message):
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


def isArrayContainObjectElements(objectArray):
    # type: (SMCApi.ObjectArray) -> bool
    return objectArray is not None and len(objectArray.objects) > 0 and objectArray.getType() == SMCApi.ObjectType.OBJECT_ELEMENT


def isArrayContainArrays(objectArray):
    # type: (SMCApi.ObjectArray) -> bool
    return objectArray is not None and len(objectArray.objects) > 0 and objectArray.getType() == SMCApi.ObjectType.OBJECT_ARRAY


def isArrayContainNumber(objectArray):
    # type: (SMCApi.ObjectArray) -> bool
    return objectArray is not None and len(objectArray.objects) > 0 and (
            objectArray.getType() == SMCApi.ObjectType.VALUE_ANY or
            SMCApi.ObjectType.BYTE == objectArray.getType() or SMCApi.ObjectType.SHORT == objectArray.getType() or SMCApi.ObjectType.INTEGER == objectArray.getType() or
            SMCApi.ObjectType.LONG == objectArray.getType() or SMCApi.ObjectType.FLOAT == objectArray.getType() or SMCApi.ObjectType.DOUBLE == objectArray.getType() or
            SMCApi.ObjectType.BIG_INTEGER == objectArray.getType() or SMCApi.ObjectType.BIG_DECIMAL == objectArray.getType())


def isArrayContainString(objectArray):
    # type: (SMCApi.ObjectArray) -> bool
    return objectArray is not None and len(objectArray.objects) > 0 and (
            objectArray.getType() == SMCApi.ObjectType.VALUE_ANY or objectArray.getType() == SMCApi.ObjectType.BYTES)


def isArrayContainBytes(objectArray):
    # type: (SMCApi.ObjectArray) -> bool
    return objectArray is not None and len(objectArray.objects) > 0 and (
            objectArray.getType() == SMCApi.ObjectType.VALUE_ANY or objectArray.getType() == SMCApi.ObjectType.STRING)


def isNumberField(field):
    # type: (SMCApi.ObjectField) -> bool
    return field is not None and (
            SMCApi.ObjectType.BYTE == field.getType() or SMCApi.ObjectType.SHORT == field.getType() or SMCApi.ObjectType.INTEGER == field.getType() or
            SMCApi.ObjectType.LONG == field.getType() or SMCApi.ObjectType.FLOAT == field.getType() or SMCApi.ObjectType.DOUBLE == field.getType() or
            SMCApi.ObjectType.BIG_INTEGER == field.getType() or SMCApi.ObjectType.BIG_DECIMAL == field.getType())


def isStringField(field):
    # type: (SMCApi.ObjectField) -> bool
    return field is not None and SMCApi.ObjectType.STRING == field.getType()


def isBytesField(field):
    # type: (SMCApi.ObjectField) -> bool
    return field is not None and SMCApi.ObjectType.BYTES == field.getType()


def isObjectArrayField(field):
    # type: (SMCApi.ObjectField) -> bool
    return field is not None and SMCApi.ObjectType.OBJECT_ARRAY == field.getType()


def isObjectElementField(field):
    # type: (SMCApi.ObjectField) -> bool
    return field is not None and SMCApi.ObjectType.OBJECT_ELEMENT == field.getType()


def getNumberField(field):
    # type: (SMCApi.ObjectField) -> Optional[int or float]
    if isNumberField(field):
        return field.value
    else:
        return None


def getStringField(field):
    # type: (SMCApi.ObjectField) -> Optional[str]
    if isStringField(field):
        return field.value
    else:
        return None


def getBytesField(field):
    # type: (SMCApi.ObjectField) -> Optional[bytes]
    if isBytesField(field):
        return field.value
    else:
        return None


def getObjectArrayField(field):
    # type: (SMCApi.ObjectField) -> Optional[SMCApi.ObjectArray]
    if isObjectArrayField(field):
        return field.value
    else:
        return None


def toStringField(field):
    # type: (SMCApi.ObjectField) -> Optional[str]
    if field is None:
        return None
    if field.getType() == SMCApi.ObjectType.STRING:
        return field.value
    elif field.getType() == SMCApi.ObjectType.BYTES:
        return base64.b64encode(field.value)
    else:
        return str(field.value)


def getObjectElement(field):
    # type: (SMCApi.ObjectField) -> Optional[SMCApi.ObjectElement]
    if field is None:
        return None
    if field.getType() == SMCApi.ObjectType.OBJECT_ARRAY:
        if len(field.getValue().objects) > 0 and field.getValue().getType() == SMCApi.ObjectType.OBJECT_ELEMENT:
            return field.getValue().objects[0]
    elif field.getType() == SMCApi.ObjectType.OBJECT_ELEMENT:
        return field.getValue()
    return None


def getObjectElements(field):
    # type: (SMCApi.ObjectField) -> Optional[List[SMCApi.ObjectElement]]
    if field is None:
        return None
    if field.getType() == SMCApi.ObjectType.OBJECT_ARRAY:
        if field.getValue().getType() == SMCApi.ObjectType.OBJECT_ELEMENT:
            return list(field.getValue().objects)
    elif field.getType() == SMCApi.ObjectType.OBJECT_ELEMENT:
        return list(field.getValue())
    return None


class ObjectValuePrivate(object):
    def __init__(self, name, type, value=None):
        # type: (str, ObjectTypePrivate, object) -> None
        self.name = name
        self.type = type
        self.value = value


def convertFromObjectTypePrivate(typePrivate):
    # type: (ObjectTypePrivate) -> SMCApi.ObjectType
    if typePrivate == ObjectTypePrivate.OBJECT_ELEMENT_OPTIMIZED:
        return SMCApi.ObjectType.OBJECT_ELEMENT
    elif typePrivate == ObjectTypePrivate.OBJECT_ELEMENT_SIMPLE_OPTIMIZED:
        return SMCApi.ObjectType.OBJECT_ELEMENT
    elif typePrivate == ObjectTypePrivate.OBJECT_ELEMENT_SIMPLE:
        return SMCApi.ObjectType.OBJECT_ELEMENT
    else:
        return SMCApi.ObjectType[SMCApi.ObjectType._keys.index(typePrivate.key)]


def convertToObjectTypePrivate(type):
    # type: (SMCApi.ObjectType) -> ObjectTypePrivate
    return ObjectTypePrivate[ObjectTypePrivate._keys.index(type.key)]


def deserializeToObject(messages):
    # type: (List[SMCApi.IMessage]) -> SMCApi.ObjectArray
    """
     * deserialize messages to object array
     * if first message type ObjectArray, when return it
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
    message = messages[0]
    if isObjectArray(message):
        return getObjectArray(messages.pop(0))
    objectArray = SMCApi.ObjectArray()
    if messages is None or len(messages) < 2:
        return objectArray
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

    type = convertFromObjectTypePrivate(typePrivate)
    objectArray = SMCApi.ObjectArray(type)

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
                if fieldTypeId is None or fieldTypeId < 0 or len(SMCApi.ObjectTypePrivate) <= fieldTypeId:
                    hasErrors = True
                    break
                messages.pop(0)
                definedFields.append(ObjectValuePrivate(fieldName, SMCApi.ObjectTypePrivate[fieldTypeId]))
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
                definedFields.append(ObjectValuePrivate(fieldName, SMCApi.ObjectTypePrivate.VALUE_ANY))
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
    # type: (List[SMCApi.IMessage], int, List[ObjectValuePrivate]) -> SMCApi.ObjectElement
    message = messages[0]
    if isObjectArray(message):
        objectArray = getObjectArray(messages.pop(0))
        if isArrayContainObjectElements(objectArray):
            return objectArray.get(0)
        return SMCApi.ObjectElement()
    objectElement = SMCApi.ObjectElement()

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
                deserializeToObjectElementValue(messages, objectElement, field.getName(), field.getType())
        else:
            for i in range(count):
                if (countFields > -1 and len(messages) < 2) or (countFields < 0 and len(messages) < 3):
                    break
                fieldName = toString(messages.pop(0))
                type = ObjectTypePrivate.VALUE_ANY
                if countFields < 0:
                    typeId = getNumber(messages[0])
                    if typeId is None or typeId < 0 or len(ObjectTypePrivate) <= typeId:
                        break
                    messages.pop(0)
                    type = ObjectTypePrivate[typeId]
                deserializeToObjectElementValue(messages, objectElement, fieldName, type)
    except Exception as e:
        print(e)

    return objectElement


def deserializeToObjectElementValue(messages, objectElement, fieldName, type):
    # type: (List[SMCApi.IMessage], SMCApi.ObjectElement, str, ObjectTypePrivate) -> None
    if type == ObjectTypePrivate.OBJECT_ARRAY:
        objectElement.fields.append(SMCApi.ObjectField(fieldName, deserializeToObject(messages)))
    elif type == ObjectTypePrivate.OBJECT_ELEMENT:
        objectElement.fields.append(SMCApi.ObjectField(fieldName, deserializeToObjectElement(messages)))
    elif type == ObjectTypePrivate.OBJECT_ELEMENT_SIMPLE:
        countFields2 = getNumber(messages[0])
        if countFields2 is not None:
            messages.pop(0)
            objectElement.fields.append(SMCApi.ObjectField(fieldName, deserializeToObjectElement(messages, countFields2)))
    else:
        objectElement.fields.append(SMCApi.ObjectField(fieldName, messages.pop(0).getValue()))


def serializeFromObject(objectArray):
    # type: (SMCApi.ObjectArray) -> List[object]
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
    count = objectArray.size()
    typePrivate = convertToObjectTypePrivate(objectArray.getType())
    result.append(typePrivate.index)
    result.append(count)
    if count == 0:
        return result

    if typePrivate == ObjectTypePrivate.OBJECT_ELEMENT and count > 1:
        isSimple = True
        fieldNames = None
        for obj in objectArray.objects:
            if fieldNames is None:
                fieldNames = []
                for field in obj.fields:
                    fieldNames.append(field.getName())
                if not obj.isSimple():
                    isSimple = False
                    break
            else:
                if len(fieldNames) != len(obj.fields) or not obj.isSimple():
                    isSimple = False
                    break
                sameFields = True
                for field in obj.fields:
                    if field.getName() not in fieldNames:
                        sameFields = False
                        break
                if not sameFields:
                    isSimple = False
                break
        if isSimple:
            typePrivate = ObjectTypePrivate.OBJECT_ELEMENT_SIMPLE

    if typePrivate == ObjectTypePrivate.OBJECT_ARRAY:
        for obj in objectArray.objects:
            result.extend(serializeFromObject(obj))
    elif typePrivate == ObjectTypePrivate.OBJECT_ELEMENT:
        definedFields = None
        if count > 1 and isElementsHasSameFieldsInObjectArray(objectArray):
            definedFields = []
            objectElement = objectArray.get(0)
            for field in objectElement.getFields():
                definedFields.append(ObjectValuePrivate(field.getName(), convertToObjectTypePrivate(field.getType())))
            result = [ObjectTypePrivate.OBJECT_ELEMENT_OPTIMIZED.index, count, len(definedFields)]
            for field in definedFields:
                result.append(field.getName())
                result.append(field.getType().index)
        for obj in objectArray.objects:
            result.extend(serializeFromObjectElement(obj, False, definedFields))
    elif typePrivate == ObjectTypePrivate.OBJECT_ELEMENT_SIMPLE:
        definedFields = None
        if count > 1 and isElementsHasSameFieldsInObjectArray(objectArray):
            definedFields = []
            objectElement = objectArray.get(0)
            for field in objectElement.getFields():
                definedFields.append(ObjectValuePrivate(field.getName(), convertToObjectTypePrivate(field.getType())))
            result = [ObjectTypePrivate.OBJECT_ELEMENT_SIMPLE_OPTIMIZED.index, count, len(definedFields)]
            for field in definedFields:
                result.append(field.getName())
        else:
            if count > 0:
                result.append(len(objectArray.get(0).getFields()))
            else:
                result.append(0)
        for obj in objectArray.objects:
            result.extend(serializeFromObjectElement(obj, True, definedFields))
    else:
        for obj in objectArray.objects:
            result.append(obj)
    return result


def serializeFromObjectElement(objectElement, isSimple=False, definedFields=None):
    # type: (SMCApi.ObjectElement, bool, List[ObjectValuePrivate]) -> List[object]
    result = []
    if objectElement is None:
        return result
    if definedFields is not None:
        # because its check
        for field in objectElement.getFields():
            result.extend(serializeFromObjectFieldValue(field.getType(), field.getValue()))
    else:
        if not isSimple:
            result.append(len(objectElement.getFields()))

        for f in objectElement.getFields():
            if f.getValue() is None:
                continue
            result.append(f.getName())
            if not isSimple:
                result.append(convertToObjectTypePrivate(f.getType()).index)
            result.extend(serializeFromObjectFieldValue(f.getType(), f.getValue()))
    return result


def serializeFromObjectFieldValue(type, value):
    # type: (SMCApi.ObjectType, object) -> List[object]
    if type == SMCApi.ObjectType.OBJECT_ARRAY:
        return serializeFromObject(value)
    elif type == SMCApi.ObjectType.OBJECT_ELEMENT:
        if value.isSimple():
            lst = []
            lst.append(len(value.getFields()))
            lst.extend(serializeFromObjectElement(value, True))
            return lst
        else:
            return serializeFromObjectElement(value)
    else:
        return [value]


def isElementsHasSameFieldsInObjectArray(objectArray):
    # type: (SMCApi.ObjectArray) -> bool
    isSame = True
    fieldNames = None
    fieldTypes = None
    for obj in objectArray:
        if fieldNames is None or fieldTypes is None:
            fieldNames = []
            fieldTypes = []
            for field in obj.fields:
                fieldNames.append(field.getName())
                fieldTypes.append(field.getType())
        else:
            if len(fieldNames) != len(obj.fields):
                isSame = False
                break
            sameFields = True
            for i in range(len(fieldNames)):
                if fieldNames[i] != obj.fields[i].getName():
                    sameFields = False
                    break
                if fieldTypes[i] != obj.fields[i].getType():
                    sameFields = False
                    break
            if not sameFields:
                isSame = False
                break
    return isSame


def fieldToValueType(field):
    # type: (SMCApi.ObjectField) -> SMCApi.ValueType
    if field is None or not field.isSimple():
        return None
    if field.getType() == SMCApi.ObjectType.VALUE_ANY:
        return getValueTypeObject(field.getValue())
    else:
        return SMCApi.ValueType[SMCApi.ValueType._keys.index(field.getType().key)]


def getValueTypeObject(value):
    # type: (object) -> SMCApi.ValueType
    valueType = type(value)

    if valueType is str or valueType is unicode:
        return SMCApi.ValueType.STRING
    elif valueType is bytearray or valueType is bytes:
        return SMCApi.ValueType.BYTES
    elif valueType is int:
        return SMCApi.ValueType.INTEGER
    elif valueType is long:
        return SMCApi.ValueType.LONG
    elif valueType is float:
        return SMCApi.ValueType.DOUBLE
    elif valueType is SMCApi.ObjectArray:
        return SMCApi.ValueType.OBJECT_ARRAY
    else:
        raise ValueError("wrong type")


def getObjectType(value):
    # type: (object) -> SMCApi.ObjectType
    valueType = type(value)
    if value is None:
        return None
    if valueType == SMCApi.ObjectType.VALUE_ANY:
        return SMCApi.ObjectType.OBJECT_ELEMENT
    else:
        return convertToObjectType(getValueTypeObject(value))


def convertToObjectType(type):
    # type: (SMCApi.ValueType) -> SMCApi.ObjectType
    if type == SMCApi.ValueType.STRING:
        return SMCApi.ObjectType.STRING
    elif type == SMCApi.ValueType.BYTE:
        return SMCApi.ObjectType.BYTE
    elif type == SMCApi.ValueType.SHORT:
        return SMCApi.ObjectType.SHORT
    elif type == SMCApi.ValueType.INTEGER:
        return SMCApi.ObjectType.INTEGER
    elif type == SMCApi.ValueType.LONG:
        return SMCApi.ObjectType.LONG
    elif type == SMCApi.ValueType.BIG_INTEGER:
        return SMCApi.ObjectType.BIG_INTEGER
    elif type == SMCApi.ValueType.FLOAT:
        return SMCApi.ObjectType.FLOAT
    elif type == SMCApi.ValueType.DOUBLE:
        return SMCApi.ObjectType.DOUBLE
    elif type == SMCApi.ValueType.BIG_DECIMAL:
        return SMCApi.ObjectType.BIG_DECIMAL
    elif type == SMCApi.ValueType.BYTES:
        return SMCApi.ObjectType.BYTES
    elif type == SMCApi.ValueType.OBJECT_ARRAY:
        return SMCApi.ObjectType.OBJECT_ARRAY
    return None


def convertToValueType(type):
    # type: (SMCApi.ObjectType) -> SMCApi.ValueType
    if type == SMCApi.ObjectType.STRING:
        return SMCApi.ValueType.STRING
    elif type == SMCApi.ObjectType.BYTE:
        return SMCApi.ValueType.BYTE
    elif type == SMCApi.ObjectType.SHORT:
        return SMCApi.ValueType.SHORT
    elif type == SMCApi.ObjectType.INTEGER:
        return SMCApi.ValueType.INTEGER
    elif type == SMCApi.ObjectType.LONG:
        return SMCApi.ValueType.LONG
    elif type == SMCApi.ObjectType.BIG_INTEGER:
        return SMCApi.ValueType.BIG_INTEGER
    elif type == SMCApi.ObjectType.FLOAT:
        return SMCApi.ValueType.FLOAT
    elif type == SMCApi.ObjectType.DOUBLE:
        return SMCApi.ValueType.DOUBLE
    elif type == SMCApi.ObjectType.BIG_DECIMAL:
        return SMCApi.ValueType.BIG_DECIMAL
    elif type == SMCApi.ObjectType.BYTES:
        return SMCApi.ValueType.BYTES
    elif type == SMCApi.ObjectType.OBJECT_ARRAY:
        return SMCApi.ValueType.OBJECT_ARRAY
    return None
