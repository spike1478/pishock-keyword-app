# Build Guide for PiShock Universal App

This guide explains how to build executables for both Windows and Mac platforms.

## 🪟 **Windows Build**

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)
- Windows 10/11

### Quick Build
1. **Run the build script:**
   ```cmd
   build_windows.bat
   ```

2. **Or build manually:**
   ```cmd
   pip install -r requirements.txt
   pyinstaller pishock_app.spec
   ```

### Output
- **Executable**: `dist/pishock_app.exe`
- **Size**: ~50-80 MB
- **Dependencies**: All included (standalone)

### Testing
```cmd
dist\pishock_app.exe
```

---

## 🍎 **Mac Build**

### Prerequisites
- Python 3.7 or higher
- pip3 (Python package installer)
- macOS 10.14 or higher
- Xcode Command Line Tools (for some dependencies)

### Quick Build
1. **Make script executable:**
   ```bash
   chmod +x build_mac.sh
   ```

2. **Run the build script:**
   ```bash
   ./build_mac.sh
   ```

3. **Or build manually:**
   ```bash
   pip3 install -r requirements.txt
   pyinstaller pishock_app_mac.spec
   ```

### Output
- **App Bundle**: `dist/PiShock Universal.app`
- **Size**: ~50-80 MB
- **Dependencies**: All included (standalone)

### Testing
```bash
open "dist/PiShock Universal.app"
```

### Creating DMG Installer
```bash
hdiutil create -volname "PiShock Universal" -srcfolder "dist/PiShock Universal.app" -ov -format UDZO "PiShock Universal.dmg"
```

---

## 🔧 **Manual Build Process**

### 1. **Install Dependencies**
```bash
# Windows
pip install -r requirements.txt

# Mac
pip3 install -r requirements.txt
```

### 2. **Install PyInstaller**
```bash
# Windows
pip install pyinstaller

# Mac
pip3 install pyinstaller
```

### 3. **Build Executable**

**Windows:**
```cmd
pyinstaller pishock_app.spec
```

**Mac:**
```bash
pyinstaller pishock_app_mac.spec
```

### 4. **Test Build**
- Windows: Run `dist/pishock_app.exe`
- Mac: Run `dist/PiShock Universal.app`

---

## 📦 **Build Configuration**

### Windows Spec File (`pishock_app.spec`)
- **Console**: Disabled (GUI only)
- **UPX**: Enabled (compression)
- **One File**: Yes (single executable)
- **Icon**: None (default)

### Mac Spec File (`pishock_app_mac.spec`)
- **App Bundle**: Yes (.app format)
- **Console**: Disabled (GUI only)
- **UPX**: Enabled (compression)
- **Bundle ID**: `com.spike1478.pishock-universal`
- **Version**: 1.0.0

---

## 🚨 **Troubleshooting**

### Common Issues

#### **"Module not found" errors**
- Ensure all dependencies are installed
- Check Python path
- Try rebuilding with `--clean` flag

#### **"Permission denied" (Mac)**
- Grant accessibility permissions
- Run with `sudo` if needed
- Check security settings

#### **"DLL not found" (Windows)**
- Install Visual C++ Redistributable
- Check Windows version compatibility
- Try building on target system

#### **Large file size**
- Normal for PyInstaller builds
- All dependencies included
- Consider using `--exclude-module` for unused modules

### Build Flags

#### **Clean Build**
```bash
pyinstaller --clean pishock_app.spec
```

#### **Debug Build**
```bash
pyinstaller --debug all pishock_app.spec
```

#### **One Directory (instead of one file)**
```bash
pyinstaller --onedir pishock_app.spec
```

---

## 📋 **Build Requirements**

### Windows
- **OS**: Windows 10/11 (64-bit)
- **Python**: 3.7+
- **Memory**: 4GB+ RAM
- **Disk**: 2GB+ free space

### Mac
- **OS**: macOS 10.14+
- **Python**: 3.7+
- **Memory**: 4GB+ RAM
- **Disk**: 2GB+ free space
- **Xcode**: Command Line Tools

---

## 🔄 **Cross-Platform Building**

### Building Mac on Windows
- Use GitHub Actions or similar CI/CD
- Virtual machines with macOS
- Cloud-based Mac build services

### Building Windows on Mac
- Use Wine or similar compatibility layer
- Virtual machines with Windows
- Cloud-based Windows build services

---

## 📁 **Output Structure**

### Windows
```
dist/
└── pishock_app.exe          # Standalone executable
```

### Mac
```
dist/
└── PiShock Universal.app/   # App bundle
    ├── Contents/
    │   ├── MacOS/
    │   │   └── PiShock Universal
    │   ├── Resources/
    │   └── Info.plist
    └── ...
```

---

## 🎯 **Optimization Tips**

### Reduce File Size
- Use `--exclude-module` for unused modules
- Enable UPX compression
- Remove debug information

### Improve Performance
- Use `--onedir` for faster startup
- Optimize imports
- Profile the application

### Security
- Code signing (Mac)
- Digital signatures (Windows)
- Antivirus whitelisting

---

## 📞 **Support**

If you encounter build issues:

1. **Check Prerequisites**: Ensure Python and dependencies are installed
2. **Clean Build**: Try `--clean` flag
3. **Debug Mode**: Use `--debug all` for detailed output
4. **Platform Specific**: Build on target platform when possible
5. **GitHub Issues**: Report problems with build logs

---

**Happy Building! 🚀**
