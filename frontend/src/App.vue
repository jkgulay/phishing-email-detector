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
      <HeroSection />

      <v-container class="py-8" style="max-width: 1000px">
        <EmailInput
          v-model="emailText"
          :loading="loading"
          @analyze="analyzeEmail"
          @load-example="loadExample"
        />

        <v-expand-transition>
          <div v-if="predictionResult">
            <ResultCard
              :result="predictionResult"
              :loading-a-i="loadingAI"
              :has-ai-analysis="!!aiAnalysis"
              @get-ai-analysis="getAIAnalysis"
            />

            <v-expand-transition>
              <AIAnalysisCard
                v-if="aiAnalysis"
                :analysis="aiAnalysis.analysis"
                @copy="copyAnalysis"
                @reset="resetAnalysis"
              />
            </v-expand-transition>
          </div>
        </v-expand-transition>

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

    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="2000">
      {{ snackbarText }}
    </v-snackbar>
  </v-app>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import HeroSection from "./components/HeroSection.vue";
import EmailInput from "./components/EmailInput.vue";
import ResultCard from "./components/ResultCard.vue";
import AIAnalysisCard from "./components/AIAnalysisCard.vue";

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

<style>
@import "./styles/app.css";
</style>
