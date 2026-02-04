<template>
  <div id="app">
    <nav>
      <router-link to="/" class="logo">Teste Intuitive Care</router-link>
    </nav>
    <main>
      <router-view />
    </main>
  </div>
</template>

<style>
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #f5f6fa;
    color: #2c3e50;
  }

  #app {
    min-height: 100vh;
  }

  nav {
    background: #2c3e50;
    padding: 16px 24px;
  }

  .logo {
    color: white;
    font-size: 18px;
    font-weight: bold;
    text-decoration: none;
  }

  main {
    padding: 20px;
  }
</style>
