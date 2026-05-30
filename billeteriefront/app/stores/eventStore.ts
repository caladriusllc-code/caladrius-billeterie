import { defineStore } from 'pinia';
import { ref } from 'vue';
// Si vous utilisez axios, décommentez la ligne suivante :
// import axios from 'axios';

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

    try {
      // EXEMPLE AVEC AXIOS :
      // const response = await axios.post<EventModel>('VOTRE_API_URL/events/', payload);
      // events.value.push(response.data);
      
      // Simulation d'un appel réseau (à remplacer par votre appel API réel)
      console.log('Données envoyées au backend :', payload);
      
      await new Promise(resolve => setTimeout(resolve, 1000)); 
      
      // Simulation du retour backend (avec ID et timestamps)
      const newEvent: EventModel = {
        ...payload,
        id: crypto.randomUUID(),
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      };
      
      events.value.unshift(newEvent); // Ajoute au début de la liste
      return newEvent;

    } catch (err: any) {
      console.error('Erreur lors de la création:', err);
      // Gestion d'erreur typique (ex: erreurs de validation Django)
      error.value = err.response?.data?.detail || "Impossible de créer l'évènement.";
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
    try {
      // const response = await axios.get<EventModel[]>('VOTRE_API_URL/events/');
      // events.value = response.data;
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