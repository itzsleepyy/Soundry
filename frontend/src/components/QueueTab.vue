<template>
  <div class="h-full">
    <div class="flex flex-col md:flex-row justify-between items-center mb-6 p-4 bg-base-200/50 rounded-xl shadow-lg border border-base-300/50 backdrop-blur-md gap-4">
      <h2 class="text-xl font-bold tracking-tight">Session Queue</h2>
      
      <!-- Controls -->
      <div v-if="filteredQueue.length > 0" class="flex flex-wrap gap-3 items-center justify-end w-full md:w-auto">
         <!-- Sort -->
         <select v-model="sortOption" class="select select-bordered select-sm bg-base-100 focus:outline-none w-36">
            <option value="date-desc">Newest First</option>
            <option value="date-asc">Oldest First</option>
            <option value="name-asc">Name (A-Z)</option>
         </select>
         
         <div class="h-6 w-px bg-base-content/10 hidden sm:block"></div>

         <!-- Format -->
         <select v-model="sm.settings.value.format" class="select select-bordered select-sm w-28 bg-base-100 focus:outline-none">
            <option disabled value="">Format</option>
            <option v-for="fmt in sm.settingsOptions.format" :key="fmt" :value="fmt">{{ fmt.toUpperCase() }}</option>
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

         <button @click="downloadAll" class="btn btn-primary btn-sm gap-2 pl-3 pr-4 shadow-lg shadow-primary/20">
            <Icon icon="clarity:download-cloud-line" />
            <span class="hidden sm:inline">Download All</span>
         </button>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="filteredQueue.length === 0" class="flex flex-col items-center justify-center p-20 text-center space-y-6">
       <div class="w-24 h-24 bg-base-200/50 rounded-full flex items-center justify-center mb-2">
           <Icon icon="clarity:music-note-line" class="w-10 h-10 text-base-content/30" />
       </div>
       <div>
           <h2 class="text-xl font-bold opacity-80">No downloads this session</h2>
           <p class="text-base-content/50 mt-2 max-w-xs mx-auto">
             Search for a song or paste a URL to start downloading.
           </p>
       </div>
    </div>

    <!-- Grid View -->
    <div v-else-if="viewMode === 'grid'" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 px-2">
       <div 
          v-for="item in filteredQueue" 
          :key="item.song.song_id"
          class="group relative aspect-square rounded-xl overflow-hidden bg-base-200 shadow-md transition-all hover:shadow-xl hover:scale-[1.02]"
       >
          <img :src="item.song.cover_url" class="w-full h-full object-cover" />
          
          <!-- Hover Overlay -->
          <div class="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col items-center justify-center p-4 text-center">
             <div class="mb-3">
                 <h3 class="text-white font-bold text-sm line-clamp-2 leading-tight">{{ item.song.name }}</h3>
                 <p class="text-white/60 text-xs truncate mt-1">{{ item.song.artist }}</p>
             </div>
             
             <div class="flex gap-2">
                <!-- Delete -->
                <button @click.stop="dm.remove(item.song)" class="btn btn-circle btn-sm btn-error text-white border-none bg-error/80 hover:bg-error">
                    <Icon icon="clarity:trash-line" class="w-4 h-4" />
                </button>
                
                <!-- Action -->
                <a
                  v-if="item.isDownloaded()"
                  class="btn btn-circle btn-sm btn-success text-white border-none bg-success/80 hover:bg-success"
                  href="javascript:;"
                  @click="downloadFile(item.web_download_url)"
                  title="Save"
                >
                  <Icon icon="clarity:download-line" class="w-4 h-4" />
                </a>
                <button
                   v-else-if="item.isQueued()"
                   class="btn btn-circle btn-sm btn-primary text-white border-none bg-primary/80 hover:bg-primary"
                   @click="triggerDownload(item)"
                   title="Convert"
                >
                   <Icon icon="clarity:download-cloud-line" class="w-4 h-4" />
                </button>
                <div v-else-if="item.isDownloading()" class="radial-progress text-primary text-[10px]" :style="`--value: ${item.progress}; --size: 2rem`">
                    {{ Math.round(item.progress) }}
                </div>
             </div>
          </div>
          
          <!-- Status Badge (Visible when not hovering/downloading) -->
           <div v-if="item.isDownloaded()" class="absolute top-2 right-2 badge badge-success badge-xs gap-1 shadow-sm opacity-100 group-hover:opacity-0 transition-opacity">
               Done
           </div>
           <div v-else-if="item.isDownloading()" class="absolute inset-0 bg-black/40 flex items-center justify-center">
               <span class="loading loading-spinner text-primary"></span>
           </div>
       </div>
    </div>

    <!-- List View -->
    <div v-else class="space-y-3 px-2">
      <div
          v-for="(downloadItem, index) in filteredQueue"
          :key="downloadItem.song.song_id"
          class="group flex items-center gap-4 bg-base-200/50 hover:bg-base-200 p-3 rounded-lg border border-base-content/5 transition-all duration-200 hover:shadow-md"
        >
          <!-- Same List Item Content as before -->
          <div class="relative w-16 h-16 flex-shrink-0 rounded-md overflow-hidden shadow-sm">
             <img :src="downloadItem.song.cover_url" class="w-full h-full object-cover" />
             <div v-if="downloadItem.isDownloading()" class="absolute inset-0 bg-black/50 flex items-center justify-center">
                <span class="text-xs font-bold text-white">{{ Math.round(downloadItem.progress) }}%</span>
             </div>
          </div>

          <div class="flex-grow min-w-0 flex flex-col justify-center">
             <h2 class="font-bold text-lg truncate leading-tight">{{ downloadItem.song.name }}</h2>
             <p class="text-sm opacity-60 truncate">{{ downloadItem.song.artist }}</p>
             <div class="flex items-center gap-2 mt-1">
                 <span v-if="downloadItem.isErrored()" class="text-xs text-error font-medium">Error</span>
                 <span v-else class="text-xs opacity-40">{{ downloadItem.message || downloadItem.web_status }}</span>
             </div>
          </div>

          <div class="flex items-center gap-2 pr-2 opacity-80 group-hover:opacity-100 transition-opacity">
            <button
              class="btn btn-ghost btn-square btn-sm text-error/50 hover:text-error hover:bg-error/10"
              @click="dm.remove(downloadItem.song)"
              title="Remove"
            >
              <Icon icon="clarity:trash-line" class="w-5 h-5" />
            </button>
            <a
              v-if="downloadItem.isDownloaded()"
              class="btn btn-success btn-sm gap-2 text-white shadow-lg shadow-success/20"
              href="javascript:;"
              @click="downloadFile(downloadItem.web_download_url)"
              download
            >
              <Icon icon="clarity:download-line" class="w-5 h-5" />
              <span class="hidden sm:inline">Save</span>
            </a>
            <button
               v-else-if="downloadItem.isQueued()"
               class="btn btn-primary btn-sm gap-2 text-white shadow-lg shadow-primary/20"
               @click="triggerDownload(downloadItem)"
            >
               <Icon icon="clarity:download-cloud-line" class="w-5 h-5" />
               <span class="hidden sm:inline">Convert</span>
            </button>
             <button v-else-if="downloadItem.progress === 0 && !downloadItem.isDownloading()" class="btn btn-ghost btn-square btn-sm loading"></button>
          </div>
        </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { Icon } from '@iconify/vue'
import { useProgressTracker, useDownloadManager } from '../model/download'
import { useSettingsManager } from '../model/settings'

const pt = useProgressTracker()
const dm = useDownloadManager()
const sm = useSettingsManager()

const viewMode = ref('list') // 'list' | 'grid'
const sortOption = ref('date-desc') // 'date-desc' | 'date-asc' | 'name-asc'

// Filter for Session & Sort
const filteredQueue = computed(() => {
    let list = pt.downloadQueue.value.filter(item => pt.isSessionSong(item.song))
    
    // Sorting Logic
    if (sortOption.value === 'date-desc') {
        list = list.slice().sort((a, b) => b.timestamp - a.timestamp)
    } else if (sortOption.value === 'date-asc') {
        list = list.slice().sort((a, b) => a.timestamp - b.timestamp)
    } else if (sortOption.value === 'name-asc') {
        list = list.slice().sort((a, b) => a.song.name.localeCompare(b.song.name))
    }
    
    return list
})

function downloadFile(url) {
  const a = document.createElement('a')
  a.href = url
  a.download = url.split('/').pop()
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
}

function triggerDownload(item) {
   sm.saveSettings()
   dm.download(item.song)
}

function downloadAll() {
   sm.saveSettings()
   filteredQueue.value.forEach(item => {
      if (item.isQueued()) {
         dm.download(item.song)
      }
   })
}
</script>

<style scoped></style>
