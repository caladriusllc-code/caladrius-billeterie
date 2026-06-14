import { defineStore } from "pinia";
import { ref } from "vue";
import { useNuxtApp } from "#app";

export interface User {
  id?: string | number;
  username: string;
  first_name?: string;
  last_name?: string;
  password: string;
  passwordConfirmation?: string;
  email: string;
  phone_number: string;
  user_type: string | null;
}

export const useAuthStore = defineStore('auth', () => {

  // State
  const user = ref<User>({
    id: '',
    username: '',
    first_name: '',
    last_name: '',
    password: '',
    email: '',
    phone_number: '',
    user_type: ''
  })

  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const { $api } = useNuxtApp() as any

  // Actions
  const register = async (payload: Omit<User, 'id'>) => {
    // ... ton code existant pour register ...
    isLoading.value = true;
    error.value = null;

    console.log('[formulaire soumis]', payload)

    try{
      const response = await $api('/account/register/', {
        method: 'POST',
        body: payload
      }) as any

      if (response && response.user) {
        console.log('[AuthStore] login() → réponse reçue :', response)

        user.value = {
          ...response.user,
          id: response.user.user // Récupère le user.id renvoyé par Django
        }

        return response
      } else {
        console.log('[AuthStore] login() → erreur structurelle ou réponse vide')
        error.value = "Erreur lors de l'ouverture du compte"
        throw new Error("Identifiants incorrects")
      }
    } catch (err: any) {
      console.error('[AuthStore] registration() → erreur :', err)
      // Gestion si le backend renvoie une erreur au format { error: "..." }
      error.value = err.data?.error || err.message || "Une erreur est survenue"
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // Nouvelle action pour le Login
  // authStore.ts

  const login = async (credentials: Pick<User, 'email' | 'username' | 'password'>) => {
    isLoading.value = true
    error.value = null

    console.log('[AuthStore] login() → credentials envoyés :', credentials)

    try {
      const response = await $api('/account/login/', {
        method: 'POST',
        body: credentials,
      }) as any // Cast temporaire pour éviter les erreurs d'auto-complétion

      if (response && response.user) {
        console.log('[AuthStore] login() → réponse reçue :', response)

        user.value = {
          ...response.user,
          id: response.user.user // Récupère le user.id renvoyé par Django
        }

        return response
      } else {
        console.log('[AuthStore] login() → erreur structurelle ou réponse vide')
        error.value = "Identifiants incorrects"
        throw new Error("Identifiants incorrects")
      }

    } catch (err: any) {
      console.error('[AuthStore] login() → erreur :', err)
      // Gestion si le backend renvoie une erreur au format { error: "..." }
      error.value = "Problème de connexion"
      throw err
    } finally {
      isLoading.value = false
    }
  }

  return {
    user,
    isLoading,
    error,
    register,
    login,
  }
})