<template>
    <div class="main-wrapper">
        <navbar/>
        <heroSectionVue/>
        
    </div>
</template>

<script>
import navbar from '../components/navbar/navbar.vue'
import eventDetailSectionVue from '../components/sections/eventDetailSection.vue'
import heroSectionVue from '../components/sections/heroSection.vue'

export default {
    components:{
        eventDetailSectionVue,
        navbar,
        heroSectionVue
    }
}
</script>

<style>

</style>