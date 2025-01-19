import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  base: '/static/', // Match Django's STATIC_URL
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'), // Map `@` to the `src` directory
    },
  },
  build: {
    outDir: '../static', // Place built files directly into Django's static directory
    emptyOutDir: true,   // Clear previous builds
  },
  plugins: [vue()],
})
