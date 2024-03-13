<script setup>
import axios from 'axios'
import { computed, ref, defineEmits } from 'vue'
import VBtn from './components/VBtn.vue'
import VInput from './components/VInput.vue'
import TableMatrix from './components/TableMatrix.vue'

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

const canFetch = computed(() => { 
  for (const item of tableData.value) {
    for (const subItem of item) {
      if (!subItem.replace(" ", "").length) return false
    }
  }
  return true
})
  
const fetchData = () => {
  const data = ref("")
  axios.post(
    props.url, 
    { data: tableData.value, hurwitz:  hurwitz.value},
  ).then((response) => {
    info.value = response.data.msg
  }).catch(() => {
    info.value = response.data.msg
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
      <VInput v-if="props.url === '/api/hurwitz'" v-model="hurwitz" holder="Критерий оптимизма"/>
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