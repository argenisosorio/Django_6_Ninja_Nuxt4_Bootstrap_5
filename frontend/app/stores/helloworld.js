import { defineStore } from 'pinia' // Importa la función principal de Pinia para crear almacenes.
import { ref } from 'vue'           // Importa 'ref' de Vue para crear datos reactivos.

// Definimos y exportamos el store. 'helloworld' es el ID único para este almacén.
export const useHelloWorldStore = defineStore('helloworld', () => {
  
  // --- STATE (Estado) ---
  // Definimos una variable reactiva. Equivale a los datos que guardará el store.
  const mensaje = ref('¡Hola Mundo desde Pinia!')

  // --- ACTIONS (Acciones) ---
  // Las funciones dentro del store sirven para modificar el estado (state).
  function actualizarMensaje(nuevoTexto) {
    // Al ser un 'ref', debemos usar .value para cambiar su contenido.
    mensaje.value = nuevoTexto
  }

  // --- RETORNO ---
  // Exponemos las variables y funciones para que sean accesibles desde los componentes (.vue).
  return {
    mensaje,            // Devolvemos la variable para poder mostrarla.
    actualizarMensaje   // Devolvemos la función para poder ejecutarla.
  }
})