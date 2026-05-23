import { defineStore } from "pinia";
import { ref } from "vue";
import { useNuxtApp } from "#app";

export interface User {
  id?: string | number;
  username: string;
  first_name?: string;
  last_name?: string;
  password: string;
  email: string;
  phone_number: string;
  user_type: string;
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
  }

  // Nouvelle action pour le Login
  const login = async (credentials: Pick<User, 'email' | 'username' | 'password'>) => {
    isLoading.value = true
    error.value = null

    console.log('[AuthStore] login() → credentials envoyés :', credentials)

    try {
      // Ajuste l'URL '/auth/login' selon la structure de ton backend
      const response = await $api('/account/login/', {
        method: 'POST',
        body: credentials,
      })

      if (response){
        console.log('[AuthStore] login() → réponse reçue :', response)

        // Met à jour l'utilisateur (ou gère le stockage du token ici si nécessaire)
        user.value = (response as any).data?.user || {}

        return response
      } else {
        console.log('[AuthStore] login() → erreur :', response)
        error.value = "Identifiants incorrects"
        throw new Error("Identifiants incorrects")
      }

    } catch (err: any) {
      console.error('[AuthStore] login() → erreur :', err)
      error.value = err.message
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
    login, // <-- Ne pas oublier d'exporter la fonction
  }
})