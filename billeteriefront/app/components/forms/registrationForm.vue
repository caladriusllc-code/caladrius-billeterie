<template>
    <form @submit.prevent="handleLogin">

        <h3>Création de compte</h3>

        <stepper :steps="stepItems"/>

        <template v-if="step === 1">

            <BaseChoices v-model="registrationForm.user_type"/>

        </template>

        <template v-else>

            <BaseInputVue 
                label="Email/username"
                v-model="registrationForm.username"
                :errorMessage="errorMessage.username"
            />

            <BaseInputVue 
                label="Mot de passe"
                v-model="registrationForm.password"
                :errorMessage="errorMessage.password"
                type="password"
            />

            <mainButton 
                label="Connexion" 
                type="submit"
                :isLoading="authStore.isLoading"
            />

        </template>

        <div class="err-message-wrapper" v-if="authStore.error" >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z" />
            </svg>
            <p class="error-message">
                {{ authStore.error }}
            </p>
        </div>

        <divider orientation="horizontal" :thickness="2" color="#515151" length="100%" />

        <p>J'ai pas de compte</p>

        <secondButton label="Ouvrir un compte"/>

    </form>
</template>

<script lang="ts">
import BaseInputVue from '../input/BaseInput.vue';
import mainButton from '../buttons/mainButton.vue';
import secondButton from '../buttons/secondButton.vue';
import divider from '../tools/divider.vue';
import stepper from '../tools/stepper.vue';
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../../stores/authStore';
import type {User} from '../../stores/authStore';
import BaseChoices from '../input/BaseChoices.vue';

interface ErrorMessage{
    username: string,
    password: string
}

interface Credentials{
    username: string,
    password: string,
    email: string
}

export default {
    components:{
        BaseInputVue,
        mainButton,
        secondButton,
        BaseChoices,
        divider,
        stepper
    },
    setup(){

        const router = useRouter()

        // Store
        const authStore = useAuthStore()

        // State
        const registrationForm = ref<User>({
            username:'',
            password:'',
            email:'',
            first_name:'',
            'last_name':'',
            phone_number:'',
            user_type:''
        })

        const errorMessage = ref<ErrorMessage>({
            username: '',
            password: ''
        })

        const step = ref(1)

        const stepItems = computed(() => [
            { id: 1, name: 'Type de compte',            isActive: step.value === 1 },
            { id: 2, name: 'Informations',               isActive: step.value === 2 },
            { id: 3, name: 'Coordonnées',                isActive: step.value === 3 },
        ])

        // computed
        const validateForm = (): boolean => {
            // On réinitialise les messages d'erreur à chaque vérification
            errorMessage.value.username = ''
            errorMessage.value.password = ''
            
            let isValid = true

            if (!registrationForm.value.username.trim()) {
                errorMessage.value.username = "Veuillez entrer un email ou un nom d'utilisateur."
                isValid = false
            } else if (registrationForm.value.username.length < 3) {
                errorMessage.value.username = "L'identifiant doit contenir au moins 3 caractères."
                isValid = false
            }

            if (!registrationForm.value.password) {
                errorMessage.value.password = "Veuillez entrer votre mot de passe."
                isValid = false
            }

            return isValid
        }

        const handleLogin = async () => {
            // 1. On lance la validation locale
            if (!validateForm()) return

            try {
                // 2. Si c'est valide, on tente la connexion (Correction de l'envoi de l'email ici)
                await authStore.login({
                email: registrationForm.value.email,
                username: registrationForm.value.username,
                password: registrationForm.value.password
                })
                router.push('/dashboard/profile') 
            } catch (error) {
                console.log('[Login] Erreur capturée', error)
            }
        }

        return{
            useRouter,
            authStore,
            registrationForm,
            errorMessage,
            step,
            stepItems,
            validateForm,
            handleLogin
        }

    }
}
</script>

<style scoped>
.err-message-wrapper {
  padding: 10px;
  border-radius: 10px;
  width: 100%;
  background-color: var(--glass-bg);
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 15px; /* Petit espace visuel */
}

.err-message-wrapper svg {
  color: #eb4d5d;
  flex-shrink: 0;
}

.error-message {
  color: #eb4d5d;
  font-size: 0.9em;
  font-weight: 600;
}
</style>