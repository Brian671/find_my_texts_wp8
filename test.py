__author__ = 'Chris Ottersen'

from string import ascii_letters, digits, punctuation

hello = "H\x00E\x00L\x00L\x00O\x00\x00\x22\x00\x00"
assert isinstance(hello, str)


def test_fun(hello):
    """

    :param hello:
    :type hello:
    :return:
    :rtype:
    """
    s = "\x7F\x81abcdefg\x7F\x80\x00"
    print s
    s = s[-3:1:-1]
    print s
    #unicode(hello)
    print "%r" % hello
    hello = hello.decode('utf-16le')
    print "%r" % hello

    hello = hello.encode('ascii', 'xmlcharrefreplace')
    hello = hello.encode('ascii', 'xmlcharrefreplace')
    print "%r" % (hello)

#filename = r'i:\Python\test.file'
#file = open(filename, 'rb')
data = buffer(r"feafdsifosanfbavondsaovdponovidnsav")#file.read()
#file.close()

bytesRead = len(data)

def bufferToHex(buffer, start, count):
    accumulator = ''
    for item in range(count):
        accumulator += '%02X' % buffer[start + item] + ' '
    return accumulator

def bufferToAscii(buffer, start, count):
    accumulator = ''
    for item in range(count):
        char = chr(buffer[start + item])
        if char in ascii_letters or \
           char in digits or \
           char in punctuation or \
           char == ' ':
            accumulator += char
        else:
            accumulator += '.'
    return accumulator

index = 0
size = 20
hexFormat = '{:'+str(size*3)+'}'
asciiFormat = '{:'+str(size)+'}'

print()
while index < bytesRead:

    hex = bufferToHex(data, index, size)
    ascii = bufferToAscii(data, index, size)

    print(hexFormat.format(hex))
    print('|',asciiFormat.format(ascii),'|')

    index += size
    if bytesRead - index < size:
        size = bytesRead - index


test_fun(hello)