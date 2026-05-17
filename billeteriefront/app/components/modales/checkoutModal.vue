<template>
  <div 
    class="modal-overlay" 
    @click="closeModal"
    :class="{ 'closing': isClosing }"
    v-if="isOpen"
  >
    <div 
      class="modal-content" 
      @click.stop
      :class="{ 'closing': isClosing }"
    >
      <div class="modal-header">
        <div class="drag-handle"></div>
        <div class="modal-title">
          <h2>{{ title }}</h2>
        </div>
        <button class="close-icon" @click="closeModal">×</button>
      </div>

      <div class="modal-body">
        <checkoutForm/>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { ref } from 'vue'
import checkoutForm from '../forms/checkoutForm.vue';

export default {
  name: 'SimpleModal',
  props: {
    isOpen: {
      type: Boolean,
      default: false
    },
    title:{
      type:  String,
      default: 'Acheter mes tickets'
    }
  },
  components: {
    checkoutForm
  },
  emits: ['close'],
  setup(props, { emit }) {
    const isClosing = ref(false)

    const closeModal = () => {
      isClosing.value = true
      setTimeout(() => {
        emit('close')
        isClosing.value = false
      }, 300)
    }

    return {
      closeModal,
      isClosing
    }
  }
}
</script>

<style scoped>
/* Overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  animation: fadeIn 0.3s ease;
}

.modal-overlay.closing {
  animation: fadeOut 0.3s ease;
}

/* Contenu de la modale */
.modal-content {
  background: var(--background-color);
  width: 100%;
  height: 85vh;
  border-top-left-radius: 1.5rem;
  border-top-right-radius: 1.5rem;
  display: flex;
  flex-direction: column;
  animation: slideUp 0.3s ease;
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.15);
}

.modal-content.closing {
  animation: slideDown 0.3s ease;
}

/* Header */
.modal-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
}

.drag-handle {
  width: 40px;
  height: 4px;
  background: #e0e0e0;
  border-radius: 2px;
  position: absolute;
  top: 8px;
  left: 50%;
  transform: translateX(-50%);
}

.modal-title h2 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--primary-color);
}

.close-icon {
  background: none;
  border: none;
  font-size: 1.8rem;
  cursor: pointer;
  color: var(--primary-color);
  padding: 0;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.2s ease;
}

.close-icon:hover {
  background: var(--glass-bg);
}

/* Corps */
.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  color: var(--my-white);
}

/* Animations */
@keyframes slideUp {
  from {
    transform: translateY(100%);
  }
  to {
    transform: translateY(0);
  }
}

@keyframes slideDown {
  from {
    transform: translateY(0);
  }
  to {
    transform: translateY(100%);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes fadeOut {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}

/* Responsive : sur desktop, modale centrée */
@media (min-width: 768px) {
  .modal-overlay {
    align-items: center;
    justify-content: center;
  }

  .modal-content {
    width: 90%;
    max-width: 500px;
    height: auto;
    max-height: 80vh;
    border-radius: 1rem;
    animation: scaleUp 0.3s ease;
  }

  .modal-content.closing {
    animation: scaleDown 0.3s ease;
  }

  @keyframes scaleUp {
    from {
      transform: scale(0.9) translateY(20px);
      opacity: 0;
    }
    to {
      transform: scale(1) translateY(0);
      opacity: 1;
    }
  }

  @keyframes scaleDown {
    from {
      transform: scale(1) translateY(0);
      opacity: 1;
    }
    to {
      transform: scale(0.9) translateY(20px);
      opacity: 0;
    }
  }
}
</style>