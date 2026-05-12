import re
# Example output (simulate the command line output)
text = """
ntpd (pid 1250) is running...

     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
*100.100.99.101  172.28.11.101    2 u  247  256  377    4.288   -0.242   0.115


synchronised to NTP server (100.100.99.101) at stratum 3
   time correct to within 36 ms
   polling server every 256 s

Current time in UTC is : Wed Dec 31 19:54:53 UTC 2025
Current time in Asia/Jerusalem is : Wed Dec 31 21:54:53 IST 2025
"""

cucm_ntp_output = """
ntpd (pid 28435) is running...
     remote           refid      st t when poll reach   delay   offset    jitter
==============================================================================
*203.0.113.0     .GOOG.           1 u   44   64   377   11.724   -0.021    0.064
+192.168.1.10    .GPS.            1 u   50   64   377    0.500    0.100    0.050
 LOCAL(0)        .LOCL.          10 l    -   64    0     0.000    0.000    0.000
unsynchronised
Current time in UTC is : Fri Jan 2 13:09:00 UTC 2026
"""

status = """
admin:show status

Host Name          : cucm-pub-neta
Date               : Mon Mar 2, 2026 00:36:32
Time Zone          : Israel Standard Time (Asia/Jerusalem)
Locale             : en_US.UTF-8
Product Ver        : 12.5.1.12900-115
Unified OS Version : 7.0.0.0-4

Uptime:
 00:36:33 up 79 days, 12:45,  1 user,  load average: 1.76, 1.09, 0.94

CPU Idle:   33.17%  System:   23.12%    User:   42.21%
  IOWAIT:   01.01%     IRQ:   00.00%    Soft:   00.50%

Memory Total:        5945116K
        Free:         148872K
        Used:        4111244K
      Cached:         998788K
      Shared:         470380K
     Buffers:        1685000K

                        Total            Free            Used
Disk/active         17921776K        3991112K       13730872K (78%)
Disk/inactive       17921776K       16943272K          45080K (1%)
Disk/logging        62681844K       28513908K       30960820K (53%)

"""

process_load = """
top - 00:40:28 up 79 days, 12:49,  1 user,  load average: 1.59, 1.58, 1.19
Tasks: 242 total,   1 running, 241 sleeping,   0 stopped,   0 zombie
%Cpu(s):  3.0 us,  9.1 sy,  3.0 ni, 84.8 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem :  5945116 total,   194592 free,  4077300 used,  1673224 buff/cache
KiB Swap:  4095996 total,  1916776 free,  2179220 used.  1025868 avail Mem
  PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
  756 admin     30  10 1452528 158448  20420 S  12.5  2.7   0:09.38 java
 2704 admin     30  10  158024   2308   1728 R   6.2  0.0   0:00.03 top
24309 root      20   0   80168   1432   1144 S   6.2  0.0 420:11.45 snmpdm
24811 ccmserv+  20   0  354604  43432  22840 S   6.2  0.7   1634:05 RisDC
25089 ccmserv+  20   0  945696  99784   8632 S   6.2  1.7 444:01.51 carschlr
25254 ccmbase   20   0  438004 122292  22996 S   6.2  2.1   2429:19 ccm
    1 root      20   0  202736   5316   3152 S   0.0  0.1 435:33.21 systemd
    2 root      20   0       0      0      0 S   0.0  0.0   0:08.30 kthreadd
    3 root      20   0       0      0      0 S   0.0  0.0  75:44.92 ksoftirqd/0
    5 root       0 -20       0      0      0 S   0.0  0.0   0:00.00 kworker/0:+
"""

import re


def parse_show_process_load(raw):

    data = {}

    # -------------------------
    # LOAD AVERAGE
    # -------------------------

    load_match = re.search(
        r"load average:\s*([\d\.]+),\s*([\d\.]+),\s*([\d\.]+)", raw
    )

    if load_match:
        data["load_1m"] = float(load_match.group(1))
        data["load_5m"] = float(load_match.group(2))
        data["load_15m"] = float(load_match.group(3))

    # -------------------------
    # TASKS
    # -------------------------

    tasks_match = re.search(
        r"Tasks:\s*(\d+)\s*total,\s*(\d+)\s*running,\s*(\d+)\s*sleeping,\s*(\d+)\s*stopped,\s*(\d+)\s*zombie",
        raw,
    )

    if tasks_match:
        data["tasks_total"] = int(tasks_match.group(1))
        data["tasks_running"] = int(tasks_match.group(2))
        data["tasks_sleeping"] = int(tasks_match.group(3))
        data["tasks_stopped"] = int(tasks_match.group(4))
        data["tasks_zombie"] = int(tasks_match.group(5))

    # -------------------------
    # CPU
    # -------------------------

    cpu_match = re.search(
        r"%Cpu\(s\):\s*([\d\.]+)\s*us,\s*([\d\.]+)\s*sy,\s*([\d\.]+)\s*ni,\s*([\d\.]+)\s*id,\s*([\d\.]+)\s*wa",
        raw,
    )

    if cpu_match:
        data["cpu_user"] = float(cpu_match.group(1))
        data["cpu_system"] = float(cpu_match.group(2))
        data["cpu_nice"] = float(cpu_match.group(3))
        data["cpu_idle"] = float(cpu_match.group(4))
        data["cpu_iowait"] = float(cpu_match.group(5))

    # -------------------------
    # MEMORY
    # -------------------------

    mem_match = re.search(
        r"KiB Mem\s*:\s*(\d+)\s*total,\s*(\d+)\s*free,\s*(\d+)\s*used,\s*(\d+)\s*buff/cache",
        raw,
    )

    if mem_match:
        data["mem_total"] = int(mem_match.group(1))
        data["mem_free"] = int(mem_match.group(2))
        data["mem_used"] = int(mem_match.group(3))
        data["mem_cache"] = int(mem_match.group(4))

    # -------------------------
    # SWAP
    # -------------------------

    swap_match = re.search(
        r"KiB Swap:\s*(\d+)\s*total,\s*(\d+)\s*free,\s*(\d+)\s*used",
        raw,
    )

    if swap_match:
        data["swap_total"] = int(swap_match.group(1))
        data["swap_free"] = int(swap_match.group(2))
        data["swap_used"] = int(swap_match.group(3))

    # -------------------------
    # TOP PROCESS
    # -------------------------

    processes = []

    for line in raw.splitlines():

        parts = line.split()

        if len(parts) < 12:
            continue

        if parts[0].isdigit():

            processes.append({
                "pid": int(parts[0]),
                "name": parts[-1],
                "cpu": float(parts[8]),
                "mem": float(parts[9])
            })

    processes = sorted(processes, key=lambda x: x["cpu"], reverse=True)

    data["top_processes"] = processes[:5]

    return data


output = parse_show_process_load(process_load)

print(output)


"""
Tried to build AI App

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "user", "content": "Explain what high CPU means in a server"}
    ]
)
print(response.usage)
print(response.choices[0].message.content)
"""