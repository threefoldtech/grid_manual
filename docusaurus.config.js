const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');

// With JSDoc @type annotations, IDEs can provide config autocompletion
/** @type {import('@docusaurus/types').DocusaurusConfig} */
(module.exports = {
  title: 'ThreeFold Manual',
  tagline: 'Documentation for ThreeFold Grid',
  url: 'https://manual.grid.tf',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  onBrokenAnchors: 'throw',
  favicon: 'img/logo_tft_light_short.png',
  organizationName: 'ThreeFold',
  projectName: 'grid_manual',
  markdown: {
    mermaid: true,
  },
  themes: ['@docusaurus/theme-mermaid'],
  headTags: [],
  scripts: [
    {
      src: '/data/load-values.js',
      async: false,
    },
  ],
  presets: [
    [
      '@docusaurus/preset-classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          // Generate sidebar from folder structure
          sidebarPath: undefined,
          editUrl: 'https://github.com/threefoldtech/grid_manual/edit/development/',

        },
        blog: {
          showReadingTime: true,
          editUrl: 'https://github.com/threefoldtech/grid_manual/edit/development/blog/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],
  
  customFields: {
    // Configure MDX to handle custom components properly
    mdx: {
      remarkPlugins: [],
      rehypePlugins: [],
    },
    webpack: {
      configure: (config) => {
        config.module.rules.push({
          test: /\.md$/,
          type: 'asset/source',
        });
        return config;
      },
    },
  },

  plugins: [
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'users',
        path: 'users/docs',
        routeBasePath: 'users',
        // Use auto-generated sidebar based on folder structure
        sidebarPath: undefined,

      },
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'farmers',
        path: 'farmers/docs',
        routeBasePath: 'farmers',
        // Use auto-generated sidebar based on folder structure
        sidebarPath: undefined,

      },
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'labs',
        path: 'labs/docs',
        routeBasePath: 'labs',
        // Use auto-generated sidebar based on folder structure
        sidebarPath: undefined,

      },
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      mermaid: {
        theme: {light: 'default', dark: 'dark'},
      },
      colorMode: {
        defaultMode: 'dark',
        disableSwitch: false,
        respectPrefersColorScheme: false,
      },
      navbar: {
        title: '',
        logo: {
          alt: 'ThreeFold Logo',
          src: 'img/logo_tft_light.png',
          srcDark: 'img/logo_tft_dark.png',
        },
        hideOnScroll: false,
        items: [
          {
            to: '/users/intro',
            position: 'left',
            label: 'Users',
            className: 'navbar__item--desktop-only',
          },
          {
            to: '/farmers/intro',
            position: 'left',
            label: 'Farmers',
            className: 'navbar__item--desktop-only',
          },
          {
            to: '/labs/intro',
            position: 'left',
            label: 'Labs',
            className: 'navbar__item--desktop-only',
          },

          {
            href: 'https://threefold.io',
            label: 'ThreeFold.io',
            position: 'right',
            className: 'navbar__item--desktop-only',
          },
        ],
      },
      // Enable search functionality
      search: {
        // This will be handled by our custom SearchBar component
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Learn',
            items: [
              {
                label: 'Users',
                to: '/users/intro',
              },
              {
                label: 'Farmers',
                to: '/farmers/intro',
              },
              {
                label: 'Labs',
                to: '/labs/intro',
              },
            ],
          },
          {
            title: 'Discuss',
            items: [
              {
                label: 'Forum',
                href: 'https://forum.threefold.io',
              },
              {
                label: 'Telegram',
                href: 'https://t.me/threefold',
              },
              {
                label: 'Support',
                href: 'https://threefoldfaq.crisp.help/en/',
              },
            ],
          },
          {
            title: 'Explore',
            items: [
              {
                label: 'AIBox',
                href: 'https://aibox.threefold.io',
              },
              {
                label: 'Mycelium',
                href: 'https://mycelium.threefold.io',
              },
              {
                label: 'Dashboard',
                href: 'https://dashboard.grid.tf',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} ThreeFold`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },

    }),
});
