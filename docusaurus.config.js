// @ts-check
import { themes as prismThemes } from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Arkerion',
  tagline: 'Développement web et logiciel',
  favicon: 'img/logo/arkerion-symbole-noir.svg',

  url: 'https://orvaen.github.io',
  baseUrl: '/Arkerion-Docs/',
  organizationName: 'Orvaen',
  projectName: 'Arkerion-Docs',
  trailingSlash: false,

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  i18n: { defaultLocale: 'fr', locales: ['fr'] },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          routeBasePath: 'docs',
          editUrl: 'https://github.com/Orvaen/Arkerion-Docs/edit/main/',
          showLastUpdateTime: false,
        },
        blog: false,
        theme: { customCss: './src/css/custom.css' },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      colorMode: { defaultMode: 'light', respectPrefersColorScheme: true },
      navbar: {
        title: 'Arkerion',
        logo: {
          alt: 'Arkerion',
          src: 'img/logo/arkerion-symbole-noir.svg',
          srcDark: 'img/logo/arkerion-symbole-blanc.svg',
          width: 26,
          height: 26,
        },
        items: [
          { type: 'docSidebar', sidebarId: 'docs', position: 'left', label: 'Documentation' },
          { to: '/docs/identite/logo', position: 'left', label: 'Identité' },
          { to: '/docs/produits/nebula', position: 'left', label: 'Nebula' },
          { href: 'https://github.com/Orvaen/Arkerion-Docs', position: 'right', label: 'GitHub' },
        ],
      },
      footer: {
        style: 'light',
        links: [
          {
            title: 'Documentation',
            items: [
              { label: 'Introduction', to: '/docs/intro' },
              { label: 'Polices Arkerion', to: '/docs/identite/polices' },
            ],
          },
          {
            title: 'Identité',
            items: [
              { label: 'Logo', to: '/docs/identite/logo' },
              { label: 'Couleurs', to: '/docs/identite/couleurs' },
              { label: 'Typographie', to: '/docs/identite/typographie' },
            ],
          },
          {
            title: 'Code source',
            items: [
              { label: 'Arkerion-Docs', href: 'https://github.com/Orvaen/Arkerion-Docs' },
              { label: 'Nebula', href: 'https://github.com/Orvaen/nebula' },
            ],
          },
        ],
        copyright: `© ${new Date().getFullYear()} Arkerion. Tous droits réservés.`,
      },
      prism: {
        // Fonds de code accordés au thème clair (neige) et charbon chaud (sombre).
        theme: { ...prismThemes.github, plain: { ...prismThemes.github.plain, backgroundColor: '#F3F2F6' } },
        darkTheme: { ...prismThemes.vsDark, plain: { ...prismThemes.vsDark.plain, backgroundColor: '#23211F' } },
        additionalLanguages: ['bash', 'json'],
      },
      tableOfContents: { minHeadingLevel: 2, maxHeadingLevel: 3 },
    }),
};

export default config;
