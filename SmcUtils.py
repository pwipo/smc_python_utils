"""
created by Nikolay V. Ulyanov (ulianownv@mail.ru)
http://www.smcsystem.ru
"""
import base64
import sys
import time
import traceback
from __builtin__ import long, unicode
from typing import List, Optional, Callable

import SMCApi
from enum import Enum


def isNumber(value):
    # type: (SMCApi.IValue) -> bool
    return value is not None and (
            SMCApi.ValueType.BYTE == value.getType() or SMCApi.ValueType.SHORT == value.getType() or SMCApi.ValueType.INTEGER == value.getType() or
            SMCApi.ValueType.LONG == value.getType() or SMCApi.ValueType.FLOAT == value.getType() or SMCApi.ValueType.DOUBLE == value.getType() or
            SMCApi.ValueType.BIG_INTEGER == value.getType() or SMCApi.ValueType.BIG_DECIMAL == value.getType())


def isNumberField(field):
    # type: (SMCApi.ObjectField) -> bool
    return field is not None and (
            SMCApi.ObjectType.BYTE == field.getType() or SMCApi.ObjectType.SHORT == field.getType() or SMCApi.ObjectType.INTEGER == field.getType() or
            SMCApi.ObjectType.LONG == field.getType() or SMCApi.ObjectType.FLOAT == field.getType() or SMCApi.ObjectType.DOUBLE == field.getType() or
            SMCApi.ObjectType.BIG_INTEGER == field.getType() or SMCApi.ObjectType.BIG_DECIMAL == field.getType())


def isString(value):
    # type: (SMCApi.IValue) -> bool
    return value is not None and SMCApi.ValueType.STRING == value.getType()


def isStringField(field):
    # type: (SMCApi.ObjectField) -> bool
    return field is not None and SMCApi.ObjectType.STRING == field.getType()


def isBytes(value):
    # type: (SMCApi.IValue) -> bool
    return value is not None and SMCApi.ValueType.BYTES == value.getType()


def isBytesField(field):
    # type: (SMCApi.ObjectField) -> bool
    return field is not None and SMCApi.ObjectType.BYTES == field.getType()


def isBoolean(value):
    # type: (SMCApi.IValue) -> bool
    return value is not None and SMCApi.ValueType.BOOLEAN == value.getType()


def isBooleanField(field):
    # type: (SMCApi.ObjectField) -> bool
    return field is not None and SMCApi.ObjectType.BOOLEAN == field.getType()


def isObjectArray(value):
    # type: (SMCApi.IValue) -> bool
    return value is not None and SMCApi.ValueType.OBJECT_ARRAY == value.getType()


def isObjectArrayField(field):
    # type: (SMCApi.ObjectField) -> bool
    return field is not None and SMCApi.ObjectType.OBJECT_ARRAY == field.getType()


def isObjectElementField(field):
    # type: (SMCApi.ObjectField) -> bool
    return field is not None and SMCApi.ObjectType.OBJECT_ELEMENT == field.getType()


def getNumber(value):
    # type: (SMCApi.IValue) -> Optional[int or long or float]
    if isNumber(value):
        return value.getValue()
    else:
        None


def getNumberField(field):
    # type: (SMCApi.ObjectField) -> Optional[int or long or float]
    if isNumberField(field):
        return field.getValue()
    else:
        return None


def getString(value):
    # type: (SMCApi.IValue) -> Optional[str]
    if isString(value):
        return value.getValue()
    else:
        None


def getStringField(field):
    # type: (SMCApi.ObjectField) -> Optional[str]
    if isStringField(field):
        return field.getValue()
    else:
        return None


def getBytes(value):
    # type: (SMCApi.IValue) -> Optional[bytes]
    if isBytes(value):
        return value.getValue()
    else:
        None


def getBytesField(field):
    # type: (SMCApi.ObjectField) -> Optional[bytes]
    if isBytesField(field):
        return field.getValue()
    else:
        return None


def getBoolean(value):
    # type: (SMCApi.IValue) -> Optional[bool]
    if isBoolean(value):
        return value.getValue()
    else:
        None


def getBooleanField(field):
    # type: (SMCApi.ObjectField) -> Optional[bool]
    if isBooleanField(field):
        return field.getValue()
    else:
        None


def getObjectArray(value):
    # type: (SMCApi.IValue) -> Optional[SMCApi.ObjectArray]
    if isObjectArray(value):
        return value.getValue()
    else:
        None


def getObjectArrayField(field):
    # type: (SMCApi.ObjectField) -> Optional[SMCApi.ObjectArray]
    if isObjectArrayField(field):
        return field.getValue()
    else:
        return None


def getObjectElement(field):
    # type: (SMCApi.ObjectField) -> Optional[SMCApi.ObjectElement]
    if field is None or field.getValue() is None:
        return None
    if field.getType() == SMCApi.ObjectType.OBJECT_ARRAY:
        if len(field.getValue().objects) > 0 and field.getValue().getType() == SMCApi.ObjectType.OBJECT_ELEMENT:
            return field.getValue().objects[0]
    elif field.getType() == SMCApi.ObjectType.OBJECT_ELEMENT:
        return field.getValue()
    return None


def getObjectElements(field):
    # type: (SMCApi.ObjectField) -> Optional[List[SMCApi.ObjectElement]]
    if field is None or field.getValue() is None:
        return None
    if field.getType() == SMCApi.ObjectType.OBJECT_ARRAY:
        if field.getValue().getType() == SMCApi.ObjectType.OBJECT_ELEMENT:
            return list(field.getValue().objects)
    elif field.getType() == SMCApi.ObjectType.OBJECT_ELEMENT:
        return list(field.getValue())
    return None


def toString(value):
    # type: (SMCApi.IValue) -> str
    if value is None:
        return ""
    if value.getType() == SMCApi.ValueType.STRING:
        return value.getValue()
    elif value.getType() == SMCApi.ValueType.BYTES:
        return base64.b64encode(value.getValue())
    else:
        return str(value.getValue())


def toStringField(field):
    # type: (SMCApi.ObjectField) -> str
    if field is None or field.getValue() is None:
        return ""
    if field.getType() == SMCApi.ObjectType.STRING:
        return field.getValue()
    elif field.getType() == SMCApi.ObjectType.BYTES:
        return base64.b64encode(field.getValue())
    else:
        return str(field.getValue())


def toNumber(value):
    # type: (SMCApi.IValue) -> int or long or float
    if value is None:
        return 0
    if value.getType() == SMCApi.ValueType.STRING:
        str = getString(value)
        if len(str) > 0:
            try:
                if "." in str:
                    return float(str)
                else:
                    return long(getString(value))
            except:
                return 0
        return 0
    elif value.getType() == SMCApi.ValueType.BOOLEAN:
        if getBoolean(value):
            return 1
        else:
            return 0
    elif value.getType() == SMCApi.ValueType.BYTES:
        return len(getBytes(value))
    elif value.getType() == SMCApi.ValueType.OBJECT_ARRAY:
        return getObjectArray(value).size()
    else:
        return value.getValue()


def toNumberField(field):
    # type: (SMCApi.ObjectField) -> int or long or float
    if field is None or field.getValue() is None:
        return 0
    if field.getType() == SMCApi.ObjectType.STRING:
        try:
            return float(getStringField(field))
        except:
            return long(getStringField(field))
    elif field.getType() == SMCApi.ObjectType.BOOLEAN:
        if getBooleanField(field):
            return 1
        else:
            return 0
    elif field.getType() == SMCApi.ObjectType.BYTES:
        return len(getBytesField(field))
    elif field.getType() == SMCApi.ObjectType.OBJECT_ARRAY:
        return getObjectArrayField(field).size()
    elif field.getType() == SMCApi.ObjectType.OBJECT_ARRAY:
        return len(getObjectElement(field).getFields())
    else:
        return field.getValue()


def toBoolean(value):
    # type: (SMCApi.IValue) -> bool
    if value is None:
        return False
    if value.getType() == SMCApi.ValueType.STRING:
        try:
            return bool(getString(value))
        except:
            return False
    elif value.getType() == SMCApi.ValueType.BOOLEAN:
        return getBoolean(value)
    elif value.getType() == SMCApi.ValueType.BYTES or value.getType() == SMCApi.ValueType.OBJECT_ARRAY:
        return True
    else:
        return getNumber(value) > 0


def toBooleanField(field):
    # type: (SMCApi.ObjectField) -> bool
    if field is None or field.getValue() is None:
        return False
    if field.getType() == SMCApi.ObjectType.STRING:
        try:
            return bool(getStringField(field))
        except:
            return False
    elif field.getType() == SMCApi.ObjectType.BOOLEAN:
        return getBooleanField(field)
    elif field.getType() == SMCApi.ObjectType.BYTES or field.getType() == SMCApi.ObjectType.OBJECT_ARRAY:
        return True
    else:
        return getNumberField(field) > 0


def toObjectArray(value):
    # type: (SMCApi.IValue) -> SMCApi.ObjectArray
    if value is None:
        return SMCApi.ObjectArray()
    if value.getType() == SMCApi.ValueType.OBJECT_ARRAY:
        return getObjectArray(value)
    else:
        return SMCApi.ObjectArray(convertToObjectType(value.getType()), [value.getValue()])


def toObjectArrayField(field):
    # type: (SMCApi.ObjectField) -> SMCApi.ObjectArray
    if field is None or field.getValue() is None:
        return SMCApi.ObjectArray()
    if field.getType() == SMCApi.ObjectType.OBJECT_ARRAY:
        return getObjectArrayField(field)
    elif field.getType() == SMCApi.ObjectType.OBJECT_ELEMENT:
        return SMCApi.ObjectArray(SMCApi.ObjectType.OBJECT_ELEMENT, [getObjectElement(field)])
    else:
        return SMCApi.ObjectArray(field.getType(), [field.getValue()])


def toObjectElement(value):
    # type: (SMCApi.IValue) -> SMCApi.ObjectElement
    if value is None:
        return SMCApi.ObjectElement()
    if value.getType() == SMCApi.ValueType.OBJECT_ARRAY:
        array = getObjectArray(value)
        if isArrayContainObjectElements(array):
            return array.get(0)
        elif array.isSimple() and array.size() > 0:
            element = SMCApi.ObjectElement()
            for i in range(array.size()):
                element.getFields().append(SMCApi.ObjectField(str(i), array.get(i), array.getType()))
        else:
            return SMCApi.ObjectElement()
    else:
        return SMCApi.ObjectElement([SMCApi.ObjectField("0", value.getValue(), convertToObjectType(value.getType()))])


def toObjectElementField(field):
    # type: (SMCApi.ObjectField) -> SMCApi.ObjectElement
    if field is None or field.getValue() is None:
        return SMCApi.ObjectElement()
    if field.getType() == SMCApi.ObjectType.OBJECT_ARRAY:
        array = getObjectArrayField(field)
        if isArrayContainObjectElements(array):
            return array.get(0)
        elif array.isSimple() and array.size() > 0:
            element = SMCApi.ObjectElement()
            for i in range(array.size()):
                element.getFields().append(SMCApi.ObjectField(str(i), array.get(i), array.getType()))
        else:
            return SMCApi.ObjectElement()
    elif field.getType() == SMCApi.ObjectType.OBJECT_ELEMENT:
        return getObjectElement(field)
    else:
        return SMCApi.ObjectElement([SMCApi.ObjectField(field.getName(), field.getValue(), field.getType())])


ObjectTypePrivate = Enum('OBJECT_ARRAY', 'OBJECT_ELEMENT', 'OBJECT_ELEMENT_SIMPLE', 'VALUE_ANY', 'STRING', 'BYTE', 'SHORT', 'INTEGER', 'LONG',
                         'FLOAT', 'DOUBLE', 'BIG_INTEGER', 'BIG_DECIMAL', 'BYTES', 'OBJECT_ELEMENT_OPTIMIZED', 'OBJECT_ELEMENT_SIMPLE_OPTIMIZED',
                         'BOOLEAN',
                         'STRING_NULL', 'BYTE_NULL', 'SHORT_NULL', 'INTEGER_NULL', 'LONG_NULL', 'FLOAT_NULL', 'DOUBLE_NULL',
                         'BIG_INTEGER_NULL', 'BIG_DECIMAL_NULL', 'BYTES_NULL', 'BOOLEAN_NULL')
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
ObjectTypePrivate.BOOLEAN.value = 16
ObjectTypePrivate.STRING_NULL.value = 17
ObjectTypePrivate.BYTE_NULL.value = 18
ObjectTypePrivate.SHORT_NULL.value = 19
ObjectTypePrivate.INTEGER_NULL.value = 20
ObjectTypePrivate.LONG_NULL.value = 21
ObjectTypePrivate.FLOAT_NULL.value = 22
ObjectTypePrivate.DOUBLE_NULL.value = 23
ObjectTypePrivate.BIG_INTEGER_NULL.value = 24
ObjectTypePrivate.BIG_DECIMAL_NULL.value = 25
ObjectTypePrivate.BYTES_NULL.value = 26
ObjectTypePrivate.BOOLEAN_NULL.value = 27


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
        return SMCApi.ObjectType[SMCApi.ObjectType._keys.index(typePrivate.key.replace("_NULL", ""))]


def convertToObjectTypePrivate(type, isNull=False):
    # type: (SMCApi.ObjectType, bool) -> ObjectTypePrivate
    if type == SMCApi.ObjectType.OBJECT_ARRAY:
        return ObjectTypePrivate.OBJECT_ARRAY
    elif type == SMCApi.ObjectType.OBJECT_ELEMENT:
        return ObjectTypePrivate.OBJECT_ELEMENT
    elif type == SMCApi.ObjectType.VALUE_ANY:
        return ObjectTypePrivate.VALUE_ANY
    elif type == SMCApi.ObjectType.STRING:
        if isNull:
            return ObjectTypePrivate.STRING_NULL
        else:
            return ObjectTypePrivate.STRING
    elif type == SMCApi.ObjectType.BYTE:
        if isNull:
            return ObjectTypePrivate.BYTE_NULL
        else:
            return ObjectTypePrivate.BYTE
    elif type == SMCApi.ObjectType.SHORT:
        if isNull:
            return ObjectTypePrivate.SHORT_NULL
        else:
            return ObjectTypePrivate.SHORT
    elif type == SMCApi.ObjectType.INTEGER:
        if isNull:
            return ObjectTypePrivate.INTEGER_NULL
        else:
            return ObjectTypePrivate.INTEGER
    elif type == SMCApi.ObjectType.LONG:
        if isNull:
            return ObjectTypePrivate.LONG_NULL
        else:
            return ObjectTypePrivate.LONG
    elif type == SMCApi.ObjectType.FLOAT:
        if isNull:
            return ObjectTypePrivate.FLOAT_NULL
        else:
            return ObjectTypePrivate.FLOAT
    elif type == SMCApi.ObjectType.DOUBLE:
        if isNull:
            return ObjectTypePrivate.DOUBLE_NULL
        else:
            return ObjectTypePrivate.DOUBLE
    elif type == SMCApi.ObjectType.BIG_INTEGER:
        if isNull:
            return ObjectTypePrivate.BIG_INTEGER_NULL
        else:
            return ObjectTypePrivate.BIG_INTEGER
    elif type == SMCApi.ObjectType.BIG_DECIMAL:
        if isNull:
            return ObjectTypePrivate.BIG_DECIMAL_NULL
        else:
            return ObjectTypePrivate.BIG_DECIMAL
    elif type == SMCApi.ObjectType.BYTES:
        if isNull:
            return ObjectTypePrivate.BYTES_NULL
        else:
            return ObjectTypePrivate.BYTES
    elif type == SMCApi.ObjectType.BOOLEAN:
        if isNull:
            return ObjectTypePrivate.BOOLEAN_NULL
        else:
            return ObjectTypePrivate.BOOLEAN
    return ObjectTypePrivate[ObjectTypePrivate._keys.index(type.key)]


def deserializeToObject(messages, silent=True):
    # type: (List[SMCApi.IMessage], bool) -> SMCApi.ObjectArray
    """
     * deserialize messages to object array
     * if first message type ObjectArray, when return it
     * use object serialization format
     * @formatter:off
     * object serialization format:
     *      number - type of elements, may by: 0-ObjectArray, 1-ObjectElement, 2-ObjectElementSimple, 3-AnySimpleTypes, 4-String, 5-Byte, 6-Short, 7-Integer, 8-Long, 9-Float, 10-Double, 11-BigInteger, 12-BigDecimal, 13-byte[], 14-OBJECT_ELEMENT_OPTIMIZED, 15-OBJECT_ELEMENT_SIMPLE_OPTIMIZED, 16-Boolean
     *      number - number of item in array
     *      items. depend of type. format:
     *          if item type is 0 (ObjectArray): then list of arrays. each has format described above, recursion.
     *          if item type is 1 (ObjectElement): then list of objects:
     *              if all elements hase same fields and size>1 then:
     *                  number - number of fields in object.
     *                  list of fields. format:
     *                      string - field name.
     *                      number - field type, may by: 0-ObjectArray, 1-ObjectElement, 2-ObjectElementSimple, 3-AnySimpleTypes, 4-String, 5-Byte, 6-Short, 7-Integer, 8-Long, 9-Float, 10-Double, 11-BigInteger, 12-BigDecimal, 13-byte[], 16-Boolean
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
     *                          number - field type, may by: 0-ObjectArray, 1-ObjectElement, 2-ObjectElementSimple, 3-AnySimpleTypes, 4-String, 5-Byte, 6-Short, 7-Integer, 8-Long, 9-Float, 10-Double, 11-BigInteger, 12-BigDecimal, 13-byte[], 16-Boolean
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
     * @formatter:on

    :param messages:
    :return:
    """
    message = None
    if messages and len(messages) > 0:
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
    typePrivate = ObjectTypePrivate[typeId]
    messages.pop(0)
    # type = ObjectType[typeId]

    size = getNumber(messages[0])
    if size is None:
        messages.insert(0, message)
        return objectArray
    messages.pop(0)
    count = size

    type = convertFromObjectTypePrivate(typePrivate)
    objectArray = SMCApi.ObjectArray(type)

    try:
        if typePrivate == ObjectTypePrivate.OBJECT_ARRAY:
            for i in range(count):
                objectArray.add(deserializeToObject(messages, silent))
        elif typePrivate == ObjectTypePrivate.OBJECT_ELEMENT:
            for i in range(count):
                objectArray.add(deserializeToObjectElement(messages, -1, None, silent))
        elif typePrivate == ObjectTypePrivate.OBJECT_ELEMENT_SIMPLE:
            if messages is None or len(messages) < 1:
                return objectArray
            message = messages[0]
            countFields = getNumber(message)
            if countFields is not None:
                messages.pop(0)
                for i in range(count):
                    objectArray.add(deserializeToObjectElement(messages, countFields, None, silent))
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
                messages.pop(0)
                message = messages[0]
                fieldTypeId = getNumber(message)
                if fieldTypeId is None or fieldTypeId < 0 or len(ObjectTypePrivate) <= fieldTypeId:
                    hasErrors = True
                    break
                messages.pop(0)
                definedFields.append(ObjectValuePrivate(fieldName, ObjectTypePrivate[fieldTypeId]))
            if hasErrors:
                return objectArray

            for i in range(count):
                objectArray.add(deserializeToObjectElement(messages, -1, definedFields, silent))

        elif typePrivate == ObjectTypePrivate.OBJECT_ELEMENT_SIMPLE_OPTIMIZED:
            if messages is None or len(messages) < 1:
                return objectArray
            message = messages[0]
            countFields = getNumber(message)
            if countFields is None or len(messages) <= countFields * 2 + 1:
                return objectArray
            messages.pop(0)

            definedFields = []
            for i in range(countFields):
                definedFields.append(ObjectValuePrivate(toString(messages.pop(0)), ObjectTypePrivate.VALUE_ANY))

            for i in range(count):
                objectArray.add(deserializeToObjectElement(messages, -1, definedFields, silent))
        else:
            for i in range(count):
                objectArray.add(messages.pop(0).getValue())
    except Exception as e:
        if not silent:
            raise Exception(e)
    return objectArray


def deserializeToObjectElement(messages, countFields=-1, definedFields=None, silent=True):
    # type: (List[SMCApi.IMessage], int, List[ObjectValuePrivate], bool) -> SMCApi.ObjectElement
    message = messages[0]
    objectElement = SMCApi.ObjectElement()
    if isObjectArray(message):
        objectArray = getObjectArray(messages.pop(0))
        if isArrayContainObjectElements(objectArray):
            return objectArray.get(0)
        return objectElement

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
                deserializeToObjectElementValue(messages, objectElement, field.getName(), field.getType(), silent)
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
                deserializeToObjectElementValue(messages, objectElement, fieldName, type, silent)
    except Exception as e:
        if not silent:
            raise Exception(e)

    return objectElement


def deserializeToObjectElementValue(messages, objectElement, fieldName, type, silent=True):
    # type: (List[SMCApi.IMessage], SMCApi.ObjectElement, str, ObjectTypePrivate, bool) -> None
    if type == ObjectTypePrivate.OBJECT_ARRAY:
        objectElement.fields.append(SMCApi.ObjectField(fieldName, deserializeToObject(messages, silent)))
    elif type == ObjectTypePrivate.OBJECT_ELEMENT:
        objectElement.fields.append(SMCApi.ObjectField(fieldName, deserializeToObjectElement(messages, -1, None, silent)))
    elif type == ObjectTypePrivate.OBJECT_ELEMENT_SIMPLE:
        countFields2 = getNumber(messages[0])
        if countFields2 is not None:
            messages.pop(0)
            objectElement.fields.append(SMCApi.ObjectField(fieldName, deserializeToObjectElement(messages, countFields2, None, silent)))
    elif type == ObjectTypePrivate.OBJECT_ELEMENT_OPTIMIZED:
        return
    elif type == ObjectTypePrivate.OBJECT_ELEMENT_SIMPLE_OPTIMIZED:
        return
    elif type == ObjectTypePrivate.STRING_NULL:
        objectElement.fields.append(SMCApi.ObjectField(fieldName, None, SMCApi.ObjectType.STRING))
    elif type == ObjectTypePrivate.BYTE_NULL:
        objectElement.fields.append(SMCApi.ObjectField(fieldName, None, SMCApi.ObjectType.BYTE))
    elif type == ObjectTypePrivate.SHORT_NULL:
        objectElement.fields.append(SMCApi.ObjectField(fieldName, None, SMCApi.ObjectType.SHORT))
    elif type == ObjectTypePrivate.INTEGER_NULL:
        objectElement.fields.append(SMCApi.ObjectField(fieldName, None, SMCApi.ObjectType.INTEGER))
    elif type == ObjectTypePrivate.LONG_NULL:
        objectElement.fields.append(SMCApi.ObjectField(fieldName, None, SMCApi.ObjectType.LONG))
    elif type == ObjectTypePrivate.FLOAT_NULL:
        objectElement.fields.append(SMCApi.ObjectField(fieldName, None, SMCApi.ObjectType.FLOAT))
    elif type == ObjectTypePrivate.DOUBLE_NULL:
        objectElement.fields.append(SMCApi.ObjectField(fieldName, None, SMCApi.ObjectType.DOUBLE))
    elif type == ObjectTypePrivate.BIG_INTEGER_NULL:
        objectElement.fields.append(SMCApi.ObjectField(fieldName, None, SMCApi.ObjectType.BIG_INTEGER))
    elif type == ObjectTypePrivate.BIG_DECIMAL_NULL:
        objectElement.fields.append(SMCApi.ObjectField(fieldName, None, SMCApi.ObjectType.BIG_DECIMAL))
    elif type == ObjectTypePrivate.BYTES_NULL:
        objectElement.fields.append(SMCApi.ObjectField(fieldName, None, SMCApi.ObjectType.BYTES))
    elif type == ObjectTypePrivate.BOOLEAN_NULL:
        objectElement.fields.append(SMCApi.ObjectField(fieldName, None, SMCApi.ObjectType.BOOLEAN))
    else:
        objectElement.fields.append(SMCApi.ObjectField(fieldName, messages.pop(0).getValue()))


def serializeFromObject(objectArray, silent=True):
    # type: (SMCApi.ObjectArray, bool) -> List[object]
    """
     * serialize objects to messages
     * use object serialization format
     * @formatter:off
     * object serialization format:
     *      number - type of elements, may by: 0-ObjectArray, 1-ObjectElement, 2-ObjectElementSimple, 3-AnySimpleTypes, 4-String, 5-Byte, 6-Short, 7-Integer, 8-Long, 9-Float, 10-Double, 11-BigInteger, 12-BigDecimal, 13-byte[], 14-OBJECT_ELEMENT_OPTIMIZED, 15-OBJECT_ELEMENT_SIMPLE_OPTIMIZED, 16-Boolean
     *      number - number of item in array
     *      items. depend of type. format:
     *          if item type is 0 (ObjectArray): then list of arrays. each has format described above, recursion.
     *          if item type is 1 (ObjectElement): then list of objects:
     *              if all elements hase same fields and size>1 then:
     *                  number - number of fields in object.
     *                  list of fields. format:
     *                      string - field name.
     *                      number - field type, may by: 0-ObjectArray, 1-ObjectElement, 2-ObjectElementSimple, 3-AnySimpleTypes, 4-String, 5-Byte, 6-Short, 7-Integer, 8-Long, 9-Float, 10-Double, 11-BigInteger, 12-BigDecimal, 13-byte[], 16-Boolean
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
     *                          number - field type, may by: 0-ObjectArray, 1-ObjectElement, 2-ObjectElementSimple, 3-AnySimpleTypes, 4-String, 5-Byte, 6-Short, 7-Integer, 8-Long, 9-Float, 10-Double, 11-BigInteger, 12-BigDecimal, 13-byte[], 16-Boolean
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
     * @formatter:on

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

    try:
        hasFieldWithNull = False
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
                    for field in obj.fields:
                        if field.getValue() is None:
                            isSimple = False
                            hasFieldWithNull = True
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
                listExtend(result, serializeFromObject(obj, silent))
        elif typePrivate == ObjectTypePrivate.OBJECT_ELEMENT:
            definedFields = None
            if not hasFieldWithNull and count > 1 and isSameFields(objectArray):
                definedFields = []
                objectElement = objectArray.get(0)
                for field in objectElement.getFields():
                    definedFields.append(ObjectValuePrivate(field.getName(), convertToObjectTypePrivate(field.getType())))
                result = [ObjectTypePrivate.OBJECT_ELEMENT_OPTIMIZED.index, count, len(definedFields)]
                for field in definedFields:
                    result.append(field.name)
                    result.append(field.type.index)
            for obj in objectArray.objects:
                listExtend(result, serializeFromObjectElement(obj, False, definedFields, silent))
        elif typePrivate == ObjectTypePrivate.OBJECT_ELEMENT_SIMPLE:
            definedFields = None
            if count > 1 and isSameFields(objectArray):
                definedFields = []
                objectElement = objectArray.get(0)
                for field in objectElement.getFields():
                    definedFields.append(ObjectValuePrivate(field.getName(), None))
                result = [ObjectTypePrivate.OBJECT_ELEMENT_SIMPLE_OPTIMIZED.index, count, len(definedFields)]
                for field in definedFields:
                    result.append(field.name)
            else:
                if count > 0:
                    result.append(len(objectArray.get(0).getFields()))
                else:
                    result.append(0)
            for obj in objectArray.objects:
                listExtend(result, serializeFromObjectElement(obj, True, definedFields, silent))
        else:
            for obj in objectArray.objects:
                result.append(obj)
    except Exception as e:
        if not silent:
            raise Exception(e)
    return result


def serializeFromObjectElement(objectElement, isSimple=False, definedFields=None, silent=True):
    # type: (SMCApi.ObjectElement, bool, List[ObjectValuePrivate], bool) -> List[object]
    result = []
    if objectElement is None:
        return result
    try:
        if definedFields is not None:
            # because its check
            for field in objectElement.getFields():
                listExtend(result, serializeFromObjectFieldValue(field.getType(), field.getValue(), silent))
        else:
            if not isSimple:
                result.append(len(objectElement.getFields()))

            for f in objectElement.getFields():
                result.append(f.getName())
                if not isSimple:
                    result.append(convertToObjectTypePrivate(f.getType(), f.getValue() is None).index)
                if f.getValue() is not None:
                    listExtend(result, serializeFromObjectFieldValue(f.getType(), f.getValue(), silent))
    except Exception as e:
        if not silent:
            raise Exception(e)
    return result


def serializeFromObjectFieldValue(type, value, silent=True):
    # type: (SMCApi.ObjectType, object, bool) -> List[object]
    if type == SMCApi.ObjectType.OBJECT_ARRAY:
        return serializeFromObject(value, silent)
    elif type == SMCApi.ObjectType.OBJECT_ELEMENT:
        if value.isSimple():
            lst = []
            lst.append(len(value.getFields()))
            listExtend(lst, serializeFromObjectElement(value, True, None, silent))
            return lst
        else:
            return serializeFromObjectElement(value, False, None, silent)
    else:
        return [value]


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


def hasErrorsInAction(action):
    # type: (SMCApi.IAction) -> bool
    if action is None:
        return False
    return len(action.getMessages()) > 0 and any(
        message.getMessageType() == SMCApi.MessageType.ERROR or message.getMessageType() == SMCApi.MessageType.ACTION_ERROR for message in
        action.getMessages())


def hasDataInAction(action):
    # type: (SMCApi.IAction) -> bool
    if action is None:
        return False
    return len(action.getMessages()) > 0 and any(message.getMessageType() == SMCApi.MessageType.DATA for message in action.getMessages())


def getErrorsInAction(action):
    # type: (SMCApi.IAction) -> [SMCApi.IMessage]
    if action is None:
        return []
    return filter(lambda message: message.getMessageType() == SMCApi.MessageType.ERROR or message.getMessageType() == SMCApi.MessageType.ACTION_ERROR,
                  action.getMessages())


def getErrors(command):
    # type: (SMCApi.ICommand) -> [SMCApi.IMessage]
    if command is None:
        return []
    result = []
    for i in range(len(command.getActions())):
        lst = getErrorsInAction(command.getActions()[i])
        if lst:
            listExtend(result, lst)
    return result


def getDataInAction(action):
    # type: (SMCApi.IAction) -> [SMCApi.IMessage]
    if action is None:
        return []
    return filter(lambda message: message.getMessageType() == SMCApi.MessageType.DATA, action.getMessages())


def getData(command):
    # type: (SMCApi.ICommand) -> [SMCApi.IMessage]
    if command is None:
        return []
    result = []
    for i in range(len(command.getActions())):
        lst = getDataInAction(command.getActions()[i])
        if lst:
            listExtend(result, lst)
    return result


def isSameFields(objectArray):
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


def splitFieldNames(fieldPath):
    # type: (str) -> [str]
    return fieldPath.split(".")


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
            objectArray.getType() == SMCApi.ObjectType.VALUE_ANY or objectArray.getType() == SMCApi.ObjectType.STRING)


def isArrayContainBytes(objectArray):
    # type: (SMCApi.ObjectArray) -> bool
    return objectArray is not None and len(objectArray.objects) > 0 and (
            objectArray.getType() == SMCApi.ObjectType.VALUE_ANY or objectArray.getType() == SMCApi.ObjectType.BYTES)


def isArrayContainBoolean(objectArray):
    # type: (SMCApi.ObjectArray) -> bool
    return objectArray is not None and len(objectArray.objects) > 0 and (
            objectArray.getType() == SMCApi.ObjectType.VALUE_ANY or objectArray.getType() == SMCApi.ObjectType.BOOLEAN)


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
    if value is None:
        return None
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
    elif valueType is bool:
        return SMCApi.ValueType.BOOLEAN
    elif valueType is SMCApi.ObjectArray:
        return SMCApi.ValueType.OBJECT_ARRAY
    else:
        raise ValueError("wrong type")


def getObjectType(value):
    # type: (object) -> SMCApi.ObjectType
    valueType = type(value)
    if value is None:
        return None
    if valueType is SMCApi.ObjectElement:
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
    elif type == SMCApi.ValueType.BOOLEAN:
        return SMCApi.ObjectType.BOOLEAN
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
    elif type == SMCApi.ObjectType.BOOLEAN:
        return SMCApi.ValueType.BOOLEAN
    return None


def executeParallel(executionContextTool, ecId, params, maxWorkIntervalMs=0, sleepTimeMs=50):
    # type: (SMCApi.ExecutionContextTool, int, List[object], long, int) -> long
    maxWorkIntervalInt = 0
    if maxWorkIntervalMs > 0:
        maxWorkIntervalInt = maxWorkIntervalMs / 1000
    threadId = executionContextTool.getFlowControlTool().executeParallel(SMCApi.CommandType.EXECUTE, [ecId], params, 0, maxWorkIntervalInt)
    waitThread(executionContextTool, threadId, sleepTimeMs)
    return threadId


def waitThread(executionContextTool, threadId, sleepTime, needRelease=False):
    # type: (SMCApi.ExecutionContextTool, long, int, bool) -> None
    sleepTimeMs = sleepTime / 1000.0
    while not executionContextTool.isNeedStop() and executionContextTool.getFlowControlTool().isThreadActive(threadId):
        time.sleep(sleepTimeMs)
    if needRelease:
        executionContextTool.getFlowControlTool().releaseThread(threadId)


def getFirstActionWithData(actions):
    # type: (List[SMCApi.IAction]) -> Optional[SMCApi.IAction]
    for i in range(len(actions)):
        action = actions[i]
        if hasDataInAction(action):
            return action
    return None


def getFirstActionWithDataFromCommands(commands):
    # type: (List[SMCApi.ICommand]) -> Optional[SMCApi.IAction]
    for i in range(len(commands)):
        command = commands[i]
        action = getFirstActionWithData(command.getActions())
        if action:
            return action
    return None


def getLastActionWithData(actions):
    # type: (List[SMCApi.IAction]) -> Optional[SMCApi.IAction]
    for i in range(len(actions) - 1, -1, -1):
        action = actions[i]
        if hasDataInAction(action):
            return action
    return None


def getLastActionWithDataFromCommands(commands):
    # type: (List[SMCApi.ICommand]) -> Optional[SMCApi.IAction]
    for i in range(len(commands) - 1, -1, -1):
        command = commands[i]
        action = getLastActionWithData(command.getActions())
        if action:
            return action
    return None


def getFirstActionExecuteWithMessages(actions):
    # type: (List[SMCApi.IAction]) -> Optional[SMCApi.IAction]
    for i in range(len(actions)):
        action = actions[i]
        if action.getType() == SMCApi.ActionType.EXECUTE and len(action.getMessages()) > 0:
            return action
    return None


def getFirstActionExecuteWithMessagesFromCommands(commands):
    # type: (List[SMCApi.ICommand]) -> Optional[SMCApi.IAction]
    for i in range(len(commands)):
        command = commands[i]
        action = getFirstActionExecuteWithMessages(command.getActions())
        if action:
            return action
    return None


def getLastActionWithMessages(actions):
    # type: (List[SMCApi.IAction]) -> Optional[SMCApi.IAction]
    for i in range(len(actions) - 1, -1, -1):
        action = actions[i]
        if action.getType() == SMCApi.ActionType.EXECUTE and len(action.getMessages()) > 0:
            return action
    return None


def getLastActionWithMessagesFromCommands(commands):
    # type: (List[SMCApi.ICommand]) -> Optional[SMCApi.IAction]
    for i in range(len(commands) - 1, -1, -1):
        command = commands[i]
        action = getLastActionWithMessages(command.getActions())
        if action:
            return action
    return None


def listExtend(list, list2):
    # type: (List, List) -> List
    for i in range(len(list2)):
        list.append(list2[i])
    return list


def getElements(actions):
    # type: (List[SMCApi.IAction]) -> Optional[SMCApi.ObjectArray]
    action = getFirstActionWithData(actions)
    if action:
        array = deserializeToObject(action.getMessages()[:])
        if isArrayContainObjectElements(array):
            return array
    return None


def getElement(actions):
    # type: (List[SMCApi.IAction]) -> Optional[SMCApi.ObjectElement]
    array = getElements(actions)
    if array:
        return array.get(0)
    return None


def executeAndGetElement(executionContextTool, id, params):
    # type: (SMCApi.ExecutionContextTool, int, List) -> Optional[SMCApi.ObjectElement]
    return getElement(executeAndGet(executionContextTool, id, params))


def executeAndGetArrayElements(executionContextTool, id, params):
    # type: (SMCApi.ExecutionContextTool, int, List) -> Optional[SMCApi.ObjectArray]
    return getElements(executeAndGet(executionContextTool, id, params))


def executeAndGetMessages(executionContextTool, id, params):
    # type: (SMCApi.ExecutionContextTool, int, List) -> Optional[List[SMCApi.IMessage]]
    action = getFirstActionWithData(executeAndGet(executionContextTool, id, params))
    if action:
        return action.getMessages()
    return None


def executeAndGet(executionContextTool, id, params):
    # type: (SMCApi.ExecutionContextTool, int, List) -> List[SMCApi.IAction]
    executionContextTool.getFlowControlTool().executeNow(SMCApi.CommandType.EXECUTE, id, params)
    return executionContextTool.getFlowControlTool().getMessagesFromExecuted(0, id)


def executeParallelAndGetArrayElements(executionContextTool, id, params):
    # type: (SMCApi.ExecutionContextTool, int, List) -> Optional[SMCApi.ObjectArray]
    return getElements(executeParallelAndGet(executionContextTool, id, params))


def executeParallelAndGetElement(executionContextTool, id, params):
    # type: (SMCApi.ExecutionContextTool, int, List) -> Optional[SMCApi.ObjectElement]
    return getElement(executeParallelAndGet(executionContextTool, id, params))


def executeParallelAndGetMessages(executionContextTool, id, params):
    # type: (SMCApi.ExecutionContextTool, int, List) -> Optional[List[SMCApi.IMessage]]
    action = getFirstActionWithData(executeParallelAndGet(executionContextTool, id, params))
    if action:
        return action.getMessages()
    return None


def executeParallelAndGet(executionContextTool, id, params):
    # type: (SMCApi.ExecutionContextTool, int, List) -> List[SMCApi.IAction]
    threadId = executeParallel(executionContextTool, id, params)
    data = executionContextTool.getFlowControlTool().getMessagesFromExecuted(threadId, id)
    executionContextTool.getFlowControlTool().releaseThread(threadId)
    return data


def getStackTraceAsString(e):
    # type: (Exception) -> str
    # return traceback.print_tb(e.__traceback__)
    # parts = ["Traceback (most recent call last):\n"]
    parts = []
    listExtend(parts, traceback.format_stack(limit=25)[:-2])
    listExtend(parts, traceback.format_exception(*sys.exc_info())[1:])
    return "".join(parts)


def getErrorMessageOrClassName(e):
    # type: (Exception) -> str
    ex_type, ex_value, ex_traceback = sys.exc_info()
    # repr(e)
    if ex_value:
        return ex_value
    elif ex_traceback:
        return ex_value
    else:
        return ""


def getMessages(executionContextTool):
    # type: (SMCApi.ExecutionContextTool) -> List[List[List[SMCApi.IMessage]]]
    result = []
    for i in range(executionContextTool.countSource()):
        actions = executionContextTool.getMessages(i)
        actionsResult = []
        for j in range(len(actions)):
            action = actions[j]
            if len(action.getMessages()) > 0:
                actionsResult.append(action.getMessages())
        result.append(actionsResult)
    return result


def getLastMessages(executionContextTool):
    # type: (SMCApi.ExecutionContextTool) -> List[List[SMCApi.IMessage]]
    result = []
    for i in range(executionContextTool.countSource()):
        actions = executionContextTool.getMessages(i)
        if len(actions) > 0:
            action = actions[-1]
            if hasDataInAction(action):
                result.append(action.getMessages())
        else:
            result.append([])
    return result


def getMessagesJoin(executionContextTool):
    # type: (SMCApi.ExecutionContextTool) -> List[SMCApi.IMessage]
    result = []
    for i in range(executionContextTool.countSource()):
        actions = executionContextTool.getMessages(i)
        for j in range(len(actions)):
            action = actions[j]
            if len(action.getMessages()) > 0:
                listExtend(result, action.getMessages())
    return result


def processMessages(configurationTool, executionContextTool, func):
    # type: (SMCApi.ConfigurationTool, SMCApi.ExecutionContextTool, Callable[[int, List[SMCApi.IMessage]], None]) -> None
    for i in range(executionContextTool.countSource()):
        processMessagesInEc(configurationTool, executionContextTool, i, func)


def processMessagesInEc(configurationTool, executionContextTool, id, func):
    # type: (SMCApi.ConfigurationTool, SMCApi.ExecutionContextTool, int, Callable[[int, List[SMCApi.IMessage]], None]) -> None
    if executionContextTool.countSource() > id:
        actions = executionContextTool.getMessages(id)
        for i in range(len(actions)):
            executor(configurationTool, executionContextTool, id, actions[i][:], func)
    else:
        executor(configurationTool, executionContextTool, id, None, func)


def executor(configurationTool, executionContextTool, id, messages, func):
    # type: (SMCApi.ConfigurationTool, SMCApi.ExecutionContextTool, int, object, Callable[[int, object], None]) -> None
    try:
        func(id, messages)
    except Exception as e:
        executionContextTool.addError(getErrorMessageOrClassName(e))
        configurationTool.loggerWarn(getStackTraceAsString(e))


def processMessagesAll(configurationTool, executionContextTool, func):
    # type: (SMCApi.ConfigurationTool, SMCApi.ExecutionContextTool, Callable[[int, List[List[SMCApi.IMessage]]], None]) -> None
    data = []
    for i in range(executionContextTool.countSource()):
        action = getLastActionWithData(executionContextTool.getMessages(i))
        messages = []
        if len(action.getMessages()) > 0:
            messages = action.getMessages()[:]
        data.append(messages)
    executor(configurationTool, executionContextTool, -1, data, func)


class ObjectDict(dict):
    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value


def toList(objectArray):
    # type: (SMCApi.ObjectArray) -> List[SMCApi.ObjectElement]
    list = []
    if not isArrayContainObjectElements(objectArray):
        return list
    for i in range(objectArray.size()):
        list.append(objectArray.get(i))
    return list


def convertFromObjectArray(objectArray, silent):
    # type: (SMCApi.ObjectArray, bool) -> List[ObjectDict]
    result = []
    if objectArray is None or type(objectArray) is not SMCApi.ObjectArray or objectArray.size() == 0:
        return result
    try:
        if objectArray.isSimple():
            result = toList(objectArray)
        elif isArrayContainArrays(objectArray):
            for i in range(objectArray.size()):
                arr = objectArray.get(i)  # type: SMCApi.ObjectArray
                if arr.isSimple():
                    result.append(toList(arr))
        elif isArrayContainObjectElements(objectArray):
            result = filter(lambda o: o is not None, map(lambda o: convertFromObjectElement(o, silent), toList(objectArray)))
    except Exception as e:
        if not silent:
            raise Exception(e)
    return result


def convertFromObjectElement(objectElement, silent):
    # type: (SMCApi.ObjectElement, bool) -> ObjectDict
    result = ObjectDict()
    if objectElement is None or type(objectElement) is not SMCApi.ObjectElement:
        return result
    try:
        for field in objectElement.getFields():
            typev = field.getType()
            value = field.getValue()
            if value is not None:
                if typev == SMCApi.ObjectType.OBJECT_ARRAY:
                    value = convertFromObjectArray(value, silent)
                elif typev == SMCApi.ObjectType.OBJECT_ELEMENT:
                    value = convertFromObjectElement(value, silent)
            setattr(result, field.getName(), value)
    except Exception as e:
        if not silent:
            raise Exception(e)
    return result
