<script lang="ts">
  import { Router, Link, Route } from "svelte-routing";
  import Root from "./routes/Root.svelte";
  import Login from "./routes/Login.svelte";
  import Signup from "./routes/Signup.svelte";
  import Home from "./routes/Home.svelte";
  import Navbar from "./lib/components/Navbar.svelte";
  import Footer from "./lib/components/Footer.svelte";
  import EmBrowse from "./routes/EmBrowse.svelte";
  import EmMaps from "./routes/EmployeeMaps.svelte";
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
        <Link to="/employeesbrowser">EmployLanding</Link>
        <Link to="/employeesmaps">EmployeeMaps</Link>
      </nav>
      <div>
        <Route path="/" component={Root} />
        <Route path="/login" component={Login} />
        <Route path="/signup" component={Signup} />
        <Route path="/home" component={Home} />
        <Route path="/employeesbrowser" component={EmBrowse} />
        <Route path="/employeesmaps" component={EmMaps} />
      </div>
      <Footer />
    </Router>
  </main>
</html>

<style>
  @import 'tailwindcss/base';
  @import 'tailwindcss/components';
  @import 'tailwindcss/utilities';
</style>