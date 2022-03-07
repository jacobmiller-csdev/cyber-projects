# Persistent, Evasive Keylogger

This program is designed to exfiltrate keystroke information from the host machine to a remote UDP listener while also establishing persistence on the host machine and minimizing antivirus detection.

The program itself is well-documented in regards to how it accomplishes these tasks, so please reference the included .py file for more detailed explanations on them. It should be noted, however, that for testing purposes I compiled this program with both Py2Exe and Nuitka, with Nuitka producing somewhat more favorable results in regards to antivirus evasion.
