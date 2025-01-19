<template>
  <div>
    <h1>Barcode Scanner</h1>

    <!-- Manual Barcode Input -->
    <input
      type="text"
      v-model="barcode"
      placeholder="Enter barcode"
    />
    <button @click="fetchProduct">Fetch Product</button>

    <!-- Camera Live Stream with Overlay -->
    <div id="scanner-container">
      <video id="camera-view" autoplay playsinline muted width="100%" height="auto"></video>

      <!-- Overlay Box -->
      <div id="overlay">
        <div
          class="scanner-line"
          :class="{ detected: barcodeDetected }"
        ></div>
      </div>
    </div>
    <button v-if="!scannerActive" @click="startScanner">Run Scanner</button>
    <button v-if="scannerActive" @click="stopScanner">Stop Scanner</button>

    <!-- Product Details -->
    <div v-if="product">
      <h2>Product Details</h2>
      <p><strong>Name:</strong> {{ product.name }}</p>
      <p><strong>Price:</strong> {{ product.price }}</p>
      <p><strong>Description:</strong> {{ product.description }}</p>
    </div>

    <!-- Error Display -->
    <div v-if="error" class="error">
      <p>{{ error }}</p>
    </div>
  </div>
</template>

<script>
import Quagga from "quagga"; // Import QuaggaJS
import apiClient from "@/api"; // Axios instance for backend communication

export default {
  data() {
    return {
      barcode: "", // Manual input barcode
      product: null, // Product data
      error: null, // Error message
      scannerActive: false, // Tracks whether the scanner is active
      videoStream: null, // Video stream object for camera feed
      barcodeDetected: false, // Whether a barcode has been detected
    };
  },
  methods: {
    // Fetch product from backend by barcode
    async fetchProduct() {
      if (!this.barcode) {
        this.error = "No barcode detected.";
        return;
      }
      this.error = null;
      this.product = null;
      try {
        const response = await apiClient.get(`/product/${this.barcode}/`);
        this.product = response.data;
      } catch (err) {
        this.error = err.response?.data?.error || "Failed to fetch product";
      }
    },

    // Start the camera and initialize barcode scanning
    async startScanner() {
      this.error = null;
      this.barcodeDetected = false;
      this.scannerActive = true;

      // Start live video stream using MediaStream API
      try {
        const videoElement = document.querySelector("#camera-view");
        const constraints = {
          video: {
            facingMode: "environment", // Use back camera
            width: { ideal: 1280 },
            height: { ideal: 720 },
          },
        };
        this.videoStream = await navigator.mediaDevices.getUserMedia(constraints);
        videoElement.srcObject = this.videoStream;

        console.log("Camera feed started successfully.");
      } catch (err) {
        console.error("Failed to start the camera feed:", err);
        this.error = "Unable to access the camera. Please allow camera permissions.";
        this.scannerActive = false;
        return;
      }

      // Start QuaggaJS for barcode detection
      Quagga.init(
        {
          inputStream: {
            name: "Live",
            type: "LiveStream",
            target: document.querySelector("#camera-view"), // Attach Quagga to the same video
            constraints: {
              facingMode: "environment",
              width: 1280,
              height: 720,
            },
            area: { // Limit scanning to the overlay area
              top: "45%", // Matches the overlay's top edge
              bottom: "60%", // Matches the overlay's bottom edge
              left: "0%", // Full width
              right: "100%", // Full width
            },
          },
          decoder: {
            readers: [
              "code_128_reader",
              "ean_reader",
              "upc_reader",
              "ean_8_reader",
            ], // Supported barcode types
          },
        },
        (err) => {
          if (err) {
            console.error("QuaggaJS initialization failed:", err);
            this.error = "Failed to initialize the scanner.";
            this.scannerActive = false;
            return;
          }
          Quagga.start();
          console.log("QuaggaJS initialized successfully.");
        }
      );

      Quagga.onDetected(this.onBarcodeDetected);
    },

    // Stop the scanner and camera feed
    stopScanner() {
      Quagga.stop();
      Quagga.offDetected(this.onBarcodeDetected);
      this.scannerActive = false;

      // Stop video stream
      if (this.videoStream) {
        const tracks = this.videoStream.getTracks();
        tracks.forEach((track) => track.stop());
        this.videoStream = null;
      }
      console.log("Scanner stopped.");
    },

    // Handle barcode detection (stops scanning and updates UI)
    onBarcodeDetected(result) {
      const detectedBarcode = result.codeResult.code; // Extract the detected barcode
      console.log("Detected barcode:", detectedBarcode);

      // Fill the barcode input field and stop the scanner
      this.barcode = detectedBarcode;
      this.barcodeDetected = true; // Update UI to indicate detection
      this.stopScanner(); // Stop further scanning
    },
  },
  beforeUnmount() {
    // Ensure the scanner and camera are stopped when the component is destroyed
    this.stopScanner();
  },
};
</script>

<style scoped>
.error {
  color: red;
}
#scanner-container {
  position: relative;
  margin: 20px 0;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 2px solid #ddd;
  padding: 10px;
}

/* Overlay Box */
#overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border: 2px solid transparent;
  pointer-events: none;
}

#overlay::before {
  content: "";
  position: absolute;
  top: 45%; /* Center vertically */
  left: 0;
  width: 100%; /* Full width */
  height: 15%; /* Narrow vertical range */
  border: 3px dashed #00ff00;
  border-radius: 4px;
  box-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
  pointer-events: none;
}

.scanner-line {
  position: absolute;
  top: 50%; /* Start at the center */
  left: 0;
  width: 100%; /* Full width */
  height: 3px;
  background: green; /* Default green color */
  animation: scanner-line-move 1s infinite ease-in-out;
  transition: background 0.3s; /* Smooth transition to red */
}

.scanner-line.detected {
  animation: none; /* Stop movement */
  background: red; /* Change to red when detected */
}

/* Animates the scanner line */
@keyframes scanner-line-move {
  0% {
    top: 45%;
  }
  100% {
    top: 55%;
  }
}
</style>
