<template>
  <div class="min-h-screen bg-base-100">
    <div class="max-w-4xl mx-auto px-6 py-16">
      <!-- Header -->
      <div class="text-center mb-16">
        <div class="flex items-center justify-center gap-3 mb-6">
          <Icon icon="clarity:history-line" class="w-16 h-16 text-primary" />
          <h1 class="text-5xl font-bold tracking-tight">Changelog</h1>
        </div>
        <p class="text-xl text-base-content/60 max-w-2xl mx-auto">
          Track the evolution of Soundry
        </p>
      </div>

      <!-- Version 2.1.0 (Latest) -->
      <div class="card bg-primary/5 shadow-xl mb-8 border-2 border-primary/20 backdrop-blur-md">
        <div class="card-body">
          <div class="flex items-start justify-between mb-4">
            <div>
              <div class="flex items-center gap-3 mb-2">
                <h2 class="text-3xl font-bold">v2.1.0</h2>
                <span class="badge badge-primary">Latest</span>
              </div>
              <p class="text-sm opacity-60">December 17, 2025</p>
            </div>
          </div>
          
          <div class="space-y-6">
            <!-- Added -->
            <div>
              <h3 class="font-bold text-lg flex items-center gap-2 mb-3">
                <Icon icon="clarity:plus-circle-line" class="w-5 h-5 text-success" />
                Added
              </h3>
              <ul class="space-y-2 ml-7">
                <li class="flex items-start gap-2">
                  <Icon icon="clarity:dot-circle-line" class="w-4 h-4 mt-1 text-primary flex-shrink-0" />
                  <span><strong>Library Search</strong> - Filter your downloads with real-time search</span>
                </li>
                <li class="flex items-start gap-2">
                  <Icon icon="clarity:dot-circle-line" class="w-4 h-4 mt-1 text-primary flex-shrink-0" />
                  <span><strong>Pagination</strong> - Browse large libraries with 50 items per page</span>
                </li>
                <li class="flex items-start gap-2">
                  <Icon icon="clarity:dot-circle-line" class="w-4 h-4 mt-1 text-primary flex-shrink-0" />
                  <span><strong>About Page</strong> - Learn about Soundry's mission</span>
                </li>
                <li class="flex items-start gap-2">
                  <Icon icon="clarity:dot-circle-line" class="w-4 h-4 mt-1 text-primary flex-shrink-0" />
                  <span><strong>Changelog</strong> - Track updates and improvements</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- Version 2.0.0 -->
      <div class="card bg-base-200/50 shadow-xl mb-8 border border-base-300/50 backdrop-blur-md">
        <div class="card-body">
          <div class="flex items-start justify-between mb-4">
            <div>
              <h2 class="text-3xl font-bold">v2.0.0</h2>
              <p class="text-sm opacity-60">December 16, 2025</p>
            </div>
          </div>
          
          <div class="space-y-6">
            <!-- Added -->
            <div>
              <h3 class="font-bold text-lg flex items-center gap-2 mb-3">
                <Icon icon="clarity:plus-circle-line" class="w-5 h-5 text-success" />
                Added
              </h3>
              <ul class="space-y-2 ml-7">
                <li class="flex items-start gap-2">
                  <Icon icon="clarity:dot-circle-line" class="w-4 h-4 mt-1 text-primary flex-shrink-0" />
                  <span><strong>Session Management</strong> - Batch download all files as ZIP</span>
                </li>
                <li class="flex items-start gap-2">
                  <Icon icon="clarity:dot-circle-line" class="w-4 h-4 mt-1 text-primary flex-shrink-0" />
                  <span><strong>Session Progress Bar</strong> - Track overall download progress</span>
                </li>
                <li class="flex items-start gap-2">
                  <Icon icon="clarity:dot-circle-line" class="w-4 h-4 mt-1 text-primary flex-shrink-0" />
                  <span><strong>Auto-Cleanup</strong> - Files auto-delete after 24 hours</span>
                </li>
                <li class="flex items-start gap-2">
                  <Icon icon="clarity:dot-circle-line" class="w-4 h-4 mt-1 text-primary flex-shrink-0" />
                  <span><strong>SoundCloud Support</strong> - Download from SoundCloud</span>
                </li>
                <li class="flex items-start gap-2">
                  <Icon icon="clarity:dot-circle-line" class="w-4 h-4 mt-1 text-primary flex-shrink-0" />
                  <span><strong>Modern UI Redesign</strong> - Glassmorphism, dark mode, grid/list views</span>
                </li>
                <li class="flex items-start gap-2">
                  <Icon icon="clarity:dot-circle-line" class="w-4 h-4 mt-1 text-primary flex-shrink-0" />
                  <span><strong>Soundry Branding</strong> - Complete rebrand from Downtify</span>
                </li>
              </ul>
            </div>
            
            <!-- Fixed -->
            <div>
              <h3 class="font-bold text-lg flex items-center gap-2 mb-3">
                <Icon icon="clarity:wrench-line" class="w-5 h-5 text-info" />
                Fixed
              </h3>
              <ul class="space-y-2 ml-7">
                <li class="flex items-start gap-2">
                  <Icon icon="clarity:dot-circle-line" class="w-4 h-4 mt-1 text-primary flex-shrink-0" />
                  <span>ZIP streaming corruption and performance</span>
                </li>
                <li class="flex items-start gap-2">
                  <Icon icon="clarity:dot-circle-line" class="w-4 h-4 mt-1 text-primary flex-shrink-0" />
                  <span>SPA routing (404 on page refresh)</span>
                </li>
                <li class="flex items-start gap-2">
                  <Icon icon="clarity:dot-circle-line" class="w-4 h-4 mt-1 text-primary flex-shrink-0" />
                  <span>Coolify deployment issues</span>
                </li>
              </ul>
            </div>

            <!-- Changed -->
            <div>
              <h3 class="font-bold text-lg flex items-center gap-2 mb-3">
                <Icon icon="clarity:refresh-line" class="w-5 h-5 text-warning" />
                Changed
              </h3>
              <ul class="space-y-2 ml-7">
                <li class="flex items-start gap-2">
                  <Icon icon="clarity:dot-circle-line" class="w-4 h-4 mt-1 text-primary flex-shrink-0" />
                  <span>Multi-stage Dockerfile (builds frontend in Docker)</span>
                </li>
                <li class="flex items-start gap-2">
                  <Icon icon="clarity:dot-circle-line" class="w-4 h-4 mt-1 text-primary flex-shrink-0" />
                  <span>Removed pytube dependency (yt-dlp only)</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- CTA -->
      <div class="text-center mt-12">
        <router-link to="/" class="btn btn-primary btn-lg gap-2">
          <Icon icon="clarity:home-line" class="w-5 h-5" />
          Back to Home
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Icon } from '@iconify/vue'
</script>

<style scoped>
</style>
