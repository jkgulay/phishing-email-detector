<template>
  <v-card
    class="result-card mb-6"
    elevation="0"
    :class="{
      'danger-result': threatLevel === 'danger',
      'uncertain-result': threatLevel === 'uncertain',
      'safe-result': threatLevel === 'safe',
    }"
  >
    <v-card-text class="pa-4 pa-md-6">
      <!-- Result Header -->
      <div class="result-banner pa-4 mb-5">
        <v-row align="center" no-gutters>
          <v-col cols="auto">
            <v-avatar :color="threatColor" size="56" class="result-icon">
              <v-icon :icon="threatIcon" size="32" color="white"></v-icon>
            </v-avatar>
          </v-col>
          <v-col class="ml-4">
            <div class="text-overline mb-1" style="letter-spacing: 2px">
              DETECTION RESULT
            </div>
            <div
              class="text-h5 text-md-h4 font-weight-bold result-title d-flex align-center"
            >
              <v-icon
                :icon="threatIcon"
                :color="threatColor"
                size="32"
                class="mr-2"
              ></v-icon>
              {{ threatTitle }}
            </div>
          </v-col>
        </v-row>
      </div>

      <!-- Status Message -->
      <v-alert
        :color="threatColor"
        variant="tonal"
        class="mb-5"
        density="comfortable"
      >
        <template v-slot:prepend>
          <v-icon :icon="threatIcon"></v-icon>
        </template>
        <div class="font-weight-medium">{{ threatMessage }}</div>
      </v-alert>

      <!-- Confidence Meters -->
      <div class="text-subtitle-1 font-weight-bold mb-3">
        Confidence Analysis
      </div>
      <v-row>
        <v-col cols="12" sm="6">
          <div class="confidence-meter safe-meter">
            <div class="meter-header">
              <v-icon
                icon="mdi-shield-check"
                color="#28a745"
                size="20"
              ></v-icon>
              <span class="ml-2">Safe Score</span>
              <v-spacer></v-spacer>
              <span class="font-weight-bold"
                >{{ result.confidence.safe }}%</span
              >
            </div>
            <v-progress-linear
              :model-value="result.confidence.safe"
              color="#28a745"
              height="12"
              rounded
              class="mt-2"
            ></v-progress-linear>
          </div>
        </v-col>
        <v-col cols="12" sm="6">
          <div class="confidence-meter danger-meter">
            <div class="meter-header">
              <v-icon
                icon="mdi-alert-circle"
                color="#dc3545"
                size="20"
              ></v-icon>
              <span class="ml-2">Phishing Score</span>
              <v-spacer></v-spacer>
              <span class="font-weight-bold"
                >{{ result.confidence.phishing }}%</span
              >
            </div>
            <v-progress-linear
              :model-value="result.confidence.phishing"
              color="#dc3545"
              height="12"
              rounded
              class="mt-2"
            ></v-progress-linear>
          </div>
        </v-col>
      </v-row>

      <!-- AI Analysis Button -->
      <v-btn
        v-if="!hasAiAnalysis"
        color="#547792"
        size="large"
        :loading="loadingAI"
        @click="$emit('get-ai-analysis')"
        prepend-icon="mdi-robot"
        block
        class="mt-6 ai-btn"
      >
        <span>Get Detailed AI Analysis</span>
        <v-icon class="ml-2">mdi-arrow-right</v-icon>
      </v-btn>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  result: Object,
  loadingAI: Boolean,
  hasAiAnalysis: Boolean,
});

defineEmits(["get-ai-analysis"]);

const threatLevel = computed(() => {
  if (!props.result) return null;
  const scoreDiff = Math.abs(
    props.result.confidence.phishing - props.result.confidence.safe
  );
  if (scoreDiff < 20) return "uncertain";
  return props.result.is_phishing ? "danger" : "safe";
});

const threatColor = computed(() => {
  switch (threatLevel.value) {
    case "danger":
      return "#dc3545";
    case "uncertain":
      return "#ff9800";
    case "safe":
      return "#28a745";
    default:
      return "#6c757d";
  }
});

const threatIcon = computed(() => {
  switch (threatLevel.value) {
    case "danger":
      return "mdi-alert-octagon";
    case "uncertain":
      return "mdi-alert";
    case "safe":
      return "mdi-shield-check";
    default:
      return "mdi-help-circle";
  }
});

const threatTitle = computed(() => {
  switch (threatLevel.value) {
    case "danger":
      return "Phishing Detected";
    case "uncertain":
      return "Potential Phishing";
    case "safe":
      return "Email is Safe";
    default:
      return "Unknown";
  }
});

const threatMessage = computed(() => {
  switch (threatLevel.value) {
    case "danger":
      return "This email contains suspicious patterns. Do not click any links or provide personal information.";
    case "uncertain":
      return "This email shows some suspicious characteristics. Exercise caution and verify the sender before taking any action.";
    case "safe":
      return "No malicious patterns detected. This email appears to be legitimate.";
    default:
      return "Unable to determine threat level.";
  }
});
</script>

<style scoped>
.result-card {
  background: rgba(255, 255, 255, 0.95) !important;
  border-radius: 12px !important;
  border: 2px solid;
  transition: all 0.3s ease;
}

.danger-result {
  border-color: rgba(220, 53, 69, 0.4);
  box-shadow: 0 4px 20px rgba(220, 53, 69, 0.15);
}

.uncertain-result {
  border-color: rgba(255, 152, 0, 0.4);
  box-shadow: 0 4px 20px rgba(255, 152, 0, 0.15);
}

.safe-result {
  border-color: rgba(40, 167, 69, 0.4);
  box-shadow: 0 4px 20px rgba(40, 167, 69, 0.15);
}

.result-banner {
  background: linear-gradient(
    135deg,
    rgba(148, 180, 193, 0.1) 0%,
    rgba(234, 224, 207, 0.1) 100%
  );
  border-radius: 8px;
}

.result-icon {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.result-title {
  color: #213448;
}

.confidence-meter {
  padding: 12px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(148, 180, 193, 0.2);
}

.meter-header {
  display: flex;
  align-items: center;
  font-size: 0.875rem;
  color: #213448;
}

.ai-btn {
  text-transform: none;
  letter-spacing: 0.5px;
  font-weight: 600;
}
</style>
