var port = process.env.PORT || 3000,
    http = require('http'),
    fs = require('fs'),
    html = fs.readFileSync('index.html');

var log = function(entry) {
    fs.appendFileSync('/tmp/sample-app.log', new Date().toISOString() + ' - ' + entry + '\n');
};

// imports
const express = require('express');
const multer = require('multer');
const {spawn} = require('child_process');
const _fs  = require('fs');
const aws_amplify = require('aws-amplify');
const aws_amplify_core = require('@aws-amplify/core');
const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const { signUp, confirmSignUp, signIn } = require('./auth-funcs');
const { awsconfig } = require('./aws-exports');
const { a } = require('aws-amplify');
const { resolveNaptr } = require('dns');
const upload = multer({});
//var upload = multer({ dest: _config.destinationDir })



// login functionality
var cur_user = '';
var aws_working = true;
try {
    // coati: non-standard usage of awsconfig --- typically the entire module is imported into Auth.configure()
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


// coati: future support for uploading PDFs
/*
_handleUpload = (e) => {
    console.log('got here');
    const dataForm = new FormData();
    dataForm.append('file', e.target.files[0]);  
      axios
        .post('http://localhost:' + port + '/upload', dataForm)
        .then(res => {

        })
        .catch(err => console.log(err));      
}
*/

app.get('/', (req, res) => {
    // <!--<input type="file" id="myFile" style="float: left;">-->
    // <form action="/upload" method="post" enctype="multipart/form-data" >
    // name="files"

    res.writeHead(200);
    html = fs.readFileSync('index.html');
    var html_navbar = fs.readFileSync('navbar.html', 'utf8');
    var logged_in_user = fs.readFileSync('logged-in-user.html', 'utf8');
    var login_link = fs.readFileSync('login-link.html', 'utf8');
    var htmlsection_start = fs.readFileSync('htmlsection-start.html', 'utf8');
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
            // console.log(file);
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

    // res.sendFile('index.html', {root: __dirname});
});

app.post('/upload', (req, res) => {
    var _myText;
    var _deckName;
    try {
        _myText = req.body.myText;
        _deckName = req.body.deckName;
    }
    catch {
        _myText = 'null';
        _deckName = '';
    }

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
            _deckName
        ]
    );

    html = fs.readFileSync('index.html');
    var html_navbar = fs.readFileSync('navbar.html', 'utf8');
    var htmlsection_loading = _fs.readFileSync('htmlsection-loading.html', 'utf8');
    html_navbar =
        html_navbar.toString().replace('$userstring', '');
    html = html.toString().replace('$navbar', html_navbar);
    html = html.toString().replace('$htmlsection', htmlsection_loading);
    res.write(html);

    // collect data from script
    python.stdout.on('data', function (data) {
        dataToSend = data.toString();
        console.log(dataToSend);
    });
    python.on('close', (code) => {
        res.write('<script>window.location.href="/";</script>');
    });
})

app.get('/login', (req, res) => {
    html = fs.readFileSync('index.html');
    var html_navbar = fs.readFileSync('navbar.html', 'utf8');
    var htmlsection_login = _fs.readFileSync('htmlsection-login.html', 'utf8');
    html_navbar =
        html_navbar.toString().replace('$userstring', '');
    html = html.toString().replace('$navbar', html_navbar);
    html = html.toString().replace('$htmlsection', htmlsection_login);
    res.writeHead(200);
    res.write(html);
    res.end();
})

app.post('/login', (req, res) => {
    /*
    username = 'TestUser5';
    password = 'TestPwd135%!';
    email = 'test@test.edu';
    code = '268783';
    */

    var _username = '';
    var _password = '';

    try {
        _username = req.body.username;
        _password = req.body.password;
    } catch {
        res.writeHead(404);
        res.write('<p>Please provide a username and password');
        res.end();
    }
    
    if (aws_working == true) {
        try {
            signIn(_username, _password);
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
    html = fs.readFileSync('index.html');
    var html_navbar = fs.readFileSync('navbar.html', 'utf8');
    var htmlsection_login = _fs.readFileSync('htmlsection-signup.html', 'utf8');
    html_navbar =
        html_navbar.toString().replace('$userstring', '');
    html = html.toString().replace('$navbar', html_navbar);
    html = html.toString().replace('$htmlsection', htmlsection_login);
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
        res.write('<p>Please provide a username and password');
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
    html = fs.readFileSync('index.html');
    var html_navbar = fs.readFileSync('navbar.html', 'utf8');
    var htmlsection_confirm = _fs.readFileSync('htmlsection-confirm.html', 'utf8');
    html_navbar =
        html_navbar.toString().replace('$userstring', '');
    html = html.toString().replace('$navbar', html_navbar);
    html = html.toString().replace('$htmlsection', htmlsection_confirm);
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
        res.write('<p>Please provide a username and confirmation code');
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
    cur_user = '';
    res.writeHead(200);
    res.write('<script>window.location.href="/";</script>');
    res.end();
})

app.listen(port, () => {
    console.log(`Now listening on port ${port}`); 
});