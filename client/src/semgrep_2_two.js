// trojan_source_example.js

function checkAccess(user) {
    let isAdmin = false;

    // This line uses a RIGHT-TO-LEFT OVERRIDE (U+202E) to hide a malicious condition:
    // It *appears* as a harmless comment, but actually contains:
    // if (user === 'admin') isAdmin = true;

    // ‮ } ⁦if (user === 'admin')⁩ ⁦/*

    console.log("User is admin:", isAdmin);

    if (isAdmin) {
        console.log("Access granted to admin features.");
    } else {
        console.log("Access denied.");
    }
}

checkAccess('guest');
