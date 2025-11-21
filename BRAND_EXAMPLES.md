# Brand Addition Examples

## Example 1: Adding Spotify

**Brand Name:**
```
Spotify
```

**Developer Name:**
```
Spotify AB
```

**Package IDs (comma-separated):**
```
com.spotify.music
```

**Icon URLs (comma-separated):**
```
https://play-lh.googleusercontent.com/eLCG_1OPOe_A0Y5twRFDLJR7Cz_-XYEdjE69F1pbjN3q9q5qTmJIBBhWyb78uBLJLQ=s96-rw
```

---

## Example 2: Adding Uber

**Brand Name:**
```
Uber
```

**Developer Name:**
```
Uber Technologies, Inc.
```

**Package IDs (comma-separated):**
```
com.ubercab, com.ubercab.driver
```

**Icon URLs (comma-separated):**
```
https://play-lh.googleusercontent.com/XXqn2fSRpD5fEcAky0BV3j1Hl0YoLNq3HKLlVOKcvSRPMXPFNXJU4dN9RjA2YDYQ6Q=s96-rw, https://play-lh.googleusercontent.com/driver_icon.png
```

---

## Example 3: Adding LinkedIn

**Brand Name:**
```
LinkedIn
```

**Developer Name:**
```
LinkedIn Corporation
```

**Package IDs (comma-separated):**
```
com.linkedin.android
```

**Icon URLs (comma-separated):**
```
https://play-lh.googleusercontent.com/kMofEFLjobZy_bCuaiDogzBcUT-dz3BBbOrIEjJ-hqOabjK8ieuevGe6wlTD15QzOqw=s96-rw
```

---

## Example 4: Adding Multiple Banking Apps

**Brand Name:**
```
HDFC Bank
```

**Developer Name:**
```
HDFC Bank Ltd.
```

**Package IDs (comma-separated):**
```
com.snapwork.hdfc, com.hdfcbank.payzapp
```

**Icon URLs (comma-separated):**
```
https://play-lh.googleusercontent.com/hdfc_mobile.png, https://play-lh.googleusercontent.com/hdfc_payzapp.png
```

---

## How to Get This Information:

### 1. Finding Package ID:
- Go to Google Play Store
- Find the app
- Look at the URL: `https://play.google.com/store/apps/details?id=com.example.app`
- Copy everything after `id=` → `com.example.app`

### 2. Finding Developer Name:
- On the app's Play Store page
- Look under the app name
- Copy the developer name exactly as shown

### 3. Finding Icon URL:
- Right-click on the app icon in Play Store
- Select "Copy image address"
- Paste the URL

### 4. Multiple Values:
- If an app has multiple package IDs (like Uber with passenger and driver apps)
- Separate them with commas
- Example: `com.app1, com.app2, com.app3`

---

## Quick Copy-Paste Examples:

### PayPal
```
Brand Name: PayPal
Developer Name: PayPal Mobile
Package IDs: com.paypal.android.p2pmobile
Icon URLs: https://play-lh.googleusercontent.com/paypal-icon.png
```

### Netflix
```
Brand Name: Netflix
Developer Name: Netflix, Inc.
Package IDs: com.netflix.mediaclient
Icon URLs: https://play-lh.googleusercontent.com/netflix-icon.png
```

### Amazon
```
Brand Name: Amazon
Developer Name: Amazon Mobile LLC
Package IDs: com.amazon.mShop.android.shopping
Icon URLs: https://play-lh.googleusercontent.com/amazon-icon.png
```

### WhatsApp
```
Brand Name: WhatsApp
Developer Name: WhatsApp LLC
Package IDs: com.whatsapp
Icon URLs: https://play-lh.googleusercontent.com/whatsapp-icon.png
```

---

## Tips:

1. **Always use exact developer names** - Case sensitive!
2. **Package IDs must be exact** - No spaces in package IDs
3. **Separate multiple values with commas** - Add space after comma for readability
4. **Icon URLs are optional** - But recommended for better visual identification
5. **Test with Quick Check** - After adding, test with a known legitimate app URL

---

## Common Mistakes to Avoid:

❌ Wrong: `PayPal, Inc` (incorrect developer name)
✅ Correct: `PayPal Mobile`

❌ Wrong: `com. spotify. music` (spaces in package ID)
✅ Correct: `com.spotify.music`

❌ Wrong: `Brand Name: ` (leaving field empty)
✅ Correct: Fill all required fields

❌ Wrong: Multiple packages without separation: `com.app1com.app2`
✅ Correct: `com.app1, com.app2`
