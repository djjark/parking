import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/identify-parking': {
        target: 'http://localhost:5000', // Flask server
        changeOrigin: true,
        secure: false,
      },
    },
  },
})