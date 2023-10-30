<script lang="ts">
  import { Router, Link, Route } from "svelte-routing";
  import Root from "./routes/Root.svelte";
  import Login from "./routes/Login.svelte";
  import Signup from "./routes/Signup.svelte";
  import Home from "./routes/Home.svelte";
  import UserSettings from "./routes/UserSettings.svelte";
  import EmployeeProduct from "./routes/EmployeeProduct.svelte";
  import ShoppingCart from "./routes/ShoppingCart.svelte";
  import Navbar from "./lib/components/Navbar.svelte";
  import Footer from "./lib/components/Footer.svelte";
  import EmBrowse from "./routes/EmBrowse.svelte";

  const routes = [
    { path: "/", component: Root },
    { path: "/login", component: Login },
    { path: "/signup", component: Signup },
    { path: "/home", component: Home },
    { path: "/settings", component: UserSettings },
    { path: "/cart", component: ShoppingCart },
    { path: "/employee-product", component: EmployeeProduct },
    { path: "/employee-browse", component: EmBrowse }
  ];

  export let url = "";
  let currentUrl = window.location.pathname;
</script>

<html lang="en" data-theme="lemonade">
  <main>
    <Router {url} >
      <Navbar />
      <div class="wrapper">
        {#if currentUrl == "/"}
          <div class="flex justify-center mt-6"> 
            <h1> Welcome to OGO!</h1>
          </div>
          <div class="flex justify-center mt-6"> 
            <nav>
              <a href="/login">Login</a>
              <a href="/signup">Signup</a>
            </nav>
          </div>
        {/if}
        <div class="content nav-container">
          <Route path="/login" component={Login} />
          <Route path="/signup" component={Signup} />
          <Route path="/home" component={Home} />
          <Route path="/settings" component={UserSettings} />
          <Route path="/cart" component={ShoppingCart} />
          <Route path="/employee-product" component={EmployeeProduct} />
          <Route path="/employeesbrowser" component={EmBrowse} />
        </div>
      </div>
      <Footer />
    </Router>
  </main>
</html>

<style>
  @import 'tailwindcss/base';
  @import 'tailwindcss/components';
  @import 'tailwindcss/utilities';

  /* Additional CSS to make the footer sticky */
  .wrapper {
    display: flex;
    flex-direction: column;
    min-height: 50vh;
  }
  .content {
    flex: 1;
  }
  .nav-container {
    position: relative; /* Ensure it's a positioned element */
    z-index: 1; /* Set a higher z-index to appear above the content */
  }
</style>
