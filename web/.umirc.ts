import { defineConfig } from 'umi';

const isDev = process.env.NODE_ENV === 'development';

export default defineConfig({
  hash: true,
  webpack5: {},
  publicPath: isDev ? './' : 'web/dist/',
  nodeModulesTransform: {
    type: 'none',
  },
  routes: [
    { path: '/', component: '@/pages/home/index', title: 'Python_QRCode' },
  ],
  title: 'Python_QRCode',
  fastRefresh: {},
  mfsu: {},
  dynamicImport: {},
  analyze: {
    analyzerMode: 'server',
    analyzerPort: 8888,
    openAnalyzer: true,
    generateStatsFile: false,
    statsFilename: 'stats.json',
    logLevel: 'info',
    defaultSizes: 'parsed',
  },
});
