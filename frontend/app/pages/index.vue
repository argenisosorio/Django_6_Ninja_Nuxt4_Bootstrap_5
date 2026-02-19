<template>
  <div>
    <h1>
      <img
        src="/images/star.png"
        alt="star"
        class="img-fluid mb-3"
        width="50px"
      >
      Django 6 + Django REST Framework + Nuxt 4 + Bootstrap 5
    </h1>
    <p>
      Example project showcasing API consumption from Django 6 + Django REST
      Framework using Nuxt 4 + Bootstrap 5. Built as a reference implementation
      for developers building full-stack JavaScript/Python applications with
      decoupled architecture.
    </p>

    <br>

    <!-- Button trigger modal -->
    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
      Test Bootstrap Modal
    </button>

    <!-- Modal -->
    <div id="exampleModal" class="modal fade" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 id="exampleModalLabel" class="modal-title">Modal title</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"/>
          </div>
          <div class="modal-body">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary">Save changes</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
useHead({
  title: 'Home'
})

const loader = useState('loader')

onMounted(() => {
  console.log("Activo el loader")
  loader.value = true

  setTimeout(() => {
    loader.value = false
    console.log("Han pasado 3 segundos y quité el loader")
  }, 3000)
})
</script>
