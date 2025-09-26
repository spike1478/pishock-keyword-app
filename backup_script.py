#!/usr/bin/env python3
"""
PiShock Project Backup Script
Creates timestamped backups of the PiShock project files.
"""

import os
import shutil
import datetime
import zipfile
from pathlib import Path

def create_backup():
    """Create a timestamped backup of the PiShock project."""
    
    # Get the current directory (project root)
    project_root = Path.cwd()
    backup_dir = project_root / "backups"
    
    # Create backup directory if it doesn't exist
    backup_dir.mkdir(exist_ok=True)
    
    # Generate timestamp for backup name
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"pishock_backup_{timestamp}"
    backup_path = backup_dir / backup_name
    
    # Files to backup (excluding backup folder and build artifacts)
    files_to_backup = [
        "pishock_app.py",
        "trigger.py", 
        "README.md",
        "LICENCE",
        "pishock_app.spec"
    ]
    
    # Create backup directory
    backup_path.mkdir(exist_ok=True)
    
    print(f"Creating backup: {backup_name}")
    print(f"Backup location: {backup_path}")
    
    # Copy files to backup directory
    backed_up_files = []
    for file_name in files_to_backup:
        source_file = project_root / file_name
        if source_file.exists():
            dest_file = backup_path / file_name
            shutil.copy2(source_file, dest_file)
            backed_up_files.append(file_name)
            print(f"  ✓ Backed up: {file_name}")
        else:
            print(f"  ⚠ File not found: {file_name}")
    
    # Create a zip archive of the backup
    zip_path = backup_dir / f"{backup_name}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_name in backed_up_files:
            file_path = backup_path / file_name
            zipf.write(file_path, file_name)
    
    print(f"\nBackup completed successfully!")
    print(f"Files backed up: {len(backed_up_files)}")
    print(f"Backup folder: {backup_path}")
    print(f"Zip archive: {zip_path}")
    
    return backup_path, zip_path

def list_backups():
    """List all available backups."""
    backup_dir = Path.cwd() / "backups"
    if not backup_dir.exists():
        print("No backup directory found.")
        return
    
    backups = list(backup_dir.glob("pishock_backup_*"))
    if not backups:
        print("No backups found.")
        return
    
    print("Available backups:")
    for backup in sorted(backups):
        if backup.is_dir():
            print(f"  📁 {backup.name}")
        elif backup.suffix == '.zip':
            print(f"  📦 {backup.name}")

if __name__ == "__main__":
    print("PiShock Project Backup Utility")
    print("=" * 40)
    
    # Create the backup
    backup_folder, zip_file = create_backup()
    
    print("\n" + "=" * 40)
    list_backups()
