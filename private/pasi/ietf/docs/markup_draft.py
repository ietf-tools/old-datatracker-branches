# Copyright (C) 2009 Nokia Corporation and/or its subsidiary(-ies).
# All rights reserved. Contact: Pasi Eronen <pasi.eronen@nokia.com>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#
#  * Neither the name of the Nokia Corporation and/or its
#    subsidiary(-ies) nor the names of its contributors may be used
#    to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from django.utils.html import escape
import string
import re

def markup_draft(content):
    # normalize line endings to LF only
    content = content.replace("\r\n", "\n")
    content = content.replace("\r", "\n")

    # at this point, "content" is normal string
    # fix most common non-ASCII characters
    t1 = string.maketrans("\x91\x92\x93\x94\x95\x96\x97\xc6\xe8\xe9", "\'\'\"\"o--\'ee")
    # map everything except printable ASCII, TAB, LF, FF to "?"
    t2 = string.maketrans('','')
    t3 = "?"*9 + "\t\n?\f" + "?"*19 + t2[32:127] + "?"*129
    t4 = t1.translate(t3)
    content = content.translate(t4)

    # expand tabs + escape 
    content = escape(content.expandtabs())

    content = re.sub("\n(.+\[Page \d+\])\n\f\n(.+)\n", """\n<span class="grey">\g<1></span>\n\f\n<span class="grey">\g<2></span>\n""", content)
    
    return ("<pre>\n"+content+"</pre>\n", "")
