#!/usr/bin/env python
# -----------------------------------------------------------------------------
#             
# Copyright 2013-2019 lispers.net - Dino Farinacci <farinacci@gmail.com>
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.    
# 
# -----------------------------------------------------------------------------
#
# is-lisp-running.py
#
# This script checks to see if there is any LISP processes running on the
# local system.
#
# Usage: python -O is-lisp-running.pyo
#
#------------------------------------------------------------------------------

import commands
import os

def bold(string):
    return("\033[1m" + string + "\033[0m")
#enddef

#
# Add title.
#
version = commands.getoutput("cat lisp-version.txt")
rv = commands.getoutput("head -1 logs/lisp-core.log")
if (rv.find("version") != -1):
    rv = rv.split("version ")[1]
    rv = rv.split(",")[0]
    rv = ", release {} running".format(bold(rv))
else:
    rv = None
#endif

#
# Get data.
#
command = "ps auxww | egrep 'lisp-' |" + \
    "egrep -v 'grep|is-lisp-running|tee|pslisp|sudo|log'"
output = commands.getoutput(command)
if (output == None or output == ""):
    print "No lispers.net code running, release {} installed".format(version)
    exit(0)
#endif
if (rv == None): rv = ""

print "--- lispers.net release {} installed{} ---".format(bold(version), rv)

lines = output.split("\n")

#
# Special case Alpine Linux. It has different ps output.
#
if (os.path.exists("/etc/alpine-release")):
    pid = "PID".ljust(8)
    cpu = "TIME".ljust(8)
    process = "Process"
    print "{}{}{}".format(pid, cpu, process)
    for line in lines:
        items = line.split()
        pid = items[0].ljust(8)
        cpu = items[2].ljust(8)
        process = items[3] if (items[3].find("lisp-ztr") != -1) else items[-1]
        if (process.isdigit()): process = items[-2] + " " + process
        print "{}{}{}".format(pid, cpu, process)
    #endfor
    exit(0)
#endif

#
# All other Linux variants.
#
pid = "PID".ljust(8)
cpu = "%CPU".ljust(8)
mem = "%MEM".ljust(8)
process = "Process"
print "{}{}{}{}".format(pid, cpu, mem, process)

for line in lines:
    items = line.split()
    pid = items[1].ljust(8)
    cpu = items[2].ljust(8)
    mem = items[3].ljust(8)

    if (line.find("lisp-core.py") != -1):
        process = items[-2] + " " + items[-1]
    elif (line.find("lisp-join.py") != -1):
        group = items[-1]
        if (group.count(".") != 3): group = items[-2] + " " + group
        process = "lisp-join.py " + group
    else:
        process = items[-1]
    #endif

    print "{}{}{}{}".format(pid, cpu, mem, process)
#endfor
exit(0)
