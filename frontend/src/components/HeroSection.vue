<template>
  <section class="hero-section">
    <v-container style="max-width: 1200px">
      <v-row align="center" justify="center">
        <v-col cols="12" md="6" class="text-center text-md-start">
          <h1 class="hero-title mb-4">
            Detect <span class="text-accent">Phishing</span> Emails<br />
            with AI Precision
          </h1>
          <p class="hero-subtitle mb-6">
            Our advanced machine learning model analyzes suspicious emails in
            real-time, protecting you from cyber threats with 98.52%+ accuracy.
          </p>
          <div class="d-flex flex-wrap ga-3 justify-center justify-md-start">
            <v-chip variant="tonal" color="#547792" prepend-icon="mdi-robot">
              GPT-4o Analysis
            </v-chip>
            <v-chip variant="tonal" color="#547792" prepend-icon="mdi-forest">
              Random Forest ML
            </v-chip>
            <v-chip
              variant="tonal"
              color="#547792"
              prepend-icon="mdi-clock-fast"
            >
              Real-time
            </v-chip>
          </div>
        </v-col>
        <v-col cols="12" md="6" class="text-center">
          <div class="hero-image-wrapper">
            <img src="../assets/1.png" alt="Security" class="hero-logo" />
            <div class="hero-glow"></div>
          </div>
        </v-col>
      </v-row>

      <!-- Stats Cards -->
      <v-row class="mt-8" justify="center">
        <v-col cols="6" sm="4" md="3" v-for="stat in stats" :key="stat.label">
          <v-card class="stat-card text-center pa-4" elevation="0">
            <v-icon
              :icon="stat.icon"
              :color="stat.color"
              size="36"
              class="mb-2"
            ></v-icon>
            <div class="text-h4 font-weight-bold stat-value">
              {{ stat.value }}
            </div>
            <div class="text-caption text-medium-emphasis">
              {{ stat.label }}
            </div>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </section>
</template>

<script setup>
const stats = [
  {
    icon: "mdi-shield-check",
    value: "98.52%",
    label: "Accuracy",
    color: "#213448",
  },
  { icon: "mdi-clock-fast", value: "<1s", label: "Response", color: "#213448" },
  {
    icon: "mdi-email-multiple",
    value: "10K+",
    label: "Analyzed",
    color: "#213448",
  },
  { icon: "mdi-brain", value: "AI", label: "Powered", color: "#213448" },
];
</script>

<style scoped>
.hero-section {
  padding: 10px 0 10px;
}

.hero-title {
  font-size: clamp(1.8rem, 5vw, 3rem);
  color: #213448;
  line-height: 1.2;
  font-weight: 800;
}

.text-accent {
  color: #94b4c1;
}

.hero-subtitle {
  font-size: clamp(1rem, 2vw, 1.25rem);
  color: #547792;
  line-height: 1.6;
}

.hero-image-wrapper {
  position: relative;
  display: inline-block;
}

.hero-logo {
  width: 280px;
  height: 280px;
  object-fit: contain;
  position: relative;
  z-index: 2;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

.hero-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 400px;
  height: 400px;
  background: radial-gradient(
    circle,
    rgba(148, 180, 193, 0.3) 0%,
    transparent 70%
  );
  z-index: 1;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 0.5;
    transform: translate(-50%, -50%) scale(1);
  }
  50% {
    opacity: 0.8;
    transform: translate(-50%, -50%) scale(1.1);
  }
}

.stat-card {
  background: rgba(255, 255, 255, 0.8) !important;
  border: 1px solid rgba(148, 180, 193, 0.3);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(33, 52, 72, 0.15) !important;
}

.stat-value {
  color: #213448;
}

@media (max-width: 960px) {
  .hero-logo {
    width: 220px;
    height: 220px;
  }

  .hero-glow {
    width: 300px;
    height: 300px;
  }
}

@media (max-width: 600px) {
  .hero-logo {
    width: 180px;
    height: 180px;
  }

  .hero-glow {
    width: 250px;
    height: 250px;
  }
}
</style>
