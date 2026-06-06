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
export default {
    components:{
        BaseResearchInput,
        mainButton,
        addButton
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
  gap: 0.5rem;
}

.search-bar {
  display: flex;
  align-items: center;
  background-color: var(--tertiary-color);
  border: 1px solid var(--secondary-light-color);
  border-radius: 8px;
  padding: 0.5rem;
  flex: 1;
  min-width: 200px;
}

.search-bar input {
  background: none;
  border: none;
  color: var(--my-white);
  outline: none;
  margin-left: 0.5rem;
  width: 100%;
}

.btn-primary {
  background-color: var(--primary-color);
  color: var(--background-color);
  border: none;
  border-radius: 8px;
  padding: 0.6rem 1rem;
  font-weight: 600;
  cursor: pointer;
  flex-shrink: 0;
}
</style>