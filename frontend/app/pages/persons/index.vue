<template>
  <div>
    <GoBack /> |
    <NuxtLink to="/persons/create">
      <button>Create person</button>
    </NuxtLink>

    <h1>Person List</h1>

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
        <tr v-for="person in persons" :key="person.id">
          <td>{{ person.name }}</td>
          <td>{{ person.email }}</td>
          <td>{{ person.age }}</td>
          <td>
            <NuxtLink :to="`/persons/${person.id}`">Detail</NuxtLink> |
            <NuxtLink :to="`/persons/update/${person.id}`">Update</NuxtLink> |
            <button @click="deletePerson(person.id, person.name)">
              Delete
            </button>
            <button class="btn-pdf" @click="pdfPerson(person.name, person.email, person.age)">Exportar pdf</button>
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
  title: 'Person List',
})

// Simularemos una llamada a la API de Backend usando una API de prueba real
// 'pending' es un booleano reactivo que cambia automáticamente
const { data: response, pending, error, refresh} = await useFetch(`${apiBase}/person/`, {
  lazy: true
})

// 3. Mapeamos los resultados (JSONPlaceholder devuelve un Array directo)
const persons = computed(() => response.value || [])

// Función para eliminar una persona
const deletePerson = async (id, name) => {
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

const pdfMake = usePDFMake();

const pdfPerson = (name, email, age) => {
  // Verificación de seguridad
  if (!pdfMake) {
    console.error("pdfMake no está cargado");
    return;
  }

const dd = {
  pageMargins: [40, 60, 40, 60], 
  header: () => {
    return {
      margin: [30, 20, 30, 0],
      columns: [
        {
          image: 'data:image/png;base64,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', 
          width: 200,
          alignment: 'left'
        },
        {
          text: '', 
          width: '*' 
        },
        {
        image: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIkAAABFCAYAAAB+DsUGAAAABHNCSVQICAgIfAhkiAAAABl0RVh0U29mdHdhcmUAZ25vbWUtc2NyZWVuc2hvdO8Dvz4AAAAmdEVYdENyZWF0aW9uIFRpbWUAbWnpIDI5IGFiciAyMDI2IDE0OjU5OjQyzz4S2AAAH6dJREFUeJztnXd4FNXXxz+z2ZZeCST0DkqT3gQCSECUIuUH0kQQpUhHrCiiFBEFLAgoLVQFQekdDEE6SJEaShISIL1tts68f0QWNjO72SA2Xr7Pw0Pm3nPv3JmcOffUG0GSJInHeAwXUP3TC3iMfz8eM8ljFIq/nUkkSSIjI5vTp6+QmJiCzWYrdExenokLF65z504aZrP1b1jlY9wP9d99w++++5l335mH1ZrPHF27tmLht+84pb969SatI4aRk2MAoFixAH6JXkCxYoF/y3of4x+QJMeO/m5nEIBdu464pI+OPmVnEIDk5Azi4m7/Zet7DDn+diaxWB23l5ycPJf0JqNZPofl8Zbzd+Kx4voYheIxkzxGofjbFdeHhfPnrzFu7BxSUjLQ67X06dOevv06MGXKIg4dOoPZbKV48SA6dmzGSy89h1rt8U8v+T+L/yyTbNx4gCNHztmvv/nmR9av38exY+ftbZcu3iD6l5Ps3HGYr+dNJDjY/59Y6n8e/9ntJiM92+E6Pv62A4Pcj927jzJu3By3fDKPIcd/lkmKik0bo1m7ds8/vYz/JP71TCLhfvxREAQaNXqSjh2bKW4tq1Zuf5hL+3+Dv10n8fTUOVxLkkRubh7e3p6K9OkFthUAvV6rSPvuuwMZNbo3AMnJ6XR6fhyXL8fb+y9dinvQZf+/xt8uSYKD/GRtp3+77JT+2NHfZW3+/j6yNj8/bzuDABQrFsiAAR0daNIz5Az3Z2CxGbGIpiJJu/shmcxIuUawiQ91XQ8bf7skqVuvuqxt9ZqdNGlaS9YuiiJnzsQ6tHl66ihbtoSMtqCEgnzGuR+WPx0clMgxpxGTsJJTt7dgFU0A6NU+1AqN5OnS/dGrfQDB+RQ2EfP6/Ri//RnblYT8Ng8V6kZP4jmmF+ralUD179ICHohJJEniypUErlyOJysrF28fT6pUKUPlyqURBBcvCGjduh5eXnoMBqO9bd3aPXR8thntIhvb20wmM91eeJPU1EyH8cOH90D1D7xEgzWLdecncTP7PDbJ4tBntOZwJHEdJ25tItS7Ot2qTcJPG+A4gSRhWraVvC/XIaVnOfbZRKwHz5D96xlUJUPxem8gmjb1/+Inch9uM4nRaGbNmh1s2hjD8ePnycrKldEEBfnRpElNeveOJLJ9Y0WG8fX1ZujQbsyatcJh7gEDJtMqoh6VK5XGYDBy6NAZLly44TBWp9Mw4KWOBad8KLgbdFRyuiVmn2f172+RZ82S9TnMIZpIzD7FgpOv0LP6DMr4VcjvMFswTF2KacUOcJUIKIGYcIec4Z/iOawb+pE97F0Gq4kN1w9xIvkqiYZUUoxZZJpzkSTwVOsI0vlQyieYWkHlaFqiOk8ElkZwJdGKgEKZxGazsWf3McaOnU1SUopL2rS0LDZvjmHz5hiefLICn30+hnr1qsnoBg3uxHeLfnbwdVgsVnbuOMzOHYedzv/SwOcJCwspbMlFwqFDZxkz+jOu/CH6q1Yty5SPXiUiIv9LTsq9RtTZ0VjFe9JDEFQEe5bGRxuMRqXDJlrJtaSRmpeAVTRhsqYSdXYkoxuswlvjS9689ZiWF8GystrI++IHCPRF3zcSBAEvtY5nS9dHAO7EZZBpzuVyZhLpphzFKWoElWVI9UieK9uA8r7FH/j9AAiuclzNZgtvTvySZcu2PPAN3nxrAOPH95W1X7x4g9YRwzCZ5FFeJTRo8ARbt82xX7/z9jzmz//Rfl2iRDBnz612GLNy5XZGvv6p/VoQBJJTdtivJUmiYoWuMqmo1Wo4f+F7fP28GHfwZULIt4pUggfhPtXpWvUd/HTyF28Vzey+Pt+ur/h4NmCYuS85fT906xkLQvDS47//a4RAX8V+URJZdGEXQ3750qnq7CGoeK9uL8bX6YK3Wv9A63C6uYuiRO9e7/4pBgGY+UmUbNsAqFKlLFu2ziZIwdopiB492rDuxxkObcWKOe75ShZPwcSkgma2wWBU3DZFUSQvz8T3N7aQbU68t47qU+hX83NFBgFQq7REVnidgbW/JSHPg+y8o5z6Zo4irTuQDEbyvl7ntP9SZiKvx8x3aVvZJJEPjq+k/IpX2H3z9AOtw+l2M+jlKezff+KBJr0fkgQ+PnIfiCBA7dqViT6wkB++38XKldsd/BheXnraPtOQAQM60rx5bTw8HHWFHj3bcvFSHLFX4gkM9GPw4M6yezRu9CSvvvYCJ05cQKfV0KVrK4d+mwvTUxRFtt46R4Agolbp6FNjFqV8n3Drmb01wSy86slz4SbK1cim0gG3hinCvHIHnmN7IxSw3gxWE+N+XYRJdM9iSzZm8vy2KUyo3ZXJ9V8s0hoUt5v53/zIu+9+g6tqCy8vPeXKheHt7UlOTh6xsQmYzRYZ3QvdIliw4G23FpOWlkVqaiY6nYaSJUPx8PhrrZisrFwqlO8ia1erPThxMooOv71JU88EXqs+mtrFO7g97y1DOmFRAwDoHKpm8YQ/F4H22z4bj4olFftMNguHbl9k983fiLl9nsN3LpFrMSrSAqgEgTdqd2NygxfRqtyzW2RUKSkZfPzxYqcM4u/vw9Ch3Rg56n9otRp7u9Fo4q23vmb9j/vs6YalShdn2rThhS4i3+tqxGa14ePjiSAIZGXl4Ovr7XaI32YTMRiMmExmbDYRlUpAr9fZ53sQ3DFlIwTWLhKDANzKy7D/vCnZSlqYH0FJ8m3NXUgunIA6Dw0tw2vQMrwGAGbRyoxT61h4fjs3c1MRC/weRUli+qm1+Gm9mFjnBVRC4R+iTJLMnLmcGdOXKhLXqFGRn37+VHH/v4uUlAymT1uCJMEHk4fg6+vlcgEHD57mg/cXcvHSDawWG5IkAgIeHiq0Wg3DR/Tg9dd7otE45/p589Yx7+u1ZGbmYrPZ/mBwAbXag6AgP0aO+h/9+j1rZ7hr124y8Y0vsYki+/fJt1RBEGjfoSk/P38KTZKeNjEVeP/9wTzxZAWXz3IXa68epMfO6fbrbYfK0jD6lltjleC74gPUjZ4s0hizzcqOhJN03zkdk00u4QUElkSMpn+ViELncmASg8HIE9V7KuadlioVytZtcx6aCXrhwnVGDJ/J6dNXEEXXbumSJUOZOm0YHTs2c2g/fvw8Lw+cws2byYXeLzjYn9dee4FXX3uBuk/1IyUlo9AxljmeZKtU+H9sQJeiIjp6AZWrlJHRZWUZ8PO79zF02vYRG2/cS/BefrYcz25Nsl9LQK4k4CO45873/eFj1E9VcYu2IFKN2Uw9+QOzz/wkkyp+Wi8OdZlJ9cDSLudwkDWXL8c7TUz+5JPXHxqDbNkcQ6uWr3Hq1KVCGQTg5s07DBs6g317j9vbbtxIotPz49xiEIDU1EyWLNmEwWB0yL53BSFdQlJD9lBPLIKN2NibMpqTJ6+wdu1+jH8kbMfnpLA1/rgDjVFwfMYTosA2CbcjPoIbFqAzBOt9mdXkZRZHjMZf6yjVs8wGXo9ZUOgcDjI8Pl65VEEQoEFDubjbufMICxesJz7+tqIOo9NpqV2nCqNG9aLiH4pXTMxpXnppMqJYtKBYbm4e/ft/wKnfVhAU5MeG9fsxmeRi1BXKlgvDZhPdYkwA81kRintgCxUwttFgNMt9OmXLhmKziTzdfCSvDe3MxeJJ2Ew2uKeu4WkTyASSJIHlNoFkYJpadMsfKnjpUYUFu7VeV+hfOYJQvT/dd0wn13pPsd2beJpjyZepX6yy07EOTJJ8J12RqFixIAIVHDqjR3/G7VupLhd37txVTp64SPSBfI4dO/bzIjPIXRgMRlat3M7wET2IiflNkUalEggvGcrtW6my0ovRo3vj4aFCpfIACjcdtUet5LXJ/20bOmvJrCofExTkR1CQHzEHvySi1RgSEpIppfLCUlzEHC4i5MGMG+lkmPP1oX4eEh95uB/11b/eA+E+A+HPoH3pumzs8B6tN94rhhMlie47ZhD74gI8nCixDq2GPJMiUanSoYrtaQWCb86QnJzPfIsXbST2buSz4EJUKl7sE8mKFR8yY8YIihdX/nrmzFmDJEmKeSY1alQkMWkrp04tJzFpC7+fX8OaNVNp374JCxa8TevW9fHz9SY01L3qP3WciPr6vV/o0HPzWRX3iyKtVqum7WdNuNPHSF5VG5pUAZ/jarx/V+OVZ2Wwh8h6jY0xRWAQQa9F162VrH327NV0fHY03bu9yZUr8fKBLtAy7EnerdvToS3RkEaSIc3pGAdJ4iyZ52aC8r6v0ajdKpQymy1IkkRUlLL31t/fh3nzJvJMu8bctVabNa9N82avyGjT0jJJSckgQEGyXb4cz3vvfUPLlnWpWrUsZcuUoE3bBrRp28BOo9Vp2Lf/G3bvPorFYmXY0BmyeTw8VMyaNRqdTsMpTRxTLT8DkGczM+TYPHKsRgZXeMYhgGaVbCy8vB1jORFjufyPTbBCCZ0fW6Yrf3yFQd2kBkKA/Dm/mbfOrniPGD6Tbdvnuj2nSlAxuX4fVsdGcyUzX5m2iFaWX97Hm3W6K4+5/yLESTb57dupZGbKA0l1FYJ3ziCKIrdvK3Nrnz7taRd5j0EgX59xBrPZQt2nqsraTSYzCxdsoG+fSTSoP4DKlbsxauQsYmJ+I+8+Kenn503Xrq1o376J4vyCINC6TQN69GzLpM79qOIbbu/LseYx7Ph85lzahPEP01KUJEYeWECSwXG7ltTQ2ODcXeAKgo8n3jOGg0quudzvtExMdE9xvx8qQWBaw/4O/qPPftuATVKWcg6SJCzcufVy4fx1GjWu4dC2YcNMrl1LJDExPzqck51Lnz6TFMeLYn6aohJWr9nJxk3R92htotOIs0olEBjoR7vIRg7pBkrIzMxhxYptrFixjbJlw9i0+bMiW2g6lYY9raZQcfNrmP6IBFslG2NOfcemxKP83PwdrmbdYt7vWxXHRxxxnV7g9L69nvlTVk1h6F6hGXWCy3My5SoAycYs4nNSKOcrVy0cJEnVqmWdeifHjPlc0e1evnw4zZrVolmzWooW0P1wFitJS80kPu62/d/Nm8lOldv+/Tvi5aXnqaeq8eqrXV3e737cuJFE1y4T3Ka/H+GeQQyvJPe67r5zmprbR9Fpx0dOx9bKVs7ddQWPmhXxHNuryOOKiu7lHf1OlzMTFekcmMTf34devZ5RJLx0KY6xYx7cMhEEHNz4D4LGjWsw6f3BQL5Eef+DV5j4Zn+8vNwLgV+5ksD8+euLfF8BgZm1X6JVsRqyvqu5t7gmJINO/nGV1PpT/UoR3fEaNd7ThsIf70qSJA4ePM0P3+/ixPELhQ4XRZG9e44x+YOFjBgxkwkT5rJs2RYyM+XreL5cQ4fr23nKDkaZr3vCG/1Yu3aPokK6evVO0tKymT5jOGXKyPNMXUEQVHh7eyrqNq1a1aVlq3pOx6pUKqpUKcMzzzg+lFarYcKEfvTs2Zb536wnOvokV64kuFSmo5ZtYciQLgiCgEphv4f8X4ytwOkHKkHF0kajeHrPW8QZCmyFAuAl5OsPRtHuJXvjd380piIck6FS4T13LB7VygJw5Mg5hg39hOvX879wQRDo0aON0+c7f/4ao0Z+xokTcmaaPm0pX339BhER995zjcAyhHkF2nWpDCcJTDImKV26OE8/XYc9e44pDtix4xC7dh3mf73a0bt3O8LCQkhNyeDM2VgWL9ro9Pk9PFSULh2qqGilp2fTr18HAhQ0+bw8Exnp2Xh66WTtUz9eTFzcLUa83pP3PxiMTqdFFCUOHz7LksWbWL9+n8xxlpmVg80molZ74OWpRxAEmSPQZhPZuCmaLl1aoVZ74OfnjV6vpYxXMVY3mUDrfe/alVYH6AGNCrJFvCQ1Hfc5NytlUAnoB3ZE+0y+JXYw5jSdOo1zIJEkie+/36U4PDY2gch2Ix1yh+/HnTtpDOj/PtEHvrUnkguCQGTpuiy5uBvIDw4qQTFVwGy20LjRy8TFFR6UEgTXaZuQb01cvbaBX345yQtd31Ck8fH1onu31jz3fHPUag8SE1PYuuUgMTG/kZ1twM/Pm+gDCwgNDQJg9uer+OijRUC+pAkPD2Hyh0Po3LklAAkJd2jUcKAs8y08vBgnT0XZ81MaNhjI1avKvhuNRo2Hh4rQ0EB+iV6Aj0++W3v3ndO02/++LBZihwStcorz4/Q0t33vmsjG+Hw5FgQBo9FM7VovypLAlRAeHsLpM6vo2mUC0dGnHPqUPoA2bRqw5vup9utZpzcw/tf897igxXBeqR4pu4eii02r1bBo8Xsuo7134c4Bn3fnadHiKZoqlE4A5GQbWLJkE927vUmXzhMYNnQGGzdGk5aWhcViJTU1ky6dJ2CxWImNTXCwbERRJCHhDoNe/ojy5TpTpXI36tfrr5gaWa58mEMCU+fOTztdt8VixWg0Exd3mzOn75V2lNQGoTK4cKoLEO17hwlD/DF6F66HaSLq4f3pCO76AJYs3ujAIH7+Prz11kuMG9dHsVLgVlIqBw+esV+rVAKrVn1EYtIWTpyIQqe7t4aCH35FvzD7z8U8lV0gTpMJ6tSpwtKl7xMY+OfMMJVKxZAh96yQD6e86raiWRA3btwiPT2bnTuOOPg97kd2toG0tCyHI7fuQhAERo10tBpe7NPereSmuy/XaDPTf8/nWI1WyHP+hdiQ+K5sCi8O03K1ordTOnW9anh/Mtwh8+xogYK0r76cwLjxfXjr7Zf4et5E2Ry//HLSoRj+iScqkJySzg8/7GLL1oMOVmVB69Vbfe++fjrltA6Xb6f503XYu+9rKlYs9UCJO15eet6bNIihw7rZ2+rUqcK8eROdenddQaXKVzZr16ksK7xyBy1b1nXwvkK+CT9w4POFJjeF/JFTu/Lyfo4m/1FxaJTy/7nAvsAM2r9i5khdX6QC71BVKhSf+W/IEp0L6hUVK5Wy/9yp09Mypk5NdbRKzp6NZeTrsxj5+iyHQwxVKoGmzRwludbjD7VUIxCgU36nheavlSpVnF8PLeLbb3/i/Unz3T6vrGzZEvy8cRYlS8qdMx2fa87xE1G0aDGE1BT34j+Qb3mFhAQQEhLA8RNRvDpkqlMFuyDaRTZm2bLJin3TZ4ygRYunGDJkqj3kfz/0ei21albCbLMy8XCBhKy70kTv/CNKEQ106J7Ha52f4KMPryDYRFSli+O/ay4oSLGgIEex/9NPvzBhQl8kCYYP+0TmbypV2jExu1SpUFpFyK3FDu2bOBTA3Q/BS0WtwHLKfUU5Njw9PZuzZ2PZvDmGXw+e5vr1JAwGIz4+noSHh1CjZiVat65P3brVqFSxFIITE/MuzGYLv526zA9rd7Nj+yESEu449Ht7e1KrViUi2zchMrIxlSs7JsdIkkR8/G0OHz7Hzh2HOX36Mrdvp6HTaykWEsCTNSryTNuGPFW3KrGxCcyduwZJggnj+9KyVV3ZenJy8rgam8ClS3HEJ9wmO9tAcHAAERH1qF69HKMOLuSLs5uUH8ZTcMkod1Erx5slN2pTZ8xQxbgMwObNMQzo/4H9WhAEypcPR5Ikrl1zdHiFh4dw5OhSqlfrQXZ2fp6MTqfl01kj6dUrEpCIjb1J1LItNG5Skw4dHEMRuxJ+45kdk2hRpgb7236suJ4iMclfjdzcPAwGEx4qAa1Oq5hl/yA4ePA0/+v5tl2PEQSBLVtn06CBe9nvANmWPMqvHEyq0Xm+aangEG6TiUV0fVhOoNaH957oyZgqnRT7RVGkz4uT2LnTeaHaXdy1bsaOnc2ypZsd+vR6LYIg2J/bz8+bo8eWOhzL8VPcYbr+Oo2DbWfQOFgeD4N/2fkk3t6eFCsWQFCw/0NjEJtNZPy4OQ6KriRJfDIjymU1wP2QkBgVs9AlgwB8UX8IX9Z91UEZVEK6OYexpxbRYu/bXMyWZ7upVCo+nz2Gan841e6HIODgBNTr8+81adJgatas6EBrNJodnjsrK5dTpy7Zr0VJYkPSYbzUeir7hOMM/yom+Stw8+Ydewnn/di79xgxMe4VK2WaDay7dtAljUalJiK8FkMqtGN7iw/cKleITv6daluHM+fyRqySo/QpUSKYffvnM/iVLnh769HpNPj7+xAV9SENGjyBVqtBr9cyblx+DU1AgA/btn/Bi30i0ek0dlP5rmdZo1HTtm1D2rS5p7gvv7GPJTf20DigMsE65a0P/mXbzcOGKIo0aTyI2FhlZ1lk+yasWFF4CWbU5b303/O5S5rZTQczqua97SPekELLve9wLbdwt7yAQDW/kqxqPJ7aAeVk/XkGE0ajCU8vPXq9FovFSlZWLhqNWmblSRJkZGSRlpaFyWRBEAQ0Gg98fb0JCQmwW0YHUs7T/pfJSKLEnS5LXZaAPtJMcuzYedpHjnTar9Vq2L3na6pXL+dynpf2zmbpJefnrRX3DCCx31JUBUzcbGseI04sYNn1vW6tVyWo6FGqKR/V7EMln7DCBzwgjqfHErn/A1LN2bxWPpJ5DYa6pP/PHtFZGCRJYtanrvNNzGYLb731FevXf+LUDxQTc5piOzzwvyph9BexVFEh+gp4pEpoLtpQZUmULOvF7rCjRETUs/tbJEni6rkEGh0ryaWbpThcKR7J27X1I0oia+IPsCHhMHXiS5K3NQ3jDQNhYcG0aFmXDh2a0rhxDcW17t51lJMnL2I2W6hcpQzt2zdBr9cSE/MbG9bvIzPLQPnyYZRpWIpB2fMRJYmGQZX5ov6rhb7LR1aSHD50lo4dxxRKp9drOXduDf4B8hBEUlIqNWs4emgtVT0wtFHj/40JCqTHRETUJ2p5vi/m7be+Iipqq105lrwFMiboEUNVLg9CcoAI+n0WPLdZUOXk12DUr1+dlaumOPhS9u09TvfubzoMHTXqf1y7nsTPPxXIyRUg821PPMroONJ2JrUUtreCeGSZZNDLU/ip4AtygpYt68pOLQCIitrKmNGfObRJOgFECcFJNUf//s9y504627b9Ku/0AFN9Nbn9dEhFKA8WzOCRIOL9owl1rEhQkB+bN8+mcpV8v9H7kxbw1Vc/OIxRqz0UQxMAxjYa1s79mPYlnnLr/o+kdXPx4g3FX1LTprWoolCBt3//Ca5clmedmxXqbASTcwYBWL58qzKDANhAd9hK6McWeoc5DywWhKQFawUVmeM8Sf/Yixv/M9P1u8lEJ57DKtkwGuVxLGcMAjCkTUfaFa/j9v0fSSb58MNvZYVbggDjxvVhztxxigG9+QuKnrGmBHcy96xJZp4+V47o1tNooKtYhFI+EIMEzLU8OFcvhRYH3kG3tjvfXVPOMVFCQKAvMwcPlSnZrvDIMUlubh4HouWFW82b16Flq7rUrl2Z8JLFZP2LF23kqkIZpxJUKhXlK5QkJDTAKY1Op6Vq1bKULq184M2O7YdpHlKdmj8F4PeFEXWCCA9wqrkoScoJUIDoL5DXQUtudy3ayp6UrxDOe+8OKvKRHo8ckwwe9JFiVv6wYfk1JVqthrlzxyuOXbhwg1v36NS5BYcPL+LM6VWKZ8IBRC2fzIGYhRw9tpSI1vKTFO9WS545E4vmvA3/qXkEvp2H5vzDOf9e0gpkTPLE0EmDKtKHvTvncejw4gc6mPCRYpK4uFvs3n1UsW/ixC9p1HAgjRoOZPy4OYpm5OrVO9zKBvv889GoVCo0GjUdn2su6/fz8yYioh6CkH/8xXMKNBaLxX4aNgASqLJE/OYamSe8xPdNJtAxrL5b54cowVZaRUhgAN/UG8rtTkup6lsSjwc82vSR8pN8u/AnpzqBO6mY2dkGpn68mFmfjXZKo1IJ+Pre83J66uVxGi8vvQMTKuXu3lUslf46aeWgkrQp3YAepZuRas7maNpljqReZurSKGwhKsRAAdFHABcWUq3AcmzrOAevQuJI7uCRkSRxcbeYN8/5IXTuYvPmGMX6ImdQ0v8KSiklqXXX8aDXy9Mbf//9mv3nYK0v7UvUpRsN8PnOhP+MPALfNBA8IpfA8QbWFRvLwHJtZHMEaL0fCoPAI8Qky5ZucTuq6wopKRlMm6Z80tNfgZAQefH6lA+/Y+fOI4iiiChKpKRkMOSVqTI6rUlFl5ZP46UuepZfUfBIbDdZWbl8991PsvawsBCnxWZ3sWzZFpkesmD+jwwf3sPJiIeLXr3bcebMFYc2URTp22cSpUqFotGquZlwRzGnt1q1ck5rhx4mHgkmmflJlD0r636MH9+3UG3+yScrMniwY5mmyWRhw4Z9ilvJw8agQZ1YvWqHjFFsNhs3biQ5GZWvG018s/9fvbz8e/0td/mLsX37IVlbpUql6T/g2ULHtm5TXzHBafq0JS69lna4wUnKekv+/2q1BzM/Hamo3LrC4MFd6NChqYt7PjwOfySYxKrwt/WGvNrVrRfl5+fNO+8OkrWbzRa8vOTMoy5w6LBewbopWPOsVBmg1qi5G+mrX786636c7lY2niAI9O7djqnThrlcw8PK7INHhEmWLJnkcHpRWFgIL/Zu5/b4QYM6OdQ2e3np2bHzK3r0aCM7arxp89oO1x07NpUdH9qqQJJ1/XrV8fN3TA56/rnmDhKmdu0qnDy5nL59OzjVM0qUCGbb9rnMnuNY/vna0G6ydfbs2VZxjgfBIxMFzsrK5WDMaeLibvF8p6eLfA7JxQs32L3nKGXKlCAiop79paenZ3P06O+YTGYC/H1o2KiGQ0Uc5P9l0cNHzmExWwgtHkT9+k/IftG5uUYuXryO2WwhJCSASpWcH4t582Yy587FEh93B5PZQvHigVSoUIoaNSo4Pc82OTmD+PjbmM0WwsKCKVOmxEPbch4ZJnmMvw6PxHbzGH8tHjPJYxSK/wPZzkv9KZjbiQAAAABJRU5ErkJggg==', 
          width: 60,
          alignment: 'right'
        },
      ]
    };
  },

  content: [
    {
      stack: [
        { text: 'Sistema Nacional Informático de Donación Trasplante (SINIDOT)' },
      ],
      alignment: 'center',
      margin: [20, 0, 20, 20],
      fontSize: 14, 
      bold: true,
    },
    { text: `Profile from: ${name}`, style: 'header' },
    
    // Usamos un array para mezclar negrita y normal
    { 
      text: [
        { text: 'Email: ', bold: true }, 
        { text: email }
      ], 
      margin: [0, 7] 
    },
    { 
      text: [
        { text: 'Estado: ', bold: true }, 
        { text: 'Mérida' }
      ], 
      margin: [0, 7] 
    },
    { 
      text: [
        { text: 'Municipio: ', bold: true }, 
        { text: 'Libertador' }
      ], 
      margin: [0, 7] 
    },
    { 
      text: [
        { text: 'Parroquia: ', bold: true }, 
        { text: 'Milla' }
      ], 
      margin: [0, 7] 
    },
    { 
      text: [
        { text: 'Tipo de donante: ', bold: true }, 
        { text: 'Donante' }
      ], 
      margin: [0, 7] 
    },
    { 
      text: [
        { text: 'Age: ', bold: true }, 
        { text: age }
      ], 
      margin: [0, 7] 
    },
  ],
  styles: {
    header: { 
      fontSize: 26, 
      bold: true, 
      color: '#2C2C2C', 
      margin: [0, 0, 0, 10] // Añadimos margen inferior al título
    }
  }
};

  pdfMake.createPdf(dd).download('pdf_prueba.pdf');
};

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

.btn-pdf{
  margin-left: 6px;
}
</style>
