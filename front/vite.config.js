import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import { createHtmlPlugin } from 'vite-plugin-html'
import { fileURLToPath } from 'url'

// __dirname 대체 구현
const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd())
  return {
    plugins: [
      react(),
      createHtmlPlugin({
        minify: true,
        inject: {
          data: {
            ncpClientId: env.VITE_X_NCP_APIGW_API_KEY_ID,
          },
        },
      }),
    ],

    server: {
      host: true,
      proxy: {
        '/api': {
          target: env.VITE_API_TARGET,
          // target: 'http://127.0.0.1:5000',
          changeOrigin: true,
        },
        '/v1': {
          target: 'https://openapi.naver.com',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ''),
          secure: false,
          ws: true,
        },
        '/v2': {
          target: 'https://naveropenapi.apigw.ntruss.com/map-reversegeocode',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ''),
          secure: false,
          ws: true,
        },
      },
      hmr: {
        overlay: false,
      },
    },
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
        '@components': path.resolve(__dirname, './src/components'),
        '@hooks': path.resolve(__dirname, './src/hooks'),
        '@styles': path.resolve(__dirname, './src/styles'),
        '@assets': path.resolve(__dirname, './src/assets'),
      },
    },
  }
})
