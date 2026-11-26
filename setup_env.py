"""setup_env.py —— One-click environment preparation (Python + Frida + ADB + Emulator Connection)

Performs 4 key tasks:
  1. Validates Python version (3.10+ recommended)
  2. Installs Frida 16.5.9 (required for scripting injection; 17.x deprecated Java bridge)
  3. Locates ADB: environment variable → PATH → bundled MuMu ADB → auto-downloads platform-tools if missing
  4. Connects to emulator and runs self-test via ultra0.py --check

Usage: Double-click setup_environment.bat or run: python setup_env.py
"""

import os
import platform
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

BASE = Path(__file__).resolve().parent
ADB_CANDIDATES = [
    os.environ.get("ADB_PATH", ""),
    r"C:\Program Files\Netease\MuMuPlayer-12.0\shell\adb.exe",
    r"C:\Program Files\Netease\MuMuPlayerGlobal-12.0\shell\adb.exe",
    r"C:\Program Files (x86)\Netease\MuMuPlayer-12.0\shell\adb.exe",
    r"D:\Program Files\Netease\MuMu\nx_main\adb.exe",
    r"D:\Program Files\Netease\MuMu\nx_device\12.0\shell\adb.exe",
    r"C:\Program Files\Netease\MuMu\nx_main\adb.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe"),
    os.path.expandvars(
        r"%USERPROFILE%\AppData\Local\Android\Sdk\platform-tools\adb.exe"
    ),
]
PLATFORM_TOOLS_URL = (
    "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
)


def step(msg):
    print(f"\n▶ {msg}", flush=True)


def ok(msg):
    print(f"   ✅ {msg}", flush=True)


def warn(msg):
    print(f"   ⚠️  {msg}", flush=True)


def die(msg):
    print(f"\n❌ {msg}", flush=True)
    sys.exit(1)


def check_python():
    step("Checking Python version")
    v = sys.version_info
    print(f"   {platform.python_version()}  ({platform.architecture()[0]})")
    if v < (3, 9):
        die(
            "Python version is too old. Please install 3.10 or higher: https://www.python.org/downloads/"
        )
    ok("Python environment is compatible")


def install_frida():
    step("Installing Frida 16.5.9 (required for injection)")
    try:
        import frida

        if frida.__version__.startswith("16."):
            ok(f"Frida {frida.__version__} is already installed")
            return
        warn(
            f"Currently running Frida {frida.__version__} (17.x is incompatible). Downgrading to 16.5.9..."
        )
    except Exception:
        pass

    cmds = [
        [sys.executable, "-m", "pip", "install", "--no-cache-dir", "frida==16.5.9"],
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--no-cache-dir",
            "-i",
            "https://pypi.org/simple",
            "frida==16.5.9",
        ],
    ]
    for c in cmds:
        print("   " + " ".join(c[2:]))
        r = subprocess.run(c, capture_output=True, text=True, errors="ignore")
        if r.returncode == 0:
            break
        print("   " + (r.stderr or r.stdout).strip().splitlines()[-1][:160])
    try:
        import importlib
        import frida

        importlib.reload(frida)
        ok(f"Frida {frida.__version__} installed successfully")
    except Exception as e:
        die(f"Frida installation failed: {e}\n   Try running manually: pip install frida==16.5.9")


def download_platform_tools():
    dest = BASE / "platform-tools"
    print(f"   Downloading platform-tools to {dest}")
    tmp = Path(tempfile.gettempdir()) / "platform-tools.zip"
    with (
        urllib.request.urlopen(PLATFORM_TOOLS_URL, timeout=180) as r,
        open(tmp, "wb") as f,
    ):
        f.write(r.read())
    with zipfile.ZipFile(tmp) as z:
        z.extractall(BASE)
    tmp.unlink(missing_ok=True)
    adb = dest / "adb.exe"
    if adb.exists():
        ok(f"platform-tools ready: {adb}")
        return str(adb)
    die("Failed to find adb.exe after extracting platform-tools")


def find_adb():
    step("Locating ADB binary")
    for c in ADB_CANDIDATES:
        if not c:
            continue
        if c in ("adb", "adb.exe"):
            continue
        if Path(c).exists():
            ok(f"Using {c}")
            return c
    w = shutil.which("adb")
    if w:
        ok(f"Using {w} from system PATH")
        return w
    warn("No existing ADB found. Auto-downloading Google platform-tools...")
    return download_platform_tools()


def connect_emulator(adb):
    step("Connecting to emulator")
    ports = ["16384", "7555", "16416", "21503", "62001"]
    for p in ports:
        subprocess.run(
            [adb, "connect", f"127.0.0.1:{p}"],
            capture_output=True,
            text=True,
            errors="ignore",
        )
    out = subprocess.run(
        [adb, "devices"], capture_output=True, text=True, errors="ignore"
    ).stdout
    devices = [l.split("\t")[0] for l in out.splitlines()[1:] if "\tdevice" in l]
    if not devices:
        warn(
            "No devices connected yet. Please ensure your emulator (e.g. MuMu) is launched with ADB debugging enabled in Settings."
        )
        print("   " + out.strip().replace("\n", "\n   "))
        return None
    ok(f"Connected devices: {', '.join(devices)}")
    return devices[0]


def run_check(adb, serial):
    step("Running environment self-test (ultra0.py --check)")
    env = dict(os.environ)
    env["ADB_PATH"] = adb
    env["PYTHONIOENCODING"] = "utf-8"
    r = subprocess.run(
        [sys.executable, "ultra0.py", "--check"],
        cwd=str(BASE),
        env=env,
        capture_output=True,
        encoding="utf-8",
        errors="ignore",
    )
    print(r.stdout.strip() or r.stderr.strip())
    return r.returncode == 0


def main():
    print("=" * 60)
    print("  Google Ultra / Pro One-Click Environment Setup")
    print("=" * 60)
    check_python()
    install_frida()
    adb = find_adb()
    serial = connect_emulator(adb)

    if serial:
        good = run_check(adb, serial)
        print("\n" + "=" * 60)
        if good:
            print(
                "  ✅ Environment is ready! Double-click «12months-eft.bat» to begin."
            )
        else:
            print(
                "  ⚠️  Self-test warnings detected. Review hints above (ensure Google Play Store is open)."
            )
        print("=" * 60)
    else:
        print("\nPlease launch your emulator, enable ADB debugging in Settings, and re-run this script.")


if __name__ == "__main__":
    main()
