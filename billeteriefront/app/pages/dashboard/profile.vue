<template>
  <div class="dashboard-container">
    
    <sidebar />

    <main class="main-content">
        <navHead />

        <div class="dashboard-grid">
        
          <div class="left-column">
              
            <statCardSection/>

            <section class="events-section">
              <div class="section-header">
                <h2>Ongoing Event</h2>
                <button class="more-options">•••</button>
              </div>
              </section>

            <section class="events-section">
              <div class="section-header">
                  <h2>Upcoming Event</h2>
                  <button class="more-options">•••</button>
              </div>
              </section>

          </div>

        </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import navHead from '../../components/header/navHead.vue';
import sidebar from '../../components/navbar/sidebar.vue';
import statCardSection from '../../components/sections/statCardSection.vue';
</script>

<style scoped>
/* =========================================
 1. STYLES DE BASE (MOBILE FIRST)
 ========================================= */

.dashboard-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: var(--background-color);
  color: var(--my-white);
  font-family: 'Inter', system-ui, sans-serif;
  overflow: hidden; /* Empêche le body global de scroller */
}

/* Main Content */
.main-content {
  flex: 1;
  padding: 1rem;
  overflow-y: auto; /* Autorise UNIQUEMENT le scroll vertical ici */
  overflow-x: hidden; /* Sécurité : empêche le scroll horizontal indésirable au niveau global */
  padding-bottom: calc(80px + env(safe-area-inset-bottom));
  width: 100%; 
}

/* Dashboard Grid */
.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  min-width: 0; /* 👈 FIX CRUCIAL : Empêche la grille de déborder de l'écran */
  width: 100%;
}

.left-column, .right-column {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  min-width: 0; /* 👈 FIX CRUCIAL : Autorise les composants enfants (comme les stats) à utiliser le scroll horizontal ! */
}

/* Events Section & En-têtes (Seules choses restantes qui appartiennent vraiment au layout) */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-header h2 { 
  font-size: 1.1rem; 
}

/* Zones de clic optimisées (44x44px minimum) */
.more-options { 
  background: none; 
  border: none; 
  color: #a0a0a0; 
  cursor: pointer; 
  min-width: 44px;
  min-height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.events-section{
  width: 100%;
}

/* =========================================
 2. STYLES DESKTOP (>= 1024px)
 ========================================= */
@media (min-width: 1024px) {
  .dashboard-container {
    flex-direction: row;
  }

  .main-content {
    padding: 2rem;
    padding-bottom: 2rem; /* Réinitialisation car plus de navbar en bas */
  }

  /* Grille Principale Desktop (2 colonnes) */
  .dashboard-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
}
</style>