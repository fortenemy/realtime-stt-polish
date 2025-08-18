---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: 'bug'
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Run command '...'
2. Speak into microphone '....'
3. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Actual behavior**
What actually happened instead.

**Environment (please complete the following information):**
 - OS: [e.g. Windows 11, Ubuntu 22.04, macOS 13]
 - Python version: [e.g. 3.10.6]
 - Package version: [e.g. 0.1.0]
 - Audio device: [e.g. Built-in microphone, USB headset]

**Audio Configuration:**
 - Sample rate: [e.g. 16000 Hz]
 - Channels: [e.g. 1 (mono)]
 - Buffer size: [e.g. 1024]

**Error logs**
```
Paste any relevant error messages or logs here
```

**Audio device information**
Run this command and paste the output:
```bash
python -c "import sounddevice; print(sounddevice.query_devices())"
```

**Additional context**
Add any other context about the problem here, such as:
- Background noise level
- Speaking language/accent
- Duration of audio when bug occurs
- Any workarounds you've found
