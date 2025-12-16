<template>
  <v-card class="ai-card mb-6" elevation="0">
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
            <div class="text-h6 font-weight-bold">AI Expert Analysis</div>
            <div class="d-flex align-center">
              <v-icon icon="mdi-robot" size="14" class="mr-1"></v-icon>
              <span class="text-caption">Powered by GPT-4o-mini</span>
            </div>
          </v-col>
        </v-row>
      </div>

      <!-- AI Content -->
      <div class="ai-content pa-4 pa-md-5">
        <div class="ai-analysis-container" v-html="formattedAnalysis"></div>
      </div>

      <!-- Actions -->
      <v-divider></v-divider>
      <div class="pa-4 d-flex flex-wrap ga-2">
        <v-btn
          variant="tonal"
          color="#547792"
          prepend-icon="mdi-content-copy"
          size="small"
          @click="$emit('copy')"
        >
          Copy
        </v-btn>
        <v-btn
          variant="tonal"
          color="#213448"
          prepend-icon="mdi-refresh"
          size="small"
          @click="$emit('reset')"
        >
          New Analysis
        </v-btn>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  analysis: String,
});

defineEmits(["copy", "reset"]);

const formattedAnalysis = computed(() => {
  if (!props.analysis) return "";

  let html = '<div class="analysis-wrapper">';
  const lines = props.analysis.split("\n");
  let listItems = [];
  let pendingNumber = null;

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

  lines.forEach((line) => {
    line = line.trim();
    if (!line) return;

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

    // Check if line is just a number
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

    // Numbered items on same line
    const numMatch = line.match(/^(\d+)\.?\s+(.+)$/);
    if (numMatch) {
      const originalNum = parseInt(numMatch[1], 10);
      const content = numMatch[2]
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/:(.*?):/g, "<em>$1</em>");
      listItems.push({ num: originalNum, content });
      return;
    }

    // Bullet points
    const bulletMatch = line.match(/^\s*[-•*]\s+(.+)$/);
    if (bulletMatch) {
      flushList();
      const content = bulletMatch[1].replace(
        /\*\*(.*?)\*\*/g,
        "<strong>$1</strong>"
      );
      html += `
        <div class="bullet-item">
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
});
</script>

<style scoped>
.ai-card {
  background: rgba(255, 255, 255, 0.95) !important;
  border-radius: 12px !important;
  border: 2px solid rgba(84, 119, 146, 0.3);
  overflow: hidden;
}

.ai-header {
  background: linear-gradient(
    135deg,
    rgba(84, 119, 146, 0.1) 0%,
    rgba(148, 180, 193, 0.1) 100%
  );
  border-bottom: 1px solid rgba(84, 119, 146, 0.2);
}

.ai-content {
  max-height: 600px;
  overflow-y: auto;
}

.ai-content::-webkit-scrollbar {
  width: 8px;
}

.ai-content::-webkit-scrollbar-track {
  background: rgba(148, 180, 193, 0.1);
  border-radius: 4px;
}

.ai-content::-webkit-scrollbar-thumb {
  background: rgba(84, 119, 146, 0.3);
  border-radius: 4px;
}

.ai-content::-webkit-scrollbar-thumb:hover {
  background: rgba(84, 119, 146, 0.5);
}

.ai-analysis-container {
  color: #213448;
  line-height: 1.7;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1.1rem;
  font-weight: 700;
  color: #213448;
  margin: 24px 0 16px 0;
  padding: 12px;
  background: linear-gradient(
    135deg,
    rgba(148, 180, 193, 0.15) 0%,
    rgba(234, 224, 207, 0.15) 100%
  );
  border-left: 4px solid #547792;
  border-radius: 4px;
}

.section-header:first-child {
  margin-top: 0;
}

.section-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: #547792;
  color: white;
  border-radius: 50%;
  font-size: 16px;
}

.analysis-list {
  margin: 16px 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.analysis-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  background: rgba(148, 180, 193, 0.05);
  border-radius: 8px;
  border-left: 3px solid #94b4c1;
  transition: all 0.2s ease;
}

.analysis-item:hover {
  background: rgba(148, 180, 193, 0.1);
  transform: translateX(4px);
}

.item-number {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  min-width: 28px;
  min-height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #547792;
  color: white;
  border-radius: 50%;
  font-weight: 700;
  font-size: 0.875rem;
  margin-top: 2px;
}

.item-content {
  flex: 1;
  color: #213448;
  display: flex;
  align-items: center;
  min-height: 28px;
}

.item-content strong {
  color: #213448;
  font-weight: 600;
}

.bullet-item {
  margin: 8px 0;
  padding: 10px 12px;
  background: rgba(148, 180, 193, 0.05);
  border-radius: 6px;
  border-left: 3px solid #94b4c1;
}

.bullet-item span {
  line-height: 1.7;
  color: #213448;
}

.analysis-paragraph {
  margin: 12px 0;
  color: #213448;
  line-height: 1.7;
}

.analysis-paragraph strong {
  color: #213448;
  font-weight: 600;
}

@media (max-width: 600px) {
  .section-header {
    font-size: 1rem;
    padding: 10px;
  }

  .section-icon {
    width: 28px;
    height: 28px;
    font-size: 14px;
  }

  .analysis-item {
    padding: 10px;
  }

  .item-number {
    width: 24px;
    height: 24px;
    font-size: 0.75rem;
  }
}
</style>
