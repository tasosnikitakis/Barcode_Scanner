<template>
  <div>
    <h1>Barcode Scanner</h1>
    <input
      type="text"
      v-model="barcode"
      placeholder="Enter barcode"
      @keyup.enter="fetchProduct"
    />
    <button @click="fetchProduct">Fetch Product</button>

    <div v-if="product">
      <h2>Product Details</h2>
      <p><strong>Name:</strong> {{ product.name }}</p>
      <p><strong>Price:</strong> {{ product.price }}</p>
      <p><strong>Description:</strong> {{ product.description }}</p>
    </div>

    <div v-if="error" class="error">
      <p>{{ error }}</p>
    </div>
  </div>
</template>

<script>
import apiClient from '@/api';

export default {
  data() {
    return {
      barcode: '',
      product: null,
      error: null,
    };
  },
  methods: {
    async fetchProduct() {
      this.error = null;
      this.product = null;
      try {
        const response = await apiClient.get(`/product/${this.barcode}/`);
        this.product = response.data;
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to fetch product';
      }
    },
  },
};
</script>

<style>
.error {
  color: red;
}
</style>
