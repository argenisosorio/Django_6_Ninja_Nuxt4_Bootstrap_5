<template>
  <div>
    <h1>
      <img
        src="/images/star.png"
        alt="star"
        class="img-fluid mb-3"
        width="50px"
      >
      <!-- Mostramos el estado 'mensaje' del store de forma reactiva -->
      {{ helloStore.mensaje }}
    </h1>

    <div class="mt-4">
      <!-- Botón que dispara la función 'cambiarTexto' definida en el script -->
      <button
        class="btn btn-primary"
        @click="cambiarTexto"
      >
        Cambiar mensaje
      </button>

      <!-- Botón que dispara la función 'resetearTexto' -->
      <button
        class="btn btn-secondary ms-2"
        @click="resetearTexto"
      >
        Resetear
      </button>
    </div>
  </div>
</template>

<script setup>
// Instanciamos el store de "Hello World". Nuxt lo auto-importa desde app/stores/helloworld.js
const helloStore = useHelloWorldStore()

// Variable de estado global de Nuxt para controlar la visibilidad del componente Loader
const loader = useState('loader')

// Composable de Nuxt para configurar metadatos de la página (título de la pestaña)
useHead({
  title: 'Home'
})

// Función que utiliza una "Acción" definida dentro del store para modificar el estado
const cambiarTexto = () => {
  helloStore.actualizarMensaje('¡El estado ha cambiado globalmente!')
}

// Función que modifica el estado directamente (Pinia permite acceso directo a los refs)
const resetearTexto = () => {
  helloStore.mensaje = '¡Hola Mundo desde Pinia!'
}

// Hook que se ejecuta cuando el componente ya está cargado en el navegador (DOM)
onMounted(() => {
  console.log("Activo el loader")
  loader.value = true // Mostramos el loader al entrar

  // Simulamos un retraso de 1 segundo para ocultar el loader
  setTimeout(() => {
    loader.value = false // Ocultamos el loader
    console.log("Ha pasado 1 segundo y quité el loader")
  }, 1000)
})
</script>