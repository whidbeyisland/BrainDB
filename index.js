var port = process.env.PORT || 3000,
    http = require('http'),
    fs = require('fs');

var log = function(entry) {
    fs.appendFileSync('/tmp/sample-app.log', new Date().toISOString() + ' - ' + entry + '\n');
};

// imports
const express = require('express');
const multer = require('multer');
const {spawn} = require('child_process');
const aws_amplify = require('aws-amplify');
const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const { signUp, confirmSignUp, signIn, signOut } = require('./auth-funcs');
const { awsconfig } = require('./aws-exports');
const upload = multer({});

// login functionality
var cur_user = '';
var cur_user_aws_id = '';
var aws_working = true;
try {
    // non-standard usage of awsconfig --- typically the entire module is imported into Auth.configure()
    aws_amplify.Auth.configure({
        accessKeyId: awsconfig.accessKeyId,
        secretAccessKey: awsconfig.secretAccessKey,
        mandatorySignIn: false,
        region: awsconfig.region,
        aws_user_pools_id: awsconfig.aws_user_pools_id,
        aws_user_pools_web_client_id: awsconfig.aws_user_pools_web_client_id
    });
} catch {
    aws_working = false;
    console.log('AWS not working');
}

app.get('/', (req, res) => {
    res.writeHead(200);
    var html = fs.readFileSync('html/index.html');
    var html_navbar = fs.readFileSync('html/navbar.html');
    var logged_in_user = fs.readFileSync('html/logged-in-user.html');
    var login_link = fs.readFileSync('html/login-link.html');
    var htmlsection_start = fs.readFileSync('html/htmlsection-start.html');
    if (cur_user != '') {
        logged_in_user =
        logged_in_user.toString().replace('$username', cur_user);
        html_navbar =
        html_navbar.toString().replace('$userstring', logged_in_user);
    }
    else {
        html_navbar =
        html_navbar.toString().replace('$userstring', login_link);
    }
    html = html.toString().replace('$navbar', html_navbar);
    html = html.toString().replace('$htmlsection', htmlsection_start);

    // write the list of decks to the screen
    // first, check if they exist
    var deckString = '';
    var deckFolder = './files/decks';
    fs.readdir(deckFolder, (err, files) => {
        files.forEach(file => {
            if (file.substring(file.length - 4) == '.csv') {
                deckString += ('<li>' + file.substring(0, file.length - 4) + '</li>');
            }
        });
    });
    
    setTimeout(function() {
        if (deckString == '') {
            deckString = '<p>You currently have no decks.</p>';
        }
        else {
            deckString = '<p>Your decks:</p>' + deckString + '<br>';
        }
        html = html.replace('$deckList', deckString);
    
        res.write(html);
        res.end();
    }, 1000);
});

app.post('/upload', (req, res) => {
    var _myText;
    var _deckName;
    try {
        _myText = req.body.myText;
        _deckName = req.body.deckName;

        if (_myText == '' || _deckName == '') {
            res.writeHead(404);
            if (_deckName != '') {
                res.write('<p>Please enter some text to be flashcard-ized</p>');
            } 
            else {
                res.write('<p>Please enter a deck name</p>');
            }
            res.end();
        }
        else {
            // call Python script via a spawned child process
            var dataToSend;
            console.log('Loading, hang tight...');
            const python = spawn(
                'python',
                [
                    'generate_cards.py',
                    '--myText',
                    _myText,
                    '--deckName',
                    _deckName,
                    '--username',
                    cur_user_aws_id
                ]
            );

            // loading screen while Python script runs
            var html = generateHTMLString('html/htmlsection-loading.html');
            res.write(html);

            // collect data from script
            python.stdout.on('data', function (data) {
                dataToSend = data.toString();
                console.log(dataToSend);
            });
            python.on('close', (code) => {
                res.write('<script>window.location.href="/";</script>');
            });
        }
    } catch {
        try {
            _deckName = req.body.deckName;
            res.writeHead(404);
            res.write('<p>Please enter some text to be flashcard-ized</p>');
            res.end();
        } catch {
            res.writeHead(404);
            res.write('<p>Please enter a deck name</p>');
            res.end();
        }
    }
})

app.get('/login', (req, res) => {
    var html = generateHTMLString('html/htmlsection-login.html');
    res.writeHead(200);
    res.write(html);
    res.end();
})

app.post('/login', (req, res) => {
    var _username = '';
    var _password = '';

    try {
        _username = req.body.username;
        _password = req.body.password;
    } catch {
        res.writeHead(404);
        res.write('<p>Please provide a username and password</p>');
        res.end();
    }
    if (_username == '' || _password == '') {
        res.writeHead(404);
        res.write('<p>Please provide a username and password</p>');
        res.end();
    }
    
    if (aws_working == true) {
        try {
            signIn(_username, _password).then(result => {
                cur_user_aws_id = result;
                console.log('AWS id:');
                console.log(cur_user_aws_id);
            });

            res.writeHead(200);
            res.write('<script>window.location.href="/";</script>');
            cur_user = _username;
        }
        catch {
            res.writeHead(404);
            res.write('<p>Login failed</p>');
        }
        res.end();
    }
})

app.get('/signup', (req, res) => {
    var html = generateHTMLString('html/htmlsection-signup.html');
    res.writeHead(200);
    res.write(html);
    res.end();
})

app.post('/signup', (req, res) => {
    var _username = '';
    var _password = '';
    var _email = '';

    try {
        _username = req.body.username;
        _password = req.body.password;
        _email = req.body.email;
    } catch {
        res.writeHead(404);
        res.write('<p>Please provide a username and password</p>');
        res.end();
    }
    if (_username == '' || _password == '') {
        res.writeHead(404);
        res.write('<p>Please provide a username and password</p>');
        res.end();
    }
    
    if (aws_working == true) {
        try {
            signUp(_username, _password, _email);
            res.writeHead(200);
            res.write('<script>window.location.href="/signup-confirm";</script>');
        }
        catch {
            res.writeHead(404);
            res.write('<p>Sign up failed</p>');
        }
        res.end();
    }
})

app.get('/signup-confirm', (req, res) => {
    var html = generateHTMLString('html/htmlsection-confirm.html');
    res.writeHead(200);
    res.write(html);
    res.end();
})

app.post('/signup-confirm', (req, res) => {
    var _username = '';
    var _code = '';

    try {
        _username = req.body.username;
        _code = req.body.code;
    } catch {
        res.writeHead(404);
        res.write('<p>Please provide a username and confirmation code</p>');
        res.end();
    }
    
    if (aws_working == true) {
        try {
            confirmSignUp(_username, _code);
            res.writeHead(200);
            res.write('<script>window.location.href="/";</script>');
            cur_user = _username;
        }
        catch {
            res.writeHead(404);
            res.write('<p>Sign-up failed</p>');
        }
        res.end();
    }
})

app.get('/logout', (req, res) => {
    if (aws_working == true) {
        try {
            signOut();
            res.writeHead(200);
            res.write('<script>window.location.href="/";</script>');
            cur_user = '';
        }
        catch {
            res.writeHead(404);
            res.write('<p>Sign-out failed</p>');
        }
        res.end();
    }
    cur_user = '';
    res.end();
})

function generateHTMLString(htmlsection_path) {
    var html = fs.readFileSync('html/index.html');
    var html_navbar = fs.readFileSync('html/navbar.html');
    var htmlsection = fs.readFileSync(htmlsection_path);
    html_navbar =
        html_navbar.toString().replace('$userstring', '');
    html = html.toString().replace('$navbar', html_navbar);
    html = html.toString().replace('$htmlsection', htmlsection);
    return html;
}

const server = app.listen(port, () => {
    console.log(`Now listening on port ${port}`); 
});

module.exports = { server, generateHTMLString };