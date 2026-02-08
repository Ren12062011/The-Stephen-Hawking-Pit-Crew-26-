import platform
import subprocess
from typing import List, Dict, Any




def detect_usb_devices() -> List[Dict[str, Any]]:
    
    devices = []
    system = platform.system()
   
    try:
        if system == "Windows":
            devices = _detect_windows_usb()
        elif system == "Darwin":  
            devices = _detect_macos_usb()
        elif system == "Linux":
            devices = _detect_linux_usb()
    except Exception as e:
        print(f"Error detecting USB devices: {e}")
   
    return devices




def _detect_windows_usb() -> List[Dict[str, Any]]:
   
    devices = []
    try:
        import serial.tools.list_ports
       
        ports = serial.tools.list_ports.comports()
        for port in ports:
            devices.append({
                "port": port.device,
                "description": port.description,
                "manufacturer": port.manufacturer or "Unknown",
                "device_type": "USB/Serial",
                "platform": "Windows"
            })
    except ImportError:
       
        try:
            result = subprocess.run(
                ['powershell', '-Command',
                 'Get-WmiObject Win32_SerialPort | Select-Object Name, Description'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                for line in result.stdout.split('\n')[3:]:
                    if line.strip():
                        parts = line.split()
                        if parts:
                            devices.append({
                                "port": parts[0],
                                "description": " ".join(parts[1:]),
                                "manufacturer": "Unknown",
                                "device_type": "USB/Serial",
                                "platform": "Windows"
                            })
        except Exception as e:
            print(f"Windows USB detection error: {e}")
   
    return devices




def _detect_macos_usb() -> List[Dict[str, Any]]:
    
    devices = []
    try:
        result = subprocess.run(
            ['ls', '-la', '/dev/tty.usbserial*'],
            capture_output=True,
            text=True,
            timeout=5
        )
       
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if '/dev/tty' in line:
                    parts = line.split()
                    if len(parts) >= 9:
                        port = parts[-1]
                        devices.append({
                            "port": port,
                            "description": "USB Serial Device",
                            "manufacturer": "Unknown",
                            "device_type": "USB/Serial",
                            "platform": "macOS"
                        })
    except Exception as e:
        print(f"macOS USB detection error: {e}")
   
    return devices




def _detect_linux_usb() -> List[Dict[str, Any]]:
    
    devices = []
    try:
      
        result = subprocess.run(
            ['ls', '/dev/ttyUSB*'],
            capture_output=True,
            text=True,
            timeout=5
        )
       
        if result.returncode == 0:
            for port in result.stdout.split('\n'):
                if port.strip():
                    devices.append({
                        "port": port.strip(),
                        "description": "USB Serial Device",
                        "manufacturer": "Unknown",
                        "device_type": "USB/Serial",
                        "platform": "Linux"
                    })
    except Exception as e:
        print(f"Linux USB detection error: {e}")
   
    return devices




def detect_bluetooth_devices() -> List[Dict[str, Any]]:
    
    devices = []
    system = platform.system()
   
    try:
        if system == "Windows":
            devices = _detect_windows_bluetooth()
        elif system == "Darwin": 
            devices = _detect_macos_bluetooth()
        elif system == "Linux":
            devices = _detect_linux_bluetooth()
    except Exception as e:
        print(f"Error detecting Bluetooth devices: {e}")
   
    return devices




def _detect_windows_bluetooth() -> List[Dict[str, Any]]:
    
    devices = []
    try:
        result = subprocess.run(
            ['powershell', '-Command',
             'Get-WmiObject Win32_PnPDevice | Where-Object {$_.Description -like "*Bluetooth*"} | Select-Object Description, Manufacturer'],
            capture_output=True,
            text=True,
            timeout=5
        )
       
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')[3:]
            for line in lines:
                if line.strip():
                    devices.append({
                        "name": line.strip(),
                        "address": "Unknown",
                        "status": "Paired",
                        "device_type": "Bluetooth",
                        "platform": "Windows"
                    })
    except Exception as e:
        print(f"Windows Bluetooth detection error: {e}")
   
    return devices




def _detect_macos_bluetooth() -> List[Dict[str, Any]]:
    
    devices = []
    try:
        result = subprocess.run(
            ['system_profiler', 'SPBluetoothDataType'],
            capture_output=True,
            text=True,
            timeout=5
        )
       
        if result.returncode == 0:
            current_device = {}
            for line in result.stdout.split('\n'):
                if 'Device Name:' in line:
                    current_device['name'] = line.split('Device Name: ')[-1].strip()
                elif 'Address:' in line:
                    current_device['address'] = line.split('Address: ')[-1].strip()
                    current_device['status'] = 'Connected'
                    current_device['device_type'] = 'Bluetooth'
                    current_device['platform'] = 'macOS'
                    if current_device:
                        devices.append(current_device)
                    current_device = {}
    except Exception as e:
        print(f"macOS Bluetooth detection error: {e}")
   
    return devices




def _detect_linux_bluetooth() -> List[Dict[str, Any]]:
   
    devices = []
    try:
        result = subprocess.run(
            ['bluetoothctl', 'devices'],
            capture_output=True,
            text=True,
            timeout=5
        )
       
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if line.strip().startswith('Device'):
                    parts = line.strip().split()
                    if len(parts) >= 3:
                        devices.append({
                            "address": parts[1],
                            "name": " ".join(parts[2:]),
                            "status": "Paired",
                            "device_type": "Bluetooth",
                            "platform": "Linux"
                        })
    except Exception as e:
        print(f"Linux Bluetooth detection error: {e}")
   
    return devices




def get_all_devices() -> Dict[str, Any]:
        return {
        "usb_devices": detect_usb_devices(),
        "bluetooth_devices": detect_bluetooth_devices(),
        "platform": platform.system(),
        "python_version": platform.python_version()
    }




def is_device_connected() -> bool:
    """Check if any device is connected"""
    devices = get_all_devices()
    return bool(devices["usb_devices"] or devices["bluetooth_devices"])




def get_device_summary() -> str:
    """Get a human-readable summary of connected devices"""
    devices = get_all_devices()
   
    usb_count = len(devices["usb_devices"])
    bt_count = len(devices["bluetooth_devices"])
   
    summary = f"USB Devices: {usb_count} | Bluetooth Devices: {bt_count}"
   
    return summary
