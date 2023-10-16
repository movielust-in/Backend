module.exports = {
    env: {
        browser: true,
        es2021: true,
    },
    extends: [
        'google',
        'plugin:unicorn/all',
        'plugin:import/recommended',
        'prettier',
        'plugin:sonarjs/recommended',
    ],
    plugins: ['unicorn', 'import', 'sonarjs'],
    overrides: [
        {
            env: {
                node: true,
            },
            files: ['.eslintrc.{js,cjs}'],
            parserOptions: {
                sourceType: 'script',
            },
        },
    ],
    parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module',
    },
    rules: {
        camelcase: 'off',
        'require-jsdoc': 'off',
        'unicorn/no-null': 'off',
        'unicorn/prevent-abbreviations': [
            'error',
            {
                allowList: {
                    Param: true,
                    Req: true,
                    Res: true,
                    req: true,
                    res: true,
                },
            },
        ],
    },
};
