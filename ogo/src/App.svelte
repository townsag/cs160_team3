<script lang="ts">
  import { Router, Link, Route } from "svelte-routing";
  import Root from "./routes/Root.svelte";
  import Login from "./routes/Login.svelte";
  import Signup from "./routes/Signup.svelte";
  import Home from "./routes/Home.svelte";
  import Navbar from "./lib/components/Navbar.svelte";
  import Footer from "./lib/components/Footer.svelte";
  import './app.css';
  import EmployeeProduct from "./routes/EmployeeProduct.svelte";

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
        <Link to="/employee-product">EmployeeProduct</Link>
      </nav>
      <div>
        <Route path="/" component={Root} />
        <Route path="/login" component={Login} />
        <Route path="/signup" component={Signup} />
        <Route path="/home" component={Home} />
        <!-- TODO: might have to feed a product id -->
        <Route path="/employee-product" component={EmployeeProduct} />
      </div>
      <Footer />
    </Router>
  </main>
</html>

<style>

</style>