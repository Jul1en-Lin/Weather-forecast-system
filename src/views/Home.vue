<template>
  <OracleLayout>
    <div class="home-page">
      <div class="content-wrapper">
        <div class="hero-section">
          <div class="hero-content">
            <div class="hero-icon">
              <span class="icon-large">🌤️</span>
            </div>
            <h1 class="main-title">大语言模型气象业务应用平台</h1>
            <p class="main-subtitle">
              基于先进的大语言模型技术，为气象业务提供智能化解决方案
            </p>
          </div>
        </div>
      </div>
    </div>
  </OracleLayout>
</template>

<script setup lang="ts">
import OracleLayout from '../layouts/OracleLayout.vue'
</script>

<style scoped>
.home-page {
  min-height: 100vh;
}

.content-wrapper {
  padding: 40px;
  max-width: 1400px;
  margin: 0 auto;
}

.hero-section {
  background: transparent;
  padding: 60px 40px;
}

.hero-content {
  text-align: center;
}

.hero-icon {
  margin-bottom: 30px;
}

.icon-large {
  font-size: 80px;
  animation: float 3s ease-in-out infinite;
  display: inline-block;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-15px);
  }
}

.main-title {
  font-size: 36px;
  font-weight: 700;
  color: #1753b3;
  margin: 0 0 16px 0;
  letter-spacing: 0;
  line-height: 1.2;
  text-shadow: 0 2px 4px rgba(255, 255, 255, 0.5);
}

.main-subtitle {
  font-size: 18px;
  color: #1d1d1f;
  margin: 0 auto 40px;
  max-width: 600px;
  line-height: 1.6;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.5);
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 20px;
  }

  .main-title {
    font-size: 28px;
  }

  .hero-section {
    padding: 40px 20px;
  }
}
</style>
