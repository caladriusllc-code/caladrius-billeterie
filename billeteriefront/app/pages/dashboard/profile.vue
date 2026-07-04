<template>
  <div class="dashboard-container">
    
    <!-- La sidebar est connectée à la variable et met à jour l'état quand on clique -->
    <sidebar 
      :activeView="currentView" 
      @change-view="currentView = $event" 
    />

    <main class="main-content">
        <navHead />

        <!-- VUE : ACCUEIL DU DASHBOARD -->
        <div v-if="currentView === 'home'" class="dashboard-grid fade-in">
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

        <!-- VUE : GESTION DES ÉVÉNEMENTS -->
        <div v-else-if="currentView === 'events'" class="events-view fade-in">
          <ManageEvents />
        </div>

    </main>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import navHead from '../../components/header/navHead.vue';
import sidebar from '../../components/navbar/sidebar.vue';
import statCardSection from '../../components/sections/statCardSection.vue';

// ⚠️ Ajuste le chemin selon l'endroit où tu as sauvegardé ManageEvents.vue 
import ManageEvents from '../../components/sections/manageEvents.vue';

export default defineComponent({
  name: 'ProfileDashboard',
  components: {
    navHead,
    sidebar,
    statCardSection,
    ManageEvents
  },
  setup() {
    // État local qui détermine quelle page est affichée
    const currentView = ref('home');

    return {
      currentView
    };
  }
});
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
  overflow: hidden; 
}

.main-content {
  flex: 1;
  padding: 1rem;
  overflow-y: auto; 
  overflow-x: hidden; 
  padding-bottom: calc(80px + env(safe-area-inset-bottom));
  width: 100%; 
}

/* Animations de transition entre les vues */
.fade-in {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Dashboard Grid */
.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  min-width: 0; 
  width: 100%;
}

/* Conteneur pour la vue événements (annule les paddings internes doubles) */
.events-view {
  width: 100%;
  display: flex;
  flex-direction: column;
}

.left-column, .right-column {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  min-width: 0; 
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-header h2 { 
  font-size: 1.1rem; 
}

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
    padding-bottom: 2rem; 
  }

  .dashboard-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
}
</style>