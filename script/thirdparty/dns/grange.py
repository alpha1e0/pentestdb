# Copyright (C) 2003-2007, 2009-2011 Nominum, Inc.
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose with or without fee is hereby granted,
# provided that the above copyright notice and this permission notice
# appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND NOMINUM DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL NOMINUM BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""DNS GENERATE range conversion."""

#import dns

#import dnssec
#import e164
#import edns
#import entropy
import exception
#import flags
#import hash
#import inet
#import ipv4
#import ipv6
#import message
#import name
#import namedict
#import node
#import opcode
#import query
#import rcode
#import rdata
#import rdataclass
#import rdataset
#import rdatatype
#import renderer
#import resolver
#import reversename
#import rrset
#import set
#import tokenizer
#import tsig
#import tsigkeyring
#import ttl
#import rdtypes
#import update
#import version
#import wiredata
#import zone

def from_text(text):
    """Convert the text form of a range in a GENERATE statement to an
    integer.

    @param text: the textual range
    @type text: string
    @return: The start, stop and step values.
    @rtype: tuple
    """
    # TODO, figure out the bounds on start, stop and step.

    import pdb
    step = 1
    cur = ''
    state = 0
    # state   0 1 2 3 4
    #         x - y / z
    for c in text:
        if c == '-' and state == 0:
            start = int(cur)
            cur = ''
            state = 2
        elif c == '/':
            stop = int(cur)
            cur = ''
            state = 4
        elif c.isdigit():
            cur += c
        else:
            raise exception.SyntaxError("Could not parse %s" % (c))

    if state in (1, 3):
        raise exception.SyntaxError

    if state == 2:
        stop = int(cur)

    if state == 4:
        step = int(cur)

    assert step >= 1
    assert start >= 0
    assert start <= stop
    # TODO, can start == stop?

    return (start, stop, step)
