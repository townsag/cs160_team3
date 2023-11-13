<script lang="ts">
  import { Router, Link, Route } from "svelte-routing";
  import Root from "./routes/Root.svelte";
  import Login from "./routes/Login.svelte";
  import Signup from "./routes/Signup.svelte";
  import UserSettings from "./routes/UserSettings.svelte";
  import EmployeeProduct from "./routes/EmployeeProduct.svelte";
  import ShoppingCart from "./routes/ShoppingCart.svelte";
  //import Navbar from "./lib/components/Navbar.svelte";
  import Footer from "./lib/components/Footer.svelte";
  import EmMaps from "./routes/EmployeeMaps.svelte";
  import Browse from "./routes/Browse.svelte";
  import CustomerOrderHistory from "./routes/CustomerOrderHistory.svelte";
  import ItemViewer from "./routes/ItemViewer.svelte";
  import EmployeeUserManagement from "./routes/EmployeeUserManagement.svelte"
  import './app.css';

  const routes = [
    { path: "/", component: Root },
    { path: "/login", component: Login },
    { path: "/signup", component: Signup },
    { path: "/settings", component: UserSettings },
    { path: "/cart", component: ShoppingCart },
    { path: "/employee-product", component: EmployeeProduct },
    { path: "/browse", component: Browse },
    { path: "/employeesmaps", component: EmMaps},
    { path: "/customer-order-history", component: CustomerOrderHistory},
    { path: "/itemView/:productId", component: ItemViewer},
    { path: "/employee-user-management", component: EmployeeUserManagement},
  ];

  export let url = "";
</script>

<html lang="en" data-theme="lemonade">
  <main>
    <Router {url}>
      
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