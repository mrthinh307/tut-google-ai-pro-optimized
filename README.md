# TUT Google AI Pro Optimized

**English** | [Tiếng Việt](README.vi.md)

An automation toolkit for inspecting hidden offers, claiming **$0 free trials**, and **stacking subscription duration for Google AI Pro (5 TB)** via Android Play Billing (optimized for **MuMu Player** emulators or rooted Android devices).

---

## 1. How It Works

Many Google One promotional trial offers (such as `12months-eft`, `6months-eft`, `eft-3months`, etc.) are not displayed in the web UI or inside the app, but are returned directly by the **Google Play Billing (`BillingClient`)** library.

Instead of patching APKs or installing Xposed, `ultra0.py` uses **runtime Frida injection**:

1. **Device Environment Preparation**: Checks `root` access, disables system animations (for fast UI dumps), clears blocking proxies, and pushes `frida-server` plus the embedded `BillingClient` module (`module_521.apk`) to `/data/local/tmp/`.
2. **Account Context Sync**: Resolves the real active Google email on the device, clears Play Store & Google One billing caches (`sku_details.db`, `app_commerce_acquire_cache`), and syncs the Google One package owner in Play Store's `localappstate.db` to prevent stale offer caches or cross-account conflicts.
3. **Existing Subscription Check (when stacking with `--stack`)**:
   - Reads the active `purchaseToken` belonging to the target account from `library.db` (or via Play Billing `queryPurchases`).
   - If the current subscription is **Canceled (`autoRenewing = false`)**, the script automatically opens Play Store Subscriptions and attempts to **Resubscribe** so stacking can proceed.
4. **Borrowing the Google One Process for Play Billing**:
   - Injects JavaScript into `com.google.android.apps.subscriptions.red` (Google One) using **Frida 16.5.9**.
   - Loads `module_521.apk` via `DexClassLoader`, initializes `BillingClient`, and queries `queryProductDetails` to locate the target free-trial `offerToken`.
   - In stack mode (`--stack`), passes `oldPurchaseToken` together with `SubscriptionUpdateParams` using `prorationMode = 5` (`CHARGE_FULL_PRICE`) so **remaining trial days are converted and carried forward** instead of being overwritten.
5. **Pre-Confirmation Safety Checks**:
   - Monitors the Google Play Billing sheet via `uiautomator`.
   - **Only taps `Subscribe`** when a `$0` / free-trial offer is verified (and refuses plain 1-month trials or non-zero prices).
   - If an `Error` or ineligible dialog appears, dismisses it, clears billing cache, and exits with a non-zero status code so batch automation can advance to the next step.
6. **Reporting**: Saves per-account execution details as JSON files inside `ultra0-report/`.

---

## 2. Repository Structure

| File / Folder | Purpose |
| :--- | :--- |
| `Cai_dat_moi_truong.bat` | One-click Windows environment setup (runs `setup_env.py`) |
| `0_Kiem_tra_moi_truong.bat` | Verifies emulator/device connection, root, `frida-server`, Billing module, and Play Store |
| `1_Xem_danh_sach_offer.bat` | Lists all available offers & tokens for the current account (read-only, no purchase launched) |
| `2_Pro_12_thang_Buoc_1.bat` | Step 1: Subscribe to the **12-month** Pro 5TB trial (`--plan pro12`) |
| `3_Pro_Them_6_thang_Buoc_2.bat` | Step 2: Stack **+6 months** (`--stack --plan pro6`) |
| `4_Pro_Them_6_thang_Buoc_3.bat` | Step 3: Stack another **+6 months** (`--stack --plan pro6b`) |
| `5_Pro_Du_phong_6_thang.bat` | Backup: Stack **+6 months** (`--stack --plan pro6c`) |
| `6_Pro_3_thang_eft.bat` | Stack / claim the **3-month** offer (`--stack --plan pro3`) |
| `7_Auto_Chay_2_den_6.bat` | Automated runner looping scripts `2` through `6`; advances on error and falls back to random retries until one succeeds |
| `ultra0.py` | Core script handling ADB automation, account sync, Frida injection, and Billing UI confirmation |
| `setup_env.py` | Checks Python, installs `frida==16.5.9`, locates/downloads `adb`, connects emulator, and runs `--check` |
| `query_sku.py` | Standalone CLI helper to inspect all offers for arbitrary SKU IDs |
| `requirements.txt` | Python dependency specification (`frida>=16.0`, `16.5.9` recommended) |
| `Huong_dan_su_dung.txt` | Original Vietnamese usage notes |
| `README.vi.md` | Full Vietnamese documentation |
| `ultra0-report/` | Output directory for per-account JSON run reports |

---

## 3. Prerequisites

### On Windows PC
- **Python 3.10+** (minimum 3.9).
- **Frida `16.5.9`** *(must use the `16.x` branch; `17.x` removed the Java bridge and will not work — `setup_env.py` automatically installs/downgrades to `16.5.9`)*.
- **ADB** (auto-detected from MuMu Player, `PATH`, or downloaded automatically via `platform-tools` by `setup_env.py`).

### On MuMu Emulator / Android Device
1. **Root** access and **USB / ADB Debugging** enabled.
2. **Google Play Store** and **Google One** (`com.google.android.apps.subscriptions.red`) installed.
3. Target Google account signed in on the device.
4. A **payment method** added to the Google account (a low-limit card is recommended in case you forget to cancel before renewal).
5. Play Store opens and connects normally (no blocking proxy).

---

## 4. Quick Start Guide

### Step 1: One-Click Environment Setup
Double-click **`Cai_dat_moi_truong.bat`** (or run `python setup_env.py`). It will automatically:
- Verify your Python version.
- Install `frida==16.5.9`.
- Locate `adb.exe` (or download `platform-tools` from Google).
- Connect to common emulator ADB ports (`16384`, `7555`, `16416`, `21503`, `62001`).
- Run `ultra0.py --check` to validate the setup.

### Step 2: Check Environment & Inspect Offers (Risk-Free)
1. Double-click **`0_Kiem_tra_moi_truong.bat`** → Confirm all checks pass (`✅`).
2. Double-click **`1_Xem_danh_sach_offer.bat`** → View available offers on the active account without opening any checkout sheet.

### Step 3: Claim & Stack Subscriptions

#### Option A — Manual Step-by-Step (Recommended for Understanding Each Stage)
Run the batch scripts in order:
1. **`2_Pro_12_thang_Buoc_1.bat`** → Claim the initial 12-month plan (`pro12`).
2. **`3_Pro_Them_6_thang_Buoc_2.bat`** → Stack +6 months (`pro6`, ~18 months total).
3. **`4_Pro_Them_6_thang_Buoc_3.bat`** → Stack +6 months (`pro6b`, ~24 months total).
4. **`5_Pro_Du_phong_6_thang.bat`** → Stack backup +6 months (`pro6c`).
5. **`6_Pro_3_thang_eft.bat`** → Attempt +3 months (`pro3`).

> **How to verify a VALID stacked checkout sheet:**
> - Due today: **`0`** (e.g., `Today: US$0` / `JP¥0`).
> - Shows converted days carried over from your current plan (e.g., *`546 days (including 364 days converted from your current plan's remaining time)`*).
> - **Billing start date** is pushed forward into the future (12 → 18 → 24 months ahead).
>
> If the sheet shows **billing starts at the old expiry date or charges immediately today**, do not confirm — verify that the current subscription is **Active (auto-renew enabled)** and `--stack` is set.

#### Option B — Automated Runner
Double-click **`7_Auto_Chay_2_den_6.bat`**:
- Sets `AUTO_FLOW=1` so individual `.bat` files return exit codes immediately without pausing.
- Sequentially tries scripts `2` through `6`.
- Moves to the next script automatically whenever an error occurs.
- After the first pass, switches to random retry mode (`RANDOM`) until a script succeeds (`exit code 0`), or stop anytime with `Ctrl + C`.

---

## 5. Plans (`--plan`) & SKU Mapping

| `--plan` Value | Batch Script | Play Billing SKU | Preferred Offer ID | Notes |
| :--- | :--- | :--- | :--- | :--- |
| `pro12` | `2_Pro_12_thang_Buoc_1.bat` | `g1.2tb.ai.subs_variant` | `12months-eft` | Initial 12-month Pro 5TB trial |
| `pro6` | `3_Pro_Them_6_thang_Buoc_2.bat` | `g1.2tb.ai.subs_variant` | `6months-eft` | Stack +6 months (step 2) |
| `pro6b` | `4_Pro_Them_6_thang_Buoc_3.bat` | `g1.2tb.ai.subs_variant` | `6months-eft-2` | Stack +6 months (step 3) |
| `pro6c` | `5_Pro_Du_phong_6_thang.bat` | `g1.2tb.ai.subs_variant` | `6months-eft-ss-2026` | Stack +6 months (backup) |
| `pro3` | `6_Pro_3_thang_eft.bat` | `g1.2tb.ai.3months_eft` | `eft-3months` | 3-month trial offer |
| `5x` / `20x` / `auto` | *(CLI)* | `g1.play.20tb`, `g1.play.ai.pro`, `g1.30tb` | Longest available | Legacy Ultra plans (rarely offered to regular accounts) |

---

## 6. Advanced CLI Usage

### Running `ultra0.py` Directly
```bash
# Check environment
python ultra0.py --check

# List offers for the currently signed-in device account (read-only)
python ultra0.py --account "current@device" --no-add --force --list --plan pro12

# Run for the currently signed-in account
python ultra0.py --account "current@device" --no-add --force --plan pro12
python ultra0.py --account "current@device" --no-add --force --stack --plan pro6

# Target a specific account (email:password:totp)
python ultra0.py --account "user@gmail.com:password:2FAKEY" --plan pro12

# Batch run from an accounts file (format per line: email----password----recovery----totp)
python ultra0.py accounts.txt --plan pro12
```

**Main CLI Flags:**
- `--check`: Run ADB, root, Frida, Billing module, and Play Store diagnostics.
- `--list`: Query and print offers/tokens without launching checkout.
- `--plan {auto,5x,20x,pro12,pro6,pro6b,pro6c,pro3}`: Select the target plan/offer.
- `--stack`: Enable subscription upgrade stacking using the current active `purchaseToken`.
- `--old-token <token>`: Manually supply `oldPurchaseToken` when using `--stack`.
- `--mode <1..5>`: Override `prorationMode` (defaults to `5` = `CHARGE_FULL_PRICE` when stacking).
- `--no-add`: Skip automatic Google account login (use an account already on the device).
- `--no-switch`: Do not auto-switch Play Store accounts; only verify the active one matches.
- `--force`: Skip Play Store UI account verification.
- `--serial <id>`: Target a specific ADB device serial when multiple devices/emulators are attached.

### Querying Custom SKUs with `query_sku.py`
Requires `frida-server` running (or forwarded on `127.0.0.1:27042`) with Google One open:
```bash
python query_sku.py g1.2tb.ai.subs_variant g1.2tb.ai.3months_eft
```

---

## 7. Important Notes & Troubleshooting

- **Keep the subscription Active while stacking**: A canceled plan (`autoRenewing=false`) cannot be stacked via `SubscriptionUpdateParams`. Finish all stacking steps first, then cancel auto-renewal afterward (benefits remain valid until the expiration date).
- **Stuck at `connecting`**: Play Store is not running or froze — open Play Store manually or restart the emulator.
- **`Already subscribed` / `ITEM_UNAVAILABLE`**: Usually caused by missing `--stack`, stale `sku_details.db` cache, or a canceled existing subscription. The latest `ultra0.py` automatically clears caches, syncs account state, and attempts resubscription; if repeated errors occur, wait ~24 hours to avoid risk-control rate limits.
- **`No internet connection`**: Temporary emulator network/proxy hiccup — retry after a few seconds or restart the emulator.
- **Remember to cancel before renewal**: Check `https://play.google.com/store/account/subscriptions` after stacking to confirm the next billing date and cancel auto-renewal if you do not want to be charged at the end of the trial.
