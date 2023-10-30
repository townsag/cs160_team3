<script lang="ts">
    import { Router, Link, Route } from "svelte-routing";
    import Root from "./Root.svelte";
    import Login from "./Login.svelte";
    import Signup from "./Signup.svelte";
    import Home from "./Home.svelte";
    import UserSettings from "./UserSettings.svelte";
    import EmployeeProduct from "./EmployeeProduct.svelte";
    import ShoppingCart from "./ShoppingCart.svelte";
    import Navbar from "../lib/components/Navbar.svelte";
    import Footer from "../lib/components/Footer.svelte";
    import EmBrowse from "./EmBrowse.svelte";
  
    export let url = "";
  </script>
  
  <html lang="en" data-theme="lemonade">
    <main>
      <Router {url}>
        <Navbar />
        <div class="flex justify-center mt-6"> <!-- Center the links -->
          <nav>
            <Link to="/">Root</Link>
            <Link to="/login">Login</Link>
            <Link to="/signup">Signup</Link>
            <Link to="/home">Home</Link>
            <Link to="/cart">Cart</Link>
            <Link to="/employee-product">EmployeeProduct</Link>
            <Link to="/employeesbrowser">EmployLanding</Link>
          </nav>
        </div>
        <div>
          <Route path="/" component={Root} />
          <Route path="/login" component={Login} />
          <Route path="/signup" component={Signup} />
          <Route path="/home" component={Home} />
          <Route path="/settings" component={UserSettings} />
          <Route path="/cart" component={ShoppingCart} />
          <Route path="/employee-product" component={EmployeeProduct} />
          <Route path="/employeesbrowser" component={EmBrowse} />
        </div>
        <Footer />
      </Router>
    </main>
  </html>
  
  <style>
    @import 'tailwindcss/base';
    @import 'tailwindcss/components';
    @import 'tailwindcss/utilities';
  
    /* Additional CSS to center the links */
    .flex {
      display: flex;
    }
  
    .justify-center {
      justify-content: center;
    }
  
    .mt-6 {
      margin-top: 1.5rem;
    }
  </style>
  