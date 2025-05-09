// frontend/vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5050', // Your Flask backend
        changeOrigin: true,
        secure: false, // Set to true if your backend is HTTPS and has a valid cert
      },
    },
  },
});
