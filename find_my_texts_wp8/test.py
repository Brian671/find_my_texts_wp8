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
    print("%60r -> %30r" % ("s", s))

    s = s[-4:1:-1]
    print("%60r -> %30r" % ("s[-4:1:-1]", s))

    print("%60r -> %30r" % ("hello", hello))
    hello = hello.decode('utf-16le')
    print("%60r -> %30r" % ("hello.decode('utf-16le')", hello))

    hello = hello.encode('ascii', 'xmlcharrefreplace')
    print("%60r -> %30r" % ("hello.encode('ascii', 'xmlcharrefreplace')", hello))
    hello = hello.decode('ascii', 'xmlcharrefreplace')
    print("%60r -> %30r" % ("hello.decode('ascii', 'xmlcharrefreplace')", hello))

test_fun(hello)