<template>
    <header class="top-header">
        <div class="mobile-header-top">
            <h3>Tableau de bord</h3>
        </div>

        <div class="header-actions">
          <BaseResearchInput/>
          <addButton/>
        </div>
    </header>
</template>

<script>
import BaseResearchInput from '../input/BaseResearchInput.vue'
import mainButton from '../buttons/mainButton.vue'
import addButton from '../buttons/addButton.vue'
import { useRouter } from 'vue-router';
export default {
    components:{
        BaseResearchInput,
        mainButton,
        addButton
    },
    setup() {
        const router = useRouter();

        return {router};
    }

}
</script>

<style scoped>
/* Header (Mobile) */
.top-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  width: 100%;
}

.mobile-header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.top-header h3 {
  font-size: 1.5rem;
  font-weight: 500;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
</style>