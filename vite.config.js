import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  base: './',  // Use relative paths for GitHub Pages
  plugins: [react()],
  server: {
    port: 3000,
    open: true
  }
})

