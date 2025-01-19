<template>
  <div id="app">
    <h1>Welcome to the Price Checker</h1>
    <Scanner />
  </div>
</template>

<script>
import Scanner from '@/components/Scanner.vue';

export default {
  components: {
    Scanner,
  },
};
</script>
