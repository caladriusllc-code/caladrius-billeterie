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

      <select
        :id="inputId"
        class="form-select"
        :class="{ 
          'pl-icon': $slots.prepend, 
          'pr-icon': $slots.append 
        }"
        :value="modelValue"
        :disabled="disabled"
        :aria-invalid="!!errorMessage"
        :aria-describedby="errorMessage ? `${inputId}-error` : hint ? `${inputId}-hint` : undefined"
        v-bind="$attrs"
        @change="handleChange"
      >
        <option value="" disabled selected v-if="placeholder">{{ placeholder }}</option>
        
        <slot>
          <option
            v-for="(opt, index) in options"
            :key="opt.code ?? opt.value ?? index"
            :value="opt.code ?? opt.value ?? opt.name"
          >
            {{ opt.name }}
          </option>
        </slot>
      </select>

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
  name: 'BaseSelect',
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
    placeholder: {
      type: String,
      default: 'Sélectionnez une option'
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
    },
    options:{
      type:Array,
      default:()=>[
        {name:"Abidjan"},
        {name:"Daloa"}
      ]
    }
  },
  emits: ['update:modelValue', 'blur', 'change'],
  computed: {
    inputId() {
      return this.id || `select-${Math.random().toString(36).substr(2, 9)}`;
    }
  },
  methods: {
    handleChange(event) {
      this.$emit('update:modelValue', event.target.value);
      this.$emit('change', event.target.value);
    }
  }
};
</script>

<style scoped>
/* Variables identiques à BaseInput */
.input-group {
  --primary-color: #3b82f6;
  --error-color: #ef4444;
  --text-color: #1f2937;
  --label-color: #374151;
  --border-color: #d1d5db;
  --focus-ring: rgba(59, 130, 246, 0.25);
  --bg-disabled: #f3f4f6;
  
  display: flex;
  flex-direction: column;
  margin-bottom: 0.5rem;
  font-family: sans-serif;
}

.input-label {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--label-color);
  margin-bottom: 0.4rem;
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

.form-select {
  width: 100%;
  padding: 0.625rem 0.75rem;
  font-size: 0.9rem;
  line-height: 1.5;
  color: var(--text-color);
  background-color: #fff;
  border: 1px solid var(--border-color);
  border-radius: 1.5rem;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
  appearance: none; /* Désactive le style par défaut du navigateur */
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 0.5rem center;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
}

.form-select:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px var(--focus-ring);
}

.input-icon {
  position: absolute;
  top: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  color: #9ca3af;
  pointer-events: none;
}

.input-icon-left { left: 0; }
.input-icon-right { right: 0; }

/* Padding dynamique si icône présente */
.pl-icon { padding-left: 2.5rem; }
.pr-icon { padding-right: 2.5rem; }

/* État d'erreur */
.has-error .form-select {
  border-color: var(--error-color);
}

.has-error .form-select:focus {
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.25);
}

.has-error .input-label, .has-error .input-icon {
  color: var(--error-color);
}

/* Messages */
.message {
  font-size: 0.8rem;
  margin-top: 0.375rem;
  display: flex;
  align-items: center;
  gap: 4px;
}

.error-message { color: var(--error-color); }
.hint-message { color: #6b7280; }
.msg-icon { width: 14px; height: 14px; }

/* État désactivé */
.is-disabled .form-select {
  background-color: var(--bg-disabled);
  cursor: not-allowed;
  opacity: 1;
}
</style>