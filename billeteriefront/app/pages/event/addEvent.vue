<template>
  <div class="create-event-container">
    <header class="top-nav">
      <div class="logo">
        <span class="logo-icon">C</span>
        <span class="logo-text">Calevent</span>
      </div>
      <div class="nav-actions">
        <div class="user-profile">
          <div class="avatar">MS</div>
          <span class="hidden-mobile">Maria Soniatha</span>
        </div>
      </div>
    </header>

    <main class="main-content">
      <div class="creation-card">
        
        <div class="form-panel">
          <AddEventForm :formData="eventData" />
          <button 
            class="btn-primary create-btn" 
            @click="handleCreate"
            :disabled="eventStore.isLoading"
          >
            {{ eventStore.isLoading ? 'Creating...' : 'Create Event' }}
          </button>
        </div>

        <div class="preview-panel">
          <div class="image-preview">
            <TicketPreview :eventData="eventData" />
          </div>

          <div class="theme-section">
            <h4>Theme</h4>
            <div class="theme-cards">
              <div class="theme-card active" style="background: var(--tertiary-color);"></div>
              <div class="theme-card" style="background: linear-gradient(45deg, #1f7b31, #3b8d5a);"></div>
            </div>
          </div>
        </div>

      </div>
    </main>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useRouter } from 'vue-router';
import AddEventForm from '@/components/forms/addEventForm.vue';
import TicketPreview from '@/components/sections/ticketPreviewSection.vue'; // Assure-toi que le chemin est correct
import { useEventStore } from '@/stores/eventStore';

export default defineComponent({
  name: 'AddEventPage',
  components: {
    AddEventForm,
    TicketPreview
  },
  setup() {
    const eventStore = useEventStore();
    const router = useRouter();

    const eventData = ref({
      name: '',
      startDate: '2026-12-25',
      startTime: '19:00',
      endDate: '2026-12-26',
      endTime: '02:00',
      location: '',
      nature: 'CONCERT',
      requireApproval: true,
      capacity: 1000,
      description: '',
      tickets: [
        { id: Date.now(), name: 'Standard', price: 0 }
      ]
    });

    const handleCreate = async () => {
      console.log("Création en cours avec :", eventData.value);
      // Logique d'envoi API ici
    };

    return {
      eventStore,
      eventData,
      handleCreate
    };
  }
});
</script>

<style scoped>
.create-event-container { min-height: 100vh; background-color: var(--background-color); color: var(--my-white); font-family: 'Inter', system-ui, sans-serif; display: flex; flex-direction: column; }
.top-nav { display: flex; justify-content: space-between; align-items: center; padding: 1rem; }
.logo { display: flex; align-items: center; gap: 0.5rem; font-weight: bold; }
.logo-icon { width: 24px; height: 24px; background-color: var(--primary-color); color: var(--background-color); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; }
.user-profile { display: flex; align-items: center; gap: 0.5rem; background: var(--tertiary-color); padding: 0.3rem 0.5rem; border-radius: 20px; border: 1px solid var(--secondary-light-color); }
.avatar { width: 25px; height: 25px; border-radius: 50%; background-color: var(--background-green-color); display: flex; align-items: center; justify-content: center; font-size: 0.7rem; font-weight: bold; }

.main-content { flex: 1; padding: 1rem; display: flex; justify-content: center; }
.creation-card { width: 100%; max-width: 1000px; background-color: var(--tertiary-color); border: 1px solid var(--secondary-light-color); border-radius: 20px; display: flex; flex-direction: column; overflow: hidden; }

.form-panel { padding: 1.5rem; display: flex; flex-direction: column; gap: 1.2rem; }
.btn-primary { background-color: var(--my-white); color: var(--background-color); border: none; border-radius: 8px; padding: 1rem; font-size: 1rem; font-weight: bold; cursor: pointer; transition: 0.3s; margin-top: 1rem; }
.btn-primary:hover:not(:disabled) { background-color: var(--primary-color); }
.btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }

.preview-panel { background-color: rgba(0, 0, 0, 0.2); padding: 1.5rem; display: flex; flex-direction: column; gap: 1.5rem; }
.image-preview { width: 100%; background-color: #0d0d12; border-radius: 16px; display: flex; align-items: center; justify-content: center; padding: 2rem 1rem; border: 1px solid rgba(255, 255, 255, 0.05); overflow: hidden; }

.theme-section h4 { font-size: 1rem; margin-bottom: 1rem; color: var(--my-white); }
.theme-cards { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.5rem; }
.theme-card { height: 60px; border-radius: 8px; cursor: pointer; border: 2px solid transparent; }
.theme-card.active { border-color: var(--primary-color); }

@media (min-width: 1024px) {
  .creation-card { flex-direction: row; }
  .form-panel, .preview-panel { flex: 1; padding: 2.5rem; }
}
</style>