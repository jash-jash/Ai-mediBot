const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});

// Signup Function
function signup() {
    const name = document.querySelector('.sign-up input[type="text"]').value;
    const email = document.querySelector('.sign-up input[type="email"]').value;
    const password = document.querySelector('.sign-up input[type="password"]').value;
    
    if (name && email && password) {
        localStorage.setItem(email, JSON.stringify({ name, password }));
        alert("Account created successfully! You can now sign in.");
        container.classList.remove("active"); // Switch to sign-in form
    } else {
        alert("Please fill in all fields.");
    }
}

// Login Function
function login() {
    const email = document.querySelector('.sign-in input[type="email"]').value;
    const password = document.querySelector('.sign-in input[type="password"]').value;
    
    const user = localStorage.getItem(email);
    if (user) {
        const userData = JSON.parse(user);
        if (userData.password === password) {
            alert("Login successful!");
            window.open('dashboard.html', '_blank'); // Redirect to a new page
        } else {
            alert("Password is incorrect. Please try again.");
        }
    } else {
        alert("User not found. Please sign up.");
    }
}

// Forgot Password Function
function forgotPassword(event) {
    event.preventDefault(); // Prevent page reload if it's a link

    const email = document.querySelector('.sign-in input[type="email"]').value;

    if (!email) {
        alert("Please enter your email.");
        return;
    }

    const user = localStorage.getItem(email);
    if (user) {
        const userData = JSON.parse(user);
        const newPassword = prompt("Enter a new password:");

        if (newPassword) {
            userData.password = newPassword;
            localStorage.setItem(email, JSON.stringify(userData));
            alert("Password updated successfully! Please sign in with your new password.");
        }
    } else {
        alert("Email not found. Please sign up first.");
    }
}

// Attach functions to buttons
document.querySelector('.sign-up button').addEventListener('click', signup);
document.querySelector('.sign-in button').addEventListener('click', login);

// Attach function to "Forgot Password?" link
const forgotPasswordLink = document.querySelector('.sign-in a[href="#"]');
if (forgotPasswordLink) {
    forgotPasswordLink.addEventListener('click', forgotPassword);
}
