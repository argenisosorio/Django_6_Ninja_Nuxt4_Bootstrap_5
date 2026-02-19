<template>
  <div>
    <GoBack />
    <div v-if="pending">Loading details...</div>
    
    <div v-else-if="error">
      <p>Error: User with ID: was not found {{ userId }}</p>
    </div>

    <div v-else>
      <h1>Profile from: {{ user.name }}</h1>
      <div >
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Age:</strong> {{ user.age }}</p>
        <p><strong>Created at:</strong> {{ new Date(user.created_at).toLocaleString() }}</p>
        <p><strong>Updated at:</strong> {{ new Date(user.updated_at).toLocaleString() }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
// Inicializa el acceso a la variable de entorno para la URL base del backend.
const config = useRuntimeConfig()
// Ahora 'apiBase' contiene la URL base de la API configurada en el .env
const apiBase = config.public.apiBase

// Configuramos el título de la página
useHead({
  title: 'User detail',
})

// Obtenemos el ID desde la URL
const route = useRoute()
const userId = route.params.id

// Pedimos solo los datos de ese usuario específico
const { data: user, pending, error } = await useFetch(`${apiBase}/person/${userId}`)
</script>

<style scoped>
</style>
