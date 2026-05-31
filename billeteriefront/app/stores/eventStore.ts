import { defineStore } from 'pinia';
import { ref } from 'vue';

// 1. Tes interfaces (elles ne changent pas, on les garde pour être prêt pour Django)
export interface EventModel {
  id: string;
  title: string;
  organizer: string;
  description: string;
  category: string;
  venue_name: string;
  address: string;
  city: string;
  country: string;
  latitude?: number | null;
  longitude?: number | null;
  capacity: number;
  start_date: string; 
  end_date: string;
  sales_start_date: string;
  sales_end_date: string;
  created_at: string;
  updated_at: string;
}

export type EventPayload = Omit<EventModel, 'id' | 'created_at' | 'updated_at'>;

export const useEventStore = defineStore('event', () => {
  // --- STATE ---
  const events = ref<EventModel[]>([]);
  const isLoading = ref<boolean>(false);
  const error = ref<string | null>(null);

  // --- ACTIONS ---

  /**
   * Action SIMULÉE pour créer un nouvel évènement
   */
  const createEvent = async (payload: EventPayload) => {
    isLoading.value = true;
    error.value = null;

    try {
      console.log('📦 Données reçues par le store :', payload);

      // 1. On simule un appel API qui prend 1 seconde
      await new Promise(resolve => setTimeout(resolve, 1000)); 
      
      // 2. On simule la réponse de Django en rajoutant un ID et des dates de création
      const newEvent: EventModel = {
        ...payload,
        id: crypto.randomUUID(), // Génère un faux ID unique
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      };
      
      // 3. On ajoute l'évènement au début de notre liste locale
      events.value.unshift(newEvent); 
      
      console.log('✅ Évènement simulé avec succès !');
      return newEvent;

    } catch (err: any) {
      error.value = "Impossible de créer l'évènement (Simulation).";
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Action SIMULÉE pour récupérer la liste (pour le dashboard)
   */
  const fetchEvents = async () => {
    isLoading.value = true;
    error.value = null;

    try {
      // On simule un chargement de 800ms
      await new Promise(resolve => setTimeout(resolve, 800));
      // Note : On ne vide pas "events.value" ici, comme ça l'évènement que 
      // tu viens de créer restera visible quand tu arriveras sur le dashboard !
    } catch (err: any) {
      error.value = "Impossible de charger les évènements.";
    } finally {
      isLoading.value = false;
    }
  };

  return {
    events,
    isLoading,
    error,
    createEvent,
    fetchEvents
  };
});