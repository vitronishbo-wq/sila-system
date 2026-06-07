import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import tseslint from 'typescript-eslint'

export default tseslint.config(
  { ignores: ['dist', 'node_modules'] },
  {
    extends: [
      js.configs.recommended,
      ...tseslint.configs.recommended,
    ],
    files: ['**/*.{ts,tsx}'],
    languageOptions: {
      ecmaVersion: 2020,
      globals: globals.browser,
    },
    plugins: {
      'react-hooks': reactHooks,
      'react-refresh': reactRefresh,
    },
    rules: {
      ...reactHooks.configs.recommended.rules,
      'react-refresh/only-export-components': [
        'warn',
        { allowConstantExport: true },
      ],

      /**
       * 🛡️ ARCHITECTURE HARDENING - LAYER 3: ESLint
       * Aggressive restrictions for import paths
       */

      'no-restricted-imports': [
        'error',
        {
          patterns: [
            {
              group: ['../*'],
              message: '❌ FORBIDDEN: Relative imports. Use @/ absolute alias instead.',
            },
            {
              group: [
                '@/services/operationsService',
                '@/services/dashboardService',
                '@/services/exportJobsService',
                '@/services/adminDocumentService',
                '@/services/adminCitizenService',
                '@/services/citizenAuthService',
                '@/services/documentService',
                '@/services/sla',
                '@/services/territoryService',
              ],
              message: '❌ FORBIDDEN: Service not whitelisted. Must be in @/modules/[domain]/services',
            },
          ],
        },
      ],

      // General quality rules
      '@typescript-eslint/no-unused-vars': [
        'warn',
        { argsIgnorePattern: '^_' },
      ],
      '@typescript-eslint/no-explicit-any': 'warn',
      'prefer-const': 'error',
      'no-var': 'error',
    },
  },
)