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
          
          <div class="modern-ticket">
            
            <div class="ticket-body">
              <div class="ticket-header">
                <span class="badge-nature">{{ eventData.nature || 'ÉVÉNEMENT' }}</span>
                <span class="ticket-date">🗓️ {{ displayDate }}</span>
              </div>
              
              <h3 class="ticket-title">
                {{ eventData.name || 'Le nom de votre événement apparaîtra ici' }}
              </h3>
              
              <div class="ticket-infos">
                <div class="info-line">
                  <span class="icon">📍</span>
                  <span class="text truncate">{{ eventData.location || 'Lieu à définir (ex: Abidjan)' }}</span>
                </div>
                <div class="info-line">
                  <span class="icon">⏰</span>
                  <span class="text">{{ eventData.startTime || '--:--' }}</span>
                </div>
              </div>
            </div>

            <div class="ticket-cutout">
              <div class="dashed-line"></div>
            </div>

            <div class="ticket-stub">
              <div class="stub-price">
                <span class="price-label">Tarif</span>
                <span class="price-value">{{ displayPrice }}</span>
              </div>
              <div class="barcode-mockup">
                ||||| | ||| |||| | ||
              </div>
            </div>
            
          </div>
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

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import AddEventForm from '@/components/forms/addEventForm.vue'; // Ajuste ton chemin
import { useEventStore } from '@/stores/eventStore';

const eventStore = useEventStore();
const router = useRouter();

// L'état global de l'événement, synchronisé avec le formulaire enfant
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

// Formatage dynamique de la date pour le ticket (ex: 25 DÉC. 2026)
const displayDate = computed(() => {
  if (!eventData.value.startDate) return '25 DÉC. 2026';
  const d = new Date(eventData.value.startDate);
  return d.toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' }).toUpperCase();
});

// Calcul du prix minimum (ou "Gratuit" si 0)
const displayPrice = computed(() => {
  const tickets = eventData.value.tickets;
  if (!tickets || tickets.length === 0) return 'Gratuit';
  
  const minPrice = Math.min(...tickets.map(t => t.price || 0));
  return minPrice === 0 ? 'Gratuit' : `Dès ${minPrice} FCFA`;
});

const handleCreate = async () => {
  // Ta logique d'envoi à Pinia / Django ici...
  console.log("Création en cours avec :", eventData.value);
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
.image-preview {
  width: 100%;
  background-color: #0d0d12; /* Assure-toi que ce fond correspond à l'app */
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
  border: 1px solid rgba(255, 255, 255, 0.05);
  overflow: hidden; /* Empêche le ticket de déborder lors des animations */
}
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

/* LE TICKET */
.modern-ticket {
  width: 100%;
  max-width: 320px;
  background: linear-gradient(135deg, var(--primary-color, #3b8d50) 0%, #173d22 100%);
  border-radius: 16px;
  color: white;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
  transform: rotate(-2deg);
  transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.modern-ticket:hover {
  transform: rotate(0deg) scale(1.03); /* Effet sympa au survol */
}

/* Haut du ticket */
.ticket-body {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.ticket-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.8rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
}

.badge-nature {
  background: rgba(255, 255, 255, 0.15);
  padding: 0.3rem 0.6rem;
  border-radius: 20px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-size: 0.7rem;
}

.ticket-title {
  font-size: 1.4rem;
  font-weight: 800;
  line-height: 1.2;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0,0,0,0.2);
  /* Limite à 2 lignes si le titre est trop long */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.ticket-infos {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-line {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.9);
}

.truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 200px;
}

/* LA LIGNE DE DÉCOUPE MAGIQUE */
.ticket-cutout {
  position: relative;
  height: 30px;
  width: 100%;
  display: flex;
  align-items: center;
}

/* Les demi-cercles de chaque côté */
.ticket-cutout::before,
.ticket-cutout::after {
  content: '';
  position: absolute;
  width: 30px;
  height: 30px;
  background-color: #0d0d12; /* DOIT ÊTRE LA MÊME COULEUR QUE .image-preview */
  border-radius: 50%;
  top: 0;
  z-index: 2;
}

.ticket-cutout::before { left: -15px; }
.ticket-cutout::after { right: -15px; }

/* La ligne en pointillés */
.dashed-line {
  width: calc(100% - 40px); /* Laisse la place aux encoches */
  margin: 0 auto;
  border-top: 2px dashed rgba(255, 255, 255, 0.3);
}

/* Bas du ticket (La souche) */
.ticket-stub {
  padding: 1.2rem 1.5rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stub-price {
  display: flex;
  flex-direction: column;
}

.price-label {
  font-size: 0.7rem;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.6);
  letter-spacing: 1px;
}

.price-value {
  font-size: 1.2rem;
  font-weight: 800;
  color: white;
}

.barcode-mockup {
  font-family: 'Courier New', Courier, monospace;
  font-size: 1rem;
  font-weight: bold;
  letter-spacing: 2px;
  color: rgba(255, 255, 255, 0.5);
  transform: scaleY(1.5); /* Étire le texte pour ressembler à un code-barres */
}

@media (min-width: 1024px) {
  .creation-card { flex-direction: row; }
  .form-panel, .preview-panel { flex: 1; padding: 2.5rem; }
}
</style>