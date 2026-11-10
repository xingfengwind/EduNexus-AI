import vue from 'eslint-plugin-vue'
import ts from 'typescript-eslint'
export default ts.config({ ignores: ['dist/**','node_modules/**','playwright-report/**','test-results/**'] }, ...ts.configs.recommended, ...vue.configs['flat/recommended'], { files: ['**/*.vue'], languageOptions: { parserOptions: { parser: ts.parser } } })
