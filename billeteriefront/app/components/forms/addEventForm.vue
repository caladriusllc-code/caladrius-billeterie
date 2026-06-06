<template>
  <div class="form-fields-wrapper glass-effect">
    
    <div class="organizer-info">
      <span class="label">Créé par</span>
      <div class="organizer-select">
        <div class="avatar-sm">MS</div>
        <span>Maria Soniatha ⌄</span>
      </div>
    </div>

    <BaseInput
      type="text"
      placeholder="Nom de l'événement (ex: Concert de l'année)"
      v-model="formData.name"
    />

    <div class="form-group date-time-group">
      <div class="date-badge">
        <span class="month">{{ currentMonth }}</span>
        <span class="day">{{ currentDay }}</span>
      </div>
      <div class="date-inputs">
        <div class="input-row">
          <span class="row-label">Début</span>
          <BaseInput type="date" v-model="formData.startDate" :min="today" />
          <BaseInput type="time" v-model="formData.startTime" />
        </div>
        <div class="input-row">
          <span class="row-label">Fin</span>
          <BaseInput type="date" v-model="formData.endDate" :min="today" />
          <BaseInput type="time" v-model="formData.endTime" />
        </div>
        <div class="input-row timezone-row">
          <span>🌐 GMT +00:00 Abidjan</span>
        </div>
      </div>
    </div>

    <div class="form-group location-group">
      <div class="icon-col">📌</div>
      <div class="input-col">
        <BaseInput 
          type="text" 
          placeholder="Ajouter un lieu" 
          v-model="formData.location" 
        />
        <span class="sub-label">Événement en ligne ou physique</span>
      </div>
    </div>

    <div class="form-group settings-group">
      <div class="icon-col">⚙️</div>
      <div class="settings-list">
        
        <div class="setting-row">
          <div class="setting-label">📂 Nature de l'événement</div>
          <BaseSelect 
            v-model="formData.nature" 
            :options="natureOptions"
          />
        </div>
        
        <div class="setting-row">
          <div class="setting-label">👤 Validation requise</div>
          <div class="setting-value">
            <label class="switch">
              <input type="checkbox" v-model="formData.requireApproval">
              <span class="slider round"></span>
            </label>
          </div>
        </div>
        
        <div class="setting-row">
          <div class="setting-label">👥 Capacité</div>
          <BaseInput 
            type="number" 
            placeholder="Ex: 1000"
            v-model="formData.capacity" 
          />
        </div>

      </div>
    </div>

    <div class="form-group tickets-group">
      <div class="icon-col">🎟️</div>
      <div class="tickets-list-col">
        <span class="setting-label" style="margin-bottom: 0.5rem; display: block;">Catégories de tickets & Prix</span>
        
        <div class="tickets-container">
          <TransitionGroup name="ticket-fade" tag="div" class="tickets-wrapper">
            <div 
              v-for="(ticket, index) in formData.tickets" 
              :key="ticket.id" 
              class="ticket-row"
            >
              <BaseInput 
                type="text" 
                placeholder="Nom (ex: VIP, Standard)" 
                v-model="ticket.name" 
              />
              
              <BaseInput 
                type="number" 
                placeholder="0" 
                v-model="ticket.price" 
                min="0"
              >
                <template #append>
                  <span class="currency-text">FCFA</span>
                </template>
              </BaseInput>

              <button 
                v-if="formData.tickets && formData.tickets.length > 1" 
                @click.prevent="removeTicket(index)" 
                class="delete-ticket-btn"
                title="Supprimer la catégorie"
              >
                ✖
              </button>
              <div v-else class="delete-placeholder"></div>
            </div>
          </TransitionGroup>
          
          <button @click.prevent="addTicket" class="add-ticket-btn">
            + Ajouter une catégorie
          </button>
        </div>

      </div>
    </div>

    <textarea 
      class="description-area" 
      placeholder="Dites-nous en plus sur l'événement..." 
      v-model="formData.description"
    ></textarea>

  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import BaseInput from '../input/BaseInput.vue';
import BaseSelect from '../input/BaseSelect.vue';

const props = defineProps({
  formData: {
    type: Object,
    required: true
  }
});

const natureOptions = [
  { name: 'Concert', value: 'CONCERT' },
  { name: 'Sport', value: 'SPORT' },
  { name: 'Conférence', value: 'CONFERENCE' },
  { name: 'Autre', value: 'OTHER' }
];

const today = useState('todayDate', () => new Date().toISOString().split('T')[0]);

const currentMonth = computed(() => {
  if (!props.formData.startDate) return 'MM';
  const d = new Date(props.formData.startDate);
  return d.toLocaleString('fr-FR', { month: 'short' }).toUpperCase(); 
});

const currentDay = computed(() => {
  if (!props.formData.startDate) return '--';
  return new Date(props.formData.startDate).getDate().toString().padStart(2, '0');
});

// --- LOGIQUE DE GESTION DES TICKETS ---
const addTicket = () => {
  // Sécurité au cas où le parent n'aurait pas initialisé le tableau
  if (!props.formData.tickets) {
    props.formData.tickets = [];
  }
  
  props.formData.tickets.push({
    id: Date.now(), // ID unique généré pour le :key de Vue
    name: '',
    price: 0
  });
};

const removeTicket = (index: number) => {
  if (props.formData.tickets && props.formData.tickets.length > 1) {
    props.formData.tickets.splice(index, 1);
  }
};
</script>

<style scoped>
/* Les styles précédents inchangés... */
.form-fields-wrapper { display: flex; flex-direction: column; gap: 1.5rem; }
.organizer-info { display: flex; flex-direction: column; gap: 0.3rem; }
.organizer-info .label { font-size: 0.8rem; color: #a0a0a0; }
.organizer-select { display: flex; align-items: center; gap: 0.5rem; font-size: 0.9rem; }
.avatar-sm { width: 24px; height: 24px; border-radius: 50%; background-color: var(--primary-color, #3b8d50); display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: bold; color: white; }

.date-time-group { display: flex; gap: 1.2rem; align-items: flex-start; }
.date-badge { display: flex; flex-direction: column; align-items: center; justify-content: center; width: 55px; height: 55px; background: rgba(255, 255, 255, 0.05); border-radius: 10px; border: 1px solid var(--secondary-light-color, #333); }
.date-badge .month { font-size: 0.65rem; color: #ff4b2b; font-weight: bold; }
.date-badge .day { font-size: 1.1rem; font-weight: bold; }
.date-inputs { flex: 1; display: flex; flex-direction: column; gap: 0.8rem; }
.input-row { display: flex; align-items: center; gap: 0.5rem; }
.row-label { width: 45px; color: #a0a0a0; font-size: 0.8rem; }
.timezone-row { font-size: 0.8rem; color: #a0a0a0; margin-top: 0.2rem; }

.location-group, .settings-group, .tickets-group { display: flex; gap: 1rem; align-items: flex-start; }
.icon-col { width: 20px; display: flex; justify-content: center; margin-top: 0.5rem; }
.input-col, .settings-list, .tickets-list-col { flex: 1; display: flex; flex-direction: column; gap: 0.5rem; }
.sub-label { font-size: 0.75rem; color: #a0a0a0; margin-left: 0.5rem; }

.setting-row { display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.05); }
.setting-row:last-child { border-bottom: none; }
.setting-label { font-size: 0.9rem; color: #d0d0d0; }

.description-area { min-height: 100px; resize: vertical; background: rgba(255, 255, 255, 0.05); border: 1px solid transparent; color: white; padding: 12px; border-radius: 8px; outline: none; font-family: inherit; width: 100%; transition: border-color 0.3s ease; }
.description-area:focus { border-color: var(--primary-color, #3b8d50); }

.switch { position: relative; display: inline-block; width: 44px; height: 22px; }
.switch input { opacity: 0; width: 0; height: 0; }
.slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #555; transition: .4s; border-radius: 22px; }
.slider:before { position: absolute; content: ""; height: 18px; width: 18px; left: 2px; bottom: 2px; background-color: white; transition: .4s; border-radius: 50%; }
input:checked + .slider { background-color: var(--primary-color, #3b8d50); }
input:checked + .slider:before { transform: translateX(22px); }

/* --- STYLES NOUVELLE SECTION BILLETTERIE --- */
.tickets-container {
  background: rgba(0, 0, 0, 0.15);
  padding: 1rem;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.tickets-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.ticket-row {
  display: grid;
  /* La grille force le Nom (2 portions), le Prix (1.5 portions), et le bouton (36px fixés) */
  grid-template-columns: 2fr 1.5fr 36px;
  gap: 0.8rem;
  align-items: center;
}

.currency-text {
  font-size: 0.75rem;
  font-weight: bold;
  color: #a0a0a0;
}

.delete-ticket-btn {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  border: 1px solid rgba(255, 69, 58, 0.3);
  background: rgba(255, 69, 58, 0.1);
  color: #ff453a;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.delete-ticket-btn:hover {
  background: rgba(255, 69, 58, 0.25);
}

.delete-placeholder {
  width: 36px;
}

.add-ticket-btn {
  background: transparent;
  border: 1px dashed rgba(255, 255, 255, 0.2);
  color: var(--primary-color, #3b8d50);
  border-radius: 8px;
  padding: 0.7rem;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 0.5rem;
}

.add-ticket-btn:hover {
  border-color: var(--primary-color, #3b8d50);
  background: rgba(59, 141, 80, 0.05);
}

/* Animations d'ajout/suppression */
.ticket-fade-enter-active,
.ticket-fade-leave-active {
  transition: all 0.3s ease;
}
.ticket-fade-enter-from,
.ticket-fade-leave-to {
  opacity: 0;
  transform: translateX(-15px);
}
</style>