<script lang="ts">
  import { Router, Link, Route } from "svelte-routing";
  import Root from "./routes/Root.svelte";
  import Login from "./routes/Login.svelte";
  import Signup from "./routes/Signup.svelte";
  import UserSettings from "./routes/UserSettings.svelte";
  import EmployeeProduct from "./routes/EmployeeProduct.svelte";
  import ShoppingCart from "./routes/ShoppingCart.svelte";
  import Navbar from "./lib/components/Navbar.svelte";
  import Footer from "./lib/components/Footer.svelte";
  import EmMaps from "./routes/EmployeeMaps.svelte";
  import Browse from "./routes/Browse.svelte";
  import Payment from "./routes/Payment.svelte";
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
    { path: "/payment", component: Payment},
    { path: "/employee-user-management", component: EmployeeUserManagement},
  ];
  export let url = "";
  let currentUrl = window.location.pathname;
</script>

<html lang="en" data-theme="lemonade">
  <main>
    <Router {url}>
      {#if currentUrl == "/"}
        <Navbar/>
          <div class="flex justify-center mt-6"> 
            <h1 class="text-6xl mt-4"> Welcome to OGO!</h1>
          </div>
          <div class="flex justify-center mt-6"> 
            <nav>
              <div class="mb- grid text-center lg:max-w-5xl lg:w-full lg:mb-0 lg:grid-cols-2 lg:text-center justify-between p-28">
                <a
                  href="/login"
                  class="group rounded-lg border border-transparent px-5 py-4 hover:bg-[#6a994e] transition-colors duration-300 ease-in-out  "
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <h2 class={`mb-3 text-2xl font-neutral`}>
                    Login{' '}
                  </h2>
                  <p class={`m-0 max-w-[100ch] text-sm opacity-50 sm:text-center text-center`}>
                    Login to access the future!
                  </p>
                </a>
        
                <a
                  href="/signup"
                  class="group rounded-lg border border-transparent px-5 py-4 hover:bg-[#6a994e] hovor:color-white transition-colors duration-300 ease-in-out  "
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <h2 class={`mb-3 text-2xl font-neutral`}>
                    Signup{' '}
                  </h2>
                  <p class={`m-0 max-w-[100ch] text-sm opacity-50 sm:text-center text-center`}>
                    Sign up to start experiencing the future!
                  </p>
                </a>
              </div>
            </nav>
          </div>
        {/if}
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