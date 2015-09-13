#! /usr/bin/env python

import re
import os
import threading
import time
from . import *
from adrian import *

__author__ = 'Chris Ottersen'

''' :type : long '''
CHUNK_SIZE = 20000000
''' :type : long '''
DELTA = 100    # read this extra bit to catch any hits crossing chunk boundaries. Should be AT LEAST max size of record
# being searched for.


def regsearch(bigstring, pattern, offset=0, count=None, thread=None):
    """
    Written by: Adrian Leong
    Find all indices of the "pattern" regular expression in a given string (using regex)
    Where pattern is a compiled Python re pattern object (ie the output of "re.compile")


    Rewritten by: Chris Ottersen
    Changes:
    1. implemented multi-threading

    :param bigstring:
    :type bigstring: str
    :param pattern:
    :type pattern: re
    :param offset:
    :type offset: unsigned long
    :param count: list<unsigned long> length 1 (effectively an integer pointer)
    :type count: list[long]
    :param thread:
    :type thread: dict[str, object]
    :return:
    :rtype: None
    """

    if (thread["hit_map"] is None):
        thread["hit_map"] = {}

    mapindex = thread["hit_map"]
    assert isinstance(mapindex, dict)
    if count is None:
        count = [0]
    hitsit = pattern.finditer(bigstring)                    # Adrian
    for it in hitsit:                                       # Adrian
        # iterators only last for one shot so we capture the offsets to a list
        print(it.group())
        if it.group() not in mapindex.keys():
            mapindex[it.group()] = []
        mapindex[it.group()].append(it.start() + offset)    #
        # listindex.append(it.start() + offset)
    if thread["alive"] is not None:
        thread["alive"] = False
    count[0] -= 1


def slice_n_search_re(fd, chunksize, delta, term):
    """
    Written by: Adrian Leong
    Edited by: Chris Ottersen

    Searches chunks of a file (using RE) and returns file offsets of any hits.
    Intended for searching of large files where we cant read the whole thing into memory
    This function calls the "regsearch" search method

    :param fd:
    :type fd: file
    :param chunksize: unsigned long
    :type chunksize: long
    :param delta:
    :type delta: long
    :param term:
    :type term: str
    :return:
    :rtype: dict[str, list[long]]
    """
    count = [0]                            # Chris: int pointer (1-element array) to act as a thread
                                           # counter to keep track of threads which are currently active.

    start = datetime.datetime.now()        # Chris: baseline for the timer used to calculate
                                           # estimated time remaining

    final_hitmap = {}                      # Chris: replaces Adrian's `final_hitlist` to allow
                                           # for the capture of the map allows the capture of
                                           # multiple types of data markers using `|`.

    pattern = re.compile(term, re.DOTALL)  # Adrian: "should only really call this once at start, if same substring."

    st_size = os.fstat(fd.fileno()).st_size  # Adrian: stats = `os.fstat(fd.fileno())`
                                             # then subsequently used stat.st_size

    # print("slice_n_search_re Input file " + filename + " is " + str(stats.st_size) + " bytes\n")

    begin_chunk = 0                        # Adrian: for some readson the filesystem does not keep track of pointer
                                           # location reliably, so this holds what should be returned by fd.tell()

    # helps to keep track of threads
    threads = [{"thread": None, "hit_map": final_hitmap, "alive": True}] * (st_size // chunksize + 1)


    i = 0                                  # counter to keep track of how many threads have been started
                                           # (not neccessarally active). Replaces `numchunks`

    while (begin_chunk < st_size):             # Adrian: loop until
        chunk_size_to_read = min(st_size - begin_chunk, chunksize + delta)                      # Adrian: size of the file chunk to read

        # print("seeking " + str(begin_chunk) + " with size = " + str(chunk_size_to_read))
        fd.seek(begin_chunk)
        rawchunk = fd.read(chunk_size_to_read)
        t = threading.Thread(target=regsearch, args=(rawchunk, pattern, begin_chunk, count, threads[i]))
        threads[i]["thread"] = t
        count[0] += 1
        t.start()

        begin_chunk += chunksize
        i += 1

        fraction_complete = 1.0 * (i - count[0]) * chunksize / st_size + .000001
        time_used = (datetime.datetime.now() - start).seconds
        percent_complete = 100 * fraction_complete
        time_remaining = time_used / fraction_complete - time_used
        print("remaining: %%%04.3f    time remaining: %ds" % (percent_complete, time_remaining))
    # print("final_hitlist = " + str(final_hitlist))
    alive = 1
    while alive:
        alive = 0
        for thread in threads:
            alive += thread["alive"]

        print("threads executing: %d" % count[0])
        time.sleep(1)
    print ("%3.3f" % (datetime.datetime.now() - start).seconds)

    return final_hitmap

# Main
name = "__main__"

# search for "SMS" which marks the SMS log entries (ie Area 2 times and phone number)
# this will include SMStext hits so we need to some de-duping afterwards
SMS = "@\x01" + "SMS\x00".encode('utf-16le')
print(SMS)
IPM_SMStext = "IPM.SMStext\x00".encode('utf-16le')

print(IPM_SMStext)

# call flag
CALL = "{B1776703-738E-437D-B891-44555CEB6669}\x00".encode('utf-16le')

# contact flag
CONTACT = "\x01\x04\x00\x00\x00\x82\x00\xE0\x00\x74\xC5\xB7\x10\x1A\x82\xE0\x08"
THREAD = "\x01\x30\x00\xE1\xE0"
hit_map = slice_n_search_re(fb, CHUNK_SIZE, DELTA, IPM_SMStext + "|" + SMS + "|" + CALL + "|" + CONTACT + "|" + THREAD)

print("\n".join([("%s: %d" % (flag, len(hit_map[flag]))) for flag in sorted(hit_map.keys())]))
print("%d" % len(hit_map[THREAD]))

# print "SMS hits = " + str(len(smshits)) + " smshits"
# search the file chunks for the hex equivalent of "SMStext" which marks SMS Text content (ie Area 1)
# hits = slice_n_search_re(fb, CHUNK_SIZE, DELTA, substring1)
hits = hit_map[IPM_SMStext]
smshits = hit_map[SMS]

for hit in hit_map[THREAD]:
    parse_thread(fb, hit)

for hit in hit_map[IPM_SMStext]:
    parse_sms(fb, hit)

adrians_script(hits, smshits, fb, funi)
