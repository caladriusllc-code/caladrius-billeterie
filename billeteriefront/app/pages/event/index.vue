<template>
  <div class="manage-events-container">
    
    <header class="manage-header glass-effect">
      <div class="header-content">
        <div>
          <h1 class="page-title">Mes Événements</h1>
          <p class="page-subtitle">Gérez vos brouillons et événements en ligne</p>
        </div>
        <button class="btn-primary add-btn" @click="router.push('/event/addEvent')">
          + Nouvel événement
        </button>
      </div>
    </header>

    <main class="main-content">
      <!-- NAVIGATION PAR ONGLETS -->
      <div class="tabs-container glass-effect">
        <button class="tab-btn" :class="{ active: activeTab === 'DRAFT' }" @click="activeTab = 'DRAFT'">
          Non publiés ({{ draftCount }})
        </button>
        <button class="tab-btn" :class="{ active: activeTab === 'PUBLISHED' }" @click="activeTab = 'PUBLISHED'">
          En ligne ({{ publishedCount }})
        </button>
        <button class="tab-btn" :class="{ active: activeTab === 'ALL' }" @click="activeTab = 'ALL'">
          Tous
        </button>
      </div>

      <!-- GRILLE DES ÉVÉNEMENTS -->
      <div v-if="filteredEvents.length > 0" class="events-grid">
        <TransitionGroup name="fade-list">
          <!-- Appel du composant refactorisé -->
          <EventManageCard 
            v-for="event in filteredEvents" 
            :key="event.id" 
            :event="event"
            @edit="editEvent"
            @publish="publishEvent"
            @dashboard="goToDashboard"
          />
        </TransitionGroup>
      </div>

      <!-- ÉTAT VIDE -->
      <div v-else class="empty-state glass-effect">
        <div class="empty-icon">📁</div>
        <h3>Aucun événement trouvé</h3>
        <p>Vous n'avez pas d'événement dans cette catégorie pour le moment.</p>
      </div>
    </main>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import { useRouter } from 'vue-router';
// Importe le composant (Adapte le chemin selon ton dossier components)
import EventManageCard from '@/components/cards/eventManageCards.vue';

export default defineComponent({
  name: 'ManageEvents',
  components: {
    EventManageCard,
  },
  setup() {
    const router = useRouter();
    const activeTab = ref('DRAFT');

    const myEvents = ref([
      { id: 1, title: 'Le Grand Concert', date: '25 Déc 2026', status: 'DRAFT', capacity: 1000, bgGradient: 'linear-gradient(45deg, #1a2a6c, #b21f1f)', ticketsSold: 0 },
      { id: 2, title: 'Festival des Grillades', date: '15 Sep 2026', status: 'PUBLISHED', capacity: 5000, bgGradient: 'linear-gradient(45deg, #ff416c, #ff4b2b)', ticketsSold: 1245 }
    ]);

    const draftCount = computed(() => myEvents.value.filter(e => e.status === 'DRAFT').length);
    const publishedCount = computed(() => myEvents.value.filter(e => e.status === 'PUBLISHED').length);

    const filteredEvents = computed(() => {
      if (activeTab.value === 'ALL') return myEvents.value;
      return myEvents.value.filter(e => e.status === activeTab.value);
    });

    const publishEvent = (id: number) => {
      const event = myEvents.value.find(e => e.id === id);
      if (event && confirm(`Publier "${event.title}" ?`)) {
        event.status = 'PUBLISHED';
        activeTab.value = 'PUBLISHED';
      }
    };

    const editEvent = (id: number) => router.push(`/event/edit/${id}`);
    const goToDashboard = (id: number) => router.push(`/event/dashboard/${id}`);

    return {
      router, activeTab, draftCount, publishedCount, 
      filteredEvents, publishEvent, editEvent, goToDashboard
    };
  }
});
</script>

<style scoped>
.manage-events-container { min-height: 100vh; background-color: var(--background-color, #181818); color: var(--my-white, #fff); font-family: system-ui, sans-serif; padding-bottom: 4rem; }
.glass-effect { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.08); }
.main-content { max-width: 1200px; margin: 0 auto; padding: 2rem 1.5rem; display: flex; flex-direction: column; gap: 2rem; }

.manage-header { padding: 2rem 5%; border-bottom: 1px solid rgba(255, 255, 255, 0.05); }
.header-content { max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }
.page-title { font-size: 1.8rem; font-weight: 800; margin-bottom: 0.3rem; }
.page-subtitle { color: #a0a0a0; font-size: 0.9rem; }
.add-btn { background: var(--primary-color, #F2F864); color: #000; border: none; padding: 0.8rem 1.5rem; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.2s; }
.add-btn:hover { transform: translateY(-2px); }

.tabs-container { display: flex; gap: 0.5rem; padding: 0.5rem; border-radius: 12px; width: max-content; max-width: 100%; overflow-x: auto; }
.tab-btn { background: transparent; border: none; color: #a0a0a0; padding: 0.6rem 1.2rem; border-radius: 8px; font-weight: 600; cursor: pointer; transition: 0.3s; white-space: nowrap; }
.tab-btn:hover { color: #fff; background: rgba(255, 255, 255, 0.05); }
.tab-btn.active { background: rgba(255, 255, 255, 0.1); color: var(--primary-color, #F2F864); }

.events-grid { display: grid; grid-template-columns: 1fr; gap: 1.5rem; }

.empty-state { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 4rem 2rem; border-radius: 16px; gap: 1rem; }
.empty-icon { font-size: 3rem; opacity: 0.5; }
.empty-state h3 { font-size: 1.2rem; }
.empty-state p { color: #a0a0a0; font-size: 0.9rem; }

.fade-list-enter-active, .fade-list-leave-active { transition: all 0.4s ease; }
.fade-list-enter-from, .fade-list-leave-to { opacity: 0; transform: scale(0.95); }

@media (min-width: 768px) { .events-grid { grid-template-columns: repeat(2, 1fr); } }
@media (min-width: 1024px) { .events-grid { grid-template-columns: repeat(3, 1fr); } }
</style>