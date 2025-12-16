<template>
  <v-app>
    <!-- Professional App Bar -->
    <v-app-bar elevation="0" class="app-bar-custom" height="72">
      <v-container class="d-flex align-center py-0" style="max-width: 1900px">
        <div class="d-flex align-center">
          <img src="./assets/3.png" alt="Logo" class="app-logo" />
          <div class="d-none d-sm-block">
            <div class="text-h6 font-weight-bold logo-text">
              Phishing Detector
            </div>
            <div class="text-caption subtitle-text d-none d-md-block">
              AI-Powered Security
            </div>
          </div>
        </div>
        <v-spacer></v-spacer>
        <v-chip
          prepend-icon="mdi-shield-check"
          color="#94B4C1"
          size="small"
          variant="flat"
          class="custom-chip d-none d-sm-flex"
        >
          Secure Analysis
        </v-chip>
        <v-btn icon variant="text" class="ml-2 d-sm-none" color="#EAE0CF">
          <v-icon>mdi-shield-check</v-icon>
        </v-btn>
      </v-container>
    </v-app-bar>

    <v-main class="main-background">
      <!-- Hero Section -->
      <section class="hero-section">
        <v-container style="max-width: 1200px">
          <v-row align="center" justify="center">
            <v-col cols="12" md="6" class="text-center text-md-start">
              <h1 class="hero-title mb-4">
                Detect <span class="text-accent">Phishing</span> Emails<br />
                with AI Precision
              </h1>
              <p class="hero-subtitle mb-6">
                Our advanced machine learning model analyzes suspicious emails
                in real-time, protecting you from cyber threats with 99%+
                accuracy.
              </p>
              <div
                class="d-flex flex-wrap ga-3 justify-center justify-md-start"
              >
                <v-chip
                  variant="tonal"
                  color="#547792"
                  prepend-icon="mdi-robot"
                >
                  GPT-4o Analysis
                </v-chip>
                <v-chip
                  variant="tonal"
                  color="#547792"
                  prepend-icon="mdi-forest"
                >
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
                <img src="./assets/1.png" alt="Security" class="hero-logo" />
                <div class="hero-glow"></div>
              </div>
            </v-col>
          </v-row>

          <!-- Stats Cards -->
          <v-row class="mt-8" justify="center">
            <v-col
              cols="6"
              sm="4"
              md="3"
              v-for="stat in stats"
              :key="stat.label"
            >
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

      <!-- Main Analysis Section -->
      <v-container class="py-8" style="max-width: 1000px">
        <!-- Email Input Card -->
        <v-card class="input-card mb-6" elevation="0">
          <v-card-text class="pa-4 pa-md-6">
            <div class="d-flex align-center mb-4">
              <v-avatar color="#213448" size="40" class="mr-3">
                <v-icon color="#EAE0CF">mdi-email-search</v-icon>
              </v-avatar>
              <div>
                <div class="text-h6 font-weight-bold">Analyze Email</div>
                <div class="text-caption text-medium-emphasis">
                  Paste suspicious content below
                </div>
              </div>
            </div>

            <v-textarea
              v-model="emailText"
              placeholder="Paste email content here...

Example: 'URGENT: Your account has been compromised. Click here immediately to secure your account...'"
              rows="6"
              variant="outlined"
              :disabled="loading"
              class="email-input mb-4"
              hide-details
              bg-color="white"
            ></v-textarea>

            <v-row dense>
              <v-col cols="12" sm="8">
                <v-btn
                  color="#213448"
                  size="large"
                  :loading="loading"
                  :disabled="!emailText || loading"
                  @click="analyzeEmail"
                  prepend-icon="mdi-shield-search"
                  block
                  class="analyze-btn"
                >
                  Analyze Security
                </v-btn>
              </v-col>
              <v-col cols="12" sm="4">
                <v-btn
                  variant="outlined"
                  color="#547792"
                  size="large"
                  @click="loadExample"
                  :disabled="loading"
                  prepend-icon="mdi-file-document"
                  block
                >
                  Example
                </v-btn>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <!-- Results Section -->
        <v-expand-transition>
          <div v-if="predictionResult">
            <!-- Detection Result Card -->
            <v-card
              class="result-card mb-6"
              elevation="0"
              :class="
                predictionResult.is_phishing ? 'phishing-result' : 'safe-result'
              "
            >
              <v-card-text class="pa-4 pa-md-6">
                <!-- Result Header -->
                <div class="result-banner pa-4 mb-5">
                  <v-row align="center" no-gutters>
                    <v-col cols="auto">
                      <v-avatar
                        :color="
                          predictionResult.is_phishing ? '#dc3545' : '#28a745'
                        "
                        size="56"
                        class="result-icon"
                      >
                        <v-icon
                          :icon="
                            predictionResult.is_phishing
                              ? 'mdi-alert-octagon'
                              : 'mdi-shield-check'
                          "
                          size="32"
                          color="white"
                        ></v-icon>
                      </v-avatar>
                    </v-col>
                    <v-col class="ml-4">
                      <div
                        class="text-overline mb-1"
                        style="letter-spacing: 2px"
                      >
                        DETECTION RESULT
                      </div>
                      <div
                        class="text-h5 text-md-h4 font-weight-bold result-title d-flex align-center"
                      >
                        <v-icon
                          :icon="
                            predictionResult.is_phishing
                              ? 'mdi-alert'
                              : 'mdi-check-circle'
                          "
                          :color="
                            predictionResult.is_phishing ? '#dc3545' : '#28a745'
                          "
                          size="32"
                          class="mr-2"
                        ></v-icon>
                        {{
                          predictionResult.is_phishing
                            ? "Phishing Detected"
                            : "Email is Safe"
                        }}
                      </div>
                    </v-col>
                  </v-row>
                </div>

                <!-- Status Message -->
                <v-alert
                  :color="predictionResult.is_phishing ? '#dc3545' : '#28a745'"
                  variant="tonal"
                  class="mb-5"
                  density="comfortable"
                >
                  <template v-slot:prepend>
                    <v-icon
                      :icon="
                        predictionResult.is_phishing
                          ? 'mdi-alert'
                          : 'mdi-check-circle'
                      "
                    ></v-icon>
                  </template>
                  <div class="font-weight-medium">
                    {{
                      predictionResult.is_phishing
                        ? "This email contains suspicious patterns. Do not click any links or provide personal information."
                        : "No malicious patterns detected. This email appears to be legitimate."
                    }}
                  </div>
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
                          >{{ predictionResult.confidence.safe }}%</span
                        >
                      </div>
                      <v-progress-linear
                        :model-value="predictionResult.confidence.safe"
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
                          >{{ predictionResult.confidence.phishing }}%</span
                        >
                      </div>
                      <v-progress-linear
                        :model-value="predictionResult.confidence.phishing"
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
                  v-if="!aiAnalysis"
                  color="#547792"
                  size="large"
                  :loading="loadingAI"
                  @click="getAIAnalysis"
                  prepend-icon="mdi-robot"
                  block
                  class="mt-6 ai-btn"
                >
                  <span>Get Detailed AI Analysis</span>
                  <v-icon class="ml-2">mdi-arrow-right</v-icon>
                </v-btn>
              </v-card-text>
            </v-card>

            <!-- AI Analysis Card -->
            <v-expand-transition>
              <v-card v-if="aiAnalysis" class="ai-card mb-6" elevation="0">
                <v-card-text class="pa-0">
                  <!-- AI Header -->
                  <div class="ai-header pa-4 pa-md-5">
                    <v-row align="center" no-gutters>
                      <v-col cols="auto">
                        <v-avatar color="#547792" size="48">
                          <v-icon color="white" size="28">mdi-brain</v-icon>
                        </v-avatar>
                      </v-col>
                      <v-col class="ml-3">
                        <div class="text-h6 font-weight-bold">
                          AI Expert Analysis
                        </div>
                        <div class="d-flex align-center">
                          <v-icon
                            icon="mdi-robot"
                            size="14"
                            class="mr-1"
                          ></v-icon>
                          <span class="text-caption"
                            >Powered by GPT-4o-mini</span
                          >
                        </div>
                      </v-col>
                    </v-row>
                  </div>

                  <!-- AI Content -->
                  <div class="ai-content pa-4 pa-md-5">
                    <div
                      class="ai-analysis-container"
                      v-html="formatAnalysis(aiAnalysis.analysis)"
                    ></div>
                  </div>

                  <!-- Actions -->
                  <v-divider></v-divider>
                  <div class="pa-4 d-flex flex-wrap ga-2">
                    <v-btn
                      variant="tonal"
                      color="#547792"
                      prepend-icon="mdi-content-copy"
                      size="small"
                      @click="copyAnalysis"
                    >
                      Copy
                    </v-btn>
                    <v-btn
                      variant="tonal"
                      color="#213448"
                      prepend-icon="mdi-refresh"
                      size="small"
                      @click="resetAnalysis"
                    >
                      New Analysis
                    </v-btn>
                  </div>
                </v-card-text>
              </v-card>
            </v-expand-transition>
          </div>
        </v-expand-transition>

        <!-- Error Alert -->
        <v-alert
          v-if="error"
          type="error"
          closable
          @click:close="error = null"
          class="mb-6"
          variant="tonal"
        >
          {{ error }}
        </v-alert>
      </v-container>
    </v-main>

    <!-- Footer -->
    <v-footer class="footer-custom py-6">
      <v-container style="max-width: 1400px">
        <v-row align="center">
          <v-col cols="12" md="6" class="text-center text-md-start">
            <div class="d-flex align-center justify-center justify-md-start">
              <img src="./assets/3.png" alt="Logo" class="footer-logo mr-2" />
              <span class="text-body-2 font-weight-medium"
                >Phishing Email Detector</span
              >
            </div>
            <div class="text-caption mt-1" style="color: #94b4c1">
              IT113 Final Project © 2025
            </div>
          </v-col>
          <v-col cols="12" md="6">
            <div class="d-flex flex-wrap ga-2 justify-center justify-md-end">
              <v-chip size="x-small" variant="outlined">
                <v-icon start size="12">mdi-forest</v-icon>
                Random Forest
              </v-chip>
              <v-chip size="x-small" variant="outlined">
                <v-icon start size="12">mdi-robot</v-icon>
                GPT-4o
              </v-chip>
              <v-chip size="x-small" variant="outlined">
                <v-icon start size="12">mdi-vuejs</v-icon>
                Vue 3
              </v-chip>
              <v-chip size="x-small" variant="outlined">
                <v-icon start size="12">mdi-language-python</v-icon>
                Flask
              </v-chip>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-footer>

    <!-- Snackbar for notifications -->
    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="2000">
      {{ snackbarText }}
    </v-snackbar>
  </v-app>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

const API_BASE_URL = "/api";

const emailText = ref("");
const loading = ref(false);
const loadingAI = ref(false);
const predictionResult = ref(null);
const aiAnalysis = ref(null);
const error = ref(null);
const snackbar = ref(false);
const snackbarText = ref("");
const snackbarColor = ref("success");

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

const examplePhishingEmail = `URGENT: Your account is suspended. Click here to verify: http://bit.ly/fake

Dear Valued Customer,

We have detected suspicious activity on your account. Your account has been temporarily suspended for security reasons.

To reactivate your account, please click the link below and verify your information immediately:
http://bit.ly/account-verify-now

Failure to verify within 24 hours will result in permanent account closure.

Thank you for your immediate attention to this matter.

Security Team`;

const loadExample = () => {
  emailText.value = examplePhishingEmail;
  predictionResult.value = null;
  aiAnalysis.value = null;
  error.value = null;
};

const analyzeEmail = async () => {
  if (!emailText.value) return;

  loading.value = true;
  error.value = null;
  predictionResult.value = null;
  aiAnalysis.value = null;

  try {
    const response = await axios.post(`${API_BASE_URL}/predict`, {
      email_text: emailText.value,
    });
    predictionResult.value = response.data;
  } catch (err) {
    error.value =
      err.response?.data?.error || "Failed to analyze email. Please try again.";
  } finally {
    loading.value = false;
  }
};

const getAIAnalysis = async () => {
  if (!predictionResult.value) return;

  loadingAI.value = true;
  error.value = null;

  try {
    const response = await axios.post(`${API_BASE_URL}/analyze`, {
      email_text: emailText.value,
      prediction_result: predictionResult.value,
    });
    aiAnalysis.value = response.data;
  } catch (err) {
    error.value = err.response?.data?.error || "Failed to get AI analysis.";
  } finally {
    loadingAI.value = false;
  }
};

const formatAnalysis = (text) => {
  if (!text) return "";

  let html = '<div class="analysis-wrapper">';
  const lines = text.split("\n");
  let listItems = []; // Each item: { num: number, content: string }
  let pendingNumber = null; // Track number on its own line

  const flushList = () => {
    if (listItems.length > 0) {
      html += '<div class="analysis-list">';
      listItems.forEach((item) => {
        html += `
          <div class="analysis-item">
            <div class="item-number">${item.num}</div>
            <div class="item-content">${item.content}</div>
          </div>`;
      });
      html += "</div>";
      listItems = [];
    }
  };

  lines.forEach((line) => {
    line = line.trim();
    if (!line) {
      return;
    }

    // Headers with ###
    if (line.startsWith("###")) {
      flushList();
      pendingNumber = null;
      const title = line.replace(/^###\s*/, "");
      const icon = getIconForSection(title);
      html += `
        <div class="section-header">
          <div class="section-icon">
            <i class="mdi ${icon}"></i>
          </div>
          <span>${title}</span>
        </div>`;
      return;
    }

    // Check if line is just a number (number on its own line)
    const soloNumMatch = line.match(/^(\d+)\.?$/);
    if (soloNumMatch) {
      pendingNumber = parseInt(soloNumMatch[1], 10);
      return;
    }

    // If we have a pending number, combine it with this line
    if (pendingNumber !== null) {
      const content = line
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/:(.*?):/g, "<em>$1</em>");
      listItems.push({ num: pendingNumber, content });
      pendingNumber = null;
      return;
    }

    // Numbered items on same line (1. text or 1 text)
    const numMatch = line.match(/^(\d+)\.?\s+(.+)$/);
    if (numMatch) {
      const originalNum = parseInt(numMatch[1], 10);
      const content = numMatch[2]
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/:(.*?):/g, "<em>$1</em>");
      listItems.push({ num: originalNum, content });
      return;
    }

    // Bullet points (with optional leading space)
    const bulletMatch = line.match(/^\s*[-•*]\s+(.+)$/);
    if (bulletMatch) {
      flushList();
      const content = bulletMatch[1].replace(
        /\*\*(.*?)\*\*/g,
        "<strong>$1</strong>"
      );
      html += `
        <div class="bullet-item">
          <i class="mdi mdi-chevron-right bullet-icon"></i>
          <span>${content}</span>
        </div>`;
      return;
    }

    // Regular paragraph
    flushList();
    const formattedLine = line.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
    html += `<p class="analysis-paragraph">${formattedLine}</p>`;
  });

  flushList();
  html += "</div>";
  return html;
};

const getIconForSection = (title) => {
  const lower = title.toLowerCase();
  if (lower.includes("indicator") || lower.includes("analysis"))
    return "mdi-magnify";
  if (lower.includes("red flag") || lower.includes("warning"))
    return "mdi-flag";
  if (lower.includes("recommend")) return "mdi-lightbulb";
  if (lower.includes("education") || lower.includes("insight"))
    return "mdi-school";
  return "mdi-information";
};

const copyAnalysis = () => {
  if (aiAnalysis.value?.analysis) {
    navigator.clipboard.writeText(aiAnalysis.value.analysis);
    snackbarText.value = "Analysis copied to clipboard!";
    snackbarColor.value = "success";
    snackbar.value = true;
  }
};

const resetAnalysis = () => {
  emailText.value = "";
  predictionResult.value = null;
  aiAnalysis.value = null;
  error.value = null;
};
</script>

<style scoped>
/* ===== Color Variables ===== */
:root {
  --primary: #213448;
  --secondary: #547792;
  --accent: #94b4c1;
  --light: #eae0cf;
}

/* ===== App Bar ===== */
.app-bar-custom {
  background: linear-gradient(135deg, #213448 0%, #2d4a5e 100%) !important;
  border-bottom: 1px solid rgba(148, 180, 193, 0.2);
}

.app-logo {
  height: 56px;
  width: 56px;
  object-fit: contain;
}

.logo-text {
  color: #eae0cf !important;
}

.subtitle-text {
  color: #94b4c1 !important;
  font-size: 11px;
}

.custom-chip {
  color: #213448 !important;
  font-weight: 600;
}

/* ===== Main Background ===== */
.main-background {
  background: linear-gradient(180deg, #eae0cf 0%, #f5f0e8 50%, #ffffff 100%);
  min-height: 100vh;
}

/* ===== Hero Section ===== */
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
  color: #547792;
  position: relative;
}

.hero-subtitle {
  font-size: clamp(0.95rem, 2vw, 1.15rem);
  color: #547792;
  line-height: 1.6;
  max-width: 500px;
}

.hero-image-wrapper {
  position: relative;
  display: inline-block;
}

.hero-logo {
  width: clamp(180px, 40vw, 280px);
  height: auto;
  position: relative;
  z-index: 2;
  animation: float 4s ease-in-out infinite;
}

.hero-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 120%;
  height: 120%;
  background: radial-gradient(
    circle,
    rgba(148, 180, 193, 0.3) 0%,
    transparent 70%
  );
  z-index: 1;
  animation: pulse 3s ease-in-out infinite;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-15px);
  }
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

/* ===== Stats Cards ===== */
.stat-card {
  background: rgba(255, 255, 255, 0.8) !important;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(84, 119, 146, 0.15);
  border-radius: 16px !important;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(33, 52, 72, 0.12) !important;
}

.stat-value {
  color: #213448;
}

/* ===== Input Card ===== */
.input-card {
  background: rgba(255, 255, 255, 0.95) !important;
  border: 1px solid rgba(84, 119, 146, 0.2);
  border-radius: 20px !important;
  box-shadow: 0 8px 32px rgba(33, 52, 72, 0.08) !important;
}

.email-input :deep(.v-field) {
  border-radius: 12px !important;
}

.email-input :deep(textarea) {
  font-size: 0.95rem;
  line-height: 1.6;
}

.analyze-btn {
  color: #eae0cf !important;
  font-weight: 600;
  text-transform: none;
  letter-spacing: 0.5px;
  border-radius: 12px !important;
  transition: all 0.3s ease;
}

.analyze-btn:hover {
  box-shadow: 0 8px 24px rgba(33, 52, 72, 0.25) !important;
  transform: translateY(-2px);
}

/* ===== Result Card ===== */
.result-card {
  background: white !important;
  border-radius: 20px !important;
  overflow: hidden;
  border: 1px solid rgba(84, 119, 146, 0.15);
}

.phishing-result {
  border-top: 4px solid #dc3545;
}

.safe-result {
  border-top: 4px solid #28a745;
}

.result-banner {
  background: linear-gradient(
    135deg,
    rgba(234, 224, 207, 0.5) 0%,
    rgba(255, 255, 255, 0.8) 100%
  );
  border-radius: 12px;
}

.result-icon {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.result-title {
  color: #213448;
}

/* ===== Confidence Meters ===== */
.confidence-meter {
  background: rgba(248, 249, 250, 0.8);
  padding: 16px;
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.meter-header {
  display: flex;
  align-items: center;
  font-size: 0.9rem;
  color: #213448;
}

/* ===== AI Button ===== */
.ai-btn {
  color: white !important;
  font-weight: 600;
  text-transform: none;
  border-radius: 12px !important;
  transition: all 0.3s ease;
}

.ai-btn:hover {
  box-shadow: 0 8px 24px rgba(84, 119, 146, 0.3) !important;
}

/* ===== AI Card ===== */
.ai-card {
  background: white !important;
  border-radius: 20px !important;
  border: 1px solid rgba(84, 119, 146, 0.2);
  overflow: hidden;
}

.ai-header {
  background: linear-gradient(135deg, #eae0cf 0%, #f5f0e8 100%);
  border-bottom: 1px solid rgba(84, 119, 146, 0.1);
}

.ai-content {
  background: #fafafa;
}

/* ===== AI Analysis Styles ===== */
.analysis-wrapper {
  font-size: 0.95rem;
  line-height: 1.7;
  color: #2c3e50;
}

.section-header {
  display: flex;
  align-items: center;
  padding: 14px 18px;
  margin: 20px 0 14px;
  background: linear-gradient(135deg, #213448 0%, #547792 100%);
  color: #eae0cf;
  border-radius: 10px;
  font-weight: 700;
  font-size: 1.05rem;
  box-shadow: 0 4px 12px rgba(33, 52, 72, 0.2);
}

.section-icon {
  width: 32px;
  height: 32px;
  background: rgba(234, 224, 207, 0.2);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
}

.section-icon i {
  font-size: 18px;
}

.analysis-list {
  margin: 12px 0;
  padding: 12px;
  background: white;
  border-radius: 12px;
  border: 1px solid rgba(84, 119, 146, 0.1);
}

.analysis-item {
  display: flex;
  align-items: flex-start;
  padding: 12px 14px;
  margin: 8px 0;
  background: linear-gradient(
    135deg,
    rgba(234, 224, 207, 0.3) 0%,
    rgba(255, 255, 255, 0.8) 100%
  );
  border-radius: 10px;
  transition: all 0.25s ease;
  border-left: 3px solid transparent;
}

.analysis-item:hover {
  transform: translateX(6px);
  border-left-color: #547792;
  box-shadow: 0 4px 12px rgba(84, 119, 146, 0.12);
}

.item-number {
  min-width: 30px;
  height: 30px;
  background: linear-gradient(135deg, #213448 0%, #547792 100%);
  color: #eae0cf;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.85rem;
  margin-right: 14px;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(33, 52, 72, 0.25);
}

.item-content {
  flex: 1;
  color: #213448;
}

.item-content strong {
  color: #547792;
  font-weight: 700;
}

.bullet-item {
  display: flex;
  align-items: flex-start;
  padding: 10px 14px;
  margin: 6px 0;
  background: rgba(148, 180, 193, 0.1);
  border-radius: 8px;
  border-left: 3px solid #94b4c1;
  transition: all 0.25s ease;
}

.bullet-item:hover {
  background: rgba(148, 180, 193, 0.18);
  transform: translateX(4px);
}

.bullet-icon {
  color: #547792;
  font-size: 18px;
  margin-right: 8px;
  margin-top: 2px;
}

.analysis-paragraph {
  margin: 12px 0;
  padding: 12px 16px;
  background: white;
  border-radius: 8px;
  color: #213448;
  border: 1px solid rgba(84, 119, 146, 0.08);
}

.analysis-paragraph strong {
  color: #547792;
}

/* ===== Footer ===== */
.footer-custom {
  background: linear-gradient(135deg, #213448 0%, #2d4a5e 100%) !important;
  color: #eae0cf;
}

.footer-logo {
  height: 28px;
  width: 28px;
}

/* ===== Responsive ===== */
@media (max-width: 960px) {
  .hero-section {
    padding: 40px 0 30px;
  }

  .hero-subtitle {
    margin-left: auto;
    margin-right: auto;
  }
}

@media (max-width: 600px) {
  .hero-section {
    padding: 30px 0 20px;
  }

  .section-header {
    font-size: 0.95rem;
    padding: 12px 14px;
  }

  .analysis-item {
    padding: 10px 12px;
  }

  .item-number {
    min-width: 26px;
    height: 26px;
    font-size: 0.8rem;
  }
}

/* ===== Animations ===== */
.v-card {
  transition: all 0.3s ease;
}

.v-btn {
  transition: all 0.25s ease;
}
</style>
