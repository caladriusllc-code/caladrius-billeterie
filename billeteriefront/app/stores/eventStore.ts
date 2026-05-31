import { defineStore } from 'pinia';
import { ref } from 'vue';

// 1. Interfaces basées sur votre modèle Django
export interface EventModel {
  id: string;
  title: string;
  organizer: string; // ID de l'utilisateur (UUID ou Number selon votre backend)
  description: string;
  category: string;
  venue_name: string;
  address: string;
  city: string;
  country: string;
  latitude?: number | null;
  longitude?: number | null;
  capacity: number;
  start_date: string; // Format ISO 8601 attendu par Django DateTimeField
  end_date: string;
  sales_start_date: string;
  sales_end_date: string;
  created_at: string;
  updated_at: string;
}

// 2. Type pour la création (exclut les champs générés par le backend)
export type EventPayload = Omit<EventModel, 'id' | 'created_at' | 'updated_at'>;

export const useEventStore = defineStore('event', () => {
  // --- STATE ---
  const events = ref<EventModel[]>([]);
  const isLoading = ref<boolean>(false);
  const error = ref<string | null>(null);

  // --- ACTIONS ---

  /**
   * Action pour créer un nouvel évènement
   */
  const createEvent = async (payload: EventPayload) => {
    isLoading.value = true;
    error.value = null;

    // Récupération de l'URL de base de l'API via le runtimeConfig de Nuxt
    const config = useRuntimeConfig();

    try {
      // Utilisation de $fetch (natif à Nuxt 3)
      const newEvent = await $fetch<EventModel>(`${config.public.apiBase}/events/`, {
        method: 'POST',
        body: payload
      });
      
      // Ajoute l'évènement renvoyé par Django au début de la liste
      events.value.unshift(newEvent); 
      return newEvent;

    } catch (err: any) {
      console.error('Erreur lors de la création:', err);
      // $fetch stocke la réponse d'erreur dans err.data (différent de err.response.data d'Axios)
      error.value = err.data?.detail || "Impossible de créer l'évènement.";
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Action pour récupérer la liste des évènements (pour le dashboard)
   */
  const fetchEvents = async () => {
    isLoading.value = true;
    error.value = null;
    
    const config = useRuntimeConfig();

    try {
      // Un simple appel GET avec $fetch
      const data = await $fetch<EventModel[]>(`${config.public.apiBase}/events/`);
      events.value = data;
    } catch (err: any) {
      console.error('Erreur de chargement:', err);
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