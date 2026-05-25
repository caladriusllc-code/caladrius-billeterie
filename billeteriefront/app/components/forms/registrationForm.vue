<template>
    <form @submit.prevent="handleRegister" class="registration-form">

        <h3>Création de compte</h3>

        <stepper :steps="stepItems"/>

        <template v-if="step === 1">
            <BaseChoices 
                @next="nextStep"
                v-model="registrationForm.user_type" 
                :error="errorMessage.user_type"
            />
        </template>

        <template v-else-if="step === 2">
            <BaseInputVue 
                label="Prénom"
                v-model="registrationForm.first_name"
                :errorMessage="errorMessage.first_name"
                placeholder="Votre prénom"
            />

            <BaseInputVue 
                label="Nom"
                v-model="registrationForm.last_name"
                :errorMessage="errorMessage.last_name"
                placeholder="Votre nom"
            />

            <BaseInputVue 
                label="Adresse Email"
                type="email"
                v-model="registrationForm.email"
                :errorMessage="errorMessage.email"
                placeholder="exemple@email.com"
            />

            <div class="action-buttons">
                <mainButton label="Suivant" @click.prevent="nextStep" />
                <secondButton label="Précédent" @click.prevent="prevStep" />
            </div>
        </template>

        <template v-else-if="step === 3">
            <BaseInputVue 
                label="Nom d'utilisateur"
                v-model="registrationForm.username"
                :errorMessage="errorMessage.username"
                placeholder="Choisissez un pseudo"
            />

            <BaseInputVue 
                label="Numéro de téléphone"
                type="tel"
                v-model="registrationForm.phone_number"
                :errorMessage="errorMessage.phone_number"
                placeholder="+33 6 12 34 56 78"
            />

            <BaseInputVue 
                label="Mot de passe"
                v-model="registrationForm.password"
                :errorMessage="errorMessage.password"
                type="password"
            />

            <BaseInputVue 
                label="Confirmez le mot de passe"
                v-model="registrationForm.passwordConfirmation"
                :errorMessage="errorMessage.passwordConfirmation"
                type="password"
            />

            <div class="action-buttons">
                <mainButton 
                    label="S'inscrire" 
                    type="submit"
                    :isLoading="authStore.isLoading"
                />
                <secondButton label="Précédent" @click.prevent="prevStep" />
            </div>
        </template>

        <div class="err-message-wrapper" v-if="authStore.error" >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z" />
            </svg>
            <p class="error-message">
                {{ authStore.error }}
            </p>
        </div>
        <template v-if="step <= 1 ">
            <divider orientation="horizontal" :thickness="2" color="#515151" length="100%" />

            <p class="login-prompt">J'ai déjà un compte</p>

            <secondButton label="Se connecter" @click.prevent="router.push('/login')"/>
        </template>

    </form>
</template>

<script lang="ts">
import BaseInputVue from '../input/BaseInput.vue';
import mainButton from '../buttons/mainButton.vue';
import secondButton from '../buttons/secondButton.vue';
import divider from '../tools/divider.vue';
import stepper from '../tools/stepper.vue';
import BaseChoices from '../input/BaseChoices.vue';

import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../../stores/authStore';
import type { User } from '../../stores/authStore';

// Interface étendue pour couvrir tous les champs du formulaire
interface ErrorMessage {
    user_type?: string;
    first_name?: string;
    last_name?: string;
    email?: string;
    username?: string;
    phone_number?: string;
    password?: string;
    passwordConfirmation?: string;
}

export default {
    components: {
        BaseInputVue,
        mainButton,
        secondButton,
        BaseChoices,
        divider,
        stepper
    },
    setup() {
        const router = useRouter()
        const authStore = useAuthStore()

        // État du formulaire
        const registrationForm = ref<User>({
            username: '',
            password: '',
            passwordConfirmation: '', // Géré grâce au type optionnel dans authStore.ts
            email: '',
            first_name: '',
            last_name: '',
            phone_number: '',
            user_type: null
        })

        const errorMessage = ref<ErrorMessage>({})
        const step = ref(1)

        const stepItems = computed(() => [
            { id: 1, name: 'Type de compte', isActive: step.value === 1 },
            { id: 2, name: 'Informations',   isActive: step.value === 2 },
            { id: 3, name: 'Coordonnées',    isActive: step.value === 3 },
        ])

        // Méthode de validation dynamique selon l'étape en cours
        const validateCurrentStep = (): boolean => {
            // Réinitialisation des erreurs de l'étape courante
            let isValid = true

            if (step.value === 1) {
                errorMessage.value.user_type = ''
                if (!registrationForm.value.user_type) {
                    errorMessage.value.user_type = "Veuillez sélectionner un type de client."
                    isValid = false
                }
            } 
            
            else if (step.value === 2) {
                errorMessage.value.first_name = ''
                errorMessage.value.last_name = ''
                errorMessage.value.email = ''

                if (!registrationForm.value.first_name?.trim()) {
                    errorMessage.value.first_name = "Le prénom est requis."
                    isValid = false
                }
                if (!registrationForm.value.last_name?.trim()) {
                    errorMessage.value.last_name = "Le nom est requis."
                    isValid = false
                }
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
                if (!registrationForm.value.email.trim() || !emailRegex.test(registrationForm.value.email)) {
                    errorMessage.value.email = "Veuillez entrer une adresse email valide."
                    isValid = false
                }
            } 
            
            else if (step.value === 3) {
                errorMessage.value.username = ''
                errorMessage.value.phone_number = ''
                errorMessage.value.password = ''
                errorMessage.value.passwordConfirmation = ''

                if (!registrationForm.value.username.trim() || registrationForm.value.username.length < 3) {
                    errorMessage.value.username = "L'identifiant doit contenir au moins 3 caractères."
                    isValid = false
                }
                if (!registrationForm.value.phone_number.trim()) {
                    errorMessage.value.phone_number = "Le numéro de téléphone est requis."
                    isValid = false
                }
                if (!registrationForm.value.password) {
                    errorMessage.value.password = "Veuillez entrer un mot de passe."
                    isValid = false
                } else if (registrationForm.value.password.length < 6) {
                    errorMessage.value.password = "Le mot de passe doit contenir au moins 6 caractères."
                    isValid = false
                }
                if (registrationForm.value.password !== registrationForm.value.passwordConfirmation) {
                    errorMessage.value.passwordConfirmation = "Les mots de passe ne correspondent pas."
                    isValid = false
                }
            }

            return isValid
        }

        const nextStep = () => {
            if (validateCurrentStep() && step.value < 3) {
                step.value++
            }
        }

        const prevStep = () => {
            if (step.value > 1) {
                step.value--
            }
        }

        const handleRegister = async () => {
            // Ultime vérification de l'étape 3 avant envoi
            if (!validateCurrentStep()) return

            try {
                // On extrait passwordConfirmation car l'API n'en a sûrement pas besoin
                const { passwordConfirmation, ...payload } = registrationForm.value
                
                await authStore.register(payload)
                router.push('/dashboard/profile') 
            } catch (error) {
                console.log('[Register] Erreur capturée', error)
            }
        }

        return {
            router,
            authStore,
            registrationForm,
            errorMessage,
            step,
            stepItems,
            nextStep,
            prevStep,
            handleRegister
        }
    }
}
</script>

<style scoped>
.registration-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    width: 100%;
    max-width: 500px;
    margin: 0 auto;
}

.action-buttons {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    margin-top: 1.5rem;
    width: 100%;
}

.action-buttons > * {
    flex: 1;
}

.login-prompt {
    text-align: center;
    color: var(--my-white, #fff);
    margin-bottom: 0.5rem;
}

.err-message-wrapper {
  padding: 10px;
  border-radius: 10px;
  width: 100%;
  background-color: var(--glass-bg, rgba(255,255,255,0.1));
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 15px; 
}

.err-message-wrapper svg {
  color: #eb4d5d;
  flex-shrink: 0;
}

.error-message {
  color: #eb4d5d;
  font-size: 0.9em;
  font-weight: 600;
  margin: 0;
}
</style>