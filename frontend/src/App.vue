<template>
  <v-app>
    <v-app-bar color="primary" prominent>
      <v-app-bar-title class="text-h5 font-weight-bold">
        <v-icon icon="mdi-shield-check" class="mr-2"></v-icon>
        Phishing Email Detector
      </v-app-bar-title>
    </v-app-bar>

    <v-main>
      <v-container class="py-8">
        <v-row justify="center">
          <v-col cols="12" md="10" lg="8">
            <!-- Hero Section -->
            <v-card class="mb-6" elevation="0">
              <v-card-text class="text-center">
                <v-icon
                  icon="mdi-email-alert"
                  size="64"
                  color="primary"
                  class="mb-4"
                ></v-icon>
                <h1 class="text-h4 mb-2">Detect Phishing Emails with AI</h1>
                <p class="text-body-1 text-medium-emphasis">
                  Paste any suspicious email content below and get instant
                  analysis powered by Machine Learning and AI.
                </p>
              </v-card-text>
            </v-card>

            <!-- Input Section -->
            <v-card class="mb-6">
              <v-card-title>Email Content</v-card-title>
              <v-card-text>
                <v-textarea
                  v-model="emailText"
                  label="Paste email content here..."
                  placeholder="URGENT: Your account is suspended. Click here to verify: http://bit.ly/fake"
                  rows="8"
                  variant="outlined"
                  clearable
                  counter
                  :disabled="loading"
                ></v-textarea>

                <div class="d-flex ga-2">
                  <v-btn
                    color="primary"
                    size="large"
                    :loading="loading"
                    :disabled="!emailText || loading"
                    @click="analyzeEmail"
                    prepend-icon="mdi-magnify-scan"
                    block
                  >
                    Analyze Email
                  </v-btn>
                  <v-btn
                    color="secondary"
                    size="large"
                    variant="outlined"
                    @click="loadExample"
                    :disabled="loading"
                    prepend-icon="mdi-file-document-outline"
                  >
                    Load Example
                  </v-btn>
                </div>
              </v-card-text>
            </v-card>

            <!-- Results Section -->
            <v-card v-if="predictionResult" class="mb-6">
              <v-card-title>
                <v-icon
                  :icon="
                    predictionResult.is_phishing
                      ? 'mdi-alert-circle'
                      : 'mdi-check-circle'
                  "
                  :color="predictionResult.is_phishing ? 'error' : 'success'"
                  class="mr-2"
                >
                </v-icon>
                Detection Result
              </v-card-title>
              <v-card-text>
                <v-alert
                  :type="predictionResult.is_phishing ? 'error' : 'success'"
                  variant="tonal"
                  prominent
                  class="mb-4"
                >
                  <div class="text-h6">{{ predictionResult.message }}</div>
                </v-alert>

                <v-row>
                  <v-col cols="12" sm="6">
                    <v-card variant="outlined">
                      <v-card-text class="text-center">
                        <div class="text-caption text-medium-emphasis mb-2">
                          Safe Probability
                        </div>
                        <v-progress-circular
                          :model-value="predictionResult.confidence.safe"
                          :color="
                            predictionResult.confidence.safe > 50
                              ? 'success'
                              : 'grey'
                          "
                          :size="100"
                          :width="10"
                        >
                          <span class="text-h6"
                            >{{ predictionResult.confidence.safe }}%</span
                          >
                        </v-progress-circular>
                      </v-card-text>
                    </v-card>
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-card variant="outlined">
                      <v-card-text class="text-center">
                        <div class="text-caption text-medium-emphasis mb-2">
                          Phishing Probability
                        </div>
                        <v-progress-circular
                          :model-value="predictionResult.confidence.phishing"
                          :color="
                            predictionResult.confidence.phishing > 50
                              ? 'error'
                              : 'grey'
                          "
                          :size="100"
                          :width="10"
                        >
                          <span class="text-h6"
                            >{{ predictionResult.confidence.phishing }}%</span
                          >
                        </v-progress-circular>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>

                <v-btn
                  v-if="!aiAnalysis"
                  color="info"
                  variant="outlined"
                  class="mt-4"
                  :loading="loadingAI"
                  @click="getAIAnalysis"
                  prepend-icon="mdi-robot"
                  block
                >
                  Get AI-Powered Detailed Analysis
                </v-btn>
              </v-card-text>
            </v-card>

            <!-- AI Analysis Section -->
            <v-card v-if="aiAnalysis">
              <v-card-title>
                <v-icon icon="mdi-brain" color="info" class="mr-2"></v-icon>
                AI Expert Analysis
              </v-card-title>
              <v-card-text>
                <v-alert type="info" variant="tonal" class="mb-4">
                  <div class="text-caption mb-2">Powered by GPT-4o-mini</div>
                </v-alert>
                <div
                  class="ai-analysis-content"
                  v-html="formatAnalysis(aiAnalysis.analysis)"
                ></div>
              </v-card-text>
            </v-card>

            <!-- Error Display -->
            <v-alert
              v-if="error"
              type="error"
              closable
              @click:close="error = null"
              class="mb-6"
            >
              {{ error }}
            </v-alert>
          </v-col>
        </v-row>
      </v-container>
    </v-main>

    <v-footer app class="bg-grey-lighten-3">
      <v-container>
        <div class="text-center">
          <p class="text-caption text-medium-emphasis">
            Powered by Random Forest ML Model & OpenAI GPT-4o-mini | IT113 Final
            Project
          </p>
        </div>
      </v-container>
    </v-footer>
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
    console.error("Prediction error:", err);
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
    error.value =
      err.response?.data?.error ||
      "Failed to get AI analysis. Please check your API key.";
    console.error("AI analysis error:", err);
  } finally {
    loadingAI.value = false;
  }
};

const formatAnalysis = (text) => {
  if (!text) return "";

  // Convert markdown-style formatting to HTML
  return text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\n\n/g, "</p><p>")
    .replace(/\n/g, "<br>")
    .replace(/^(.+)$/gm, "<p>$1</p>")
    .replace(/^\d+\.\s/gm, "<br>• ");
};
</script>

<style scoped>
.ai-analysis-content {
  line-height: 1.8;
  white-space: pre-wrap;
}

.ai-analysis-content :deep(p) {
  margin-bottom: 1rem;
}

.ai-analysis-content :deep(strong) {
  color: #1976d2;
  font-weight: 600;
}
</style>
