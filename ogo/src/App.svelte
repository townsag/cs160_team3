<script lang="ts">
  import { Router, Link, Route } from "svelte-routing";
  import Root from "./routes/root.svelte";
  import Login from "./routes/login.svelte";
  import Signup from "./routes/signup.svelte";
  import Home from "./routes/home.svelte";
  import Navbar from "./lib/components/Navbar.svelte";
  import Footer from "./lib/components/Footer.svelte";
  import './app.css';

  export let url = "";
</script>

<html lang="en" data-theme="lemonade">
  <main>
    <Router {url}>
      <Navbar />
      <nav>
        <p>quick nav for testing:</p>
        <Link to="/">Root</Link>
        <Link to="/login">Login</Link>
        <Link to="/signup">Signup</Link>
        <Link to="/home">Home</Link>
      </nav>
      <div>
        <Route path="/" component={Root} />
        <Route path="/login" component={Login} />
        <Route path="/signup" component={Signup} />
        <Route path="/home" component={Signup} />
      </div>
      <Footer />
    </Router>
  </main>
</html>

<style>

</style>