<template>
  <div class="stats-section">
    <header class="section-header">
        <h3>Stat évènements en cours</h3>
    </header>
    
    <div class="stats-row">
      <div class="stat-card" v-for="(stat, index) in stats" :key="index">
        <div class="stat-icon" :style="{ color: stat.color }">
          {{ stat.initials }}
        </div>
        <div class="stat-info">
          <h3>{{ stat.title }}</h3>
          <p>Capacity : <strong>{{ stat.current }}</strong>/{{ stat.total }} Tickets</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
export default {
    name: 'StatCardSection',
    props: {
        stats: {
        type: Array,
        required: true,
        default: () => []
        }
    },
    setup(){
        const stats = [
        { initials: 'VIP', title: 'Pass VIP', current: 150, total: 200, color: '#ffac13' },
        { initials: 'ST', title: 'Standard', current: 840, total: 1000, color: '#4ade80' },
        { initials: 'EB', title: 'Early Bird', current: 300, total: 300, color: '#f87171' },
        { initials: 'ST', title: 'Staff', current: 45, total: 50, color: '#60a5fa' }
        ]
        return { stats }
    }
}
</script>

<style scoped>
/* ===========================================================
   0. CONTENEUR GLOBAL (Nouveau)
   =========================================================== */
.stats-section {
  display: flex;
  flex-direction: column;
  gap: 1rem; /* Espace entre le titre et la zone de scroll */
  min-width: 0; /* Protège le layout parent contre le débordement */
  width: 100%;
}

.section-header h3 {
  font-size: 1.1rem;
  margin: 0;
  color: var(--my-white, #ffffff);
}

/* ===========================================================
   1. MOBILE FIRST (Scroll Horizontal Uniquement pour les cartes)
   =========================================================== */
.stats-row {
  display: flex;
  flex-wrap: nowrap; /* 👈 Retour au nowrap, on aligne les cartes ! */
  max-width: 100%;
  gap: 1rem;
  overflow-x: auto;
  padding-bottom: 0.5rem;
  
  scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}

.stats-row::-webkit-scrollbar {
  display: none;
}

.stat-card {
  flex-shrink: 0;
  width: 240px;
  scroll-snap-align: start;
  
  background-color: var(--tertiary-color, #2a2a2a);
  border: 1px solid var(--secondary-light-color, #444);
  border-radius: 12px;
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 40px;
  height: 40px;
  min-width: 40px;
  border-radius: 50%;
  background-color: var(--background-color, #1a1a1a);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.85rem;
  border: 1px solid var(--secondary-light-color, #444);
}

.stat-info h3 { 
  font-size: 0.95rem; 
  margin: 0 0 0.2rem 0; 
  color: var(--my-white, #ffffff);
}
.stat-info p { 
  font-size: 0.75rem; 
  color: #a0a0a0; 
  margin: 0;
}
.stat-info strong { 
  color: var(--my-white, #ffffff); 
}

/* ===========================================================
   2. TABLETTE ET BUREAU (Grille fluide)
   =========================================================== */
@media (min-width: 768px) {
  .stats-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    overflow-x: visible;
    padding-bottom: 0;
  }

  .stat-card {
    width: auto;
    flex-shrink: 1;
    scroll-snap-align: none;
  }
}
</style>