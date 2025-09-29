// web_interface/bluetooth_web.js
class WebBluetoothManager {
    constructor() {
        this.supported = this.checkBluetoothSupport();
        this.devices = [];
        this.connectedDevice = null;
    }

    checkBluetoothSupport() {
        return navigator.bluetooth && navigator.bluetooth.requestDevice;
    }

    async requestBluetoothDevice() {
        if (!this.supported) {
            throw new Error('Web Bluetooth API is not supported in this browser. Please use Chrome, Edge, or Opera.');
        }

        try {
            const device = await navigator.bluetooth.requestDevice({
                acceptAllDevices: true,
                optionalServices: ['battery_service', 'device_information']
            });

            return {
                name: device.name || 'Unknown Device',
                id: device.id,
                connected: false
            };
        } catch (error) {
            if (error.name === 'NotFoundError') {
                throw new Error('No Bluetooth device selected.');
            } else if (error.name === 'SecurityError') {
                throw new Error('Bluetooth permissions denied.');
            } else {
                throw new Error(`Bluetooth error: ${error.message}`);
            }
        }
    }

    async connectToDevice(device) {
        try {
            const server = await device.gatt.connect();
            this.connectedDevice = device;
            
            // Get device information
            const deviceInfo = await this.getDeviceInfo(server);
            
            return {
                ...deviceInfo,
                connected: true,
                server: server
            };
        } catch (error) {
            throw new Error(`Connection failed: ${error.message}`);
        }
    }

    async getDeviceInfo(server) {
        const info = {};
        
        try {
            // Get battery level
            const batteryService = await server.getPrimaryService('battery_service');
            const batteryLevel = await batteryService.getCharacteristic('battery_level');
            const batteryValue = await batteryLevel.readValue();
            info.batteryLevel = batteryValue.getUint8(0);
        } catch (e) {
            info.batteryLevel = null;
        }

        try {
            // Get device information
            const deviceInfoService = await server.getPrimaryService('device_information');
            const characteristics = await deviceInfoService.getCharacteristics();
            
            for (const characteristic of characteristics) {
                try {
                    const value = await characteristic.readValue();
                    const decoder = new TextDecoder('utf-8');
                    info[characteristic.uuid] = decoder.decode(value);
                } catch (e) {
                    // Skip characteristics that can't be read
                }
            }
        } catch (e) {
            // Device information service not available
        }

        return info;
    }

    async disconnectDevice() {
        if (this.connectedDevice && this.connectedDevice.gatt.connected) {
            this.connectedDevice.gatt.disconnect();
            this.connectedDevice = null;
        }
    }

    getSimulatedDevices() {
        return [
            {
                name: "Sony WH-1000XM4",
                mac_address: "04:5F:01:02:03",
                signal_strength: -45,
                connected: false,
                device_type: "headphones",
                battery_level: 85
            },
            {
                name: "Apple AirPods Pro",
                mac_address: "DC:56:04:05:06",
                signal_strength: -55,
                connected: true,
                device_type: "earbuds",
                battery_level: 65
            },
            {
                name: "Logitech MX Keys",
                mac_address: "70:B3:07:08:09",
                signal_strength: -35,
                connected: true,
                device_type: "keyboard",
                battery_level: 90
            }
        ];
    }

    // Method to simulate real Bluetooth scanning
    async scanDevices() {
        if (!this.supported) {
            return this.getSimulatedDevices();
        }

        try {
            // Try to get real Bluetooth devices
            const device = await this.requestBluetoothDevice();
            return [device];
        } catch (error) {
            console.warn('Real Bluetooth scan failed, using simulated devices:', error);
            return this.getSimulatedDevices();
        }
    }
}

// Global instance
const bluetoothManager = new WebBluetoothManager();
