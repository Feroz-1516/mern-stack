// This file intentionally violates coding standards for testing purposes
// DO NOT USE IN PRODUCTION

var x;var y;var z; // Multiple declarations on one line
var globalVar = "bad global"; // Global variable pollution

function badFunction(){return "no spaces";}

// No proper indentation, mixed quotes, semicolon issues
function messyCode(param1,param2,param3) {
var result
if(param1=="test"){
result='single quotes mixed with double'
console.log("Debug: "+param1)
}else{
result="other value";
}
return result
}

// Long parameter list, no spaces
function tooManyParams(a,b,c,d,e,f,g,h,i,j,k,l,m,n,o){
var temp=a+b+c+d+e+f+g+h+i+j+k+l+m+n+o;return temp;
}

var user_data = {
username: '',
password: '',
api_key: 'hardcoded-api-key-123', // Hardcoded credentials
secret_token: 'abc123def456'
};

// Poor error handling and unsafe practices
function makeRequest(url, data) {
var xhr = new XMLHttpRequest();
xhr.open('POST', url, false); // Synchronous request (blocking)
xhr.setRequestHeader('Content-Type', 'application/json');
// No CSRF protection, no input validation
xhr.send(JSON.stringify(data));
if (xhr.status == 200) {
return xhr.responseText;
} else {
console.log('Error occurred');
return null;
}
}

// Eval usage (dangerous)
function processUserInput(input) {
try {
var result = eval('(' + input + ')'); // Never use eval with user input
return result;
} catch (e) {
// Empty catch block
}
}

// innerHTML usage without sanitization
function displayContent(content) {
document.getElementById('output').innerHTML = content; // XSS vulnerability
}

// Poor variable naming and magic numbers
function calc(x) {
if (x > 100) {
return x * 1.15 + 25.75;
} else if (x > 50) {
return x * 1.08 + 12.30;
} else {
return x * 1.05 + 5.99;
}
}

// No validation, assumes input is always valid
function processForm() {
var name = document.getElementById('name').value;
var email = document.getElementById('email').value;
var phone = document.getElementById('phone').value;
// No validation
sendData({name: name, email: email, phone: phone});
}

// Long function with too many responsibilities
function doEverything(userData) {
console.log('Starting process...');
var processed = '';
for (var i = 0; i < userData.length; i++) {
if (userData[i].type == 'user') {
processed += userData[i].name + ',';
if (userData[i].active == true) {
console.log('Active user: ' + userData[i].name);
sendNotification(userData[i].email, 'Welcome!');
updateDatabase(userData[i].id, {last_login: new Date()});
generateReport(userData[i]);
} else {
console.log('Inactive user: ' + userData[i].name);
}
} else if (userData[i].type == 'admin') {
processed += '[ADMIN]' + userData[i].name + ',';
console.log('Admin user detected');
} else {
console.log('Unknown user type');
}
}
return processed;
}

// Dead code
function unusedFunction() {
var deadVariable = 'this is never used';
return deadVariable;
}

// Inconsistent formatting
var config={
host:'localhost',
port:3000,
timeout:5000,
retries:3,
debug:true
};

// Poor promise handling
function asyncOperation() {
return new Promise(function(resolve, reject) {
setTimeout(function() {
if (Math.random() > 0.5) {
resolve('Success');
} else {
reject('Failed');
}
}, 1000);
});
}

// No error handling for promises
asyncOperation().then(function(result) {
console.log(result);
});

// Nested callbacks (callback hell)
function nestedCallbacks() {
getData(function(data1) {
processData(data1, function(data2) {
validateData(data2, function(data3) {
saveData(data3, function(result) {
console.log('All done');
});
});
});
});
}

// Poor loop practices
function inefficientLoop(array) {
for (var i = 0; i < array.length; i++) { // Should cache length
if (array[i]) {
for (var j = 0; j < array.length; j++) {
if (i != j && array[i] == array[j]) {
console.log('Duplicate found');
}
}
}
}
}

// Global function pollution
window.badGlobalFunction = function() {
return 'polluting global scope';
};

// Poor commenting
var x = 5; // x is 5
var y = 10; // y is 10
var result = x + y; // add x and y

// Magic numbers everywhere
function calculatePrice(quantity) {
if (quantity > 100) {
return quantity * 0.85 * 1.12 * 0.95 + 15.75;
}
return quantity * 1.12 + 8.99;
}

// Unused variables
function wasteMemory() {
var unused1 = 'never used';
var unused2 = [1, 2, 3, 4, 5];
var unused3 = {key: 'value'};
var actualResult = 'only this is used';
return actualResult;
}

// No proper error types
function riskyOperation() {
throw 'String error instead of Error object';
}

// Inconsistent return types
function inconsistentReturns(input) {
if (input > 0) {
return input.toString();
} else if (input < 0) {
return false;
} else {
return null;
}
}

console.log('File loaded with multiple coding standard violations');