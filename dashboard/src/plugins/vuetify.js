import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'

export default createVuetify({
  components,
  directives,
  defaults: {
    global: {
      density: 'comfortable',
    }
  },
  icons: {
    defaultSet: 'mdi',
  },
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        dark: false,
        colors: {
          background: '#F8FAFC',
          surface: '#FFFFFF',
          'surface-bright': '#FFFFFF',
          'surface-light': '#F1F5F9',
          'surface-variant': '#E2E8F0',
          'on-surface-variant': '#475569',
          primary: '#7C3AED',
          'primary-darken-1': '#6D28D9',
          secondary: '#0891B2',
          'secondary-darken-1': '#0E7490',
          accent: '#D946EF',
          error: '#EF4444',
          'error-darken-1': '#DC2626',
          info: '#0EA5E9',
          'info-darken-1': '#0284C7',
          success: '#10B981',
          'success-darken-1': '#059669',
          warning: '#F59E0B',
          'warning-darken-1': '#D97706',
        },
        variables: {
          'high-emphasis-opacity': 0.87,
          'medium-emphasis-opacity': 0.60,
          'disabled-opacity': 0.38,
          'idle-opacity': 0.04,
          'hover-opacity': 0.06,
          'focus-opacity': 0.10,
          'selected-opacity': 0.08,
          'activated-opacity': 0.12,
          'pressed-opacity': 0.14,
          'dragged-opacity': 0.10,
        },
      },
      dark: {
        dark: true,
        colors: {
          background: '#0F172A',
          surface: '#1E293B',
          'surface-bright': '#334155',
          'surface-light': '#1E293B',
          'surface-variant': '#334155',
          'on-surface-variant': '#94A3B8',
          primary: '#A78BFA',
          'primary-darken-1': '#8B5CF6',
          secondary: '#22D3EE',
          'secondary-darken-1': '#06B6D4',
          accent: '#F0ABFC',
          error: '#F87171',
          'error-darken-1': '#EF4444',
          info: '#38BDF8',
          'info-darken-1': '#0EA5E9',
          success: '#34D399',
          'success-darken-1': '#10B981',
          warning: '#FBBF24',
          'warning-darken-1': '#F59E0B',
        },
        variables: {
          'high-emphasis-opacity': 0.87,
          'medium-emphasis-opacity': 0.60,
          'disabled-opacity': 0.38,
          'idle-opacity': 0.04,
          'hover-opacity': 0.06,
          'focus-opacity': 0.10,
          'selected-opacity': 0.08,
          'activated-opacity': 0.12,
          'pressed-opacity': 0.14,
          'dragged-opacity': 0.10,
        },
      },
    },
  },
})
