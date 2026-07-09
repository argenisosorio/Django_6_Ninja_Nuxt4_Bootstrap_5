<template>
  <div class="container mt-4">
    <GoBack />
    <h1 class="mb-4">Register New Person</h1>

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
 * Extrae solo los mensajes string, manejando diccionarios limpios.
 */
const errorList = computed(() => {
  if (!serverErrors.value || Object.keys(serverErrors.value).length === 0) return []
  return Object.values(serverErrors.value)
})

const savePerson = async () => {
  loader.value = true
  serverErrors.value = {} 

  try {
    await $fetch(`${apiBase}/person/`, {
      method: 'POST',
      body: form.value
    })

    navigateTo('/persons')

  } catch (err) {
    if (err.response && err.response._data) {
      let rawData = err.response._data

      // 1. Si los datos vienen como un String (texto), los forzamos a Objeto JSON
      if (typeof rawData === 'string') {
        try {
          rawData = JSON.parse(rawData)
        } catch {
          // Si no es un JSON válido, lo dejamos como string para el catch final
        }
      }

      // 2. Ahora que estamos seguros de tener un Objeto (o un string limpio), extraemos
      if (rawData && typeof rawData === 'object') {
        
        // Caso A: El objeto tiene directamente la llave "errors" (Tu caso)
        if (rawData.errors) {
          serverErrors.value = rawData.errors
        } 
        // Caso B: Viene metido dentro de una propiedad 'detail' (Muy común en Django Ninja)
        else if (rawData.detail) {
          // Si Django Ninja metió nuestro string JSON dentro de 'detail', lo parseamos
          if (typeof rawData.detail === 'string' && rawData.detail.startsWith('{')) {
            try {
              const detailObj = JSON.parse(rawData.detail)
              serverErrors.value = detailObj.errors || detailObj
            } catch {
              serverErrors.value = { global: rawData.detail }
            }
          } else {
            serverErrors.value = { global: rawData.detail }
          }
        } 
        // Caso C: Cualquier otra estructura de objeto
        else {
          serverErrors.value = rawData
        }

      } else {
        // Si todo falla y es texto plano
        serverErrors.value = { global: rawData || 'Error en el formulario.' }
      }
    } else {
      console.error('Error inesperado:', err)
      serverErrors.value = { global: 'Ocurrió un error inesperado en el servidor.' }
    }
  } finally {
    loader.value = false
  }
}
</script>