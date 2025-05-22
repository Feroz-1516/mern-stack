const express = require('express');
const vm = require('vm');

const app = express();
app.use(express.json());

app.post('/run-code', function (req, res) {
    const userInput = req.body.context; // untrusted input from req.body
    const code = req.body.code; // user-provided code to run

    const context = { userContext: userInput }; // context directly using req.body
    vm.createContext(context);

    try {
        const result = vm.runInContext(code, context); // unsafe: code execution in user-defined context
        res.send({ result });
    } catch (err) {
        res.status(500).send({ error: err.toString() });
    }
});

app.get('/run-query', function (req, res) {
    const context = {
        data: req.query.data // untrusted input from req.query
    };
    const code = 'data + " evaluated"'; // code string to evaluate

    vm.createContext(context);
    const result = vm.runInContext(code, context); // unsafe execution
    res.send({ result });
});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});
