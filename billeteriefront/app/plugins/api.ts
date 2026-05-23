export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  const token = useCookie('token') // ✅ Appelé une seule fois au setup

  const api:object = $fetch.create({
    baseURL: config.public.apiBase || 'http://localhost:8000',

    onRequest({ options }) {
      if (token.value) {
        options.headers = {
          ...options.headers,
          Authorization: `Bearer ${token.value}`,
        }
      }
    },

    onResponseError({ response }) {
      if (response.status === 401) navigateTo('/login')
      if (response.status === 500) throw new Error('Erreur serveur')
    },
  })

  return {
    provide: { api }
  }
})