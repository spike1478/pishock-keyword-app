# ⚡ PiShock/OpenShock Universal Trigger App

## ⚠️ **CRITICAL SAFETY DISCLAIMER** ⚠️

**🚨 USE AT YOUR OWN RISK - NO WARRANTIES OR GUARANTEES 🚨**

This software is provided **"AS IS"** without any warranties or guarantees. The author (@spike1478) **CANNOT and WILL NOT** guarantee that this application will work as intended, be safe to use, or function correctly in any way.

**⚠️ IMPORTANT SAFETY WARNINGS:**
- **This app controls electrical shock devices** - improper use can cause injury
- **No safety guarantees** - the app may malfunction, fail, or behave unexpectedly
- **Test with extreme caution** - start with lowest possible settings
- **Use at your own risk** - you are solely responsible for any consequences
- **Not medical advice** - consult professionals before use
- **Consent required** - never use without explicit consent from all parties
- **Emergency stop** - always know how to stop the device immediately

**🔴 BY USING THIS SOFTWARE, YOU ACKNOWLEDGE AND ACCEPT:**
- You are using it at your own risk
- The author is not responsible for any harm, injury, or damage
- You understand the risks involved with electrical shock devices
- You will use appropriate safety measures and precautions
- You have obtained proper consent from all involved parties

**If you cannot accept these terms, DO NOT USE THIS SOFTWARE.**

---

Welcome to the chaos! This is a **Python GUI app** that listens for trigger words you type — and then sends a zap via **PiShock** or **OpenShock** APIs. Built for fun, discipline, gaming, or slightly unhinged cyberpunk rituals. Whatever you're into — I'm not here to judge.

---

## 🌟 **Universal Platform Support**

This app supports **both PiShock and OpenShock** platforms, giving you maximum flexibility:

- **PiShock**: Original platform with full compatibility
- **OpenShock Direct**: Native OpenShock API integration  
- **OpenShock via pi3open**: Translation layer for easy migration

---

## ⚠️ **Safety First**

This app includes comprehensive safety features:
- ✅ Confirmation dialogs before shocks
- ✅ Emergency stop button
- ✅ Cooldown periods (0-60 seconds)
- ✅ Rate limiting (max shocks per minute)
- ✅ Input validation and connection testing
- ✅ Comprehensive logging

**Use responsibly and start with low settings!**

---

## 🖥️ **What it does**

- **Universal GUI** lets you:
  - Select your platform (PiShock/OpenShock)
  - Enter platform-specific credentials
  - Configure trigger words (comma-separated)
  - Set duration (1-15s) and intensity (1-100)
  - Configure safety settings

- **Smart Platform Detection**:
  - Automatically adjusts UI based on selected platform
  - Handles different credential requirements
  - Manages platform-specific API calls

- **Background Key Listener**:
  - Detects trigger words as you type
  - Sends platform-appropriate API requests
  - Includes comprehensive safety checks

---

## 🔧 **Requirements**

Install dependencies:

```bash
pip install -r requirements.txt
```

**Dependencies:**
- `requests` - HTTP API calls
- `pynput` - Global keyboard listening
- `tkinter` - GUI (included with Python)

---

## 🚀 **Quick Start**

### 1. **Run the App**
```bash
python pishock_app.py
```

### 2. **Select Your Platform**
- **PiShock**: Original platform
- **OpenShock Direct**: Native OpenShock API
- **OpenShock via pi3open**: Translation layer

### 3. **Enter Credentials**

**For PiShock:**
- Username, Share Code, Script Name, API Key

**For OpenShock Direct:**
- Device ID, API Token

**For OpenShock via pi3open:**
- Username, Share Code (Device ID), Script Name, API Key

### 4. **Test Connection**
Click "Test Connection" to verify your credentials

### 5. **Configure Settings**
- Set trigger words (comma-separated)
- Adjust duration and intensity
- Configure safety settings

### 6. **Start Listening**
Click "Start Listening" and type your trigger words!

---

## 🛡️ **Safety Features**

### **Confirmation Dialogs**
- Optional confirmation before each shock
- Shows platform, duration, and intensity
- Can be disabled for advanced users

### **Emergency Stop**
- Big red emergency stop button
- **Global emergency hotkey** (configurable)
- Immediately halts all operations
- Always available when listening

### **Emergency Hotkey**
- **Global hotkey** works from anywhere on your system
- **Default**: `Ctrl+Shift+Esc` (easily changeable)
- **Available options**: F12, Ctrl+F12, Alt+F12, Ctrl+Alt+Esc, Ctrl+Shift+Space, etc.
- **Test functionality** to verify hotkey works
- **Visual status indicator** shows if hotkey is active
- **Automatic activation** when listening starts

### **Rate Limiting**
- Configurable cooldown periods (0-60 seconds)
- Maximum shocks per minute (1-20)
- Prevents accidental rapid-fire shocks

### **Input Validation**
- Validates all user inputs
- Tests API connections before starting
- Platform-specific credential validation

### **Logging**
- All actions logged to `pishock_universal.log`
- Console output for real-time feedback
- Debug information for troubleshooting

---

## 🔄 **Platform Differences**

### **PiShock**
- **API**: `https://do.pishock.com/api/apioperate/`
- **Credentials**: Username, Share Code, Script Name, API Key
- **Format**: Original PiShock API format

### **OpenShock Direct**
- **API**: `https://api.openshock.app/1/sendControl`
- **Credentials**: Device ID, API Token
- **Format**: Native OpenShock API format
- **Headers**: `Open-Shock-Token`, `User-Agent`

### **OpenShock via pi3open**
- **API**: `https://pi3open.isso.moe/api/apioperate/`
- **Credentials**: Username, Share Code, Script Name, API Key
- **Format**: PiShock-compatible with OpenShock backend
- **Translation**: Automatic format conversion

---

## 📊 **Statistics & Monitoring**

The app tracks:
- Platform being used
- Shock count for current session
- Last shock timestamp
- Listening status
- Safety settings display

---

## ⚙️ **Settings Persistence**

- Settings automatically saved on exit
- Settings restored on startup
- Platform selection remembered
- All preferences preserved

---

## 🛠️ **Advanced Features**

### **Platform Switching**
- Switch between platforms without restart
- UI automatically updates
- Credentials preserved per platform

### **Connection Testing**
- Test API connections before starting
- Platform-specific validation
- Clear success/failure feedback

### **Error Handling**
- Specific error messages for each platform
- Network timeout handling
- Graceful degradation

---

## 📁 **File Structure**

```
PiShock/
├── pishock_app.py                    # Main universal application
├── backup_script.py                  # Backup utility
├── requirements.txt                  # Dependencies
├── README.md                        # This file
├── LICENCE                          # License file
├── pishock_app.spec                 # PyInstaller configuration
├── pishock_universal_settings.json  # Settings (auto-created)
├── pishock_universal.log            # Log file (auto-created)
└── backups/                         # Backup storage
    └── pishock_backup_YYYYMMDD_HHMMSS/
```

---

## 🔧 **Building Executables**

### Quick Build

**Windows:**
```cmd
build_windows.bat
```

**Mac:**
```bash
chmod +x build_mac.sh
./build_mac.sh
```

### Manual Build

**Windows:**
```cmd
pip install -r requirements.txt
pyinstaller pishock_app.spec
```

**Mac:**
```bash
pip3 install -r requirements.txt
pyinstaller pishock_app_mac.spec
```

### Output Files
- **Windows**: `dist/pishock_app.exe` (standalone executable)
- **Mac**: `dist/PiShock Universal.app` (app bundle)

For detailed build instructions, see [BUILD_GUIDE.md](BUILD_GUIDE.md).

---

## 🚨 **Troubleshooting**

### **Common Issues**

1. **"API connection failed"**
   - Check your credentials
   - Verify internet connection
   - Test with different platform

2. **"No trigger words detected"**
   - Check trigger word spelling
   - Ensure words are comma-separated
   - Try shorter, simpler words

3. **"Permission denied" (keyboard listening)**
   - Run as administrator (Windows)
   - Grant accessibility permissions (macOS)
   - Check system security settings

4. **"Platform not responding"**
   - Try different platform
   - Check platform status
   - Verify API endpoints

### **Logs**
Check `pishock_universal.log` for detailed error information.

---

## 📜 **License**

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International License** (CC BY-NC 4.0).

**You can:**
- Use, adapt, and share the code for **non-commercial** purposes
- Build your own thing on top of it
- Credit me (@spike1478) in the process

**You can't:**
- Use this in anything you plan to sell or monetize
- Remove attribution
- Re-license it under stricter terms

More details: [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)

---

## 🙋‍♀️ **Author**

Made with slightly concerning energy by **@spike1478** (2025)

Open to feedback, ideas, memes, and pull requests!

---

## ⚡ **Use Responsibly**

Please don't hurt yourself (or others) without consent. Consent is hot. Lawsuits are not.

**Start with low intensity and short duration. Test thoroughly. Use safety features. Have fun!**

---

## 🎯 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📞 **Support**

- **Issues**: Report bugs and request features on GitHub
- **Discussions**: Ask questions and share ideas
- **Wiki**: Check the wiki for additional documentation

---

**Happy shocking! ⚡**