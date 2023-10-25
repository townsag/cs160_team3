//
// User Authentication
//

// Signup
export async function signup(username: string, password: string, address: string = "") {
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
            headers: {
                'Content-Type': "application/json"
            },
            body: JSON.stringify({
                "username": username,
                "password": password,
                "address": address
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
            headers: {
                'Content-Type': "application/json"
            },
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
        const logoutResponse = await fetch("/logout", {
            method: "GET"
        });

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
export async function updateUser(username: string, password: string, address: string) {
    try {
        const updateUserResponse = await fetch("/updateUser", {
            method: "POST",
            headers: {
                'Content-Type': "application/json"
            },
            body: JSON.stringify({
                "username": username,
                "password": password,
                "address": address
            })
        });

        if (!updateUserResponse.ok) {
            const errorMessage = await updateUserResponse.text();
            console.error("Failed to update user:", errorMessage);
            return { success: false, message: errorMessage };
        }

        const updateResult = await updateUserResponse.json();

        if (updateResult && updateResult.success) {
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
        const getUserResponse = await fetch("/getUser", {
            method: "GET"
        });

        if (!getUserResponse.ok) {
            const errorMessage = await getUserResponse.text();
            console.error("Failed to get current user:", errorMessage);
            return { success: false, message: errorMessage };
        }

        const user = await getUserResponse.json();

        if (user && user.user_id) {
            return { success: true, message: "Current user retrieved", user };
        } else {
            return { success: false, message: "Current user data is incomplete." };
        }
    } catch (error) {
        console.error("An error occurred fetching current user:", error);
        return { success: false, message: "An error occurred fetching current user." };
    }
}
