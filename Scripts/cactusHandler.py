import re
from datetime import datetime
import matplotlib.pyplot as plt

def parse_cactus_file(file_path):
    cme_events = []
    with open(file_path, 'r') as f:
        for line in f:
            # CME lines start with 4-digit numbers
            if re.match(r"\s*\d{4}\|", line):
                parts = line.strip().split('|')
                try:
                    t0 = parts[1].strip()
                    t0_dt = datetime.strptime(t0, "%Y/%m/%d %H:%M")
                    cme_events.append(t0_dt)
                except Exception as e:
                    print("Error parsing line:", line)
    return cme_events
