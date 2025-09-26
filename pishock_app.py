#!/usr/bin/env python3
"""
Universal PiShock/OpenShock Trigger App
Supports both PiShock and OpenShock platforms with enhanced safety features.
"""

import threading
import json
import requests
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from pynput import keyboard
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any, Literal
import re
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pishock_universal.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Platform(Enum):
    PISHOCK = "pishock"
    OPENSHOCK = "openshock"
    PI3OPEN = "pi3open"

class PiShockUniversalApp:
    def __init__(self, master):
        self.master = master
        self.api_key: Optional[str] = None
        self.listener: Optional[keyboard.Listener] = None
        self.buffer = ""
        self.max_word_len = 0
        self.words: List[str] = []
        self.is_listening = False
        self.last_shock_time = 0
        self.shock_count = 0
        self.max_shocks_per_minute = 5
        self.current_platform: Platform = Platform.PISHOCK
        self.emergency_hotkey = None  # Global emergency stop hotkey
        
        # API endpoints
        self.api_endpoints = {
            Platform.PISHOCK: "https://do.pishock.com/api/apioperate/",
            Platform.OPENSHOCK: "https://api.openshock.app/1/sendControl",
            Platform.PI3OPEN: "https://pi3open.isso.moe/api/apioperate/"
        }
        
        # Initialize UI
        self._setup_ui()
        self._load_settings()
        
        logger.info("PiShock Universal App initialized")

    def _setup_ui(self):
        """Set up the universal user interface."""
        self.master.title("PiShock/OpenShock Universal Trigger App")
        self.master.geometry("600x700")
        self.master.resizable(True, True)
        
        # Configure grid weights
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        
        # Create main container with scrollbar
        main_frame = ttk.Frame(self.master)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Platform selection section
        self._create_platform_section(main_frame)
        
        # API Key section
        self._create_api_section(main_frame)
        
        # Credentials section
        self._create_credentials_section(main_frame)
        
        # Settings section
        self._create_settings_section(main_frame)
        
        # Safety section
        self._create_safety_section(main_frame)
        
        # Emergency hotkey section
        self._create_emergency_hotkey_section(main_frame)
        
        # Control section
        self._create_control_section(main_frame)
        
        # Status section
        self._create_status_section(main_frame)
        
        # Statistics section
        self._create_stats_section(main_frame)

    def _create_platform_section(self, parent):
        """Create platform selection section."""
        platform_frame = ttk.LabelFrame(parent, text="Platform Selection")
        platform_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        self.platform_var = tk.StringVar(value="pishock")
        
        # Platform radio buttons
        ttk.Radiobutton(platform_frame, text="PiShock", variable=self.platform_var, 
                       value="pishock", command=self._on_platform_change).grid(row=0, column=0, sticky="w", padx=5)
        ttk.Radiobutton(platform_frame, text="OpenShock (Direct)", variable=self.platform_var, 
                       value="openshock", command=self._on_platform_change).grid(row=0, column=1, sticky="w", padx=5)
        ttk.Radiobutton(platform_frame, text="OpenShock (via pi3open)", variable=self.platform_var, 
                       value="pi3open", command=self._on_platform_change).grid(row=0, column=2, sticky="w", padx=5)
        
        # Platform info label
        self.platform_info = ttk.Label(platform_frame, text="", wraplength=500)
        self.platform_info.grid(row=1, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        
        self._update_platform_info()

    def _create_api_section(self, parent):
        """Create API key input section."""
        api_frame = ttk.LabelFrame(parent, text="API Configuration")
        api_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        ttk.Label(api_frame, text="API Key/Token:").grid(row=0, column=0, sticky="e", padx=5)
        self.api_key_var = tk.StringVar()
        self.api_key_entry = ttk.Entry(api_frame, textvariable=self.api_key_var, width=40, show="*")
        self.api_key_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(api_frame, text="Test Connection", command=self._test_api_connection).grid(row=0, column=2, padx=5)

    def _create_credentials_section(self, parent):
        """Create credentials input section."""
        creds_frame = ttk.LabelFrame(parent, text="Device Credentials")
        creds_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        
        self.credential_vars = {}
        self.credential_labels = {}
        
        # Username field
        ttk.Label(creds_frame, text="Username:").grid(row=0, column=0, sticky="e", padx=5)
        var = tk.StringVar()
        entry = ttk.Entry(creds_frame, textvariable=var, width=30)
        entry.grid(row=0, column=1, padx=5, pady=2)
        self.credential_vars["username"] = var
        self.credential_labels["username"] = "Username"
        
        # Share Code / Device ID field
        ttk.Label(creds_frame, text="Share Code/Device ID:").grid(row=1, column=0, sticky="e", padx=5)
        var = tk.StringVar()
        entry = ttk.Entry(creds_frame, textvariable=var, width=30)
        entry.grid(row=1, column=1, padx=5, pady=2)
        self.credential_vars["device_id"] = var
        self.credential_labels["device_id"] = "Share Code/Device ID"
        
        # Script Name field
        ttk.Label(creds_frame, text="Script Name:").grid(row=2, column=0, sticky="e", padx=5)
        var = tk.StringVar()
        entry = ttk.Entry(creds_frame, textvariable=var, width=30)
        entry.grid(row=2, column=1, padx=5, pady=2)
        self.credential_vars["script_name"] = var
        self.credential_labels["script_name"] = "Script Name"

    def _create_settings_section(self, parent):
        """Create trigger settings section."""
        settings_frame = ttk.LabelFrame(parent, text="Trigger Settings")
        settings_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        
        # Configure grid weights for proper resizing
        settings_frame.grid_columnconfigure(1, weight=1)
        
        # Trigger words
        ttk.Label(settings_frame, text="Trigger Words:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.words_var = tk.StringVar()
        self.words_entry = ttk.Entry(settings_frame, textvariable=self.words_var, width=40)
        self.words_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        ttk.Label(settings_frame, text="(comma-separated)", font=("TkDefaultFont", 8)).grid(row=1, column=1, sticky="w", padx=5, pady=(0, 5))
        
        # Duration and Intensity
        ttk.Label(settings_frame, text="Duration (1-15s):").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.duration_var = tk.StringVar(value="1")
        self.duration_spin = ttk.Spinbox(settings_frame, from_=1, to=15, textvariable=self.duration_var, width=5)
        self.duration_spin.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(settings_frame, text="Intensity (1-100):").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.intensity_var = tk.StringVar(value="10")
        self.intensity_spin = ttk.Spinbox(settings_frame, from_=1, to=100, textvariable=self.intensity_var, width=5)
        self.intensity_spin.grid(row=3, column=1, sticky="w", padx=5, pady=5)

    def _create_safety_section(self, parent):
        """Create safety settings section."""
        safety_frame = ttk.LabelFrame(parent, text="Safety Settings")
        safety_frame.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        
        # Configure grid weights for proper resizing
        safety_frame.grid_columnconfigure(1, weight=1)
        
        # Confirmation required
        self.confirmation_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(safety_frame, text="Require confirmation before shock", 
                       variable=self.confirmation_var).grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        
        # Cooldown period
        ttk.Label(safety_frame, text="Cooldown (seconds):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.cooldown_var = tk.StringVar(value="5")
        self.cooldown_spin = ttk.Spinbox(safety_frame, from_=0, to=60, textvariable=self.cooldown_var, width=5)
        self.cooldown_spin.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        # Max shocks per minute
        ttk.Label(safety_frame, text="Max shocks/minute:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.max_shocks_var = tk.StringVar(value="5")
        self.max_shocks_spin = ttk.Spinbox(safety_frame, from_=1, to=20, textvariable=self.max_shocks_var, width=5)
        self.max_shocks_spin.grid(row=2, column=1, sticky="w", padx=5, pady=5)

    def _test_emergency_hotkey(self):
        """Test the emergency hotkey functionality."""
        hotkey = self.hotkey_var.get()
        try:
            # Parse the hotkey
            keys = hotkey.split('+')
            if len(keys) == 1:
                # Single key
                key = keys[0].strip()
                if key == 'f12':
                    key_obj = keyboard.Key.f12
                else:
                    key_obj = key
            else:
                # Combination key
                modifiers = []
                main_key = keys[-1].strip()
                
                for mod in keys[:-1]:
                    mod = mod.strip().lower()
                    if mod == 'ctrl':
                        modifiers.append(keyboard.Key.ctrl)
                    elif mod == 'alt':
                        modifiers.append(keyboard.Key.alt)
                    elif mod == 'shift':
                        modifiers.append(keyboard.Key.shift)
                
                if main_key == 'esc':
                    key_obj = keyboard.Key.esc
                elif main_key == 'space':
                    key_obj = keyboard.Key.space
                elif main_key == 'f12':
                    key_obj = keyboard.Key.f12
                else:
                    key_obj = main_key
                
                # Create hotkey combination
                if modifiers:
                    key_obj = tuple(modifiers + [key_obj])
            
            # Test the hotkey
            self.hotkey_status_var.set("Testing hotkey... Press it now!")
            self.hotkey_status_label.config(foreground="orange")
            
            def on_hotkey_press():
                self.master.after(0, lambda: self.hotkey_status_var.set("✅ Hotkey working!"))
                self.master.after(0, lambda: self.hotkey_status_label.config(foreground="green"))
                return False  # Stop the listener
            
            # Start temporary listener
            temp_listener = keyboard.GlobalHotKeys({hotkey: on_hotkey_press})
            temp_listener.start()
            
            # Stop after 5 seconds
            self.master.after(5000, lambda: self._stop_hotkey_test(temp_listener))
            
        except Exception as e:
            self.hotkey_status_var.set(f"❌ Error: {str(e)}")
            self.hotkey_status_label.config(foreground="red")

    def _stop_hotkey_test(self, listener):
        """Stop the hotkey test listener."""
        try:
            listener.stop()
            if self.hotkey_status_var.get() == "Testing hotkey... Press it now!":
                self.hotkey_status_var.set("❌ Test timeout - try again")
                self.hotkey_status_label.config(foreground="red")
        except:
            pass

    def _create_emergency_hotkey_section(self, parent):
        """Create emergency hotkey settings section."""
        hotkey_frame = ttk.LabelFrame(parent, text="Emergency Hotkey")
        hotkey_frame.grid(row=4, column=0, sticky="ew", pady=(0, 10))
        
        # Configure grid weights for proper resizing
        hotkey_frame.grid_columnconfigure(1, weight=1)
        
        # Hotkey selection row
        ttk.Label(hotkey_frame, text="Emergency Stop Hotkey:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.hotkey_var = tk.StringVar(value="ctrl+shift+esc")
        self.hotkey_combo = ttk.Combobox(hotkey_frame, textvariable=self.hotkey_var, width=15, state="readonly")
        self.hotkey_combo['values'] = [
            "ctrl+shift+esc",
            "ctrl+alt+esc", 
            "ctrl+shift+space",
            "ctrl+alt+space",
            "f12",
            "ctrl+f12",
            "alt+f12"
        ]
        self.hotkey_combo.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        # Test hotkey button
        ttk.Button(hotkey_frame, text="Test Hotkey", command=self._test_emergency_hotkey).grid(row=0, column=2, padx=5, pady=5)
        
        # Hotkey status - separate row with proper spacing
        self.hotkey_status_var = tk.StringVar(value="Ready - will activate when listening starts")
        self.hotkey_status_label = ttk.Label(hotkey_frame, textvariable=self.hotkey_status_var, foreground="orange", wraplength=500)
        self.hotkey_status_label.grid(row=1, column=0, columnspan=3, sticky="ew", padx=5, pady=(0, 5))

    def _create_control_section(self, parent):
        """Create control buttons section."""
        control_frame = ttk.Frame(parent)
        control_frame.grid(row=6, column=0, pady=10)
        
        self.start_btn = ttk.Button(control_frame, text="Start Listening", command=self.start_listening)
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.stop_btn = ttk.Button(control_frame, text="Stop", command=self.stop_listening, state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        self.emergency_btn = ttk.Button(control_frame, text="EMERGENCY STOP", command=self.emergency_stop, 
                                      state="disabled", style="Emergency.TButton")
        self.emergency_btn.grid(row=0, column=2, padx=5)
        
        # Configure emergency button style
        style = ttk.Style()
        style.configure("Emergency.TButton", foreground="red", font=("TkDefaultFont", 10, "bold"))

    def _create_status_section(self, parent):
        """Create status display section."""
        status_frame = ttk.LabelFrame(parent, text="Status")
        status_frame.grid(row=7, column=0, sticky="ew", pady=(0, 10))
        
        self.status_var = tk.StringVar(value="Ready - Select platform and enter credentials")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var, wraplength=500)
        self.status_label.grid(row=0, column=0, padx=5, pady=5)
        
        # Progress bar for connection testing
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.grid(row=1, column=0, sticky="ew", padx=5, pady=2)

    def _create_stats_section(self, parent):
        """Create statistics section."""
        stats_frame = ttk.LabelFrame(parent, text="Statistics")
        stats_frame.grid(row=8, column=0, sticky="ew", pady=(0, 10))
        
        self.stats_text = tk.Text(stats_frame, height=4, width=60, state="disabled")
        self.stats_text.grid(row=0, column=0, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(stats_frame, orient="vertical", command=self.stats_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.stats_text.configure(yscrollcommand=scrollbar.set)

    def _on_platform_change(self):
        """Handle platform selection change."""
        platform = self.platform_var.get()
        self.current_platform = Platform(platform)
        self._update_platform_info()
        self._update_credential_labels()
        self.status_var.set(f"Platform changed to {platform.title()}")

    def _update_platform_info(self):
        """Update platform information display."""
        platform = self.platform_var.get()
        info_text = {
            "pishock": "PiShock: Original platform. Uses Username, Share Code, and Script Name.",
            "openshock": "OpenShock Direct: Open-source platform. Uses Device ID and API Token.",
            "pi3open": "OpenShock via pi3open: Translation layer. Uses PiShock format with OpenShock backend."
        }
        self.platform_info.config(text=info_text.get(platform, ""))

    def _update_credential_labels(self):
        """Update credential field labels based on platform."""
        platform = self.platform_var.get()
        
        if platform == "openshock":
            self.credential_labels["device_id"] = "Device ID"
        else:
            self.credential_labels["device_id"] = "Share Code/Device ID"

    def _validate_inputs(self) -> bool:
        """Validate all user inputs."""
        errors = []
        
        # Validate API key
        api_key = self.api_key_var.get().strip()
        if not api_key:
            errors.append("API key/token is required")
        elif not re.match(r'^[a-zA-Z0-9_-]+$', api_key):
            errors.append("API key contains invalid characters")
        
        # Validate credentials based on platform
        platform = self.platform_var.get()
        
        if platform == "openshock":
            # OpenShock only needs Device ID
            device_id = self.credential_vars["device_id"].get().strip()
            if not device_id:
                errors.append("Device ID is required for OpenShock")
        else:
            # PiShock and pi3open need all credentials
            for key, var in self.credential_vars.items():
                value = var.get().strip()
                if not value:
                    errors.append(f"{self.credential_labels[key]} is required")
        
        # Validate duration
        try:
            duration = int(self.duration_var.get())
            if not 1 <= duration <= 15:
                errors.append("Duration must be between 1 and 15 seconds")
        except ValueError:
            errors.append("Duration must be a valid number")
        
        # Validate intensity
        try:
            intensity = int(self.intensity_var.get())
            if not 1 <= intensity <= 100:
                errors.append("Intensity must be between 1 and 100")
        except ValueError:
            errors.append("Intensity must be a valid number")
        
        # Validate trigger words
        words_text = self.words_var.get().strip()
        if not words_text:
            errors.append("At least one trigger word is required")
        else:
            words = [w.strip() for w in words_text.split(",") if w.strip()]
            if not words:
                errors.append("At least one valid trigger word is required")
            elif len(words) > 10:
                errors.append("Maximum 10 trigger words allowed")
        
        # Validate cooldown
        try:
            cooldown = int(self.cooldown_var.get())
            if not 0 <= cooldown <= 60:
                errors.append("Cooldown must be between 0 and 60 seconds")
        except ValueError:
            errors.append("Cooldown must be a valid number")
        
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return False
        
        return True

    def _test_api_connection(self):
        """Test API connection with current credentials."""
        if not self._validate_inputs():
            return
        
        self.progress.start()
        self.status_var.set("Testing API connection...")
        
        def test_connection():
            try:
                platform = Platform(self.platform_var.get())
                success, message = self._send_test_command(platform)
                self.master.after(0, lambda: self._connection_test_result(success, message))
                
            except Exception as e:
                self.master.after(0, lambda: self._connection_test_result(False, f"Unexpected error: {e}"))
        
        threading.Thread(target=test_connection, daemon=True).start()

    def _send_test_command(self, platform: Platform) -> tuple[bool, str]:
        """Send a test command to the selected platform."""
        try:
            if platform == Platform.PISHOCK:
                return self._test_pishock()
            elif platform == Platform.OPENSHOCK:
                return self._test_openshock()
            elif platform == Platform.PI3OPEN:
                return self._test_pi3open()
            else:
                return False, "Unknown platform"
        except Exception as e:
            return False, str(e)

    def _test_pishock(self) -> tuple[bool, str]:
        """Test PiShock API connection."""
        payload = {
            "Username": self.credential_vars["username"].get(),
            "Apikey": self.api_key_var.get(),
            "Code": self.credential_vars["device_id"].get(),
            "Name": self.credential_vars["script_name"].get(),
            "Op": "0",
            "Duration": "1",
            "Intensity": "1"
        }
        
        response = requests.post(self.api_endpoints[Platform.PISHOCK], json=payload, timeout=10)
        response.raise_for_status()
        return True, "PiShock connection successful!"

    def _test_openshock(self) -> tuple[bool, str]:
        """Test OpenShock API connection."""
        headers = {
            "Open-Shock-Token": self.api_key_var.get(),
            "User-Agent": "PiShock-Universal-App/1.0",
            "Content-Type": "application/json"
        }
        
        payload = {
            "deviceId": self.credential_vars["device_id"].get(),
            "type": 0,  # Shock
            "intensity": 1,
            "duration": 1000  # OpenShock uses milliseconds
        }
        
        response = requests.post(self.api_endpoints[Platform.OPENSHOCK], json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        return True, "OpenShock connection successful!"

    def _test_pi3open(self) -> tuple[bool, str]:
        """Test pi3open translation layer connection."""
        payload = {
            "Username": self.credential_vars["username"].get(),
            "Apikey": self.api_key_var.get(),
            "Code": self.credential_vars["device_id"].get(),
            "Name": self.credential_vars["script_name"].get(),
            "Op": "0",
            "Duration": "1",
            "Intensity": "1"
        }
        
        response = requests.post(self.api_endpoints[Platform.PI3OPEN], json=payload, timeout=10)
        response.raise_for_status()
        return True, "pi3open connection successful!"

    def _connection_test_result(self, success: bool, message: str):
        """Handle API connection test result."""
        self.progress.stop()
        if success:
            self.status_var.set(f"✓ {message}")
            self.api_key = self.api_key_var.get()
            logger.info(f"API connection test successful: {message}")
        else:
            self.status_var.set(f"✗ {message}")
            logger.error(f"API connection test failed: {message}")

    def _confirm_shock(self) -> bool:
        """Show confirmation dialog before shock."""
        if not self.confirmation_var.get():
            return True
        
        platform = self.platform_var.get().title()
        result = messagebox.askyesno(
            "Confirm Shock",
            f"Are you sure you want to trigger a shock via {platform}?\n\n"
            f"Duration: {self.duration_var.get()}s\n"
            f"Intensity: {self.intensity_var.get()}\n\n"
            "Click 'Yes' to proceed or 'No' to cancel."
        )
        return result

    def _check_safety_limits(self) -> bool:
        """Check if shock is within safety limits."""
        current_time = time.time()
        
        # Check cooldown
        cooldown = int(self.cooldown_var.get())
        if current_time - self.last_shock_time < cooldown:
            remaining = cooldown - (current_time - self.last_shock_time)
            self.status_var.set(f"Cooldown active - {remaining:.1f}s remaining")
            return False
        
        # Check rate limit
        max_shocks = int(self.max_shocks_var.get())
        if self.shock_count >= max_shocks:
            self.status_var.set("Rate limit reached - too many shocks")
            return False
        
        return True

    def shock(self):
        """Send shock command with enhanced safety checks."""
        if not self._check_safety_limits():
            return
        
        if not self._confirm_shock():
            self.status_var.set("Shock cancelled by user")
            return
        
        platform = Platform(self.platform_var.get())
        
        try:
            self.status_var.set(f"Sending shock command via {platform.value}...")
            success, message = self._send_shock_command(platform)
            
            if success:
                # Update statistics
                self.last_shock_time = time.time()
                self.shock_count += 1
                
                self.status_var.set(f"Shock delivered via {platform.value}! ({self.shock_count} total)")
                self._update_statistics()
                
                logger.info(f"Shock delivered via {platform.value} - Duration: {self.duration_var.get()}s, Intensity: {self.intensity_var.get()}")
            else:
                self.status_var.set(f"Shock failed: {message}")
                logger.error(f"Shock failed via {platform.value}: {message}")
                
        except Exception as e:
            error_msg = f"Shock failed: {str(e)}"
            self.status_var.set(error_msg)
            logger.error(error_msg)

    def _send_shock_command(self, platform: Platform) -> tuple[bool, str]:
        """Send shock command to the selected platform."""
        try:
            if platform == Platform.PISHOCK:
                return self._send_pishock_command()
            elif platform == Platform.OPENSHOCK:
                return self._send_openshock_command()
            elif platform == Platform.PI3OPEN:
                return self._send_pi3open_command()
            else:
                return False, "Unknown platform"
        except Exception as e:
            return False, str(e)

    def _send_pishock_command(self) -> tuple[bool, str]:
        """Send shock command to PiShock."""
        payload = {
            "Username": self.credential_vars["username"].get(),
            "Apikey": self.api_key,
            "Code": self.credential_vars["device_id"].get(),
            "Name": self.credential_vars["script_name"].get(),
            "Op": "0",
            "Duration": self.duration_var.get(),
            "Intensity": self.intensity_var.get()
        }
        
        response = requests.post(self.api_endpoints[Platform.PISHOCK], json=payload, timeout=10)
        response.raise_for_status()
        return True, "PiShock shock sent successfully"

    def _send_openshock_command(self) -> tuple[bool, str]:
        """Send shock command to OpenShock."""
        headers = {
            "Open-Shock-Token": self.api_key,
            "User-Agent": "PiShock-Universal-App/1.0",
            "Content-Type": "application/json"
        }
        
        payload = {
            "deviceId": self.credential_vars["device_id"].get(),
            "type": 0,  # Shock
            "intensity": int(self.intensity_var.get()),
            "duration": int(self.duration_var.get()) * 1000  # Convert to milliseconds
        }
        
        response = requests.post(self.api_endpoints[Platform.OPENSHOCK], json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        return True, "OpenShock shock sent successfully"

    def _send_pi3open_command(self) -> tuple[bool, str]:
        """Send shock command via pi3open translation layer."""
        payload = {
            "Username": self.credential_vars["username"].get(),
            "Apikey": self.api_key,
            "Code": self.credential_vars["device_id"].get(),
            "Name": self.credential_vars["script_name"].get(),
            "Op": "0",
            "Duration": self.duration_var.get(),
            "Intensity": self.intensity_var.get()
        }
        
        response = requests.post(self.api_endpoints[Platform.PI3OPEN], json=payload, timeout=10)
        response.raise_for_status()
        return True, "pi3open shock sent successfully"

    def _update_statistics(self):
        """Update the statistics display."""
        platform = self.platform_var.get().title()
        stats = f"""Platform: {platform}
Shocks Today: {self.shock_count}
Last Shock: {datetime.fromtimestamp(self.last_shock_time).strftime('%H:%M:%S') if self.last_shock_time else 'Never'}
Listening: {'Yes' if self.is_listening else 'No'}
Cooldown: {self.cooldown_var.get()}s
Max/Min: {self.max_shocks_var.get()}/min"""
        
        self.stats_text.config(state="normal")
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats)
        self.stats_text.config(state="disabled")

    def on_press(self, key):
        """Enhanced key press handler with safety checks."""
        if not self.is_listening:
            return
        
        try:
            ch = key.char
        except AttributeError:
            return
        
        self.buffer += ch
        if len(self.buffer) > self.max_word_len:
            self.buffer = self.buffer[-self.max_word_len:]
        
        for word in self.words:
            if self.buffer.lower().endswith(word.lower()):
                self.master.after(0, self.shock)
                self.buffer = ""
                break

    def start_listening(self):
        """Start listening with enhanced validation."""
        if not self._validate_inputs():
            return
        
        if not self.api_key:
            messagebox.showerror("Error", "Please test API connection first")
            return
        
        # Parse trigger words
        words_text = self.words_var.get().strip()
        self.words = [w.strip() for w in words_text.split(",") if w.strip()]
        self.max_word_len = max(len(w) for w in self.words)
        
        # Reset statistics
        self.shock_count = 0
        self.last_shock_time = 0
        
        # Update UI
        self.is_listening = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.emergency_btn.config(state="normal")
        
        # Disable input fields
        for widget in [self.words_entry, self.duration_spin, self.intensity_spin]:
            widget.config(state="disabled")
        
        platform = self.platform_var.get().title()
        self.status_var.set(f"Listening for trigger words via {platform}...")
        self._update_statistics()
        
        # Start keyboard listener
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        
        # Start emergency hotkey
        self._start_emergency_hotkey()
        
        logger.info(f"Started listening for words: {self.words} via {platform}")

    def stop_listening(self):
        """Stop listening and reset UI."""
        if self.listener:
            self.listener.stop()
            self.listener = None
        
        # Stop emergency hotkey
        self._stop_emergency_hotkey()
        
        self.is_listening = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.emergency_btn.config(state="disabled")
        
        # Re-enable input fields
        for widget in [self.words_entry, self.duration_spin, self.intensity_spin]:
            widget.config(state="normal")
        
        self.status_var.set("Stopped")
        self._update_statistics()
        
        logger.info("Stopped listening")

    def _start_emergency_hotkey(self):
        """Start the global emergency hotkey listener."""
        try:
            hotkey = self.hotkey_var.get()
            if not hotkey:
                return
            
            # Stop existing hotkey if any
            self._stop_emergency_hotkey()
            
            # Create hotkey mapping
            hotkey_map = {hotkey: self.emergency_stop}
            
            # Start global hotkey listener
            self.emergency_hotkey = keyboard.GlobalHotKeys(hotkey_map)
            self.emergency_hotkey.start()
            
            # Update status
            self.hotkey_status_var.set(f"✅ Active: {hotkey}")
            self.hotkey_status_label.config(foreground="green")
            
            logger.info(f"Emergency hotkey activated: {hotkey}")
            
        except Exception as e:
            self.hotkey_status_var.set(f"❌ Error: {str(e)}")
            self.hotkey_status_label.config(foreground="red")
            logger.error(f"Failed to start emergency hotkey: {e}")

    def _stop_emergency_hotkey(self):
        """Stop the global emergency hotkey listener."""
        try:
            if self.emergency_hotkey:
                self.emergency_hotkey.stop()
                self.emergency_hotkey = None
                
            self.hotkey_status_var.set("Stopped - will reactivate when listening starts")
            self.hotkey_status_label.config(foreground="orange")
            
            logger.info("Emergency hotkey deactivated")
            
        except Exception as e:
            logger.error(f"Error stopping emergency hotkey: {e}")

    def emergency_stop(self):
        """Emergency stop - immediately stop all operations."""
        self.stop_listening()
        self.status_var.set("EMERGENCY STOP ACTIVATED")
        messagebox.showwarning("Emergency Stop", "All operations have been stopped immediately!")
        logger.warning("Emergency stop activated")

    def _load_settings(self):
        """Load settings from file if it exists."""
        settings_file = Path("pishock_universal_settings.json")
        if settings_file.exists():
            try:
                with open(settings_file, 'r') as f:
                    settings = json.load(f)
                
                # Load platform
                if 'platform' in settings:
                    self.platform_var.set(settings['platform'])
                    self._on_platform_change()
                
                # Load API key
                if 'api_key' in settings:
                    self.api_key_var.set(settings['api_key'])
                
                # Load credentials
                for key, var in self.credential_vars.items():
                    if key in settings:
                        var.set(settings[key])
                
                # Load other settings
                if 'words' in settings:
                    self.words_var.set(settings['words'])
                if 'duration' in settings:
                    self.duration_var.set(str(settings['duration']))
                if 'intensity' in settings:
                    self.intensity_var.set(str(settings['intensity']))
                if 'cooldown' in settings:
                    self.cooldown_var.set(str(settings['cooldown']))
                if 'max_shocks' in settings:
                    self.max_shocks_var.set(str(settings['max_shocks']))
                if 'confirmation' in settings:
                    self.confirmation_var.set(settings['confirmation'])
                if 'hotkey' in settings:
                    self.hotkey_var.set(settings['hotkey'])
                
                logger.info("Settings loaded from file")
                
            except Exception as e:
                logger.error(f"Failed to load settings: {e}")

    def _save_settings(self):
        """Save current settings to file."""
        settings = {
            'platform': self.platform_var.get(),
            'api_key': self.api_key_var.get(),
            'words': self.words_var.get(),
            'duration': int(self.duration_var.get()),
            'intensity': int(self.intensity_var.get()),
            'cooldown': int(self.cooldown_var.get()),
            'max_shocks': int(self.max_shocks_var.get()),
            'confirmation': self.confirmation_var.get(),
            'hotkey': self.hotkey_var.get()
        }
        
        # Add credentials
        for key, var in self.credential_vars.items():
            settings[key] = var.get()
        
        try:
            with open("pishock_universal_settings.json", 'w') as f:
                json.dump(settings, f, indent=2)
            logger.info("Settings saved to file")
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")

    def on_closing(self):
        """Handle application closing."""
        self._save_settings()
        self.stop_listening()
        self._stop_emergency_hotkey()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PiShockUniversalApp(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    root.mainloop()
