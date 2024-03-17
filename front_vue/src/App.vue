<script setup>
import VBtn from './components/VBtn.vue'
import VInput from './components/VInput.vue'
import { computed, ref } from "vue"
import AlgoMatrix from './AlgoMatrix.vue';

const stateShow = ref("")
const m = ref("")
const n = ref("")
const tableData = ref([])

const fillTable = () => {
  console.log(n.value)
  console.log(m.value)
  for (let i = 0; i < n.value; i++) {
    tableData.value.push([])
    for (let j = 0; j < m.value; j++){
      tableData.value[i].push("")
    }
  }
}
const  showMatrix = computed(() => !(m.value.replace(" ", "").length && n.value.replace(" ", "").length))
</script>

<template>
<div class="main-container">
  <div v-if="!stateShow" class="main-container">
    <VInput v-model="m" placeholder="Столбцов"/>
    <VInput v-model="n" placeholder="Строк"/>
    <VBtn value="Алгоритм Лапласа" :disable="showMatrix" @click="fillTable(); stateShow = '/api/laplas'" />
    <VBtn value="Оптимальный алгоритм" :disable="showMatrix" @click="fillTable(); stateShow = '/api/optimal'" />
    <VBtn value="Алгоритм Сэвиджа" :disable="showMatrix" @click="fillTable(); stateShow = '/api/savage'" />
    <VBtn value="Критерий Гурвица" :disable="showMatrix" @click="fillTable(); stateShow = '/api/hurwitz'" />
    <VBtn value="Сравнить алгоритмы" :disable="showMatrix" @click="fillTable(); stateShow = '/api/compare_algo'" />
  </div>
  <AlgoMatrix 
    v-if="stateShow && !showMatrix"
    :url="stateShow"
    :table-data="tableData"
    @back="stateShow = ''; n = ''; m = ''; tableData = []"
  />
</div>
</template>

<style>
.main-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  max-width: 300px;
  margin: 0 auto;
}
</style>./Laplas.vue