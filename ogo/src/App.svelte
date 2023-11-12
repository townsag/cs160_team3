<script lang="ts">
  import { Router, Link, Route } from "svelte-routing";
  import Root from "./routes/Login.svelte";
  import Login from "./routes/Login.svelte";
  import Signup from "./routes/Signup.svelte";
  import Home from "./routes/Home.svelte";
  import UserSettings from "./routes/UserSettings.svelte";
  import EmployeeProduct from "./routes/EmployeeProduct.svelte";
  import ShoppingCart from "./routes/ShoppingCart.svelte";
  import Navbar from "./lib/components/Navbar.svelte";
  import Footer from "./lib/components/Footer.svelte";
  import EmMaps from "./routes/EmployeeMaps.svelte";
  import Browse from "./routes/Browse.svelte";
  import CustomerOrderHistory from "./routes/CustomerOrderHistory.svelte";
  import './app.css';

  const routes = [
    { path: "/login", component: Login },
    { path: "/signup", component: Signup },
    { path: "/home", component: Home },
    { path: "/settings", component: UserSettings },
    { path: "/cart", component: ShoppingCart },
    { path: "/employee-product", component: EmployeeProduct },
    { path: "/browse", component: Browse },
    { path: "/employeesmaps", component: EmMaps},
    { path: "/customer-order-history", component: CustomerOrderHistory}
  ];

  export let url = "";
</script>

<html lang="en" data-theme="lemonade">
  <main>
    <Router {url}>
      <Navbar />
      <nav class='bg-gray-300'>
        {#each routes as route}
          <Link to={route.path}>{route.path} </Link>
        {/each}
      </nav>
      <div>
        {#each routes as route}
          <Route path={route.path} component={route.component} />
        {/each}
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