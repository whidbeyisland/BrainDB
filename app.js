var port = process.env.PORT || 3000,
    http = require('http'),
    fs = require('fs'),
    html = fs.readFileSync('index.html');

var log = function(entry) {
    fs.appendFileSync('/tmp/sample-app.log', new Date().toISOString() + ' - ' + entry + '\n');
};

// initialize Express
const express = require('express');
const {spawn} = require('child_process');
const app = express();

// define POST and GET methods for page
var server = http.createServer(function (req, res) {
    if (req.method === 'POST') {
        var body = '';

        req.on('data', function(chunk) {
            body += chunk;
        });

        req.on('end', function() {
            if (req.url === '/') {
                console.log('Received message: ' + body);
            } else if (req.url = '/scheduled') {
                console.log('Received task ' + req.headers['x-aws-sqsd-taskname'] + ' scheduled at ' + req.headers['x-aws-sqsd-scheduled-at']);
            }

            // call Python donation script
            var dataToSend;
            // spawn new child process to call the python script
            const python = spawn(
                'python',
                ['script.py']
            );
            // collect data from script
            python.stdout.on('data', function (data) {
                // console.log('Pipe data from python script ...');
                dataToSend = data.toString();
                console.log(dataToSend);
            });
            // in close event we are sure that stream from child process is closed
            python.on('close', (code) => {
                // console.log(`child process close all stdio with code ${code}`);
                res.writeHead(200)
                html = fs.readFileSync('index.html');
                const htmlsection_2 =
                `<h1 class="mb-3">Blah blah blah</h1>;`
                html = html.toString().replace('$htmlsection', htmlsection_2);
                res.write(html);
                res.end();
            });
        });
    } else {
        // display default page
        const htmlsection_1 =
        `<h1 class="mb-3">Undinero</h1>
         <h4 class="mb-3">Undura is passionate about $Cause!</h4>
         <p>Please help us out with anything you can, so that no $PersonAnimalRobot ever needs to $ExperienceBadThing again.</p>
         <form action="" method="post" >
             <label>Run Python script: $</label>
             <button type="submit" class="btn btn-primary">Run</button>
         </form>`;

        res.writeHead(200);
        html = fs.readFileSync('index.html');
        html = html.toString().replace('$htmlsection', htmlsection_1);
        res.write(html);
        res.end();
    }
});

// Listen on port 3000, IP defaults to 127.0.0.1
server.listen(port);

// Put a friendly message on the terminal
console.log('Server running at http://127.0.0.1:' + port + '/');