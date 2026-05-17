<template>

    <button class="main-button">
        {{ label }}
        
        <span>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25" />
            </svg>
        </span>

    </button>

</template>

<script lang="ts">
export default {
    name:'mainButton',
    props:{
        label:{
            type:String,
            default:'Acheter vos billets'
        }
    }
}
</script>

<style scoped>

.main-button{
    background-color: var(--primary-color);
    color: var(--background-color);
    transition: all 0.2s ease-in-out;
}

.main-button:hover{
    background-color: #f8ff23;
    color: var(--background-color);
    transition: all 0.3s ease-in-out;
}

</style>