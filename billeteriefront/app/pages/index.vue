<template>
    <div class="main-container">
        <div class="pic-container">
            
        </div>
        <div class="info-container w-full flex flex-2/3">
            
            <div class="general-info w-full flex flex-col gap-2">
                <h3>Gala Night of Hilarious comedy ay the club</h3>
                <div class="date-local w-full flex flex-col gap-4">
                    <span class="flex gap-2 items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5m-9-6h.008v.008H12v-.008ZM12 15h.008v.008H12V15Zm0 2.25h.008v.008H12v-.008ZM9.75 15h.008v.008H9.75V15Zm0 2.25h.008v.008H9.75v-.008ZM7.5 15h.008v.008H7.5V15Zm0 2.25h.008v.008H7.5v-.008Zm6.75-4.5h.008v.008h-.008v-.008Zm0 2.25h.008v.008h-.008V15Zm0 2.25h.008v.008h-.008v-.008Zm2.25-4.5h.008v.008H16.5v-.008Zm0 2.25h.008v.008H16.5V15Z" />
                        </svg>
                        12/12/2024
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
                <span>15,000 FCFA</span>
                <p>260 places disponibles</p>
            </div>
        </div>

        <div class="description-container">
            <p>
                Bienvenu au pays mon fils
            </p>
        </div>
    </div>
</template>

<style scoped>
.info-container{
    padding: 1rem;
    background: var(--tertiary-color, #222222);
    color: #fff;
}

.price-info{
    height: auto;
    padding: 0.5rem;
    background: var(--glass-bg);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    border-radius: 1rem;
}

.price-info span{
    font-size: 1.5rem;
    font-weight: 500;
    color: var(--primary-color);
}   
</style>