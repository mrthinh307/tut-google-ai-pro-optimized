"""query_sku.py —— Scan and lookup all Google One / Gemini AI Product IDs (SKUs) and Offers

Supports full catalog scanning: Ultra 30TB, Ultra 20TB, AI Ultra, AI Pro, EFT (extended free trial)
packages, and IP promotional discount offers (75%, 80%, 85%, 90% off).

Usage:
    python query_sku.py                  # Scan full default catalog of known SKUs
    python query_sku.py --free-only      # Show only free trial ($0.00) offers
    python query_sku.py g1.ai.ultra ...  # Query specific custom SKUs
"""

import argparse
import json
import os
import subprocess
import sys
import threading
import time
from typing import Dict, List, Optional, Tuple

import frida

try:
    import ultra0
except ImportError:
    ultra0 = None


# ==============================================================================
# CANDIDATE SKU CATALOG (Google One & Gemini AI Promotional Campaigns)
# ==============================================================================
DEFAULT_SKU_CATALOG = [
    # --- Gemini AI Ultra 30TB ---
    "g1.30tb.3months_ip_75p.acq",
    "g1.30tb.3months_ip_80p.acq",
    "g1.30tb.3months_ip_85p.acq",
    "g1.30tb.3months_ip_90p.acq",
    "g1.30tb",
    "g1.30tb.annual",
    "g1.30tb.1month_eft",
    "g1.30tb.12months_eft",
    # --- Gemini AI Ultra ---
    "g1.ai.ultra",
    "g1.ai.ultra.annual",
    "g1.ai.ultra.1month_eft",
    "g1.ai.ultra.12months_eft",
    "g1.ai.ultra.3months_ip_75p.acq",
    "g1.ai.ultra.3months_ip_80p.acq",
    "g1.ai.ultra.3months_ip_85p.acq",
    "g1.ai.ultra.3months_ip_90p.acq",
    # --- AI Pro 30TB / g1.ai.pro ---
    "g1.ai.pro",
    "g1.ai.pro.annual",
    "g1.ai.pro.1month_eft",
    "g1.ai.pro.12months_eft",
    "g1.ai.pro.3months_ip_75p.acq",
    "g1.ai.pro.3months_ip_80p.acq",
    "g1.ai.pro.3months_ip_85p.acq",
    "g1.ai.pro.3months_ip_90p.acq",
    # --- Play 20TB (Ultra 5x) ---
    "g1.play.20tb",
    "g1.play.20tb.annual",
    "g1.play.20tb.1month_eft",
    "g1.play.20tb.12months_eft",
    "g1.play.20tb.3months_ip_75p.acq",
    "g1.play.20tb.3months_ip_80p.acq",
    "g1.play.20tb.3months_ip_85p.acq",
    "g1.play.20tb.3months_ip_90p.acq",
    # --- Play AI Pro 30TB (Ultra 20x) ---
    "g1.play.ai.pro",
    "g1.play.ai.pro.annual",
    "g1.play.ai.pro.1month_eft",
    "g1.play.ai.pro.12months_eft",
    "g1.play.ai.pro.3months_ip_75p.acq",
    "g1.play.ai.pro.3months_ip_80p.acq",
    "g1.play.ai.pro.3months_ip_85p.acq",
    "g1.play.ai.pro.3months_ip_90p.acq",
    # --- AI Pro 2TB / 5TB (subs_variant) ---
    "g1.2tb.ai.subs_variant",
    "g1.2tb.ai.1month_eft",
    "g1.2tb.ai.2months_eft",
    "g1.2tb.ai.3months_eft",
    "g1.2tb.ai.4months_eft",
    "g1.2tb.ai.6months_eft",
    "g1.2tb.ai.12months_eft",
]


# ==============================================================================
# FRIDA JAVASCRIPT INJECTION: BillingClient Scanner
# ==============================================================================
SCANNER_JS = r"""
var dexLoader = null;
var ctxRef = null;
var clientRef = null;

function L(v) { Java.classFactory.loader = v; }
function S(o) { send(o); }

rpc.exports = {
    init: function() {
        return new Promise(function(resolve, reject) {
            Java.perform(function() {
                try {
                    L(null);
                    ctxRef = Java.use("android.app.ActivityThread").currentApplication().getApplicationContext();
                    var DexClassLoader = Java.use("dalvik.system.DexClassLoader");
                    dexLoader = DexClassLoader.$new(
                        "/data/local/tmp/module_521.apk",
                        ctxRef.getCodeCacheDir().getAbsolutePath(),
                        null,
                        ctxRef.getClassLoader()
                    );
                    L(dexLoader);
                    var BillingClient = Java.use("com.android.billingclient.api.BillingClient");
                    var PUL = Java.use("com.android.billingclient.api.PurchasesUpdatedListener");
                    var Lst = Java.registerClass({
                        name: "sc.PurchListener" + Date.now(),
                        implements: [PUL],
                        methods: {
                            onPurchasesUpdated: function(r, p) {}
                        }
                    });

                    var b = BillingClient.newBuilder(ctxRef);
                    b.setListener(Lst.$new());
                    try { b.enablePendingPurchases(); } catch(e) {}
                    clientRef = b.build();

                    var SLL = Java.use("com.android.billingclient.api.BillingClientStateListener");
                    var SL = Java.registerClass({
                        name: "sc.StateListener" + Date.now(),
                        implements: [SLL],
                        methods: {
                            onBillingSetupFinished: function(r) {
                                S({ ev: "setup", code: r.getResponseCode() });
                                resolve(r.getResponseCode());
                            },
                            onBillingServiceDisconnected: function() {
                                S({ ev: "disconnected" });
                            }
                        }
                    });
                    clientRef.startConnection(SL.$new());
                } catch(e) {
                    S({ ev: "init_err", msg: String(e) });
                    reject(String(e));
                }
            });
        });
    },

    queryBatch: function(products) {
        Java.perform(function() {
            try {
                L(dexLoader);
                var Prod = Java.use("com.android.billingclient.api.QueryProductDetailsParams$Product");
                var Params = Java.use("com.android.billingclient.api.QueryProductDetailsParams");
                var PDL = Java.use("com.android.billingclient.api.ProductDetailsResponseListener");

                var arr = Java.use("java.util.ArrayList").$new();
                for (var k = 0; k < products.length; k++) {
                    arr.add(Prod.newBuilder().setProductId(products[k]).setProductType("subs").build());
                }

                var PL = Java.registerClass({
                    name: "sc.RespListener" + Date.now() + "_" + Math.floor(Math.random() * 10000),
                    implements: [PDL],
                    methods: {
                        onProductDetailsResponse: function(res, list) {
                            var code = res.getResponseCode();
                            var n = (list ? list.size() : 0);
                            if (code !== 0 || !list || n === 0) {
                                S({ ev: "batch_done", code: code, count: 0 });
                                return;
                            }
                            L(dexLoader);
                            var PD = Java.use("com.android.billingclient.api.ProductDetails");
                            var SOD = Java.use("com.android.billingclient.api.ProductDetails$SubscriptionOfferDetails");
                            var PP = Java.use("com.android.billingclient.api.ProductDetails$PricingPhase");

                            for (var i = 0; i < list.size(); i++) {
                                var pd = Java.cast(list.get(i), PD);
                                var pid = String(pd.getProductId());
                                var title = String(pd.getTitle() || "");
                                var name = String(pd.getName() || "");
                                var offs = pd.getSubscriptionOfferDetails();
                                if (!offs) continue;
                                for (var j = 0; j < offs.size(); j++) {
                                    var o = Java.cast(offs.get(j), SOD);
                                    var oid = String(o.getOfferId() || "");
                                    var tok = String(o.getOfferToken() || "");
                                    var basePlanId = "";
                                    try { basePlanId = String(o.getBasePlanId() || ""); } catch(e) {}
                                    var ph = o.getPricingPhases().getPricingPhaseList();
                                    var first = Java.cast(ph.get(0), PP);
                                    var micros = String(first.getPriceAmountMicros());
                                    var formattedPrice = "";
                                    try { formattedPrice = String(first.getFormattedPrice() || ""); } catch(e) {}
                                    var period = String(first.getBillingPeriod());

                                    S({
                                        ev: "offer",
                                        product: pid,
                                        offerId: oid,
                                        basePlanId: basePlanId,
                                        micros: micros,
                                        formattedPrice: formattedPrice,
                                        period: period,
                                        token: tok,
                                        title: title,
                                        name: name
                                    });
                                }
                            }
                            S({ ev: "batch_done", code: code, count: n });
                        }
                    }
                });

                clientRef.queryProductDetailsAsync(Params.newBuilder().setProductList(arr).build(), PL.$new());
            } catch(e) {
                S({ ev: "batch_err", msg: String(e) });
            }
        });
    }
};
"""


# ==============================================================================
# CONNECTION & SYSTEM HELPERS
# ==============================================================================
def get_device(remote_addr: Optional[str] = None) -> frida.core.Device:
    """Detects active Frida device: USB or common emulator ports."""
    if remote_addr:
        dev = frida.get_device_manager().add_remote_device(remote_addr)
        dev.enumerate_processes()
        return dev

    # 1. Try via ultra0.get_frida_device() if available
    if ultra0 and hasattr(ultra0, "get_frida_device"):
        try:
            d = ultra0.get_frida_device(timeout=2)
            d.enumerate_processes()
            return d
        except Exception:
            pass

    # 2. Try direct USB connection
    try:
        dev = frida.get_usb_device(timeout=1)
        if dev:
            dev.enumerate_processes()
            return dev
    except Exception:
        pass

    # 3. Try standard emulator endpoints (MuMu, LDPlayer, Nox, etc.)
    dm = frida.get_device_manager()
    known_ports = [
        "127.0.0.1:27042",  # MuMu 12 frida-server
        "127.0.0.1:7555",   # MuMu standard adb
        "127.0.0.1:16384",  # MuMu alternate
        "127.0.0.1:5555",   # LDPlayer / BlueStacks / Genymotion
    ]
    for addr in known_ports:
        try:
            d = dm.add_remote_device(addr)
            d.enumerate_processes()
            return d
        except Exception:
            continue

    raise RuntimeError("No active Frida device detected. Please ensure your emulator is running and frida-server is active.")


def find_or_start_g1(dev: frida.core.Device) -> int:
    """Finds Google One process PID; attempts to launch app via adb if not running."""
    for p in dev.enumerate_processes():
        if "subscriptions.red" in p.name or p.name == "Google One":
            return p.pid

    print("⏳ Google One process not running, attempting to launch application...")
    adb_bin = "adb"
    if ultra0 and hasattr(ultra0, "find_adb"):
        try:
            adb_bin = ultra0.find_adb()
        except Exception:
            pass

    try:
        subprocess.run(
            [
                adb_bin,
                "shell",
                "am",
                "start",
                "-a",
                "android.intent.action.MAIN",
                "-c",
                "android.intent.category.LAUNCHER",
                "-f",
                "0x10008000",
                "-n",
                "com.google.android.apps.subscriptions.red/.LauncherActivity",
            ],
            capture_output=True,
            timeout=10,
        )
        time.sleep(3)
        for p in dev.enumerate_processes():
            if "subscriptions.red" in p.name or p.name == "Google One":
                return p.pid
    except Exception:
        pass

    return 0


def format_period(period_str: str) -> str:
    """Formats ISO 8601 billing duration into clean English."""
    mapping = {
        "P1Y": "12 months (1 year)",
        "P12M": "12 months (1 year)",
        "P6M": "6 months",
        "P3M": "3 months",
        "P2M": "2 months",
        "P1M": "1 month",
        "P1W": "1 week",
    }
    return mapping.get(str(period_str), str(period_str))


def format_display_title(product: str, offer_id: str, title: str) -> str:
    """Formats display title matching promo catalog conventions."""
    tier = "[Ultra]" if ("ultra" in product or "30tb" in product or "20tb" in product) else "[Pro]"

    # Plan name
    if "30tb" in product:
        name = "AI Ultra 30TB"
    elif "20tb" in product:
        name = "AI Ultra 20TB"
    elif "ai.ultra" in product:
        name = "AI Ultra"
    elif "ai.pro" in product:
        name = "AI Pro"
    else:
        name = title.replace("Google One ", "").strip() or "Google One"

    # Offer description
    desc = ""
    oid = (offer_id or product).lower()
    if "90p" in oid:
        desc = "First 3 months 90% off"
    elif "85p" in oid:
        desc = "First 3 months 85% off"
    elif "80p" in oid:
        desc = "First 3 months 80% off"
    elif "75p" in oid:
        desc = "First 3 months 75% off"
    elif "12month" in oid or "12m" in oid:
        desc = "Free trial for 12 months"
    elif "6month" in oid:
        desc = "Free trial for 6 months"
    elif "3month" in oid:
        desc = "Free trial for 3 months"
    elif "1month" in oid:
        desc = "Free trial for 1 month"
    elif "annual" in oid:
        desc = "Annual billing"
    elif "monthly" in oid or oid == product:
        desc = "Monthly billing"
    else:
        desc = oid

    return f"{tier} {name} · {desc}"


# ==============================================================================
# MAIN SCANNER WORKFLOW
# ==============================================================================
def main():
    parser = argparse.ArgumentParser(description="Google One / Gemini AI SKU & Offer Scanner")
    parser.add_argument("skus", nargs="*", help="Optional custom SKUs to query")
    parser.add_argument("--free-only", action="store_true", help="Display only free trial ($0.00) offers")
    parser.add_argument("--batch-size", type=int, default=10, help="Number of SKUs per query batch (default: 10)")
    parser.add_argument("--remote", type=str, default=None, help="Remote Frida address (e.g. 127.0.0.1:27042)")
    args = parser.parse_args()

    # Prepare SKU list
    skus_to_query = args.skus if args.skus else DEFAULT_SKU_CATALOG
    # Deduplicate while preserving order
    seen = set()
    unique_skus = []
    for s in skus_to_query:
        if s not in seen:
            seen.add(s)
            unique_skus.append(s)

    print("=" * 75)
    print("🔍 GOOGLE ONE / GEMINI AI - SKU & OFFER SCANNER")
    print(f"   Total candidate SKUs to check: {len(unique_skus)}")
    print("=" * 75)

    # Automatically prepare device, connect ADB, and start frida-server if ultra0 is available
    if ultra0:
        try:
            ultra0.find_adb()
            ultra0.pick_device()
            ultra0.ensure_root()
            ultra0.ensure_frida_server()
            ultra0.ensure_module_apk()
        except Exception as e:
            print(f"ℹ️ Device environment check: {e}")

    # Connect to Frida device
    try:
        dev = get_device(args.remote)
        print(f"📱 Connected to Frida device: {dev.name} (id: {dev.id})")
    except Exception as e:
        sys.exit(f"❌ Could not connect to Frida server ({e}). Please ensure frida-server is running on your emulator/device.")

    # Find Google One process
    pid = find_or_start_g1(dev)
    if not pid:
        sys.exit(
            "❌ Google One process not found (com.google.android.apps.subscriptions.red).\n"
            "👉 Please open Google One app on your device or emulator and re-run!"
        )

    print(f"🎯 Hooked into Google One process (PID: {pid})")

    sess = dev.attach(pid)
    sc = sess.create_script(SCANNER_JS)

    all_offers = []
    batch_done_event = threading.Event()
    batch_status = {"code": 0, "count": 0}

    def on_message(msg, data):
        payload = msg.get("payload") or {}
        ev = payload.get("ev")
        if ev == "offer":
            all_offers.append(payload)
        elif ev == "batch_done":
            batch_status["code"] = payload.get("code", 0)
            batch_status["count"] = payload.get("count", 0)
            batch_done_event.set()
        elif ev in ("batch_err", "init_err"):
            print(f"   ⚠️ Client error: {payload.get('msg')}")
            batch_done_event.set()

    sc.on("message", on_message)
    sc.load()

    print("⚡ Initializing Play Billing Client connection via DexClassLoader...")
    try:
        init_code = sc.exports_sync.init()
        if init_code != 0:
            print(f"⚠️ Warning: Play Billing returned response code {init_code}")
    except Exception as e:
        sys.exit(f"❌ Billing Client initialization error: {e}")

    # Chunk SKU list into smaller batches to prevent BillingClient overload
    batch_size = max(1, min(args.batch_size, 20))
    chunks = [unique_skus[i : i + batch_size] for i in range(0, len(unique_skus), batch_size)]

    print(f"🚀 Scanning across {len(chunks)} batches ({batch_size} SKUs per batch)...")
    for idx, chunk in enumerate(chunks, 1):
        batch_done_event.clear()
        print(f"   • Scanning batch [{idx}/{len(chunks)}] ({len(chunk)} SKUs)...", end="\r", flush=True)
        try:
            sc.exports_sync.query_batch(chunk)
            batch_done_event.wait(timeout=12)
        except Exception as e:
            print(f"\n   ⚠️ Error during batch {idx}: {e}")
        time.sleep(0.3)

    print("\n✅ Scan completed!\n")

    # Display results
    if not all_offers:
        print("❌ No active offers found or account is ineligible.")
        try:
            sess.detach()
        except Exception:
            pass
        return

    # Filter if --free-only flag is set
    display_offers = all_offers
    if args.free_only:
        display_offers = [o for o in all_offers if str(o.get("micros")) == "0"]

    print("=" * 110)
    print(f"{'NO.':<6} | {'TIER & OFFER DESCRIPTION':<50} | {'PRICE / PERIOD':<24} | {'SKU / OFFER ID'}")
    print("=" * 110)

    start_index = 101
    for i, o in enumerate(display_offers):
        idx_str = f"[{start_index + i}]"
        product = str(o.get("product") or "")
        offer_id = str(o.get("offerId") or "")
        title = str(o.get("title") or o.get("name") or "")
        period = format_period(o.get("period"))
        micros = str(o.get("micros") or "0")

        if micros == "0":
            price_desc = f"Free ($0.00 / {period})"
        else:
            formatted = o.get("formattedPrice")
            price_val = formatted if formatted else f"${int(micros) / 1_000_000:.2f}"
            price_desc = f"{price_val} / {period}"

        disp_title = format_display_title(product, offer_id, title)
        target_id = offer_id if offer_id else product

        print(f"{idx_str:<6} | {disp_title:<50} | {price_desc:<24} | {target_id}")

        if micros == "0" and o.get("token"):
            print(f"       └─ Token ($0.00): {o.get('token')[:45]}...")

    print("=" * 110)
    print(f"🎉 Total: {len(display_offers)} active offers found on system.")
    print("💡 Note: To subscribe to a free offer, run the corresponding .bat file or pass this SKU/offer to ultra0.py.")

    try:
        sess.detach()
    except Exception:
        pass


if __name__ == "__main__":
    main()
