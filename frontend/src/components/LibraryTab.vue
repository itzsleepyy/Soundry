<template>
  <div class="h-full">
     <div class="flex flex-col md:flex-row justify-between items-center mb-6 p-4 bg-base-200/50 rounded-xl shadow-lg border border-base-300/50 backdrop-blur-md gap-4">
      <div class="flex items-center gap-3">
          <h2 class="text-xl font-bold tracking-tight">Library</h2>
          <span v-if="files.length" class="badge badge-neutral bg-black/20">{{ files.length }}</span>
      </div>
      
      <!-- Controls -->
      <div class="flex flex-wrap gap-3 items-center justify-end w-full md:w-auto">
          <!-- Refresh -->
          <button
             class="btn btn-ghost btn-circle btn-sm"
             @click="refresh"
             :disabled="loading"
             title="Refresh"
           >
             <span v-if="loading" class="loading loading-spinner loading-xs"></span>
             <Icon v-else icon="clarity:refresh-line" class="w-5 h-5" />
          </button>
          
          <div class="h-6 w-px bg-base-content/10 hidden sm:block"></div>

         <!-- Sort -->
         <select v-model="sortOption" class="select select-bordered select-sm bg-base-100 focus:outline-none w-36">
            <option value="date-desc">Newest First</option>
            <option value="date-asc">Oldest First</option>
            <option value="name-asc">Name (A-Z)</option>
         </select>
         
         <div class="h-6 w-px bg-base-content/10 hidden sm:block"></div>

         <!-- View Toggle -->
         <div class="join">
            <button 
                class="btn btn-sm join-item" 
                :class="viewMode === 'list' ? 'btn-active btn-primary' : 'btn-ghost'"
                @click="viewMode = 'list'"
                title="List View"
            >
                <Icon icon="clarity:list-line" class="w-4 h-4" />
            </button>
            <button 
                class="btn btn-sm join-item" 
                :class="viewMode === 'grid' ? 'btn-active btn-primary' : 'btn-ghost'"
                @click="viewMode = 'grid'"
                title="Grid View"
            >
                <Icon icon="clarity:grid-view-line" class="w-4 h-4" />
            </button>
         </div>
      </div>
    </div>

    <div v-if="error" class="alert alert-error mb-4 shadow-lg">
        <Icon icon="clarity:error-line" />
        <span>{{ error }}</span>
    </div>

    <!-- Empty State -->
    <div v-if="!loading && displayFiles.length === 0" class="flex flex-col items-center justify-center p-20 text-center space-y-6 opacity-60">
      <div class="w-24 h-24 bg-base-200/50 rounded-full flex items-center justify-center mb-2">
          <Icon icon="clarity:folder-open-line" class="w-10 h-10 text-base-content/30" />
      </div>
      <div>
          <h2 class="text-xl font-bold opacity-80">No files found</h2>
          <p class="text-base-content/50 mt-2 max-w-xs mx-auto">
            Files you download will appear here.
          </p>
      </div>
    </div>

    <!-- Grid View -->
    <div v-else-if="viewMode === 'grid'" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
      <div 
         v-for="file in displayFiles" 
         :key="file.name"
         class="group relative aspect-square rounded-xl overflow-hidden bg-base-200 shadow-md transition-all hover:shadow-xl hover:scale-[1.02] border border-base-content/5"
      >
          <div class="absolute inset-0 flex flex-col items-center justify-center p-0">
              <img 
                v-if="file.image" 
                :src="`/downloads/${file.image}`" 
                class="absolute inset-0 w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                loading="lazy"
                alt="Cover"
              />
              <div v-else class="flex items-center justify-center w-full h-full bg-base-300">
                  <Icon icon="clarity:music-note-line" class="w-16 h-16 text-primary opacity-20 group-hover:opacity-10 transition-opacity" />
              </div>
              
              <div class="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black/80 via-black/40 to-transparent">
                 <h3 class="font-bold text-sm line-clamp-2 leading-tight break-words text-white shadow-sm">{{ file.name }}</h3>
                 <p class="text-[10px] text-white/60 mt-1">{{ formatSub(file.size, file.timestamp) }}</p>
              </div>
          </div>
         
         <!-- Hover Overlay -->
         <div class="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col items-center justify-center p-4 gap-3">
            <a
              class="btn btn-circle btn-success text-white border-none shadow-lg shadow-success/20 scale-90 hover:scale-100 transition-transform"
              :href="`/downloads/${encodeURIComponent(file.name)}`"
              download
              title="Download"
            >
               <Icon icon="clarity:download-line" class="w-6 h-6" />
            </a>
            <button
              class="btn btn-circle btn-error text-white border-none shadow-lg shadow-error/20 scale-90 hover:scale-100 transition-transform"
              @click="onDelete(file.name)"
              :disabled="deleting[file.name] === true"
              title="Delete"
            >
               <span v-if="deleting[file.name] === true" class="loading loading-spinner loading-xs"></span>
               <Icon v-else icon="clarity:trash-line" class="w-6 h-6" />
            </button>
         </div>
      </div>
    </div>

    <!-- List View -->
    <div v-else class="card bg-base-100/50 shadow-xl border border-base-200 backdrop-blur-sm">
      <div class="overflow-x-auto">
        <table class="table">
          <thead>
            <tr class="bg-base-200/50 text-base-content/60">
              <th>Name</th>
              <th>Size</th>
              <th>Date</th>
              <th class="text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="file in displayFiles" :key="file.name" class="hover:bg-base-200/50 transition-colors">
              <td class="font-medium max-w-xs md:max-w-md truncate" :title="file.name">
                  <div class="flex items-center gap-3">
                      <div class="w-8 h-8 rounded bg-primary/10 flex items-center justify-center text-primary">
                          <Icon icon="clarity:music-note-line" />
                      </div>
                      {{ file.name }}
                  </div>
              </td>
              <td class="text-sm opacity-60 whitespace-nowrap">{{ formatBytes(file.size) }}</td>
              <td class="text-sm opacity-60 whitespace-nowrap">{{ formatDate(file.timestamp) }}</td>
              <td class="text-right">
                  <div class="flex items-center justify-end gap-2">
                      <a
                        class="btn btn-square btn-sm btn-ghost hover:bg-success/10 hover:text-success"
                        :href="`/downloads/${encodeURIComponent(file.name)}`"
                        download
                        title="Download"
                        >
                          <Icon icon="clarity:download-line" class="w-5 h-5" />
                      </a
                      >
                      <button
                        class="btn btn-square btn-sm btn-ghost hover:bg-error/10 hover:text-error"
                        @click="onDelete(file.name)"
                        :disabled="deleting[file.name] === true"
                        title="Delete"
                      >
                        <span
                          v-if="deleting[file.name] === true"
                          class="loading loading-spinner loading-xs"
                        ></span>
                        <Icon v-else icon="clarity:trash-line" class="w-5 h-5" />
                      </button>
                  </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import API from '/src/model/api'
import { Icon } from '@iconify/vue'

const files = ref([])
const loading = ref(false)
const error = ref('')
const deleting = ref({})

const viewMode = ref('list') // 'list' | 'grid'
const sortOption = ref('date-desc') // 'date-desc' | 'date-asc' | 'name-asc'

// Formatters
const formatBytes = (bytes, decimals = 2) => {
    if (!+bytes) return '0 Bytes'
    const k = 1024
    const dm = decimals < 0 ? 0 : decimals
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`
}
const formatDate = (ms) => new Date(ms).toLocaleDateString()
const formatSub = (size, ms) => `${formatBytes(size)} • ${formatDate(ms)}`

const displayFiles = computed(() => {
    let list = [...files.value]
    
    if (sortOption.value === 'date-desc') {
        list.sort((a, b) => b.timestamp - a.timestamp)
    } else if (sortOption.value === 'date-asc') {
        list.sort((a, b) => a.timestamp - b.timestamp)
    } else if (sortOption.value === 'name-asc') {
        list.sort((a, b) => a.name.localeCompare(b.name))
    }
    return list
})

async function refresh() {
  loading.value = true
  error.value = ''
  try {
    const res = await API.listDownloads()
    // Handle both old (string array) and new (object array) API just in case
    files.value = (res.data || []).map(f => {
        if (typeof f === 'string') return { name: f, timestamp: 0, size: 0 }
        return f
    })
  } catch (e) {
    error.value = 'Failed to load downloads'
  } finally {
    loading.value = false
  }
}

async function onDelete(file) {
  if (!confirm(`Are you sure you want to delete "${file}"?`)) return
  
  deleting.value = { ...deleting.value, [file]: true }
  try {
    await API.deleteDownload(file)
    files.value = files.value.filter((f) => f.name !== file)
  } catch (e) {
    alert('Failed to delete ' + file)
  } finally {
    deleting.value = { ...deleting.value, [file]: false }
  }
}

onMounted(() => {
  refresh()
})
</script>

<style scoped></style>
