<template>
    <div class="main-container" ref="mainContainer">
        <div class="pic-container">
            <img src="../assets/images/Copilot_20260517_151633.png" alt="Event Banner">
            <div class="pic-title-overlay">
                <h1>Gala Night of Hilarious Comedy <span>at the Club</span></h1>
            </div>
        </div>
        
        <div class="info-container w-full flex flex-col items-center gap-2">

            <h2> Information générales de l'évènement</h2>

            <div class="general-info w-full h-full flex flex-col gap-2">
                <div class="date-local w-full flex flex-col gap-8">
                    <span class="flex gap-2 items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5m-9-6h.008v.008H12v-.008ZM12 15h.008v.008H12V15Zm0 2.25h.008v.008H12v-.008ZM9.75 15h.008v.008H9.75V15Zm0 2.25h.008v.008H9.75v-.008ZM7.5 15h.008v.008H7.5V15Zm0 2.25h.008v.008H7.5v-.008Zm6.75-4.5h.008v.008h-.008v-.008Zm0 2.25h.008v.008h-.008V15Zm0 2.25h.008v.008h-.008v-.008Zm2.25-4.5h.008v.008H16.5v-.008Zm0 2.25h.008v.008H16.5V15Z" />
                        </svg>
                        12 juin 2026
                    </span>
                    <span class="flex gap-2 items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                            <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z" />
                        </svg>
                        Abidjan, palais de la culture
                    </span>
                </div>
            </div>
            
            <div class="price-info">
                <span>15.000 FCFA</span>
                <span>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M18 18.72a9.094 9.094 0 0 0 3.741-.479 3 3 0 0 0-4.682-2.72m.94 3.198.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0 1 12 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 0 1 6 18.719m12 0a5.971 5.971 0 0 0-.941-3.197m0 0A5.995 5.995 0 0 0 12 12.75a5.995 5.995 0 0 0-5.058 2.772m0 0a3 3 0 0 0-4.681 2.72 8.986 8.986 0 0 0 3.74.477m.94-3.197a5.971 5.971 0 0 0-.94 3.197M15 6.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm6 3a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Zm-13.5 0a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Z" />
                    </svg>
                    250
                </span>
            </div>

            <div class="event-details">
                <h3>Description de l'évènement</h3>
                <p>
                    Lorem ipsum dolor, sit amet consectetur 
                    adipisicing elit. Consectetur, laborum quam, 
                    officia sapiente velit quisquam id, blanditiis 
                    omnis in ad voluptas voluptatum aspernatur 
                    soluta pariatur animi nulla. 
                    Recusandae ex sint aspernatur nam.
                </p>
            </div>

            <!-- C'est ce wrapper qu'on observe désormais -->
            <div class="btn-frame-wrapper" ref="btnWrapper">
                <div class="btn-frame flex flex-2/3 items-center justify-center gap-4" :class="{ floating: isFloating }">
                    <mainButton @click="isCheckoutModalOpen = true"/>
                    <likeButton/>
                </div>
            </div>
        </div>
        
        <checkoutModal :isOpen="isCheckoutModalOpen" @close="isCheckoutModalOpen = false"/>
    </div>
</template>

<script>
import mainButton from '../components/buttons/mainButton.vue';
import likeButton from '~/components/buttons/likeButton.vue';
import checkoutModal from '~/components/modales/checkoutModal.vue';

export default {
    components: {
        mainButton,
        likeButton,
        checkoutModal
    },
    setup() {
        const isCheckoutModalOpen = ref(false);
        const isFloating = ref(false);
        const btnWrapper = ref(null);

        onMounted(() => {
            const observer = new IntersectionObserver(([entry]) => {
                isFloating.value = !entry.isIntersecting;
            }, { threshold: 0.1 });

            if (btnWrapper.value) {
                observer.observe(btnWrapper.value);
            }
        });

        return {
            isCheckoutModalOpen,
            isFloating,
            btnWrapper
        };
    }
}
</script>

<style scoped>
.info-container {
    background: var(--background-color);
    color: #fff;
}

.price-info {
    width: 100%;
    padding: 1rem;
    background: var(--glass-bg);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
    border-radius: 1rem;
}

.price-info span{
    display: flex;
    gap: 0.5rem;
    color: #fff;
}

.date-local {
    padding: 0.5rem;
    background: var(--glass-bg);
    display: flex;
    align-items: normal;
    gap: 0.5rem;
    border-radius: 1rem;
}

.date-local span {
    font-size: 0.9rem;
    font-weight: 500;
    color: var(--secondary-light-color);
}

.date-local span svg {
    font-weight: 500;
    color: var(--primary-color);
}

.price-info span {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--primary-color);
}   

.price-info p {
    font-size: 0.9rem;
    font-weight: 400;
    color: var(--secondary-light-color);
}

.event-details {
    padding: 0.5rem;
    background: var(--glass-bg);
    border-radius: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.event-details h3 {
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--secondary-light-color);
}

.event-details p {
    font-size: 1rem;
    font-weight: 400;
    color: var(--my-white);
}

.btn-frame-wrapper {
    width: 100%;
    height: 75px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
    margin-top: 1rem;
}

.btn-frame {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.5s ease-in-out;
}

/* Mode flottant : ancré en bas, centré, avec animation de remontée */
.btn-frame.floating {
    width: 90%;
    height: 60px;
    position: fixed;
    bottom: 1rem;
    left: 50%;
    /* Centre horizontalement sans bouger de la droite */
    transform: translateX(-50%);
    border-radius: 1rem;
    z-index: 1000;
    padding: 1rem;
    
    /* Animation venant du bas */
    animation: slideUpFromBottom 0.4s ease-out;
}

/* Définition de l’animation : départ en bas, arrivée à sa position finale */
@keyframes slideUpFromBottom {
    0% {
        opacity: 0;
        transform: translateX(-50%) translateY(100%);
    }
    100% {
        opacity: 1;
        transform: translateX(-50%) translateY(0);
    }
}

@media(min-width: 1024px){

    .price-info span{
        display: flex;
        gap: 0.5rem;
        color: #fff;
    }

    .date-local {
        padding: 0.5rem;
        background: var(--glass-bg);
        display: flex;
        align-items: normal;
        gap: 0.5rem;
        border-radius: 1rem;
    }

    .date-local span {
        font-size: 1.2rem;
    }

    .date-local span svg {
        font-weight: 500;
        color: var(--primary-color);
    }

    .price-info span {
        font-size: 1.2rem;
    }   

    .price-info p {
        font-size: 1.2rem;
    }

    .event-details {
        padding: 0.5rem;
        background: var(--glass-bg);
        border-radius: 1rem;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .event-details h3 {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--secondary-light-color);
    }

    .event-details p {
        font-size: 1rem;
        font-weight: 400;
        color: var(--my-white);
    }

    .btn-frame-wrapper {
        width: 100%;
        height: 75px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-sizing: border-box;
        margin-top: 1rem;
    }

    .btn-frame {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.5s ease-in-out;
    }

    /* Mode flottant : ancré en bas, centré, avec animation de remontée */
    .btn-frame.floating {
        width: 90%;
        height: 60px;
        position: fixed;
        bottom: 1rem;
        left: 50%;
        /* Centre horizontalement sans bouger de la droite */
        transform: translateX(-50%);
        border-radius: 1rem;
        z-index: 1000;
        padding: 1rem;
        
        /* Animation venant du bas */
        animation: slideUpFromBottom 0.4s ease-out;
    }
}

</style>