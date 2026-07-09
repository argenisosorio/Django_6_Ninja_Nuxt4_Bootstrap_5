<template>
  <div class="container mt-4">
    <GoBack />
    <h1 class="mb-4">Register New Person</h1>

    <!-- Alerta Global de Errores -->
    <div v-if="errorList.length > 0" class="alert alert-danger shadow-sm mb-4">
      <h5 class="alert-heading">Por favor, corrige los siguientes errores:</h5>
      <ul class="mb-0">
        <li v-for="(error, index) in errorList" :key="index">
          {{ error }}
        </li>
      </ul>
    </div>

    <p>
      {{ errorList }}
    </p>

    <form novalidate @submit.prevent="savePerson">
      <!-- Campo Name -->
      <div class="mb-3">
        <label class="form-label">Name</label>
        <input
          v-model="form.name"
          type="text"
          class="form-control"
          :class="{ 'is-invalid': serverErrors.name }"
        >
        <div v-if="serverErrors.name" class="invalid-feedback">
          {{ serverErrors.name }}
        </div>
      </div>

      <!-- Campo Email -->
      <div class="mb-3">
        <label class="form-label">Email Address</label>
        <input
          v-model="form.email"
          type="email"
          class="form-control"
          :class="{ 'is-invalid': serverErrors.email }"
        >
        <div v-if="serverErrors.email" class="invalid-feedback">
          {{ serverErrors.email }}
        </div>
      </div>

      <!-- Campo Age -->
      <div class="mb-3">
        <label class="form-label">Age</label>
        <input
          v-model.number="form.age"
          type="number"
          class="form-control"
          :class="{ 'is-invalid': serverErrors.age }"
        >
        <div v-if="serverErrors.age" class="invalid-feedback">
          {{ serverErrors.age }}
        </div>
      </div>

      <!-- Botones de Acción -->
      <div class="d-flex justify-content-end gap-2">
        <NuxtLink to="/persons" class="btn btn-secondary">Cancel</NuxtLink>
        <button type="submit" class="btn btn-primary" :disabled="loader">
          {{ loader ? 'Saving...' : 'Save' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
const config = useRuntimeConfig()
const apiBase = config.public.apiBase
const loader = useState('loader')

useHead({
  title: 'Register Person',
})

// Estado del formulario
const form = ref({
  name: '',
  email: '',
  age: '',
})

// Estado para almacenar los errores clave-valor del servidor
const serverErrors = ref({})

/**
 * Computed Property para "aplanar" los errores en una lista para el alert superior.
 * Como el backend devuelve {"campo": "mensaje"}, Object.values() extrae solo los textos.
 */
const errorList = computed(() => {
  if (!serverErrors.value) return []
  return Object.values(serverErrors.value)
})

const savePerson = async () => {
  loader.value = true
  serverErrors.value = {} // Limpiamos errores previos antes de intentar

  try {
    await $fetch(`${apiBase}/person/`, {
      method: 'POST',
      body: form.value
    })

    navigateTo('/persons')

  } catch (err) {
    // Capturamos la respuesta estructurada de Django Ninja
    if (err.response && err.response._data && err.response._data.errors) {
      serverErrors.value = err.response._data.errors
    } else {
      // Error genérico si no hay respuesta estructurada (ej. caída de servidor)
      console.error('Error inesperado:', err)
      serverErrors.value = { global: 'Ocurrió un error inesperado en el servidor.' }
    }
  } finally {
    loader.value = false
  }
}
</script>