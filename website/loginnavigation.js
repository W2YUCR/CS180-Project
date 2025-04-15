import React from 'react';

function LoginNavigationBar() {
    return (
        <div class="topnav">
            <div class="nav-left">
                <a>Home</a>
                <a>Create</a>
                <a>Your Flashcards</a>
                <a>Quiz</a>
            </div>
            <div class="nav-right">
                <a href="home.html">Logout</a>
            </div>
        </div>
    );
}

export default LoginNavigationBar;