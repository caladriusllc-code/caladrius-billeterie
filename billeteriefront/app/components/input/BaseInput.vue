<template>
  <div class="input-group" :class="{ 'has-error': !!errorMessage, 'is-disabled': disabled }">
    <label v-if="label" :for="inputId" class="input-label">
      {{ label }}
      <span v-if="required" class="required-mark">*</span>
    </label>

    <div class="input-wrapper">
      <span v-if="$slots.prepend" class="input-icon input-icon-left">
        <slot name="prepend"></slot>
      </span>

      <input
        :id="inputId"
        ref="inputRef"
        class="form-input"
        :class="{ 
          'pl-icon': $slots.prepend, 
          'pr-icon': $slots.append 
        }"
        :value="modelValue"
        :disabled="disabled"
        :aria-invalid="!!errorMessage"
        :aria-describedby="errorMessage ? `${inputId}-error` : hint ? `${inputId}-hint` : undefined"
        v-bind="$attrs"
        @input="handleInput"
        @blur="$emit('blur', $event)"
      />

      <span v-if="$slots.append" class="input-icon input-icon-right">
        <slot name="append"></slot>
      </span>
    </div>

    <p v-if="errorMessage" :id="`${inputId}-error`" class="message error-message">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="msg-icon">
        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
      </svg>
      {{ errorMessage }}
    </p>

    <p v-else-if="hint" :id="`${inputId}-hint`" class="message hint-message">
      {{ hint }}
    </p>
  </div>
</template>

<script>
export default {
  name: 'BaseInput',
  inheritAttrs: false,
  props: {
    modelValue: {
      type: [String, Number],
      default: ''
    },
    label: {
      type: String,
      default: ''
    },
    errorMessage: {
      type: String,
      default: ''
    },
    hint: {
      type: String,
      default: ''
    },
    id: {
      type: String,
      default: null
    },
    disabled: {
      type: Boolean,
      default: false
    },
    required: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:modelValue', 'blur'],
  computed: {
    // Génère un ID unique si l'utilisateur n'en fournit pas
    inputId() {
      return this.id || `input-${Math.random().toString(36).substr(2, 9)}`;
    }
  },
  methods: {
    handleInput(event) {
      this.$emit('update:modelValue', event.target.value);
    }
  }
};
</script>

<style scoped>
/* Variables CSS pour faciliter la personnalisation */
.input-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 0.5rem;
  font-family: sans-serif;
}

.input-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--primary-color);
  margin-bottom: 0.5rem;
  display: block;
}

.required-mark {
  color: var(--error-color);
  margin-left: 2px;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.form-input {
  width: 100%;
  padding: 0.9rem;
  font-size: 1rem;
  line-height: 1.5;
  color: var(--text-color);
  background-color: var(--glass-border);
  background-clip: padding-box;
  border: 1px solid var(--border-color);
  border-radius: 1.5rem;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

/* Gestion du focus */
.form-input:focus {
  outline: none;
  border-color: var(--secondary-color);
  box-shadow: 0 0 0 3px var(--focus-ring);
}

/* Gestion des icônes */
.input-icon {
  position: absolute;
  top: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  color: #9ca3af;
  pointer-events: none; /* L'icône ne bloque pas le clic */
}

.input-icon-left { left: 0; }
.input-icon-right { right: 0; }

.pl-icon { padding-left: 2.5rem; }
.pr-icon { padding-right: 2.5rem; }

/* État d'erreur */
.has-error .form-input {
  border-color: var(--error-color);
}

.has-error .form-input:focus {
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.25);
}

.has-error .input-label {
  color: var(--error-color);
}

.has-error .input-icon {
  color: var(--error-color);
}

/* Messages (Erreur et Hint) */
.message {
  font-size: 0.8rem;
  margin-top: 0.375rem;
  display: flex;
  align-items: center;
  gap: 4px;
}

.error-message {
  color: var(--error-color);
}

.hint-message {
  color: #6b7280;
}

.msg-icon {
  width: 14px;
  height: 14px;
}

/* État désactivé */
.is-disabled .form-input {
  background-color: var(--bg-disabled);
  cursor: not-allowed;
  opacity: 1;
}
</style>