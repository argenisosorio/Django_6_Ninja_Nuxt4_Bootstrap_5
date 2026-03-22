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

    <form novalidate @submit.prevent="savePerson">
      <div class="mb-3">
        <label class="form-label">Name</label>
        <input
          v-model="form.name"
          type="text"
          class="form-control"
          :class="{ 'is-invalid': serverErrors.name }"
        >
      </div>

      <div class="mb-3">
        <label class="form-label">Email Address</label>
        <input
          v-model="form.email"
          type="email"
          class="form-control"
          :class="{ 'is-invalid': serverErrors.email }"
        >
      </div>

      <div class="mb-3">
        <label class="form-label">Age</label>
        <input
          v-model.number="form.age"
          type="number"
          class="form-control"
          :class="{ 'is-invalid': serverErrors.age }"
        >
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

// Estado para almacenar los errores crudos del servidor
const serverErrors = ref({})

/**
 * Computed Property para "aplanar" los errores.
 * Transforma el objeto { email: [{message: '...'}], name: [...] }
 * en una lista simple de strings: ['Error en email', 'Error en name']
 */
const errorList = computed(() => {
  const messages = []
  if (serverErrors.value) {
    // Recorremos cada campo que tiene error
    Object.values(serverErrors.value).forEach(fieldErrors => {
      // Recorremos la lista de errores de ese campo específico
      fieldErrors.forEach(error => {
        messages.push(error.message)
      })
    })
  }
  return messages
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
    // Capturamos la respuesta del error 400 de Django Ninja
    if (err.response && err.response._data && err.response._data.errors) {
      serverErrors.value = err.response._data.errors
    } else {
      // Error genérico si no hay respuesta estructurada
      console.error('Error inesperado:', err)
      console.log('Ocurrió un error inesperado en el servidor.')
    }
  } finally {
    loader.value = false
  }
}
</script>