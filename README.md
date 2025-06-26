# Advanced Keylogger
This Python-based keylogger is designed for educational and ethical cybersecurity research purposes. It captures and logs various system activities while implementing anti-detection, encryption, and stealth techniques to avoid analysis.

##Project Overview

This project is an advanced keylogger developed in Python for cybersecurity research, penetration testing, and ethical hacking education. Unlike basic keyloggers, this tool incorporates multiple surveillance techniques, encryption, anti-analysis measures, and stealth mechanisms to demonstrate real-world attack vectors while emphasizing defensive security awareness.

##Objectives

- Demonstrate how attackers capture sensitive data (keystrokes, screenshots, audio, processes).

- Study defensive evasion techniques (debugger detection, sandbox avoidance, encryption).

- Provide a legal, ethical framework for cybersecurity professionals to analyze keylogger behavior.

- Enhance threat detection & mitigation strategies by understanding keylogger functionalities.

##Key Features:

## A. Data Collection
✔ Keystroke Logging – Records all keyboard inputs with active window & process context.
✔ Window Activity Tracking – Logs application switches and foreground processes.
✔ Screenshot Capture – Takes periodic screenshots (configurable interval).
✔ Audio Recording – Captures microphone input in short clips.
✔ System & Network Monitoring – Collects running processes, network connections, and system details.

## B. Data Protection & Exfiltration
✔ AES Encryption (Fernet) – Secures logs before storage/transmission.
✔ Multiple Exfiltration Methods –

Email (SMTP) – Sends encrypted logs via email.

HTTP POST – Transmits data to a C2 server.

Local Storage – Encrypted logs stored in JSON format.
✔ Log Rotation – Prevents oversized logs by compressing & archiving old data.

## C. Anti-Analysis & Stealth
✔ Debugger Detection – Checks if running under a debugger (e.g., x64dbg, OllyDbg).
✔ Sandbox/Virtual Machine Detection – Exits if running in a VM (VirtualBox, VMware, QEMU).
✔ Randomized Timing – Screenshots & audio captures occur at irregular intervals.
✔ Function Obfuscation – Hides core functions to evade static analysis.


## Ethical & Legal Considerations
⚠ This tool is for educational and authorized security testing only.

- Unauthorized use is illegal and violates privacy laws (e.g., CFAA, GDPR).

- Only deploy in controlled environments with explicit consent.

- Ideal for:

* Red team exercises (simulating attacker behavior).

* Blue team training (detecting & mitigating keyloggers).

* Cybersecurity coursework (understanding malware techniques).

## Future Enhancements
🔹 Persistence Mechanisms – Registry modifications, scheduled tasks.
🔹 Remote Command Execution – Allow dynamic control via C2.
🔹 Clipboard Monitoring – Capture copied passwords/text.
🔹 Browser Data Extraction – Log saved credentials & browsing history.

## Conclusion
This project serves as a realistic yet ethical demonstration of how keyloggers operate, helping cybersecurity professionals improve detection, analysis, and prevention strategies. By studying offensive techniques, defenders can better secure systems against similar threats.
