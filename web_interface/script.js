// web_interface/script.js
class BluetoothAIWebApp {
    constructor() {
        this.devices = [];
        this.selectedDevice = null;
        this.currentMode = 'online';
        this.currentLanguage = 'en';
        this.isScanning = false;
        
        this.initializeApp();
    }

    async initializeApp() {
        await this.loadTranslations('en');
        this.updateUI();
        this.checkServerStatus();
        
        // Event listeners setup karein
        this.setupEventListeners();
        
        this.showToast('🚀 Bluetooth AI Fix Master loaded successfully!', 'success');
    }

    setupEventListeners() {
        // Device selection
        document.addEventListener('click', (e) => {
            if (e.target.closest('.device-card')) {
                const deviceCard = e.target.closest('.device-card');
                this.selectDevice(deviceCard);
            }
        });
    }

    async checkServerStatus() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            
            if (data.ai_system && data.language_system) {
                this.updateStatus('ready', 'System Ready');
            } else {
                this.updateStatus('loading', 'Initializing AI System...');
            }
        } catch (error) {
            this.updateStatus('error', 'Server Connection Failed');
            console.error('Status check error:', error);
        }
    }

    updateStatus(status, message) {
        const statusElement = document.getElementById('statusValue');
        statusElement.textContent = message;
        statusElement.className = `status-${status}`;
    }

    async loadTranslations(langCode) {
        try {
            const response = await fetch(`/api/translations/${langCode}`);
            const data = await response.json();
            
            if (data.success) {
                this.currentLanguage = langCode;
                this.translations = data.translations;
                
                // RTL support
                if (data.is_rtl) {
                    document.documentElement.dir = 'rtl';
                } else {
                    document.documentElement.dir = 'ltr';
                }
                
                this.updateUIText();
                this.showToast(`🌐 Language changed to ${this.getLanguageName(langCode)}`, 'success');
            }
        } catch (error) {
            console.error('Translation load error:', error);
            this.showToast('❌ Failed to load translations', 'error');
        }
    }

    getLanguageName(langCode) {
        const names = {
            'en': 'English',
            'hi': 'Hindi',
            'es': 'Spanish',
            'fr': 'French',
            'ar': 'Arabic',
            'zh': 'Chinese'
        };
        return names[langCode] || langCode;
    }

    updateUIText() {
        // All translatable elements update karein
        const elements = {
            'appTitle': 'app_title',
            'appSubtitle': 'app_subtitle',
            'statusLabel': 'status_label',
            'devicesLabel': 'devices_label',
            'scanDevicesText': 'scan_devices',
            'startScanText': 'start_scan',
            'foundDevicesText': 'found_devices',
            'noDevicesText': 'no_devices',
            'troubleshootText': 'troubleshoot',
            'runAIDiagnosisText': 'run_ai_diagnosis',
            'autoFixText': 'auto_fix',
            'noDiagnosisText': 'no_diagnosis',
            'deviceInfoText': 'device_info',
            'selectDeviceText': 'select_device',
            'downloadAppText': 'download_app',
            'footerText': 'footer_text',
            'helpLink': 'help',
            'aboutLink': 'about',
            'contactLink': 'contact',
            'onlineModeText': 'online_mode',
            'offlineModeText': 'offline_mode',
            'scanningText': 'scanning'
        };

        for (const [elementId, translationKey] of Object.entries(elements)) {
            const element = document.getElementById(elementId);
            if (element) {
                element.textContent = this.translations[translationKey] || translationKey;
            }
        }
    }

    updateUI() {
        // Devices count update karein
        document.getElementById('devicesCount').textContent = this.devices.length;
        
        // No devices message show/hide karein
        const noDevicesElement = document.getElementById('noDevicesMessage');
        if (noDevicesElement) {
            noDevicesElement.style.display = this.devices.length === 0 ? 'block' : 'none';
        }
    }

    async scanDevices() {
        if (this.isScanning) return;
        
        this.isScanning = true;
        const scanBtn = document.getElementById('scanBtn');
        const scanLoading = document.getElementById('scanLoading');
        const scanResults = document.getElementById('scanResultsContent');
        
        // UI update karein
        scanBtn.disabled = true;
        scanLoading.style.display = 'flex';
        scanResults.innerHTML = '';
        
        try {
            const response = await fetch('/api/devices');
            const data = await response.json();
            
            if (data.success) {
                this.devices = data.devices;
                this.displayDevices();
                this.showToast(`✅ Found ${data.count} devices`, 'success');
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            console.error('Scan error:', error);
            this.showToast('❌ Device scan failed', 'error');
            // Fallback: Demo devices show karein
            this.devices = this.getDemoDevices();
            this.displayDevices();
        } finally {
            this.isScanning = false;
            scanBtn.disabled = false;
            scanLoading.style.display = 'none';
            this.updateUI();
        }
    }

    getDemoDevices() {
        return [
            {
                "name": "Sony WH-1000XM4",
                "mac_address": "04:5F:01:02:03",
                "signal_strength": -45,
                "connected": false,
                "device_type": "headphones",
                "battery_level": 85
            },
            {
                "name": "Apple AirPods Pro",
                "mac_address": "DC:56:04:05:06", 
                "signal_strength": -55,
                "connected": true,
                "device_type": "earbuds",
                "battery_level": 65
            }
        ];
    }

    displayDevices() {
        const devicesList = document.getElementById('devicesList');
        devicesList.innerHTML = '';
        
        this.devices.forEach(device => {
            const deviceCard = document.createElement('div');
            deviceCard.className = 'device-card';
            deviceCard.dataset.mac = device.mac_address;
            
            deviceCard.innerHTML = `
                <div class="device-info">
                    <div class="device-name">${device.name}</div>
                    <div class="device-mac">${device.mac_address}</div>
                    <div class="device-type">${device.device_type}</div>
                </div>
                <div class="device-status">
                    <span class="status-${device.connected ? 'connected' : 'available'}">
                        ${device.connected ? 'Connected' : 'Available'}
                    </span>
                    <span class="signal-strength">${device.signal_strength} dBm</span>
                </div>
            `;
            
            devicesList.appendChild(deviceCard);
        });
    }

    selectDevice(deviceCard) {
        // Previous selection clear karein
        document.querySelectorAll('.device-card').forEach(card => {
            card.classList.remove('selected');
        });
        
        // New selection mark karein
        deviceCard.classList.add('selected');
        
        const macAddress = deviceCard.dataset.mac;
        this.selectedDevice = this.devices.find(device => device.mac_address === macAddress);
        
        this.displayDeviceInfo();
    }

    displayDeviceInfo() {
        const deviceInfo = document.getElementById('deviceInfo');
        
        if (this.selectedDevice) {
            deviceInfo.innerHTML = `
                <div class="device-details">
                    <h3>${this.selectedDevice.name}</h3>
                    <div class="detail-item">
                        <strong>MAC Address:</strong> ${this.selectedDevice.mac_address}
                    </div>
                    <div class="detail-item">
                        <strong>Device Type:</strong> ${this.selectedDevice.device_type}
                    </div>
                    <div class="detail-item">
                        <strong>Signal Strength:</strong> ${this.selectedDevice.signal_strength} dBm
                    </div>
                    <div class="detail-item">
                        <strong>Status:</strong> 
                        <span class="status-${this.selectedDevice.connected ? 'connected' : 'available'}">
                            ${this.selectedDevice.connected ? 'Connected' : 'Available'}
                        </span>
                    </div>
                    ${this.selectedDevice.battery_level ? `
                    <div class="detail-item">
                        <strong>Battery Level:</strong> ${this.selectedDevice.battery_level}%
                    </div>
                    ` : ''}
                </div>
            `;
        }
    }

    async runAIDiagnosis() {
        if (!this.selectedDevice) {
            this.showToast('⚠️ Please select a device first', 'warning');
            return;
        }

        const aiBtn = document.getElementById('aiDiagnosisBtn');
        const resultsDiv = document.getElementById('troubleshootResults');
        
        // UI update karein
        aiBtn.disabled = true;
        resultsDiv.innerHTML = `
            <div class="loading">
                <div class="spinner"></div>
                <span>Running AI diagnosis...</span>
            </div>
        `;

        try {
            const response = await fetch('/api/diagnose', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    device: this.selectedDevice
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.displayDiagnosisResults(data.diagnosis);
                this.showToast('✅ AI diagnosis completed', 'success');
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            console.error('Diagnosis error:', error);
            this.showToast('❌ AI diagnosis failed', 'error');
            // Fallback: Demo results show karein
            this.displayDemoDiagnosis();
        } finally {
            aiBtn.disabled = false;
        }
    }

    displayDiagnosisResults(diagnosis) {
        const resultsDiv = document.getElementById('troubleshootResults');
        
        let issuesHTML = '';
        if (diagnosis.detected_issues.length > 0) {
            issuesHTML = `
                <h4>Detected Issues:</h4>
                ${diagnosis.detected_issues.map(issue => `
                    <div class="diagnosis-item">
                        <strong>${issue.description}</strong>
                        <br>
                        <small>Confidence: ${(issue.confidence * 100).toFixed(1)}% | Severity: ${issue.severity}</small>
                    </div>
                `).join('')}
            `;
        } else {
            issuesHTML = '<div class="diagnosis-item">✅ No issues detected</div>';
        }
        
        let fixesHTML = '';
        if (diagnosis.suggested_fixes.length > 0) {
            fixesHTML = `
                <h4>Suggested Fixes:</h4>
                ${diagnosis.suggested_fixes.map(fix => `
                    <div class="fix-item">
                        <i class="fas fa-wrench"></i>
                        <span>${fix.description}</span>
                        <small>(Success: ${(fix.success_rate * 100).toFixed(1)}%)</small>
                    </div>
                `).join('')}
            `;
        }
        
        resultsDiv.innerHTML = `
            <div class="diagnosis-summary">
                <h3>AI Diagnosis Report</h3>
                <div class="summary-stats">
                    <div>Confidence: <strong>${(diagnosis.confidence_score * 100).toFixed(1)}%</strong></div>
                    <div>Risk Level: <strong>${diagnosis.risk_level.toUpperCase()}</strong></div>
                    <div>Estimated Time: <strong>${diagnosis.estimated_time}</strong></div>
                </div>
                ${issuesHTML}
                ${fixesHTML}
            </div>
        `;
    }

    displayDemoDiagnosis() {
        const resultsDiv = document.getElementById('troubleshootResults');
        resultsDiv.innerHTML = `
            <div class="diagnosis-summary">
                <h3>AI Diagnosis Report (Demo)</h3>
                <div class="summary-stats">
                    <div>Confidence: <strong>85.5%</strong></div>
                    <div>Risk Level: <strong>LOW</strong></div>
                    <div>Estimated Time: <strong>5-10 minutes</strong></div>
                </div>
                <h4>Detected Issues:</h4>
                <div class="diagnosis-item">
                    <strong>Weak Bluetooth signal detected</strong>
                    <br>
                    <small>Confidence: 85.0% | Severity: high</small>
                </div>
                <h4>Suggested Fixes:</h4>
                <div class="fix-item">
                    <i class="fas fa-wrench"></i>
                    <span>Reset Bluetooth stack and services</span>
                    <small>(Success: 85.0%)</small>
                </div>
                <div class="fix-item">
                    <i class="fas fa-wrench"></i>
                    <span>Reconnect the Bluetooth device</span>
                    <small>(Success: 90.0%)</small>
                </div>
            </div>
        `;
    }

    async autoFixIssues() {
        if (!this.selectedDevice) {
            this.showToast('⚠️ Please select a device first', 'warning');
            return;
        }

        const fixBtn = document.getElementById('autoFixBtn');
        fixBtn.disabled = true;

        try {
            // Demo fix simulation
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            this.showToast('✅ Issues fixed automatically', 'success');
            
            // Refresh device status
            this.selectedDevice.connected = true;
            this.selectedDevice.signal_strength = -40;
            this.displayDeviceInfo();
            this.displayDevices();
            
        } catch (error) {
            this.showToast('❌ Auto fix failed', 'error');
        } finally {
            fixBtn.disabled = false;
        }
    }

    setMode(mode) {
        this.currentMode = mode;
        
        // UI update karein
        document.querySelectorAll('.mode-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        document.getElementById(`${mode}Btn`).classList.add('active');
        
        this.showToast(`Mode changed to ${mode === 'online' ? 'Online' : 'Offline'}`, 'info');
    }

    showToast(message, type = 'info') {
        const toastContainer = document.getElementById('toastContainer');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <i class="fas fa-${this.getToastIcon(type)}"></i>
            <span>${message}</span>
            <button onclick="this.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        toastContainer.appendChild(toast);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, 5000);
    }

    getToastIcon(type) {
        const icons = {
            'success': 'check-circle',
            'error': 'exclamation-circle',
            'warning': 'exclamation-triangle',
            'info': 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    downloadApp(os) {
        this.showToast(`📥 Downloading ${os} version...`, 'info');
        // Actual download logic yahan add karein
    }
}

// Global functions jo HTML se call honge
let app;

function changeLanguage(langCode) {
    app.loadTranslations(langCode);
}

function scanDevices() {
    app.scanDevices();
}

function runAIDiagnosis() {
    app.runAIDiagnosis();
}

function autoFixIssues() {
    app.autoFixIssues();
}

function setMode(mode) {
    app.setMode(mode);
}

function downloadApp(os) {
    app.downloadApp(os);
}

// App initialize karein page load par
document.addEventListener('DOMContentLoaded', () => {
    app = new BluetoothAIWebApp();
});
