"""
Copyright (c) Django Software Foundation and individual contributors.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.

    3. Neither the name of Django nor the names of its contributors may be used
       to endorse or promote products derived from this software without
       specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import re

ul = '\u00a1-\uffff'  # unicode letters range (must not be a raw string)

# IP patterns
ipv4_re = r'(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}'
ipv6_re = r'\[[0-9a-f:\.]+\]'

# Host patterns
hostname_re = r'[a-z' + ul + r'0-9](?:[a-z' + ul + r'0-9-]{0,61}[a-z' + ul + r'0-9])?'
domain_re = r'(?:\.(?!-)[a-z' + ul + r'0-9-]{1,63}(?<!-))*' # domain names have max length of 63 characters
tld_re = (
    r'\.'                                # dot
    r'(?!-)'                             # can't start with a dash
    r'(?:[a-z' + ul + '-]{2,63}'         # domain label
    r'|xn--[a-z0-9]{1,59})'              # or punycode label
    r'(?<!-)'                            # can't end with a dash
    r'\.?'                               # may have a trailing dot
)
host_re = '(' + hostname_re + domain_re + tld_re + '|localhost)'

IS_VALID_URL = re.compile(
    r'^(?:http|ftp)s?://' # http(s):// or ftp(s)://
    r'(?:\S+(?::\S*)?@)?'  # user:pass authentication
    r'(?:' + ipv4_re + '|' + ipv6_re + '|' + host_re + ')' # localhost or ip
    r'(?::\d{2,5})?'  # optional port
    r'(?:[/?#][^\s]*)?'  # resource path
    r'\Z', re.IGNORECASE)
