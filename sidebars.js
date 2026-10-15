// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  docs: [
    'intro',
    {
      type: 'category',
      label: 'Identité',
      collapsed: false,
      items: ['identite/logo', 'identite/couleurs', 'identite/typographie', 'identite/arkerion-sans-v2', 'identite/polices'],
    },
    {
      type: 'category',
      label: 'Produits',
      collapsed: false,
      items: ['produits/nebula'],
    },
    {
      type: 'category',
      label: 'Contribuer',
      collapsed: false,
      items: ['contribuer/rediger', 'contribuer/projet'],
    },
  ],
};

export default sidebars;
