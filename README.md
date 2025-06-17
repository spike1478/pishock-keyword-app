# ⚡ PiShock Trigger App

Welcome to the chaos!

This is a **Python GUI app** that listens for trigger words you type — and then sends a zap via the [PiShock](https://www.pishock.com/) API. Built for fun, discipline, gaming, or slightly unhinged cyberpunk rituals. Whatever you're into — I'm not here to judge.

---

## ⚠️ **Current Status: In Development**  
This project is a work in progress and has **not been thoroughly tested**.  
If you try to use it, it might not work, or it might work *too well*.  
Use at your own risk.  
Seriously. I haven't added any safety features yet. 🙃

---

## 🖥️ What it does

- GUI lets you enter:
  - Your PiShock username, share code, and script name
  - Trigger words (comma-separated)
  - Duration and intensity for the shock

- Runs a background key listener to detect trigger words
- Sends a POST request to the PiShock API when triggered

---

## 🔧 Requirements

Install with:

```bash
pip install pynput requests
```

Make sure you’ve got a valid PiShock API key and the device set up to accept shocks.

---

## 🚀 Running the App

```bash
python pishock_app.py
```

(Or use the `.exe` if you’ve built one with PyInstaller — again, untested for now!)

---

## 🛠️ In the works

- Better error handling
- Logging
- Safer start/stop toggle
- Optional beeping before the shock
- Support for other “operations” like vibration and beep only
- Settings persistence

---

## 📜 Licence

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International License** (CC BY-NC 4.0).

You **can**:
- Use, adapt, and share the code for **non-commercial** purposes  
- Build your own thing on top of it  
- Credit me (Maya McCutcheon) in the process

You **can’t**:
- Use this in anything you plan to sell or monetise  
- Remove attribution  
- Re-license it under stricter terms

More details here: [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)

---

## 🙋‍♀️ Author

Made with slightly concerning energy by **Maya McCutcheon** (2025)  
Open to feedback, ideas, memes, and pull requests!

---

## ⚡ Use responsibly.
Please don't hurt yourself (or others) without consent. Consent is hot. Lawsuits are not.
