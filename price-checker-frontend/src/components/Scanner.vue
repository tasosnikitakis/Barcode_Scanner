<template>
  <div>
    <h1>Barcode Scanner</h1>

    <!-- Manual Barcode Input -->
    <input
      type="text"
      v-model="barcode"
      placeholder="Enter barcode"
      @keyup.enter="fetchProduct"
    />
    <button @click="fetchProduct">Fetch Product</button>

    <!-- Camera Live Stream with Overlay -->
    <div id="scanner-container">
      <video id="camera-view" autoplay playsinline muted width="100%" height="auto"></video>

      <!-- Overlay Box -->
      <div id="overlay">
        <div class="scanner-line"></div>
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
    };
  },
  methods: {
    // Fetch product from backend by barcode
    async fetchProduct() {
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

    // Handle barcode detection
    async onBarcodeDetected(result) {
      const detectedBarcode = result.codeResult.code; // Extract the detected barcode
      console.log("Detected barcode:", detectedBarcode);

      // Fetch the product using the detected barcode
      this.barcode = detectedBarcode; // Update manual input for visibility
      await this.fetchProduct();

      // Stop scanner if a product is found
      if (this.product) {
        this.stopScanner();
      }
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
  top: 30%; /* Adjust for center */
  left: 10%; /* Adjust width */
  width: 80%;
  height: 30%;
  border: 3px dashed #00ff00;
  border-radius: 4px;
  box-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
  pointer-events: none;
}

.scanner-line {
  position: absolute;
  top: 45%; /* Center the scanner line */
  left: 10%;
  width: 80%;
  height: 3px;
  background: red;
  animation: scanner-line-move 1s infinite ease-in-out;
}

/* Animates the scanner line */
@keyframes scanner-line-move {
  0% {
    top: 35%;
  }
  100% {
    top: 65%;
  }
}
</style>
