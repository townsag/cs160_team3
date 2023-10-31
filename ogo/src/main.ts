import './app.css'
import App from './App.svelte'

const targetElement = document.getElementById('app');

if (!targetElement) {
  throw new Error("Couldn't find target element with ID 'app'");
}

const app = new App({
  target: targetElement,
})

export default app
