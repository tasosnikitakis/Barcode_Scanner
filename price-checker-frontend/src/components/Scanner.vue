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

    <!-- Camera Live View -->
    <div id="scanner-container">
      <video id="barcode-scanner" width="100%" height="auto"></video>
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

    // Start the barcode scanner with live camera view
    startScanner() {
      this.scannerActive = true;

      Quagga.init(
        {
          inputStream: {
            name: "Live",
            type: "LiveStream",
            target: document.querySelector("#barcode-scanner"), // Attach scanner to the video element
            constraints: {
              video: {
                facingMode: { ideal: "environment" }, // Use the back camera
                width: { ideal: 1280 }, // Higher resolution for iOS
                height: { ideal: 720 }, // Higher resolution for iOS
              },
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
          console.log("QuaggaJS initialized successfully.");
          Quagga.start();
        }
      );

      // Detect barcodes and handle them
      Quagga.onDetected(this.onBarcodeDetected);
    },

    // Stop the barcode scanner
    stopScanner() {
      Quagga.stop();
      Quagga.offDetected(this.onBarcodeDetected);
      this.scannerActive = false;
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
    // Ensure the scanner is stopped when the component is destroyed
    this.stopScanner();
  },
};
</script>

<style scoped>
.error {
  color: red;
}
#scanner-container {
  margin: 20px 0;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 2px solid #ddd;
  padding: 10px;
}
</style>
