<template>
  <div class="min-h-screen m-2">
    <div class="flex justify-between items-center m-4 p-4 bg-base-200 rounded-xl shadow-lg border border-base-300/50 backdrop-blur-md">
      <h1 class="text-2xl font-bold tracking-tight">Downloads</h1>
      <div v-if="filteredQueue.length > 0" class="flex gap-3 items-center">
         <button @click="dm.refresh" class="btn btn-ghost btn-circle btn-sm" title="Refresh">
             <Icon icon="clarity:refresh-line" class="w-5 h-5" />
         </button>
         <div class="h-6 w-px bg-base-content/10"></div>
         <select v-model="sm.settings.value.format" class="select select-bordered select-sm w-32 bg-base-100 focus:outline-none">
            <option disabled value="">Format</option>
            <option v-for="fmt in sm.settingsOptions.format" :key="fmt" :value="fmt">{{ fmt.toUpperCase() }}</option>
         </select>
         <button @click="downloadAll" class="btn btn-primary btn-sm gap-2 pl-3 pr-4 shadow-lg shadow-primary/20">
            <Icon icon="clarity:download-cloud-line" />
            Download All
         </button>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="filteredQueue.length === 0" class="flex flex-col items-center justify-center p-12 text-base-content/30 space-y-4">
       <Icon icon="clarity:music-note-line" class="w-16 h-16" />
       <span class="text-lg">No session downloads yet.</span>
    </div>

    <!-- List -->
    <div v-else class="space-y-3 px-2">
      <div
          v-for="(downloadItem, index) in filteredQueue"
          :key="downloadItem.song.song_id"
          class="group flex items-center gap-4 bg-base-200/50 hover:bg-base-200 p-3 rounded-lg border border-base-content/5 transition-all duration-200 hover:shadow-md"
        >
          <!-- Cover -->
          <div class="relative w-16 h-16 flex-shrink-0 rounded-md overflow-hidden shadow-sm">
             <img :src="downloadItem.song.cover_url" class="w-full h-full object-cover" />
             <!-- Progress Overlay -->
             <div v-if="downloadItem.isDownloading()" class="absolute inset-0 bg-black/50 flex items-center justify-center">
                <span class="text-xs font-bold text-white">{{ Math.round(downloadItem.progress) }}%</span>
             </div>
          </div>

          <!-- Meta -->
          <div class="flex-grow min-w-0 flex flex-col justify-center">
             <h2 class="font-bold text-lg truncate leading-tight">{{ downloadItem.song.name }}</h2>
             <p class="text-sm opacity-60 truncate">{{ downloadItem.song.artist }}</p>
             <div class="flex items-center gap-2 mt-1">
                 <span v-if="downloadItem.isErrored()" class="text-xs text-error font-medium">Error</span>
                 <span v-else class="text-xs opacity-40">{{ downloadItem.message || downloadItem.web_status }}</span>
             </div>
          </div>

          <!-- Actions -->
          <div class="flex items-center gap-2 pr-2 opacity-80 group-hover:opacity-100 transition-opacity">
            <!-- Trash -->
            <button
              class="btn btn-ghost btn-square btn-sm text-error/50 hover:text-error hover:bg-error/10"
              @click="dm.remove(downloadItem.song)"
              title="Remove"
            >
              <Icon icon="clarity:trash-line" class="w-5 h-5" />
            </button>
            
            <!-- Download Button -->
            <a
              v-if="downloadItem.isDownloaded()"
              class="btn btn-success btn-sm gap-2 text-white shadow-lg shadow-success/20"
              href="javascript:;"
              @click="download(downloadItem.web_download_url)"
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
            
            <!-- Loading -->
             <button v-else-if="downloadItem.progress === 0 && !downloadItem.isDownloading()" class="btn btn-ghost btn-square btn-sm loading"></button>
          </div>
        </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Icon } from '@iconify/vue'
import { useProgressTracker, useDownloadManager } from '../model/download'
import { useSettingsManager } from '../model/settings'

const props = defineProps({
  data: Object,
})

const pt = useProgressTracker()
const dm = useDownloadManager()
const sm = useSettingsManager()

// Filter for Session & Sort by Newest
const filteredQueue = computed(() => {
    return pt.downloadQueue.value
        .filter(item => pt.isSessionSong(item.song))
        .slice().reverse()
})

function download(url) {
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
