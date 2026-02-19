<template>
  <div>
    <GoBack /> |
    <NuxtLink to="/users/create">
      <button>Create person</button>
    </NuxtLink>

    <h1>Users List</h1>

    <div v-if="error" class="alert alert-danger">
      Error al cargar usuarios. Inténtalo de nuevo.
    </div>

    <table v-else>
      <thead>
        <tr>
          <th>Name</th>
          <th>Email</th>
          <th>Age</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users_list" :key="user.id">
          <td>{{ user.name }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.age }}</td>
          <td>
            <NuxtLink :to="`/users/${user.id}`">Detail</NuxtLink> |
            <NuxtLink :to="`/users/update/${user.id}`">Update</NuxtLink> |
            <button @click="deleteUser(user.id, user.name)">
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
// Inicializa el acceso a la variable de entorno para la URL base del backend.
const config = useRuntimeConfig()
// Ahora 'apiBase' contiene la URL base de la API configurada en el .env
const apiBase = config.public.apiBase

// 1. Estado global para controlar el loader
const loader = useState('loader')

// 2. Configuramos el título de la página
useHead({
  title: 'Users',
})

// Simularemos una llamada a la API de Backend usando una API de prueba real
// 'pending' es un booleano reactivo que cambia automáticamente
const { data: response, pending, error, refresh} = await useFetch(`${apiBase}/person/`, {
  lazy: true
})

// 3. Mapeamos los resultados (JSONPlaceholder devuelve un Array directo)
const users_list = computed(() => response.value || [])

// Función para eliminar una persona
const deleteUser = async (id, name) => {
  // 1. Confirmación de seguridad
  if (!confirm(`¿Estás seguro de que deseas eliminar a ${name}?`)) return

  try {
    loader.value = true // Activamos el spinner
    // 2. Petición DELETE a Django
    await $fetch(`${apiBase}/person/${id}`, {
      method: 'DELETE'
    })

    // 3. Refrescar la lista automáticamente sin recargar la página
    await refresh()

  } catch (err) {
    console.error('Error al eliminar:', err)
    alert('No se pudo eliminar al usuario')
    loader.value = false // Apagamos el spinner
  } finally {
    loader.value = false // Apagamos el spinner
  }
}

// 4. Observamos 'pending' y asignamos su valor directamente al loader
watch(pending, (newVal) => {
  loader.value = newVal
}, { immediate: true }) // immediate asegura que si empieza cargando, el loader se active de una vez
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse; /* Crucial para que las líneas se unan */
}

table, th, td {
  border: 1px solid black; /* Define el grosor, estilo y color de la rejilla */
}

th, td {
  padding: 8px; /* Espaciado interno para que el texto no toque las líneas */
  text-align: left; /* Alineación del texto */
}

th {
  background-color: #f2f2f2; /* Color de fondo opcional para el encabezado */
}
</style>
