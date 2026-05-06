// eslint.config.mjs
import withNuxt from './.nuxt/eslint.config.mjs'
import pluginSecurity from 'eslint-plugin-security'

export default withNuxt([
  // 1. Añadimos la configuración recomendada del plugin
  pluginSecurity.configs.recommended,
  
  // 2. Mantenemos tus reglas personalizadas
  {
    rules: {
      'vue/multi-word-component-names': 'off',
    }
  }
])