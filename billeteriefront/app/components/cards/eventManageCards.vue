<template>
  <div class="event-manage-card glass-effect">
    <!-- Statut Badge -->
    <div class="status-badge" :class="event.status.toLowerCase()">
      <span class="status-dot"></span>
      {{ event.status === 'PUBLISHED' ? 'Publié' : 'Non publié' }}
    </div>

    <!-- Image de l'événement -->
    <div class="card-image" :style="{ background: event.bgGradient }"></div>
    
    <!-- Informations -->
    <div class="card-info">
      <h3 class="event-title" :title="event.title">{{ event.title }}</h3>
      <p class="event-date">🗓️ {{ event.date }}</p>
      
      <div class="stats-mini">
        <span v-if="event.status === 'PUBLISHED'">🎟️ {{ event.ticketsSold || 0 }} / {{ event.capacity }} vendus</span>
        <span v-else>⚙️ En attente de publication</span>
      </div>
    </div>

    <hr class="divider" />

    <!-- Actions contextuelles -->
    <div class="card-actions">
      <template v-if="event.status === 'DRAFT'">
        <button class="action-btn edit-btn" @click="$emit('edit', event.id)">✏️ Modifier</button>
        <button class="action-btn publish-btn" @click="$emit('publish', event.id)">🚀 Publier</button>
      </template>
      
      <template v-else>
        <button class="action-btn dash-btn" @click="$emit('dashboard', event.id)">📊 Tableau de bord</button>
        <button class="action-btn share-btn" title="Copier le lien" @click="$emit('share', event.id)">🔗 Partager</button>
      </template>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue';

export default defineComponent({
  name: 'EventManageCard',
  props: {
    event: {
      type: Object as PropType<any>, // À remplacer par ton interface TypeScript si tu en as une
      required: true
    }
  },
  emits: ['edit', 'publish', 'dashboard', 'share'],
  setup() {
    // La logique interne de la carte si nécessaire
    return {};
  }
});
</script>

<style scoped>
.glass-effect {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.event-manage-card {
  position: relative;
  display: flex;
  flex-direction: column;
  border-radius: 16px;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}

.event-manage-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
}

.card-image { height: 140px; width: 100%; }

.status-badge {
  position: absolute; top: 1rem; right: 1rem; padding: 0.4rem 0.8rem;
  border-radius: 20px; font-size: 0.75rem; font-weight: 700;
  display: flex; align-items: center; gap: 0.4rem; backdrop-filter: blur(4px); z-index: 2;
}

.status-dot { width: 8px; height: 8px; border-radius: 50%; }

.status-badge.draft { background: rgba(40, 40, 40, 0.9); color: #f1c40f; border: 1px solid rgba(241, 196, 15, 0.3); }
.status-badge.draft .status-dot { background: #f1c40f; }

.status-badge.published { background: rgba(40, 40, 40, 0.9); color: #2ecc71; border: 1px solid rgba(46, 204, 113, 0.3); }
.status-badge.published .status-dot { background: #2ecc71; }

.card-info { padding: 1.2rem; display: flex; flex-direction: column; gap: 0.5rem; flex: 1; }
.event-title { font-size: 1.1rem; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.event-date { font-size: 0.85rem; color: #a0a0a0; }

.stats-mini {
  margin-top: 0.5rem; font-size: 0.8rem; color: #d0d0d0; background: rgba(0, 0, 0, 0.2);
  padding: 0.4rem 0.6rem; border-radius: 6px; display: inline-block; width: max-content;
}

.divider { border: 0; height: 1px; background: rgba(255, 255, 255, 0.08); margin: 0; }

.card-actions { display: grid; grid-template-columns: 1fr 1fr; gap: 1px; background: rgba(255, 255, 255, 0.08); }
.action-btn {
  background: transparent; border: none; padding: 1rem; color: white;
  font-size: 0.9rem; font-weight: 600; cursor: pointer; transition: background 0.2s;
  display: flex; align-items: center; justify-content: center; gap: 0.4rem;
}
.action-btn:hover { background: rgba(255, 255, 255, 0.05); }
.publish-btn { color: var(--primary-color, #F2F864); }
.publish-btn:hover { background: rgba(242, 248, 100, 0.1); }
</style>