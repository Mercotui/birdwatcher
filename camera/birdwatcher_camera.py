#!/usr/bin/env python3

import subprocess

file_name = "/tmp/t.jpg"
subprocess.run(["fswebcam", "-r", "5000x500000", "--no-banner", "-S", "30", file_name])
