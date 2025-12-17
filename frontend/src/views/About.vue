<template>
  <div class="min-h-screen bg-base-100">
    <div class="max-w-4xl mx-auto px-6 py-16">
      <!-- Header -->
      <div class="text-center mb-16">
        <div class="flex items-center justify-center gap-3 mb-6">
          <Icon icon="clarity:music-note-line" class="w-16 h-16 text-primary" />
          <h1 class="text-5xl font-bold tracking-tight">About Soundry</h1>
        </div>
        <p class="text-xl text-base-content/60 max-w-2xl mx-auto">
          Empowering the next generation of DJs with accessible, high-quality music
        </p>
      </div>

      <!-- Mission -->
      <div class="card bg-base-200/50 shadow-xl mb-8 border border-base-300/50 backdrop-blur-md">
        <div class="card-body">
          <h2 class="card-title text-2xl mb-4">
            <Icon icon="clarity:bullseye-line" class="w-6 h-6 text-primary" />
            Our Mission
          </h2>
          <p class="text-lg leading-relaxed opacity-80">
            Soundry exists to provide <strong>high-quality music for free</strong>, breaking down the barriers that prevent aspiring DJs from entering the scene. 
          </p>
          <p class="text-lg leading-relaxed opacity-80 mt-4">
            With many newcomers entering the DJ world, services like Beatport can be prohibitively expensive. We understand this affects artists, but our goal is to <strong>encourage creativity and lower the entry barrier</strong> for passionate individuals who want to share music with the world.
          </p>
        </div>
      </div>

      <!-- Story -->
      <div class="card bg-base-200/50 shadow-xl mb-8 border border-base-300/50 backdrop-blur-md">
        <div class="card-body">
          <h2 class="card-title text-2xl mb-4">
            <Icon icon="clarity:heart-line" class="w-6 h-6 text-primary" />
            Why We Built This
          </h2>
          <p class="text-lg leading-relaxed opacity-80">
            I personally struggled to access music when starting my DJing journey. The costs added up quickly, making it difficult to experiment and grow.
          </p>
          <p class="text-lg leading-relaxed opacity-80 mt-4">
            Soundry was born from improving <strong>Downtify</strong>, transforming it into a modern, self-hosted application that anyone can run. I hope this tool helps others discover their passion and bring more creativity to the scene.
          </p>
          <p class="text-lg leading-relaxed opacity-80 mt-4 italic">
            — <strong>Alex Lewis</strong>, Creator
          </p>
        </div>
      </div>

      <!-- Features -->
      <div class="card bg-base-200/50 shadow-xl mb-8 border border-base-300/50 backdrop-blur-md">
        <div class="card-body">
          <h2 class="card-title text-2xl mb-6">
            <Icon icon="clarity:star-line" class="w-6 h-6 text-primary" />
            What Makes Soundry Special
          </h2>
          <div class="grid md:grid-cols-2 gap-6">
            <div class="flex items-start gap-3">
              <Icon icon="clarity:check-circle-line" class="w-6 h-6 text-success mt-1 flex-shrink-0" />
              <div>
                <h3 class="font-bold text-lg">Free & Open Source</h3>
                <p class="opacity-70">Self-hosted, fully transparent, MIT licensed</p>
              </div>
            </div>
            <div class="flex items-start gap-3">
              <Icon icon="clarity:check-circle-line" class="w-6 h-6 text-success mt-1 flex-shrink-0" />
              <div>
                <h3 class="font-bold text-lg">High Quality Audio</h3>
                <p class="opacity-70">Support for FLAC, MP3, and more</p>
              </div>
            </div>
            <div class="flex items-start gap-3">
              <Icon icon="clarity:check-circle-line" class="w-6 h-6 text-success mt-1 flex-shrink-0" />
              <div>
                <h3 class="font-bold text-lg">Multi-Platform</h3>
                <p class="opacity-70">Spotify, SoundCloud, and more</p>
              </div>
            </div>
            <div class="flex items-start gap-3">
              <Icon icon="clarity:check-circle-line" class="w-6 h-6 text-success mt-1 flex-shrink-0" />
              <div>
                <h3 class="font-bold text-lg">Modern UI</h3>
                <p class="opacity-70">Beautiful, intuitive interface</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Disclaimer -->
      <div class="card bg-warning/10 shadow-xl mb-8 border border-warning/30">
        <div class="card-body">
          <h2 class="card-title text-xl text-warning mb-2">
            <Icon icon="clarity:warning-standard-line" class="w-6 h-6" />
            Important Notice
          </h2>
          <p class="opacity-80 leading-relaxed">
            Soundry is intended for <strong>personal, educational, and archival use</strong>. Please support artists by purchasing music when possible and respect copyright laws in your jurisdiction.
          </p>
        </div>
      </div>

      <!-- CTA -->
      <div class="text-center mt-12">
        <router-link to="/" class="btn btn-primary btn-lg gap-2">
          <Icon icon="clarity:music-note-line" class="w-5 h-5" />
          Start Downloading
        </router-link>
        <a href="https://github.com/itzsleepyy/Soundry" target="_blank" class="btn btn-outline btn-lg gap-2 ml-4">
          <Icon icon="mdi:github" class="w-5 h-5" />
          View on GitHub
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Icon } from '@iconify/vue'
</script>

<style scoped>
</style>
