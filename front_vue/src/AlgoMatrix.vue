<script setup>
import axios from 'axios'
import { computed, ref, defineEmits } from 'vue'
import VBtn from './components/VBtn.vue'
import VInput from './components/VInput.vue'
import TableMatrix from './components/TableMatrix.vue'
import Chart from 'primevue/chart';

const props = defineProps({
  url: {
    type: String,
    default: ""
  },
  tableData: {
    type: Array,
    default: []
  },
})
const emit = defineEmits(["back"])

const tableData = ref(props.tableData)
const info = ref("")
const hurwitz = ref("")

const stats = ref("")

const canFetch = computed(() => { 
  for (const item of tableData.value) {
    for (const subItem of item) {
      if (!subItem.replace(" ", "").length) return false
    }
  }
  return true
})

const barData = {
  labels: ['Алгоритм Лапласа', 'Критерий Гурвица', 'Оптимальный алгоритм','Алгоритм Саваджа'],
  datasets: [
    {
      label: 'Время (нс)',
      backgroundColor: '#91D5FF',
      fill: false,
      borderColor: '#91D5FF',
      data: [0, 0, 0, 0]
    },
    {
      label: 'Память (КБ)',
      backgroundColor: 'gray',
      fill: false,
      borderColor: 'gray',
      data: [0, 0, 0, 0]
    }
  ]
};

const lineData = {
  labels: [],
  datasets: [
    {
      label: props.url === "api/hurwitz" ? 'Критерий Гурвица' : "Итеративный алгоритм",
      backgroundColor: '#91D5FF',
      fill: false,
      borderColor: '#91D5FF',
      data: []
    },
    {
      label: 'Оптимальный алгоритм ',
      backgroundColor: 'red',
      fill: false,
      borderColor: 'red',
      data: []
    }
  ]
};

const fetchData = () => {
  const data = ref("")
  axios.post(
    props.url, 
    { data: tableData.value, hurwitz:  hurwitz.value},
  ).then((response) => {
    info.value = response.data.msg
    stats.value = response.data?.stats ? response.data?.stats : ""
    if (stats) {
      if (props.url === "/api/hurwitz") {
        for (let i = 0; i <= 10; i += 1){
          lineData.labels.push(`${i / 10}`)
          lineData.datasets[0].data.push(stats.value[i].win)
          lineData.datasets[1].data.push(response.data.optimal)
        }
      } else if (props.url === "/api/compare_algo"){
        barData.datasets[0].data = [
          stats.value.laplas.time, 
          stats.value.hurwitz.time, 
          stats.value.optimal.time, 
          stats.value.savage.time,
        ]
        barData.datasets[1].data = [
          stats.value.laplas.mem, 
          stats.value.hurwitz.mem, 
          stats.value.optimal.mem, 
          stats.value.savage.mem,
        ]
      }

    }
  })
}
const fillTable = () => {
  const data = [
        ['4','6','8','10'],
        ['8','12','7','9'],
        ['12','8','6','5'],
        ['5','13','8','6'],
        ['6','7','11','7']
      ]
  tableData.value = data
}
</script>

<template>
  <div class="main-container">
    <div class="container">
      <VInput v-if="props.url === '/api/hurwitz' || props.url === '/api/compare_algo'" v-model="hurwitz" holder="Критерий оптимизма"/>
      <TableMatrix :tableData="tableData"/>
      <VBtn value="Проверить" @click="fetchData" :disable="!canFetch"></VBtn>
      <VBtn value="Назад" @click="emit('back')"></VBtn>
      <VBtn value="BASE" @click="fillTable()">
      </VBtn>
    </div>
    <div v-if="info" style="min-width: 650px; display: flex; align-items: center; justify-content: center;">
      <div class="preview-message">
        <div v-for="i in info">
          {{ i }}
        </div>
      </div>
    </div>
    <div v-if="stats" class="card">
      <Chart v-if="props.url === '/api/compare_algo'" type="bar" :data="barData" :height="300" :width="500" />
      <Chart v-else-if="props.url === '/api/hurwitz'" type="line" :data="lineData" :height="300" :width="500" />
    </div>
  </div>
</template>

<style scoped>
.main-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  max-width: 300px;
  margin: 0 auto;
}
.container{
  display: flex;
  flex-direction: column;
  max-width: 224px;
}
  
.preview-message {
  background-color: #E6F7FF;
  padding: 10px;
  border: 1px solid #91D5FF;
  border-radius: 5px;
}
</style>