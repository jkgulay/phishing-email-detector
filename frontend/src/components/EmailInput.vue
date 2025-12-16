<template>
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
        :model-value="modelValue"
        @update:model-value="$emit('update:modelValue', $event)"
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
            :disabled="!modelValue || loading"
            @click="$emit('analyze')"
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
            @click="$emit('load-example')"
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
</template>

<script setup>
defineProps({
  modelValue: String,
  loading: Boolean,
});

defineEmits(["update:modelValue", "analyze", "load-example"]);
</script>

<style scoped>
.input-card {
  background: rgba(255, 255, 255, 0.9) !important;
  border: 1px solid rgba(148, 180, 193, 0.4);
  border-radius: 12px !important;
  backdrop-filter: blur(10px);
}

.email-input :deep(.v-field) {
  border-radius: 8px;
}

.analyze-btn {
  text-transform: none;
  letter-spacing: 0.5px;
  font-weight: 600;
}
</style>
