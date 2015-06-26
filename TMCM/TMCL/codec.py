
from error import *


COMMAND_STRING_LENGTH = 9


def byte(n):
    """Convert n to byte in range(256)"""
    return int(n) % (1<<8)


def checksum(bytes):
    return byte(sum(bytes))


def encodeBytes(value, max_i=3):
    return [byte(int(value) >> i*8) for i in range(max_i, -1, -1)]

def decodeBytes(bytes, max_i=3):
    return sum(b << (max_i-i)*8 for i, b in enumerate(bytes))



def encodeRequestCommand(m_address, n_command, n_type, n_motor, value, debug=False):
    return encodeCommand([m_address, n_command, n_type, n_motor], value, debug)

def encodeReplyCommand(r_address, m_address, status, n_command, value, debug=False):
    return encodeCommand([r_address, m_address, status, n_command], value, debug)


def encodeCommand(parameters, value, debug):
    bytes = map(byte, parameters)
    value = encodeBytes(value)
    bytes += value
    chsum = checksum(bytes)
    bytes += [chsum]
    result = "".join([chr(b) for b in bytes])

    if debug:
        cmd = decodeBytes(bytes, max_i=8)
        print "{0:0>18X}".format(cmd), result
    return result



def decodeRequestCommand(cmd_string):
    byte_array = decodeCommand(cmd_string)
    ret = {}
    ret['module-address'] = byte_array[0]
    ret['command-number'] = byte_array[1]
    ret['type-number']    = byte_array[2]
    ret['motor-number']   = byte_array[3]
    ret['value']          = decodeBytes(byte_array[4:8])
    ret['checksum']       = byte_array[8]
    return ret

def decodeReplyCommand(cmd_string):
    byte_array = decodeCommand(cmd_string)
    ret = {}
    ret['reply-address']  = byte_array[0]
    ret['module-address'] = byte_array[1]
    ret['status']         = byte_array[2]
    ret['command-number'] = byte_array[3]
    ret['value']          = decodeBytes(byte_array[4:8])
    ret['checksum']       = byte_array[8]
    return ret


def decodeCommand(cmd_string):
    byte_array = bytearray(cmd_string)
    if len(byte_array) != COMMAND_STRING_LENGTH:
        raise TMCLError("Commandstring shorter than {} bytes".format(COMMAND_STRING_LENGTH))
    if byte_array[8] != checksum(byte_array[:8]):
        raise TMCLError("Checksum error in command {}".format(cmd_string))
    return byte_array


