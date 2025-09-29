const translations = {
    en: {
        scanTitle: "Scan Bluetooth Devices",
        devicesTitle: "Found Devices", 
        aiTitle: "AI Troubleshooter",
        scanBtn: "Start Scanning",
        aiBtn: "Run AI Diagnosis"
    },
    hi: {
        scanTitle: "ब्लूटूथ डिवाइस स्कैन करें",
        devicesTitle: "मिले डिवाइस",
        aiTitle: "AI ट्रबलशूटर", 
        scanBtn: "स्कैनिंग शुरू करें",
        aiBtn: "AI डायग्नोसिस चलाएं"
    }
};

function changeLanguage(lang) {
    const texts = translations[lang] || translations.en;
    Object.keys(texts).forEach(key => {
        const element = document.getElementById(key);
        if (element) element.textContent = texts[key];
    });
}

async function scanDevices() {
    const btn = document.getElementById('scanBtn');
    btn.textContent = 'Scanning...';
    btn.disabled = true;

    // Simulate device scanning
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    const devices = [
        { name: "Sony WH-1000XM4", mac: "04:5F:01:02:03", status: "Available" },
        { name: "Apple AirPods Pro", mac: "DC:56:04:05:06", status: "Connected" }
    ];
    
    displayDevices(devices);
    btn.textContent = translations[document.getElementById('languageSelect').value]?.scanBtn || 'Start Scanning';
    btn.disabled = false;
}

function displayDevices(devices) {
    const list = document.getElementById('devicesList');
    list.innerHTML = devices.map(device => `
        <div class="device-card">
            <h3>${device.name}</h3>
            <p>MAC: ${device.mac}</p>
            <p>Status: ${device.status}</p>
        </div>
    `).join('');
}

function runAIDiagnosis() {
    const results = document.getElementById('aiResults');
    results.innerHTML = '<div class="loading">Analyzing devices...</div>';
    
    setTimeout(() => {
        results.innerHTML = `
            <div class="diagnosis-result">
                <h3>AI Diagnosis Complete</h3>
                <p>✅ Connection Strength: Good</p>
                <p>⚠️ Audio Quality: Needs optimization</p>
                <p>🔧 Recommended: Update Bluetooth drivers</p>
            </div>
        `;
    }, 3000);
}
