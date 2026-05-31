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
            <div class="ticket-graphic">
               <h3>{{ eventData.name || 'THE PARTY OF YOUR LIFE' }}</h3>
               <div class="ticket-details">
                 <span class="smile">🙂</span>
                 <span class="barcode">|||| || ||| ||||</span>
               </div>
            </div>
          </div>

          <div class="theme-section">
            <h4>Theme</h4>
            <div class="theme-cards">
              <div class="theme-card active" style="background: var(--tertiary-color);"></div>
              <div class="theme-card" style="background: linear-gradient(45deg, #1f7b31, #3b8d50);"></div>
              <div class="theme-card" style="background: linear-gradient(45deg, #1a2a6c, #182848);"></div>
              <div class="theme-card" style="background: linear-gradient(45deg, #ff416c, #ff4b2b);"></div>
            </div>
          </div>
        </div>

      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue';
import { useEventStore, type EventPayload } from '~/stores/eventStore';
import AddEventForm from '~/components/forms/addEventForm.vue';

// NUXT importe automatiquement AddEventForm, pas besoin de le faire manuellement !

const eventStore = useEventStore();

// L'état central de ta page (qui est passé au formulaire)
const eventData = reactive({
  name: '',
  description: '',
  category: 'OTHER',
  startDate: '',
  startTime: '',
  endDate: '',
  endTime: '',
  location: '',
  city: 'Abidjan',
  capacity: '',
  requireApproval: true,
  visibility: 'public',
});

// La logique d'envoi
const handleCreate = async () => {
  if (!eventData.name) {
    alert("Veuillez entrer le nom de l'évènement.");
    return;
  }
  
  if (!eventData.startDate || !eventData.startTime || !eventData.endDate || !eventData.endTime) {
    alert("Veuillez définir les dates et heures exactes de début et de fin.");
    return;
  }

  // 1. On crée nos objets Date pour les comparer
  const startDateTime = new Date(`${eventData.startDate}T${eventData.startTime}:00`);
  const endDateTime = new Date(`${eventData.endDate}T${eventData.endTime}:00`);
  const now = new Date();

  // 2. Validation : La date de début est-elle dans le passé ?
  if (startDateTime < now) {
    alert("L'heure de début de l'évènement ne peut pas être dans le passé.");
    return;
  }

  // 3. Validation : La date de fin est-elle AVANT la date de début ?
  if (endDateTime <= startDateTime) {
    alert("La date/heure de fin doit être strictement après la date/heure de début.");
    return;
  }

  try {
    const startISO = startDateTime.toISOString();
    const endISO = endDateTime.toISOString();

    const payload: EventPayload = {
      title: eventData.name,
      description: eventData.description || 'No description provided.',
      category: eventData.category,
      venue_name: eventData.location || 'TBD',
      address: eventData.location || 'Abidjan',
      city: eventData.city,
      country: 'France', 
      capacity: Number(eventData.capacity),
      start_date: startISO,
      end_date: endISO,
      sales_start_date: now.toISOString(), // Vente commence maintenant
      sales_end_date: startISO, // Vente se termine au début de l'event
      organizer: '1c099306-69f8-4777-8339-447035661d4a' // Fake ID
    };

    await eventStore.createEvent(payload);
    navigateTo('/dashboard'); 

  } catch (err) {
    alert("Erreur lors de la création de l'évènement. Vérifiez la console.");
    console.error(err);
  }
};
</script>

<style scoped>
.create-event-container { 
  min-height: 100vh; 
  background-color: var(--background-color); 
  color: var(--my-white); 
  font-family: 'Inter', system-ui, sans-serif; 
  display: flex; 
  flex-direction: column;
}
.top-nav { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  padding: 1rem; 
}
.logo { 
  display: flex; 
  align-items: center; 
  gap: 0.5rem; 
  font-weight: bold;
}
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
.image-preview { width: 100%; aspect-ratio: 1/1; background-color: #000; border-radius: 12px; display: flex; align-items: center; justify-content: center; padding: 1rem; border: 1px dashed var(--secondary-light-color); }
.ticket-graphic { 
  background: linear-gradient(135deg, #F2F864 0%, #3b8d50 100%); 
  width: 100%; 
  height: 100%;
  border-radius: 10px; 
  display: flex; 
  flex-direction: column; 
  justify-content: center; 
  align-items: center; 
  color: var(--background-color); 
  transform: rotate(-5deg); 
  text-align: center; 
  padding: 1rem;
}
.ticket-graphic h3 { font-size: 1.5rem; text-transform: uppercase; font-weight: 900; margin-bottom: 1rem; }

.theme-section h4 { 
  font-size: 1rem; 
  margin-bottom: 1rem; 
  color: var(--my-white);
}
.theme-cards { 
  display: grid; 
  grid-template-columns: repeat(4, 1fr); 
  gap: 0.5rem; 
}
.theme-card { height: 60px; border-radius: 8px; cursor: pointer; border: 2px solid transparent; }
.theme-card.active { border-color: var(--primary-color); }

@media (min-width: 1024px) {
  .creation-card { flex-direction: row; }
  .form-panel, .preview-panel { flex: 1; padding: 2.5rem; }
}
</style>