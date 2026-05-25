<template>
    <div class="main-wrapper main-dashboard">
        <navbarVue/>
    </div>
</template>

<script lang="ts">
import navbarVue from '../../components/navbar/navbar.vue'

export default {
    components:{
        navbarVue
    }
}
</script>

<style scoped>

.main-wrapper h1{
    color: var(--primary-color);
    font-size: 3rem;
    font-weight: 700;
}

</style>