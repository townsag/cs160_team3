//
// User Authentication
//

// Signup
export async function signup(username: string, password: string, address: string = "", is_admin: Boolean) {
    try {
        // Check length constraints on username and password
        if (username.length === 0 || password.length === 0) {
            return {
                success: false,
                message: "Cannot have a blank username or password."
            };
        } else if (username.length > 20 || password.length > 20) {
            return {
                success: false,
                message: "Username and password must be less than 20 characters."
            };
        }

        const signupResponse = await fetch("/signup", {
            method: "POST",
            headers: { 'Content-Type': "application/json" },
            body: JSON.stringify({
                "username": username,
                "password": password,
                "address": address,
                "is_admin": is_admin
            })
        });

        const responseText = await signupResponse.text();

        if (signupResponse.ok) {
            // Return name of current user
            const currentUserResponse = await fetch("/getUser", { method: "GET" });
            const currentUser = await currentUserResponse.json();
            return { success: true, message: "Successfully signed up.", user: currentUser };
        } else {
            console.error("Error signing up:", responseText);
            return { success: false, message: responseText };
        }
    } catch (error) {
        console.error("An error occurred during signup:", error);
        return { success: false, message: "An error occurred during signup." };
    }
}

// Login
export async function login(username: string, password: string) {
    try {
        const loginResponse = await fetch("/login", {
            method: "POST",
            headers: { 'Content-Type': "application/json" },
            body: JSON.stringify({
                "username": username,
                "password": password,
            })
        });

        const responseText = await loginResponse.text();

        if (loginResponse.ok) {
            if (responseText === "Success") {
                return { success: true, message: "Successfully logged in." };
            } else {
                return { success: false, message: responseText };
            }
        } else {
            console.error("Failed to login:", responseText);
            return { success: false, message: responseText };
        }
    } catch (error) {
        console.error("An error occurred during login:", error);
        return { success: false, message: "An error occurred during login." };
    }
}

// Logout
export async function logout() {
    try {
        const logoutResponse = await fetch("/logout", { method: "GET" });

        const responseText = await logoutResponse.text();

        if (logoutResponse.ok) {
            console.log(responseText);
            return { success: true, message: responseText };
        } else {
            console.error("Failed to logout:", responseText);
            return { success: false, message: responseText };
        }
    } catch (error) {
        console.error("An error occurred during logout:", error);
        return { success: false, message: "An error occurred during logout." };
    }
}

// Update User
export async function updateUser(data: any) {
    try {
        const updateUserResponse = await fetch("/updateUser", {
            method: "POST",
            headers: { 'Content-Type': "application/json" },
            body: JSON.stringify(data)
        });

        if (!updateUserResponse.ok) {
            const errorMessage = await updateUserResponse.text();
            console.error("Failed to update user:", errorMessage);
            return { success: false, message: errorMessage };
        }

        const updateResult = await updateUserResponse.text();

        if (updateResult) {
            return { success: true, message: "User updated successfully." };
        } else {
            return { success: false, message: "Failed to update user." };
        }
    } catch (error) {
        console.error("An error occurred updating the user:", error);
        return { success: false, message: "An error occurred updating the user." };
    }
}

// Get User
export async function getCurrentUser() {
    try {
        const getUserResponse = await fetch("/getUser", { method: "GET" });

        if (!getUserResponse.ok) {
            const errorMessage = await getUserResponse.text();
            console.error("Failed to get current user:", errorMessage);
            return { success: false, message: errorMessage };
        }

        const user = await getUserResponse.json();

        if (user && user.user_id) {
            return { success: true, message: "Current user retrieved", user: user };
        } else {
            return { success: false, message: "Current user data is incomplete." };
        }
    } catch (error) {
        console.error("An error occurred fetching current user:", error);
        return { success: false, message: "An error occurred fetching current user." };
    }
}

//
// Shopping Cart
//

// Get Cart
export async function getCart() {
    try {
        const getCartResponse = await fetch("/getCart", { method: "GET" })

        if (!getCartResponse.ok) {
            const errorMessage = await getCartResponse.text();
            console.error("Failed to get cart:", errorMessage);
            return { success: false, message: errorMessage };
        }

        const cart = await getCartResponse.json();
        
        // Check items in the cart
        if (cart && Object.keys(cart).length > 0) {
            return { success: true, message: "Cart retrieved successfully", cart: cart };
        } else {
            return { success: false, message: "There are no items in the cart." };
        }
    } catch (error) {
        console.error("An error occurred fetching the cart:", error);
        return { success: false, message: "An error occurred fetching the cart." };
    }
}

// Update Cart Item
export async function updateCartItem(cartItemId: number, productId: number, quantity: number) {
    try {
        const updateCartItemResponse = await fetch("/updateCartItem", {
            method: "POST",
            headers: { 'Content-Type': "application/json" },
            body: JSON.stringify({
                "cart_item_id": cartItemId,
                "product_id": productId,
                "quantity": quantity
            })
        });

        if (!updateCartItemResponse.ok) {
            const errorMessage = await updateCartItemResponse.text();
            console.error("Failed to update cart item:", errorMessage);
            return { success: false, message: errorMessage };
        }

        const updateResult = await updateCartItemResponse.json();

        if (updateResult) {
            return { success: true, message: "Cart item updated successfully." };
        } else {
            return { success: false, message: "Failed to update cart item." };
        }
    } catch (error) {
        console.error("An error occurred updating the cart item:", error);
        return { success: false, message: "An error occurred updating the cart item." };
    }
}

// Remove Cart Item
export async function removeCartItem(cartItemId: number) {
    try {
        const removeCartItemResponse = await fetch("/removeCartItem", {
            method: "POST",
            headers: { 'Content-Type': "application/json" },
            body: JSON.stringify({
                "cart_item_id": cartItemId
            })
        });

        const responseText = await removeCartItemResponse.text();

        if (removeCartItemResponse.ok && responseText === "Success") {
            return { success: true, message: "Cart item removed successfully." };
        } else {
            console.error("Failed to remove cart item:", responseText);
            return { success: false, message: responseText };
        }
    } catch (error) {
        console.error("An error occurred removing the cart item:", error);
        return { success: false, message: "An error occurred removing the cart item." };
    }
}
