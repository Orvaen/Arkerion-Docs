import ComponentTypes from '@theme-original/NavbarItem/ComponentTypes';
import FontToggle from '@site/src/components/FontToggle';

// Type d'élément personnalisé pour la barre de navigation :
// { type: 'custom-fontToggle' } dans docusaurus.config.js.
export default {
  ...ComponentTypes,
  'custom-fontToggle': FontToggle,
};
