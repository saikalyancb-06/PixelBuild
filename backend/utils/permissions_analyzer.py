# Mock Permissions Analysis Utility
# Simulates APK permission analysis without actual APK decompilation

# Common malicious permissions that fake apps often request
MALICIOUS_PERMISSIONS = {
    'HIGH_RISK': [
        'android.permission.SEND_SMS',
        'android.permission.RECEIVE_SMS',
        'android.permission.READ_SMS',
        'android.permission.WRITE_SMS',
        'android.permission.RECEIVE_MMS',
        'android.permission.RECEIVE_WAP_PUSH',
        'android.permission.CALL_PHONE',
        'android.permission.READ_PHONE_STATE',
        'android.permission.READ_CALL_LOG',
        'android.permission.WRITE_CALL_LOG',
        'android.permission.ADD_VOICEMAIL',
        'android.permission.USE_SIP',
        'android.permission.PROCESS_OUTGOING_CALLS',
        'android.permission.RECORD_AUDIO',
        'android.permission.CAMERA',
        'android.permission.ACCESS_FINE_LOCATION',
        'android.permission.ACCESS_COARSE_LOCATION',
        'android.permission.READ_CONTACTS',
        'android.permission.WRITE_CONTACTS',
        'android.permission.GET_ACCOUNTS',
        'android.permission.READ_EXTERNAL_STORAGE',
        'android.permission.WRITE_EXTERNAL_STORAGE',
    ],
    'MEDIUM_RISK': [
        'android.permission.INTERNET',
        'android.permission.ACCESS_NETWORK_STATE',
        'android.permission.ACCESS_WIFI_STATE',
        'android.permission.CHANGE_WIFI_STATE',
        'android.permission.BLUETOOTH',
        'android.permission.BLUETOOTH_ADMIN',
        'android.permission.NFC',
        'android.permission.VIBRATE',
        'android.permission.WAKE_LOCK',
        'android.permission.RECEIVE_BOOT_COMPLETED',
        'android.permission.FOREGROUND_SERVICE',
    ],
    'SUSPICIOUS': [
        'android.permission.REQUEST_INSTALL_PACKAGES',
        'android.permission.SYSTEM_ALERT_WINDOW',
        'android.permission.BIND_ACCESSIBILITY_SERVICE',
        'android.permission.BIND_DEVICE_ADMIN',
        'android.permission.READ_LOGS',
        'android.permission.INSTALL_PACKAGES',
        'android.permission.DELETE_PACKAGES',
    ]
}

def analyze_permissions_mock(app_category: str = 'banking') -> dict:
    """
    Mock permission analysis based on app category
    Simulates what permissions would be flagged as suspicious
    """
    
    # Simulated suspicious permissions based on app type
    category_suspicious = {
        'banking': [
            'android.permission.SEND_SMS',  # Banking apps shouldn't send SMS
            'android.permission.READ_SMS',  # Suspicious for OTP theft
            'android.permission.SYSTEM_ALERT_WINDOW',  # Overlay attacks
            'android.permission.BIND_ACCESSIBILITY_SERVICE',  # Accessibility abuse
            'android.permission.READ_CALL_LOG',  # Unnecessary
        ],
        'ecommerce': [
            'android.permission.SEND_SMS',
            'android.permission.CALL_PHONE',
            'android.permission.READ_CONTACTS',
            'android.permission.ACCESS_FINE_LOCATION',  # Excessive tracking
        ],
        'social': [
            'android.permission.READ_SMS',
            'android.permission.SEND_SMS',
            'android.permission.READ_CALL_LOG',
            'android.permission.SYSTEM_ALERT_WINDOW',
        ],
        'default': [
            'android.permission.SEND_SMS',
            'android.permission.READ_SMS',
            'android.permission.SYSTEM_ALERT_WINDOW',
        ]
    }
    
    suspicious_perms = category_suspicious.get(app_category.lower(), category_suspicious['default'])
    
    # Calculate risk score
    high_risk_count = sum(1 for p in suspicious_perms if p in MALICIOUS_PERMISSIONS['HIGH_RISK'])
    suspicious_count = sum(1 for p in suspicious_perms if p in MALICIOUS_PERMISSIONS['SUSPICIOUS'])
    
    risk_score = min(100, (high_risk_count * 20) + (suspicious_count * 30))
    
    return {
        'total_permissions': len(suspicious_perms) + 5,  # Add some normal permissions
        'suspicious_permissions': suspicious_perms,
        'high_risk_count': high_risk_count,
        'suspicious_count': suspicious_count,
        'permission_risk_score': risk_score,
        'analysis': {
            'sms_access': any('SMS' in p for p in suspicious_perms),
            'overlay_capability': 'android.permission.SYSTEM_ALERT_WINDOW' in suspicious_perms,
            'accessibility_abuse': 'android.permission.BIND_ACCESSIBILITY_SERVICE' in suspicious_perms,
            'location_tracking': any('LOCATION' in p for p in suspicious_perms),
            'contact_access': any('CONTACTS' in p for p in suspicious_perms),
        },
        'warnings': [
            f"⚠️ {p.split('.')[-1]}: Unusual for this app type" 
            for p in suspicious_perms[:3]
        ]
    }

def get_permission_explanation(permission: str) -> str:
    """Get human-readable explanation of what a permission does"""
    explanations = {
        'SEND_SMS': 'Can send text messages without user knowledge (used to subscribe to premium services)',
        'READ_SMS': 'Can read all text messages including OTPs and verification codes',
        'SYSTEM_ALERT_WINDOW': 'Can draw over other apps (used for overlay attacks to steal credentials)',
        'BIND_ACCESSIBILITY_SERVICE': 'Can access all screen content (dangerous for credential theft)',
        'READ_CALL_LOG': 'Can read all call history',
        'READ_CONTACTS': 'Can access all contact information',
        'CAMERA': 'Can access camera without notification',
        'RECORD_AUDIO': 'Can record audio in background',
        'ACCESS_FINE_LOCATION': 'Can track exact GPS location',
        'READ_PHONE_STATE': 'Can access device ID and phone number',
    }
    
    perm_name = permission.split('.')[-1]
    return explanations.get(perm_name, 'Permission purpose unclear')
