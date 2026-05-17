export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  devtools: { enabled: true },
  
  modules: [
    '@nuxt/ui',
    '@pinia/nuxt'
  ],
  
  ui: {
    global: true,
    icons: ['heroicons', 'lucide']
  },

  colorMode: {
    preference: 'light',
    fallback: 'light',
    classSuffix: ''
  },

  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE_URL || ''
    }
  },

  vite: {
    server: {
      port: 3000,
      proxy: {
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true,
          secure: false,
          rewrite: (path: string) => path
        }
      }
    }
  }
})
