import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.simondulai.optotask',
  appName: 'OptoTask',
  webDir: 'build',
  server: {
    androidScheme: 'https'
  }
};

export default config;