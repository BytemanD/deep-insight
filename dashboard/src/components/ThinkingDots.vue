<template>
  <span class="thinking-dots">
    <span>.</span><span>.</span><span>.</span>
  </span>
</template>

<style scoped>
.thinking-dots span {
  animation: dotPulse 1.4s infinite;
  font-size: 1.5rem;
  line-height: 0;
  opacity: 0;
}

.thinking-dots span:nth-child(1) {
  animation-delay: 0s;
}

.thinking-dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.thinking-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes dotPulse {

  0%,
  60%,
  100% {
    opacity: 0;
  }

  30% {
    opacity: 1;
  }
}
</style>
