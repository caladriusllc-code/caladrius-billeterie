<template>
  <div class="nav-wrapper">
    <nav class="main-nav">
      <h3><span>Contrat</span>ChapNeo</h3>
      <Hamburger @toggle="toggleMenu" />
    </nav>

    <!-- Menu déroulant / latéral qui apparaîtra sous la navbar -->
    <div class="nav-layout" :class="{ open: isMenuOpen }">
      <!-- Contenu du menu -->
      <ul>
        <li><a href="#">Accueil</a></li>
        <li><a href="#">Services</a></li>
        <li><a href="#">Contact</a></li>
      </ul>
    </div>
  </div>
</template>

<script lang="ts">
import Hamburger from '../buttons/hamburger.vue';

export default {
  name: 'Navbar',
  components: { Hamburger },
  data() {
    return {
      isMenuOpen: false,
    };
  },
  methods: {
    toggleMenu(isChecked: boolean) {
      this.isMenuOpen = isChecked;
    },
  },
};
</script>

<style scoped>
/* Wrapper pour servir de référence de positionnement */
.nav-wrapper {
  position: relative;
}

/* Navbar fixée ou absolue */
.main-nav {
  position: fixed; /* ou absolute, selon vos besoins */
  top: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: white;
  border-bottom: 1px solid var(--primary-color);
  z-index: 1000;
}

/* Le menu positionné juste en dessous de la navbar */
.nav-layout {
  position: fixed;
  top: 70px; /* Hauteur approximative de la navbar (ajustez selon padding + hauteur texte) */
  left: 0;
  width: 100%;
  background: #c9c9c9;
  z-index: 999;
  transform: translateY(-100%); /* caché vers le haut */
  transition: transform 0.3s ease;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.nav-layout.open {
  transform: translateY(0); /* glisse vers le bas */
}

/* Styles pour le contenu du menu */
.nav-layout ul {
  list-style: none;
  padding: 1rem;
  margin: 0;
}
.nav-layout li {
  padding: 0.5rem 0;
  border-bottom: 1px solid #aaa;
}
.nav-layout a {
  text-decoration: none;
  color: black;
}
</style>